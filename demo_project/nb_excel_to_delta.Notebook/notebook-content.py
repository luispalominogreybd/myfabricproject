# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   }
# META }

# CELL ********************

from pyspark.sql import SparkSession
from delta.tables import DeltaTable

# Crear una sesión de Spark
spark = SparkSession.builder \
    .appName("DeltaLakeExample") \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:1.0.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# CELL ********************

from azure.storage.blob import BlobServiceClient
import pandas as pd
import io

# CELL ********************

# Configura tu conexión a Azure Blob Storage
connection_string = 'DefaultEndpointsProtocol=https;AccountName=datalakeexceldelta;AccountKey=LJu73dT+IXj8MYDQWwFlRxEcFHP09TC06INHFKmKDakk7Gr0e/8IwFmNcko5EtWvCdcRUq3tMK/R+AStJ2xCvg==;EndpointSuffix=core.windows.net'
container_name = 'filesystemexceldelta'
blob_name = 'raw/dataejemplo.xlsx'

# CELL ********************

# Conéctate al servicio de blobs
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)
blob_client = container_client.get_blob_client(blob_name)

# CELL ********************

# Descarga el blob a un objeto BytesIO
stream = io.BytesIO()
blob_client.download_blob().readinto(stream)
stream.seek(0)

# CELL ********************

# Lee el archivo Excel en un DataFrame de Pandas
df = pd.read_excel(stream)
# print(df.head())

# CELL ********************

# Convertir el DataFrame de Pandas a un DataFrame de Spark
sdf = spark.createDataFrame(df)

# CELL ********************

# Especificar la ruta de la tabla Delta
delta_table_path = "abfss://filesystemexceldelta@datalakeexceldelta.dfs.core.windows.net/modeled/dataejemplo.delta"


# CELL ********************

# Si no tienes una tabla Delta existente, puedes crearla usando el siguiente código:
sdf.write.format("delta").mode("overwrite").save(delta_table_path)

# CELL ********************

# Leer la tabla Delta
delta_df = spark.read.format("delta").load(delta_table_path)

delta_df.show()

# CELL ********************

# Si la tabla ya existe se realiza el UPSERT
delta_table.alias("existing").merge(
    sdf.alias("updates"),
    "existing.id = updates.id"  # Suponiendo que 'id' es la clave de unión
).whenMatchedUpdateAll(
).whenNotMatchedInsertAll(
).execute()
