import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import warnings
import numpy as np
import sys
import os
from pprint import pprint

import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


# Get the auto logged metrics
def fetch_logged_data(run_id):
    client = mlflow.tracking.MlflowClient()
    data = client.get_run(run_id).data
    tags = {k: v for k, v in data.tags.items() if not k.startswith("mlflow.")}
    artifacts = [f.path for f in client.list_artifacts(run_id, "model")]
    return data.params, data.metrics, tags, artifacts


def mlflow_record(n_estimator, max_depth, min_samples_split):
    remote_server_uri = "http://pengfei.org:8000"  # set to your server URI
    experiment_name = "autolog"
    # mlflow.set_tracking_uri(remote_server_uri)
    os.environ["MLFLOW_TRACKING_URI"] = remote_server_uri
    os.environ["MLFLOW_EXPERIMENT_NAME"] = experiment_name
    mlflow.set_experiment(experiment_name)
    # enable autologging
    mlflow.sklearn.autolog()
    with mlflow.start_run() as run:
        # create a random forest classifier
        rf_clf = RandomForestClassifier(n_estimators=n_estimator, max_depth=max_depth,
                                        min_samples_split=min_samples_split,
                                        n_jobs=2, random_state=0)
        # train the model with training_data
        rf_clf.fit(train_X, train_y)
    # fetch logged data
    params, metrics, tags, artifacts = fetch_logged_data(run.info.run_id)
    pprint(params)
    pprint(metrics)
    pprint(tags)
    pprint(artifacts)


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
    min_samples_split = int(sys.argv[3]) if len(sys.argv) > 3 else 2

    mlflow_record(n_estimator, max_depth, min_samples_split)
