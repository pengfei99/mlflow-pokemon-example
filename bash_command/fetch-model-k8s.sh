#! /bin/bash
unset AWS_SESSION_TOKEN
export MLFLOW_S3_ENDPOINT_URL=https://minio.lab.sspcloud.fr
export AWS_ACCESS_KEY_ID=mlflow
export AWS_SECRET_ACCESS_KEY=TdsqEs8FxPecHyixK6gI
export AWS_DEFAULT_REGION=us-east-1

export MLFLOW_TRACKING_URI='https://mlflow.lab.sspcloud.fr/'

# deploy model by choosing model accuracy
# python /home/pliu/git/mlflow-pokemon-example/fetch_model/sklearn_fetch_model_search.py

# deploy model by choosing model stage
# python /home/pliu/git/mlflow-pokemon-example/fetch_model/sklearn_fetch_model_stage.py

# deploy model by choosing model version
# python /home/pliu/git/mlflow-pokemon-example/fetch_model/sklearn_fetch_model_version.py

# deploy model in a spark application
# python /home/pliu/git/mlflow-pokemon-example/fetch_model/spark_fetch_model.py

# deploy model as a web service
python /home/pliu/git/mlflow-pokemon-example/serve_model/serve_model_local.py
