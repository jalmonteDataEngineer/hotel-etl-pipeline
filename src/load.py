import pandas as pd
import boto3
from botocore.client import Config
import requests

# Conexión a MinIO
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin",
    config=Config(signature_version="s3v4")
)

# Descargar archivo Silver desde MinIO
s3.download_file(
    Bucket="silver",
    Key="hotels/reservations_silver.csv",
    Filename="../data/reservations_silver.csv"
)

print("📥 Archivo descargado desde MinIO Silver")

# Cargar en Pandas
df = pd.read_csv("../data/reservations_silver.csv")
print(f"📊 {df.shape[0]} registros listos para cargar")

# URL de ClickHouse
ch_url = "http://localhost:8123/?user=default&password=click1234"

# Crear base de datos
requests.post(ch_url, params={"query": "CREATE DATABASE IF NOT EXISTS hotel_dw"})
print("✅ Base de datos hotel_dw creada")

# Crear tabla
create_table = """
CREATE TABLE IF NOT EXISTS hotel_dw.reservations (
    reservation_id String,
    hotel_id String,
    hotel_name String,
    city String,
    guest_name String,
    guest_email String,
    guest_nationality String,
    room_type String,
    channel String,
    status String,
    check_in Date,
    check_out Date,
    nights Int32,
    rate_per_night Float64,
    total_amount Float64,
    created_at DateTime,
    year Int32,
    month Int32,
    revenue Float64
) ENGINE = MergeTree()
ORDER BY (hotel_id, check_in)
"""

requests.post(ch_url, params={"query": create_table})
print("✅ Tabla reservations creada en ClickHouse")

# Insertar datos fila por fila en lotes
ch_insert_url = f"{ch_url}&query=INSERT+INTO+hotel_dw.reservations+FORMAT+CSV"

csv_data = df.to_csv(index=False, header=False)
response = requests.post(ch_insert_url, data=csv_data.encode("utf-8"))

if response.status_code == 200:
    print(f"✅ {df.shape[0]} registros cargados en ClickHouse - hotel_dw.reservations")
else:
    print(f"❌ Error: {response.text}")