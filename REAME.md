# 🏨 Hotel ETL Pipeline

Pipeline ETL de datos hoteleros construido como práctica de ingeniería de datos.

## Arquitectura
```
Datos sintéticos (Faker) → MinIO Bronze → Transformación (Pandas) → MinIO Silver → ClickHouse (Gold)
```

## Herramientas utilizadas

- **Python** + Pandas + Faker
- **MinIO** — Data Lake (capas Bronze y Silver)
- **ClickHouse** — Data Warehouse (capa Gold)
- **Docker** — Orquestación de servicios

## Estructura del proyecto
```
hotel-etl-pipeline/
├── docker/         # docker-compose.yml
├── src/            # Scripts ETL
│   ├── generate_data.py
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── data/           # Datos generados (ignorados en git)
└── .gitignore
```

## Cómo ejecutar

1. Levantar servicios: `docker-compose up -d`
2. Generar datos: `python src/generate_data.py`
3. Extraer: `python src/extract.py`
4. Transformar: `python src/transform.py`
5. Cargar: `python src/load.py`