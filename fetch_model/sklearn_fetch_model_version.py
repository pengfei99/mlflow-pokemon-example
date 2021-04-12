import mlflow.sklearn
import pandas as pd
import os
import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

# set up the server url and experiment name
remote_server_uri = "http://pengfei.org:8000"  # set to your server URI
experiment_name = "test"
run_name = "run-2"
os.environ["MLFLOW_TRACKING_URI"] = remote_server_uri
os.environ["MLFLOW_EXPERIMENT_NAME"] = experiment_name

# get the data
data_url = (
    "https://minio.lab.sspcloud.fr/pengfei/sspcloud-demo/pokemon-cleaned.csv"
)
try:
    input_df = pd.read_csv(data_url, index_col=0)
except Exception as e:
    logger.exception(
        "Unable to read data from the giving path, check your data location. Error: %s", e
    )

## prepare sample data
# Prepare data for ml model testing
legendary_pokemon=input_df[input_df["legendary"] == True]
legendary_sample=legendary_pokemon.sample(5).drop(['legendary', 'generation', 'total'], axis=1).select_dtypes(exclude=['object'])
normal_pokemon=input_df[input_df["legendary"] == False]
normal_sample=normal_pokemon.sample(5).drop(['legendary', 'generation', 'total'], axis=1).select_dtypes(exclude=['object'])
print(legendary_sample)
print(normal_sample)

# In this example, We will fetch a model based on its version, when you add a run to model repo, you can choose a
# specific name, if empty, the default numeric name will be given which starts from 1.

model_name = "pokemon-sklearn"
version = '3'

model = mlflow.pyfunc.load_model(
    model_uri=f"models:/{model_name}/{version}"
)
# predict the sample data
print(model.predict(legendary_sample))
print(model.predict(normal_sample))
