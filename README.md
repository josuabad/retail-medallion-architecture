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


<!-- NOTAS -->

<!-- 

En la **Capa Plata (Silver)** hemos realizado las siguientes tareas clave sobre los datos que teníamos en la Capa Bronce:

1. **Estandarización y renombrado de columnas:**
* Cambiamos los nombres originales (`id`, `label`, `text`, `label_text`) a nombres más claros y representativos (`review_id`, `rating`, `review_text`, `rating_label`).


2. **Tipado de datos (Casteos):**
* Convertimos la columna `label` (ahora `rating`) a un tipo entero (`integer`) para asegurar que se puedan hacer operaciones matemáticas posteriores.


3. **Limpieza y filtrado de calidad:**
* **Limpieza de texto:** Eliminamos espacios en blanco al inicio y final del texto con la función `trim()`.
* **Filtro de nulos y vacíos:** Descartamos cualquier registro que no tuviera `review_id` o donde el texto de la reseña estuviera vacío.
* **Rango válido:** Garantizamos que las puntuaciones estuvieran dentro del rango esperado (entre 0 y 5).


4. **Enriquecimiento de datos (Columnas derivadas):**
* **`text_length`:** Calculamos la longitud en caracteres del cuerpo de cada reseña.
* **`sentiment_flag`:** Clasificamos cada reseña en *positivo* (rating $\ge$ 4), *neutral* (rating = 3) o *negativo* (rating $\le$ 2).
* **`silver_processed_timestamp`:** Añadimos la fecha y hora exacta de procesamiento para mantener la trazabilidad del pipeline.


5. **Almacenamiento:**
* Guardamos el resultado final en formato **Delta Lake** dentro de `data/silver/amazon_reviews` en modo *overwrite*.

 -->
