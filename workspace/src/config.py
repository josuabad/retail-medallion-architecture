from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip


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


if __name__ == "__main__":
    pass
