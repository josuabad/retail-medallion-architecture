import os
from src.config import create_spark_session
from src.bronze import ingest_to_bronze
from src.silver import transform_to_silver
from src.gold import build_gold_layer


def run_pipeline():
    print("=== INICIANDO PIPELINE MEDALLION CON PYSPARK Y DELTA LAKE ===")

    spark = create_spark_session()

    bronze_path = os.path.join(
        os.path.dirname(__file__), "../", "data", "bronze", "amazon_reviews"
    )
    silver_path = os.path.join(
        os.path.dirname(__file__), "../", "data", "silver", "amazon_reviews"
    )
    gold_base_path = os.path.join(os.path.dirname(__file__), "../", "data", "gold")

    print("\n---> Ejecutando Capa Bronce...")
    ingest_to_bronze(spark, bronze_path)

    print("\n---> Ejecutando Capa Plata...")
    transform_to_silver(spark, bronze_path, silver_path)

    print("\n---> Ejecutando Capa Oro...")
    build_gold_layer(spark, silver_path, gold_base_path)

    print("\n=== PIPELINE COMPLETADO EXITOSAMENTE ===")


if __name__ == "__main__":
    run_pipeline()
