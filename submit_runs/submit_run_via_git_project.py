import mlflow

project_uri = "https://github.com/pengfei99/mlflow-pokemon-example.git"
#

params = {"remote_server_uri": "http://pengfei.org:8000", "experiment_name": "test-2",
          "data_url": "https://minio.lab.sspcloud.fr/pengfei/sspcloud-demo/pokemon-partial.csv", "n_estimator": 40,
          "max_depth": 30, "min_samples_split": 2}

# Run MLflow project and create a reproducible conda environment
mlflow.run(project_uri, parameters=params)
