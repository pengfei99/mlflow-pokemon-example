import subprocess
import os


remote_server_uri = "http://pengfei.org:8000"  # set to your server URI
os.environ["MLFLOW_TRACKING_URI"] = remote_server_uri

model_name = "pokemon-sklearn"
version = '3'

model_uri=f"models:/{model_name}/{version}"
print(model_uri)
# mlflow models serve -m "models:/sk-learn-random-forest-reg-model/Production" -h 127.0.0.1 -p 8001
bashCommand = f"mlflow models serve -m {model_uri} -h 127.0.0.1 -p 8001"

print(bashCommand)

process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
print(output)
