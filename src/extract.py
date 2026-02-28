import json
import boto3
from botocore.client import Config

# Conexión a MinIO
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin",
    config=Config(signature_version="s3v4")
)

# Leer el archivo JSON generado
input_path = "../data/reservations_raw.json"
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"📦 {len(data)} reservaciones leídas desde el archivo local")

# Subir el archivo crudo a MinIO bucket 'bronze'
s3.upload_file(
    Filename=input_path,
    Bucket="bronze",
    Key="hotels/reservations_raw.json"
)

print("✅ Archivo subido a MinIO - bucket: bronze / hotels/reservations_raw.json")