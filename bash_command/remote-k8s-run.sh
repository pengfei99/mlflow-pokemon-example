#! /bin/bash
unset AWS_SESSION_TOKEN
export MLFLOW_S3_ENDPOINT_URL=https://minio.lab.sspcloud.fr
export AWS_ACCESS_KEY_ID=mlflow
export AWS_SECRET_ACCESS_KEY=changeMe
export AWS_DEFAULT_REGION=us-east-1

export MLFLOW_TRACKING_URI='https://mlflow.lab.sspcloud.fr/'
export MLFLOW_EXPERIMENT_NAME="test-2"

mlflow run git@github.com:pengfei99/mlflow-pokemon-example.git -P remote_server_uri=$MLFLOW_TRACKING_URI -P experiment_name=$MLFLOW_EXPERIMENT_NAME \
-P data_url=https://minio.lab.sspcloud.fr/pengfei/mlflow-demo/pokemon-partial.csv \
-P n_estimator=50 -P max_depth=30 -P min_samples_split=2


# we can also specify a code version by using the -v commit-id.
#mlflow run git@github.com:pengfei99/mlflow-pokemon-example.git -v f8ab9bfcb63a076ac560f9e944869bca8edcaeca \
#-P remote_server_uri=$MLFLOW_TRACKING_URI -P experiment_name=$MLFLOW_EXPERIMENT_NAME \
#-P data_url=https://minio.lab.sspcloud.fr/pengfei/mlflow-demo/pokemon-partial.csv \
#-P n_estimator=100 -P max_depth=50 -P min_samples_split=2