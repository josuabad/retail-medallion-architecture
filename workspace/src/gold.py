from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    count,
    avg,
    round as spark_round,
    current_timestamp,
)
import os
from .config import create_spark_session


def build_gold_layer(spark: SparkSession, silver_path: str, gold_base_path: str):
    """
    Lee los datos limpios de la Capa Plata y genera tablas agregadas para la Capa Oro.
    """
    print(f"Leyendo datos desde la Capa Plata ({silver_path})...")
    df_silver = spark.read.format("delta").load(silver_path)

    # -------------------------------------------------------------
    # 1. Data Mart: Métrica de Sentimiento
    # -------------------------------------------------------------
    print("Calculando Data Mart de Métricas de Sentimiento...")
    df_gold_sentiment = (
        df_silver.groupBy("sentiment_flag")
        .agg(
            count("review_id").alias("total_reviews"),
            spark_round(avg("rating"), 2).alias("avg_rating"),
            spark_round(avg("text_length"), 1).alias("avg_text_length"),
        )
        .withColumn("gold_processed_timestamp", current_timestamp())
    )

    sentiment_output_path = os.path.join(gold_base_path, "sentiment_metrics")
    (
        df_gold_sentiment.write.format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .save(sentiment_output_path)
    )

    # -------------------------------------------------------------
    # 2. Data Mart: Distribución por Calificación (Rating)
    # -------------------------------------------------------------
    print("Calculando Data Mart de Distribución por Calificación...")
    df_gold_rating = (
        df_silver.groupBy("rating", "rating_label")
        .agg(
            count("review_id").alias("total_reviews"),
            spark_round(avg("text_length"), 1).alias("avg_text_length"),
        )
        .orderBy("rating")
        .withColumn("gold_processed_timestamp", current_timestamp())
    )

    rating_output_path = os.path.join(gold_base_path, "rating_distribution")
    (
        df_gold_rating.write.format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .save(rating_output_path)
    )

    print("¡Procesamiento en Capa Oro completado con éxito!")


if __name__ == "__main__":
    spark = create_spark_session()

    silver_path = os.path.join(
        os.path.dirname(__file__), "../", "data", "silver", "amazon_reviews"
    )
    gold_base_path = os.path.join(os.path.dirname(__file__), "../", "data", "gold")

    build_gold_layer(spark, silver_path, gold_base_path)

    # Comprobación de resultados
    print("\n================== METRICAS DE SENTIMIENTO (GOLD) ==================")
    spark.read.format("delta").load(
        os.path.join(gold_base_path, "sentiment_metrics")
    ).show()

    print("\n================== DISTRIBUCION DE RATINGS (GOLD) ==================")
    spark.read.format("delta").load(
        os.path.join(gold_base_path, "rating_distribution")
    ).show()
