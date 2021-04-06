import requests
import pandas as pd
import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

host = '127.0.0.1'
port = '8001'

url = f'http://{host}:{port}/invocations'

headers = {
    'Content-Type': 'application/json',
}

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
legendary_pokemon = input_df[input_df["legendary"] == True]
legendary_sample = legendary_pokemon.sample(5).drop(['legendary', 'generation', 'total'], axis=1).select_dtypes(
    exclude=['object'])
normal_pokemon = input_df[input_df["legendary"] == False]
normal_sample = normal_pokemon.sample(5).drop(['legendary', 'generation', 'total'], axis=1).select_dtypes(
    exclude=['object'])
print(legendary_sample)
print(normal_sample)

# convert pandas data frame to json
legendary_json = legendary_sample.to_json(orient='split')
normal_json = normal_sample.to_json(orient='split')

# send a post query to the rest server
normal_prediction = requests.post(url=url, headers=headers, data=normal_json)
legendary_prediction = requests.post(url=url, headers=headers, data=legendary_json)

print(f'Normal Predictions: {normal_prediction.text}')
print(f'Legendary Predictions: {legendary_prediction.text}')


