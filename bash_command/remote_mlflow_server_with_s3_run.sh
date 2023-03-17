#! /bin/bash
# here we suppose you have required s3 creds such as AWS_DEFAULT_REGION,
# AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID and AWS_SESSION_TOKEN already
# set in your env. If not you need to also export them in below script

export MLFLOW_S3_ENDPOINT_URL='https://minio.lab.sspcloud.fr'
export MLFLOW_TRACKING_URI='https://user-pengfei-134963.user.lab.sspcloud.fr/'
export MLFLOW_EXPERIMENT_NAME="pokemon"

mlflow run https://github.com/pengfei99/mlflow-pokemon-example.git -P remote_server_uri=$MLFLOW_TRACKING_URI -P experiment_name=$MLFLOW_EXPERIMENT_NAME \
-P data_url=https://minio.lab.sspcloud.fr/pengfei/mlflow-demo/pokemon-partial.csv \
-P n_estimator=50 -P max_depth=30 -P min_samples_split=2


# we can also specify a code version by using the -v commit-id.
#mlflow run git@github.com:pengfei99/mlflow-pokemon-example.git -v 5955315f682e296e7315a567c4c142c13b21f2b0 \
#remote_server_uri=$MLFLOW_TRACKING_URI -P experiment_name=$MLFLOW_EXPERIMENT_NAME \
#-P data_url=https://minio.lab.sspcloud.fr/pengfei/mlflow-demo/pokemon-partial.csv \
#-P n_estimator=15 -P max_depth=10 -P min_samples_split=2