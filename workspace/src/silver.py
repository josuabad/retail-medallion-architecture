from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    trim,
    when,
    current_timestamp,
    length,
    concat,
    lit,
)
import os
from .config import create_spark_session


def transform_to_silver(spark: SparkSession, bronze_path: str, silver_path: str):
    print(f"Leyendo datos desde la Capa Bronce ({bronze_path})...")
    df_bronze = spark.read.format("delta").load(bronze_path)

    print("Aplicando transformaciones de limpieza...")

    # 1. Selección, casteos y renombra de columnas reales
    df_cleaned = df_bronze.select(
        col("id").alias("review_id"),
        col("label").cast("integer").alias("rating"),
        trim(col("text")).alias("review_text"),
        col("label_text").alias("rating_label"),
        col("ingestion_timestamp").alias("bronze_ingestion_timestamp"),
    )

    # 2. Filtrado de calidad de datos
    df_filtered = (
        df_cleaned.filter(col("review_id").isNotNull())
        .filter(col("rating").between(0, 5))
        .filter(col("review_text").isNotNull() & (length(col("review_text")) > 0))
    )

    # 3. Creación de campos derivados para la capa analítica
    df_silver = (
        df_filtered.withColumn("text_length", length(col("review_text")))
        .withColumn(
            "sentiment_flag",
            when(col("rating") >= 3, "positivo")
            .when(col("rating") == 2, "neutral")
            .otherwise("negativo"),
        )
        .withColumn("rating_label", concat(col("rating"), lit(" estrellas")))
        .withColumn("silver_processed_timestamp", current_timestamp())
    )

    print(f"Escribiendo tabla Delta en la Capa Plata ({silver_path})...")
    (
        df_silver.write.format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .save(silver_path)
    )
    print("¡Transformación en Capa Plata completada con éxito!")


if __name__ == "__main__":
    spark = create_spark_session()

    bronze_path = os.path.join(
        os.path.dirname(__file__), "../", "data", "bronze", "amazon_reviews"
    )
    silver_path = os.path.join(
        os.path.dirname(__file__), "../", "data", "silver", "amazon_reviews"
    )

    transform_to_silver(spark, bronze_path, silver_path)

    # Comprobación de lectura
    df_silver_read = spark.read.format("delta").load(silver_path)
    print("\n--- Esquema de la Capa Plata ---")
    df_silver_read.printSchema()

    print("\n--- Muestra de datos en Plata ---")
    df_silver_read.show(5, truncate=40)
