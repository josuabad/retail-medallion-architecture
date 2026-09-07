# retail-medallion-architecture

Retail Medallion Architecture con PySpark sobre Delta Lake

## Pasos para usar el Dockerfile:

1. **Guardar el archivo:** Guarda el contenido anterior en un archivo llamado `Dockerfile` (sin extensión) o renombra el archivo descargado.
2. **Construir la imagen:**

```bash
docker build -t jupyter-spark:latest .

```

3. **Ejecutar el contenedor (standalone):**

```bash
docker run -p 8888:8888 -p 4040:4040 -v $(pwd):/home/jovyan/work jupyter-spark:latest

```

4. **En caso de reintento:**

```bash
docker compose build --no-cache

```

## Dataset: Reseñas de Productos (E-commerce / Retail)

- Dataset: mteb/amazon_reviews_multi (o datasets similares de reseñas de Amazon/e-commerce).

- Por qué funciona: Es clásico y comprensible para cualquier reclutador.

- Flujo Medallion:
  - Bronce: Carga limpia del JSON/CSV raw desde Hugging Face a tablas Delta sin transformar.

  - Plata: Limpieza de nulos, desanidado de campos, filtrado por idioma o puntuación, formateo de fechas.

  - Oro: Agregaciones de negocio (promedio de valoración por categoría, productos con más reseñas negativas por mes, etc.).

## Estructura de carpetas del proyecto

```text
retail-medallion-architecture/
├── data/
│   ├── bronze/          # Tablas Delta de la Capa Bronce (raw ingestion)
│   ├── silver/          # Tablas Delta de la Capa Plata (cleaned & refined)
│   └── gold/            # Tablas Delta de la Capa Oro (aggregated / business metrics)
├── notebooks/           # Opcional si prefieres usar Jupyter notebooks
│   ├── 01_bronze.ipynb
│   ├── 02_silver.ipynb
│   └── 03_gold.ipynb
├── src/
│   ├── __init__.py
│   ├── config.py        # Rutas y configuración de la SparkSession
│   ├── bronze.py        # Ingesta desde Hugging Face hacia Delta
│   ├── silver.py        # Transformaciones y limpieza
│   └── gold.py          # Agregaciones de negocio
├── requirements.txt     # pyspark, delta-spark, datasets
├── README.md            # Explicación del proyecto para LinkedIn/GitHub
└── main.py              # Script principal de ejecución del pipeline
```
