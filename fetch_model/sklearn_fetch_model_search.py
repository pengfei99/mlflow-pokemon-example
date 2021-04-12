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

# In this example, We use the mlflow.search_runs() function to search runs. This function takes filter_string,
# which act as a filter to the query and returns a pandas.DataFrame of runs, where each metric, parameter, and
# tag are expanded into their own columns named metrics.*, params.*, and tags.* respectively. For runs that
# don’t have a particular metric, parameter, or tag, their value will be (NumPy) Nan, None, or None respectively.

# Here we filter all model which accuracy is more than 0.9.
df = mlflow.search_runs(filter_string="metrics.model_accuracy > 0.9")
print(df)
# As we found a list of runs, we need to specify a particular one to fetch the actual model
# here we can use two function (e.g. idxmin(), idxmax) to return the index of the row which has the minimum metric
# or the maximum metric value. For example, below, it will return the run id of the best accuracy.
run_id = df.loc[df['metrics.model_accuracy'].idxmax()]['run_id']
print(run_id)
# Load model
model = mlflow.sklearn.load_model("runs:/" + run_id + "/model")
# predict the sample data
print(model.predict(legendary_sample))
print(model.predict(normal_sample))
