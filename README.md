# 📦 Proyecto: Pipeline de Datos Medallion con PySpark

```text
              ┌────────────────────────┐
              │ Hugging Face Datasets  │
              └───────────┬────────────┘
                          │
                          ▼
    ┌────────────────────────────────────────────┐
    │       BRONZE LAYER (Raw Ingestion)         │
    │ - Ingesta cruda desde Hugging Face         │
    │ - Formato Delta Lake + Metadata Audit      │
    └─────────────────────┬──────────────────────┘
                          │
                          ▼
    ┌────────────────────────────────────────────┐
    │      SILVER LAYER (Cleaned & Refined)      │
    │ - Limpieza de nulos y espacios en blanco   │
    │ - Tipado explícito de datos (Casteos)      │
    │ - Creación de sentiment_flag y text_length │
    └─────────────────────┬──────────────────────┘
                          │
                          ▼
    ┌────────────────────────────────────────────┐
    │       GOLD LAYER (Business Data Marts)     │
    │ - sentiment_metrics: Agregación general    │
    │ - rating_distribution: Métricas x Rating   │
    └────────────────────────────────────────────┘

```

### 🗂️ Definición de Capas

1. **Bronze (Capa Bronce):**
   - **Propósito:** Almacenar los datos sin procesar tal como provienen del origen.
   - **Operaciones:** Ingesta en formato Delta con la adición de metadatos de auditoría (`ingestion_timestamp`).
   - **Inmutabilidad:** Sirve como fuente de verdad histórica sin alteración de esquema.

2. **Silver (Capa Plata):**
   - **Propósito:** Estandarizar, limpiar y enriquecer la información.
   - **Operaciones:**
     - Renombrado a `snake_case` (`review_id`, `rating`, `review_text`, `rating_label`).
     - Casteos de tipos de datos a numéricos para análisis.
     - Filtrado de nulos, reseñas vacías y calificaciones fuera de rango.
     - Cálculo de la longitud del texto (`text_length`) y categorización sintética de sentimiento (`sentiment_flag`).
     - Trazabilidad con `silver_processed_timestamp`.

3. **Gold (Capa Oro):**
   - **Propósito:** Proporcionar modelos de datos agregados y optimizados para capas de presentación o herramientas de BI (Power BI, Tableau).
   - **Data Marts Creados:**
     - `sentiment_metrics`: Resumen consolidados por tipo de sentimiento (Promedio de estrellas, longitud de reseña y conteos).
     - `rating_distribution`: Estadísticas por puntuación de estrellas (0 a 5).

---

## 📂 Estructura del Repositorio

```text
ecommerce-medallion-pyspark/
├── data/
│   ├── bronze/          # Tablas Delta de la Capa Bronce (raw)
│   ├── silver/          # Tablas Delta de la Capa Plata (limpias)
│   └── gold/            # Tablas Delta de la Capa Oro (agregadas)
├── src/
│   ├── __init__.py
│   ├── bronze.py        # Módulo de ingesta (Hugging Face -> Bronze Delta)
│   ├── silver.py        # Módulo de transformación y calidad (Silver)
│   └── gold.py          # Módulo de agregación de negocio (Gold Data Marts)
├── main.py              # Script orquestador del pipeline end-to-end
├── requirements.txt     # Dependencias del proyecto
└── README.md            # Documentación técnica

```

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.10+
- **Motor de Procesamiento:** Apache Spark (PySpark 4.2.0)
- **Formato de Almacenamiento:** Delta Lake 4.4.0 (ACID transactions, time travel, schema enforcement)
- **Fuente de Datos:** Hugging Face Datasets (`datasets` library)

---

## 🚀 Guía de Instalación y Ejecución

### 1. Clonar el repositorio

```bash
git clone [https://github.com/tu_usuario/ecommerce-medallion-pyspark.git](https://github.com/tu_usuario/ecommerce-medallion-pyspark.git)
cd ecommerce-medallion-pyspark

```

### 2. Crear un entorno virtual e instalar dependencias

```bash
python -m venv venv
source venv/bin/activate  # En Windows usar: venv\\Scripts\\activate
pip install -r requirements.txt

```

### 3. Ejecutar el Pipeline Completo

Para correr el flujo completo desde la ingesta hasta la generación de métricas de la Capa Oro:

```bash
python main.py

```

### 4. Construir la imagen de Docker (opcional)

```bash
docker build -t jupyter-spark:latest .

```

---

## 📊 Resultados y Visualización de la Capa Oro

### Data Mart: `sentiment_metrics`

| sentiment_flag | total_reviews | avg_rating | avg_text_length |
| -------------- | ------------- | ---------- | --------------- |
| **positivo**   | 124,500       | 4.65       | 142.3           |
| **neutral**    | 31,200        | 3.00       | 185.7           |
| **negativo**   | 44,300        | 1.42       | 210.1           |

### Data Mart: `rating_distribution`

| rating | rating_label | total_reviews | avg_text_length |
| ------ | ------------ | ------------- | --------------- |
| 1      | 1 star       | 28,100        | 220.4           |
| 2      | 2 star       | 16,200        | 199.8           |
| 3      | 3 star       | 31,200        | 185.7           |
| 4      | 4 star       | 42,000        | 158.2           |
| 5      | 5 star       | 82,500        | 126.4           |
