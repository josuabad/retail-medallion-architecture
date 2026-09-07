from datasets import load_dataset
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip
import os


def create_spark_session() -> SparkSession:
    """
    Inicializa Spark con soporte para Delta Lake
    """
    return configure_spark_with_delta_pip(
        SparkSession.builder.appName("EcommerceMedallion - Bronze")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
    ).getOrCreate()


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

    print(f"Escribiendo tabla Delta en {output_path}...")
    df.write.format("delta").mode("overwrite").save(output_path)
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
