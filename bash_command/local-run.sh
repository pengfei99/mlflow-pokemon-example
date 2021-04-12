export MLFLOW_TRACKING_URI='http://pengfei.org:8000'
export MLFLOW_EXPERIMENT_NAME="test-2"

# train with data version 1
mlflow run /home/pliu/git/mlflow-pokemon-example  -P remote_server_uri=$MLFLOW_TRACKING_URI -P experiment_name=$MLFLOW_EXPERIMENT_NAME \
-P data_url=https://minio.lab.sspcloud.fr/pengfei/sspcloud-demo/pokemon-partial.csv \
-P n_estimator=15 -P max_depth=10 -P min_samples_split=2

# train with data version 2
#mlflow run /home/pliu/git/mlflow-pokemon-example  -P remote_server_uri=$MLFLOW_TRACKING_URI -P experiment_name=$MLFLOW_EXPERIMENT_NAME \
#-P data_url=https://minio.lab.sspcloud.fr/pengfei/sspcloud-demo/pokemon-cleaned.csv \
#-P n_estimator=15 -P max_depth=10 -P min_samples_split=2