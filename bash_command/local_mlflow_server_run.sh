#! /bin/bash

# this script is design to run a local mlflow server which uses local file system
# to store the model. So no need for set up s3 creds here.

export MLFLOW_TRACKING_URI='http://pengfei.org:8000'
export MLFLOW_EXPERIMENT_NAME="test-2"

# train with data version 1
mlflow run /home/pliu/git/mlflow-pokemon-example  -P remote_server_uri=$MLFLOW_TRACKING_URI -P experiment_name=$MLFLOW_EXPERIMENT_NAME \
-P data_url=https://minio.lab.sspcloud.fr/pengfei/mlflow-demo/pokemon-partial.csv \
-P n_estimator=15 -P max_depth=10 -P min_samples_split=2

# train with data version 2
#mlflow run /home/pliu/git/mlflow-pokemon-example  -P remote_server_uri=$MLFLOW_TRACKING_URI -P experiment_name=$MLFLOW_EXPERIMENT_NAME \
#-P data_url=https://minio.lab.sspcloud.fr/pengfei/mlflow-demo/pokemon-new.csv \
#-P n_estimator=15 -P max_depth=10 -P min_samples_split=2

# train with data version 3
#mlflow run /home/pliu/git/mlflow-pokemon-example  -P remote_server_uri=$MLFLOW_TRACKING_URI -P experiment_name=$MLFLOW_EXPERIMENT_NAME \
#-P data_url=https://minio.lab.sspcloud.fr/pengfei/mlflow-demo/pokemon-cleaned.csv \
#-P n_estimator=15 -P max_depth=10 -P min_samples_split=2