import pyspark
from pyspark.sql import SparkSession
from pyspark import SparkFiles
import mlflow
import os
from pyspark.sql.functions import struct


def mute_spark_logs(sc):
    """Mute Spark info logging"""
    logger = sc._jvm.org.apache.log4j
    logger.LogManager.getLogger("org").setLevel(logger.Level.ERROR)
    logger.LogManager.getLogger("akka").setLevel(logger.Level.ERROR)


if __name__ == "__main__":

    # remote_server_uri = "http://pengfei.org:8000"  # set to your server URI
    remote_server_uri = "https://mlflow.lab.sspcloud.fr/"
    os.environ["MLFLOW_TRACKING_URI"] = remote_server_uri

    data_url = (
        "https://minio.lab.sspcloud.fr/pengfei/sspcloud-demo/pokemon-cleaned.csv"
    )
    spark = SparkSession.builder.master("local[*]").getOrCreate()
    mute_spark_logs(spark.sparkContext)
    spark.sparkContext.addFile(data_url)
    sdf = spark.read.csv("file://" + SparkFiles.get("pokemon-cleaned.csv"), header=True, inferSchema=True)
    sdf.show(5)
    row_number = sdf.count()
    print(row_number)
    # Load model as a Spark UDF.
    model_name = "test"
    version = '2'
    # pyfunc.spark requires a spark session
    predict_func = mlflow.pyfunc.spark_udf(spark, model_uri=f"models:/{model_name}/{version}", result_type='string')

    # Predict on a Spark DataFrame.
    predicated_df = sdf.withColumn("prediction", predict_func(
        struct("hp", "attack", "defense", "special_attack", "special_defense", "speed")))
    predicated_df.show(5)
