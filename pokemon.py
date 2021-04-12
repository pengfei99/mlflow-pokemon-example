import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import warnings
import numpy as np
import sys
import os

import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


# calculate an accuracy from the confusion matrix
def get_model_accuracy(confusion_matrix):
    diagonal_sum = confusion_matrix.trace()
    sum_of_all_elements = confusion_matrix.sum()
    return diagonal_sum / sum_of_all_elements


def mlflow_record(n_estimator, max_depth, min_samples_split):
    # can be put as parameter of this function

    # mlflow.set_tracking_uri(remote_server_uri)
    os.environ["MLFLOW_TRACKING_URI"] = remote_server_uri
    os.environ["MLFLOW_EXPERIMENT_NAME"] = experiment_name
    mlflow.set_experiment(experiment_name)
    with mlflow.start_run(run_name=run_name):
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
        mlflow.log_param("data_url", data_url)
        mlflow.log_param("n_estimator", n_estimator)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("min_samples_split", min_samples_split)
        # log shap feature explanation extension. This will generate a graph of feature importance of the model
        mlflow.shap.log_explanation(rf_clf.predict, test_X)
        mlflow.log_metric("model_accuracy", model_accuracy)
        mlflow.sklearn.log_model(rf_clf, "model")


def prepare_data(data_url):
    # read data as df
    try:
        input_df = pd.read_csv(data_url, index_col=0)
    except Exception as e:
        logger.exception(
            "Unable to read data from the giving path, check your data location. Error: %s", e
        )
    # Prepare data for ml model
    label = input_df.legendary
    feature = input_df.drop(['legendary', 'generation', 'total'], axis=1).select_dtypes(exclude=['object'])
    return feature, label


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    np.random.seed(40)
    # base line data
    base_url = "https://minio.lab.sspcloud.fr/pengfei/sspcloud-demo/pokemon-cleaned.csv"
    # Get experiment setting from cli
    remote_server_uri = str(sys.argv[1]) if len(sys.argv) > 1 else "http://pengfei.org:8000"
    experiment_name = str(sys.argv[2]) if len(sys.argv) > 2 else "test1"
    run_name = str(sys.argv[3]) if len(sys.argv) > 3 else "default"

    # Get data path
    data_url = str(sys.argv[4]) if len(
        sys.argv) > 4 else "https://minio.lab.sspcloud.fr/pengfei/sspcloud-demo/pokemon-cleaned.csv"

    # Get hyper parameters from cli arguments
    n_estimator = int(sys.argv[5]) if len(sys.argv) > 5 else 10
    max_depth = int(sys.argv[6]) if len(sys.argv) > 6 else 5
    min_samples_split = int(sys.argv[7]) if len(sys.argv) > 7 else 2

    # split data into training_data and test_data
    feature_data, label_data = prepare_data(data_url)
    train_X, test_X, train_y, test_y = train_test_split(feature_data, label_data, train_size=0.8, test_size=0.2,
                                                        random_state=0)
    # get base data for validation
    # base_feature, base_label = prepare_data(base_url)
    # tr_X, test_base_X, tr_y, test_base_y = train_test_split(base_feature, base_label, train_size=0.9, test_size=0.1,
    #                                                         random_state=0)

    mlflow_record(n_estimator, max_depth, min_samples_split)
