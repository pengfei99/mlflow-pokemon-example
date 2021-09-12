# Pokemon Classification
This project trained a RandomForest model to classify the Pokemon(i.e. Legendary, Non-legendary). 
Then we apply the model in an application web and provide a web service api.

## Project summary
This project uses the features of pokemon such as attack, defence, speed, etc. to train a 
RandomForest model to classify and predict if a pokemon is legendary or not. And we also want to know 
the weights of each feature. At last, to put this model into production, we decide to offer a web service, 
so everyone can test if their pokemon is legendary or not.

## SSP Datalab
This project is originally developed as a pure python project without any ML Ops supports. So it's hard to do 
continues integration(CI), continues deployment(CD) and continues training(CT). After we migrate this 
project to SSP Datalab. We take the advantage of many services that are provided by the
platform. Here we want to highlight three benefits:

1. Improved significantly the model performance
2. Shortened the model development life cycle
3. Automatize the model deployment process

### ML Ops service inside Datalab
When you work as a team to develop a model, you must experience the pain of logging the model and how the model 
(e.g. hyper-parameter settings, training dataset location, etc.) is trained. We can apply CI on our 
model code easily by using tools such as GitHub. But we know that code is only one factor which can 
impact your model performance. And most time, the hyper-parameter setting and training dataset have 
even more impact compare to the model code. Datalab provides a service called Mlflow which address 
all these issues.

#### Model tracking

For each trained model, it allows us to track feature importance, hyper-parameter settings, the training 
data location, their validation metrics(e.g. accuracy, ROC, AUC, etc.). In Figure-1, we show an example of 
the model tracking interface.
![Model tracking](https://raw.githubusercontent.com/pengfei99/mlflow-pokemon-example/master/img/pokemon_metric.PNG)
**Figure-1:**  Model tracking

We can also compare them between different models. In Figure-2, we show an example of the model's metrics
comparison.
![Model comparison](https://raw.githubusercontent.com/pengfei99/mlflow-pokemon-example/master/img/mdoel_camparing.PNG)
**Figure-2:**  Model comparison

You can notice that, we have improved our model, and we are able to explain which parameter make the 
improvement possible. 

#### Model deployment

To deploy a model, we can set version and status to a model, and the deployment application can fetch the 
appropriate model based on this information. Figure-3 shows an example of our model which has four versions, 
one in production, one in development and two in archive.
![Model deployment](https://raw.githubusercontent.com/pengfei99/mlflow-pokemon-example/master/img/model_version.PNG)
**Figure-3:**  Model version and status




### Data management service inside Datalab

Each year, the pokemon company will release some new types of pokemon. Each release is called a generation. So far, we 
have seven generations. As a result, the raw data of pokemon are split into different files for each generation. In many
cases, those who collect and upload the data are not the one who use them to train the model. As a result, it's a new 
challenge to find the appropriate data to train your model. Fortunately , Datalab provide us a data management service 
called Atlas which allow us to find data easily. 

We can search data by their name, type, owner, etc. Figure-4 shows an example of full text search.
![Full text search](https://raw.githubusercontent.com/pengfei99/mlflow-pokemon-example/master/img/atlas_search_by_text.PNG)
**Figure-4:**  Full text search

If the data steward has configured the classification meta-data, we can even search data by the pokemon generation.
Figure-5 shows an example of search by pokemon generation.
![Filter search result](https://raw.githubusercontent.com/pengfei99/mlflow-pokemon-example/master/img/atlas_search_by_class.png)
**Figure-5:**  Search data by using pokemon generation

After we found the data, we can know all the metadata about the data such as name, location, owner, size, creation date,
etc. Figure-6 shows an example of the pokemon data metadata.

![Pokemon metadata](https://raw.githubusercontent.com/pengfei99/mlflow-pokemon-example/master/img/atlas_data_detail.PNG)
**Figure-6:**  Pokemon metadata

### Workflow automation service inside Datalab

Datalab provides a workflow automation service, which allows us to run the complete data pipeline on the platform without
any human intervention. We can receive notification when the job finished correctly, or warnings when the job failed. Figure-7
shows an example of our data pipeline.

![Pokemon workflow automation](https://raw.githubusercontent.com/pengfei99/mlflow-pokemon-example/master/img/pokemon_workflow.PNG)

**Figure-7:**  Pokemon workflow automation


# Data and model

The full cleaned dataset can be found [here](https://minio.lab.sspcloud.fr/pengfei/mlflow-demo/pokemon-cleaned.csv)

The source codes on how to train, track and deploy model can be found [here](https://github.com/pengfei99/mlflow-pokemon-example.git)

To use our newly deployed model, you can use the following curl command to query our web service

```shell
curl -X POST -H "Content-Type:application/json; format=pandas-split" --data \
'{"columns":["hp","attack","defense","special_attack","special_defense","speed"],"index":[272,293,414,263,49],
"data":[[80,70,70,90,100,70],[64,51,23,51,23,28],[70,94,50,94,50,66],[38,30,41,30,41,60],[70,65,60,90,75,90]]}' \
https://pokemon.lab.sspcloud.fr/invocations ;
```
