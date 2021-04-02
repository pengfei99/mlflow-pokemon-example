import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import warnings
import numpy as np
import sys

import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


# calculate an accuracy from the confusion matrix
def get_model_accuracy(confusion_matrix):
    diagonal_sum = confusion_matrix.trace()
    sum_of_all_elements = confusion_matrix.sum()
    return diagonal_sum / sum_of_all_elements


def mlflow_record(n_estimator, max_depth, min_samples_split):
   # remote_server_uri = "http://pengfei.org:8000"  # set to your server URI
   # mlflow.set_tracking_uri(remote_server_uri)
    mlflow.set_experiment("pokemon-experiment")
    with mlflow.start_run():
        # create a random forest classifier
        rf_clf = RandomForestClassifier(n_estimators=n_estimator, max_depth=max_depth,
                                        min_samples_split=min_samples_split,
                                        n_jobs=2, random_state=0)
        # train the model with training_data
        rf_clf.fit(train_X, train_y)
        # predict testing data
        predicts_val = rf_clf.predict(test_X)

        # Generate a cm
        cm = confusion_matrix(test_y, predicts_val)
        model_accuracy = get_model_accuracy(cm)
        print("RandomForest model (n_estimator=%f, max_depth=%f, min_samples_split=%f):" % (n_estimator, max_depth,
                                                                                            min_samples_split))
        print("accuracy: %f" % model_accuracy)
        mlflow.log_param("n_estimator", n_estimator)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("min_samples_split", min_samples_split)
        mlflow.log_metric("model_accuracy", model_accuracy)
        mlflow.sklearn.log_model(rf_clf, "model")


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    np.random.seed(40)
    data_url = (
        "https://minio.lab.sspcloud.fr/pengfei/sspcloud-demo/pokemon-cleaned.csv"
    )

    # read data as df
    try:
        input_df = pd.read_csv(data_url, index_col=0)
    except Exception as e:
        logger.exception(
            "Unable to read data from the giving path, check your data location. Error: %s", e
        )
    # Prepare data for ml model
    label_data = input_df.legendary
    label_sample = label_data.sample(5)
    feature_data = input_df.drop(['legendary', 'generation', 'total'], axis=1).select_dtypes(exclude=['object'])
    feature_sample = feature_data.sample(5)
    # split data into training_data and test_data
    train_X, test_X, train_y, test_y = train_test_split(feature_data, label_data, train_size=0.8, test_size=0.2,
                                                        random_state=0)

    # Get hyper parameters from cli arguments
    n_estimator = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    max_depth = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    min_samples_split = int(sys.argv[2]) if len(sys.argv) > 3 else 2

    mlflow_record(n_estimator, max_depth, min_samples_split)
