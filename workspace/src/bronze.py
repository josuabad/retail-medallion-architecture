from datasets import load_dataset
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp
import os
from .config import create_spark_session


def ingest_to_bronze(spark: SparkSession, output_path: str):
    """
    Descarga el dataset desde Hugging Face, lo convierte a PySpark DataFrame
    y lo escribe en formato Delta en la Capa Bronce.
    """
    # Usamos el dataset mteb/amazon_reviews_multi (sección en español | inglés | todos los idiomas)
    print("Descargando dataset desde Hugging Face...")
    dataset = load_dataset(
        path="mteb/amazon_reviews_multi",
        revision="refs/convert/parquet",
        data_dir="all_languages",
        split="train",
    )

    # Convertir el dataset de Hugging Face a PySpark DataFrame
    print("Convirtiendo dataset a PySpark DataFrame...")
    df = spark.createDataFrame(dataset.to_pandas())

    # Metadatos de auditoría
    df_bronze = df.withColumn("ingestion_timestamp", current_timestamp())

    print(f"Escribiendo tabla Delta en {output_path}...")
    df_bronze.write.format("delta").mode("overwrite").save(output_path)
    print("\n¡Ingesta en Capa Bronce completada con éxito!")


if __name__ == "__main__":
    spark = create_spark_session()
    bronze_path = os.path.join(
        os.path.dirname(__file__), "../", "data", "bronze", "amazon_reviews"
    )
    ingest_to_bronze(spark, bronze_path)

    # Lectura de comprobación
    df_bronze = spark.read.format("delta").load(bronze_path)
    print("\nEsquema de la Capa Bronce:")
    df_bronze.printSchema()
    print("\nMuestra de datos:")
    df_bronze.show(5, truncate=30)
