#! /bin/bash
export MLFLOW_TRACKING_URI='https://user-pengfei-531016.kub.sspcloud.fr/'
export MLFLOW_EXPERIMENT_NAME="pokemon"

mlflow run git@github.com:pengfei99/mlflow-pokemon-example.git -P remote_server_uri=$MLFLOW_TRACKING_URI -P experiment_name=$MLFLOW_EXPERIMENT_NAME \
-P data_url=https://minio.lab.sspcloud.fr/pengfei/mlflow-demo/pokemon-partial.csv \
-P n_estimator=15 -P max_depth=10 -P min_samples_split=2


# we can also specify a code version by using the -v commit-id.
#mlflow run git@github.com:pengfei99/mlflow-pokemon-example.git -v 5955315f682e296e7315a567c4c142c13b21f2b0 \
#remote_server_uri=$MLFLOW_TRACKING_URI -P experiment_name=$MLFLOW_EXPERIMENT_NAME \
#-P data_url=https://minio.lab.sspcloud.fr/pengfei/mlflow-demo/pokemon-partial.csv \
#-P n_estimator=15 -P max_depth=10 -P min_samples_split=2