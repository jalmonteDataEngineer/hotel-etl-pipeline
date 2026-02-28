import json
import pandas as pd
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

# Descargar archivo crudo desde Bronze
s3.download_file(
    Bucket="bronze",
    Key="hotels/reservations_raw.json",
    Filename="../data/reservations_raw_download.json"
)

print("📥 Archivo descargado desde MinIO Bronze")

# Cargar en Pandas
with open("../data/reservations_raw_download.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)
print(f"📊 Shape original: {df.shape}")

# Transformaciones
# 1. Eliminar duplicados
df = df.drop_duplicates(subset="reservation_id")

# 2. Convertir fechas
df["check_in"] = pd.to_datetime(df["check_in"])
df["check_out"] = pd.to_datetime(df["check_out"])
df["created_at"] = pd.to_datetime(df["created_at"])

# 3. Extraer año y mes de check_in
df["year"] = df["check_in"].dt.year
df["month"] = df["check_in"].dt.month

# 4. Filtrar solo reservas válidas (no canceladas)
df_clean = df[df["status"] != "cancelled"].copy()

# 5. Calcular revenue real (solo reservas activas)
df_clean["revenue"] = df_clean["total_amount"]

print(f"📊 Shape después de transformación: {df_clean.shape}")
print(f"✅ Reservas eliminadas (canceladas): {df.shape[0] - df_clean.shape[0]}")

# Guardar como CSV
output_path = "../data/reservations_silver.csv"
df_clean.to_csv(output_path, index=False)

# Subir CSV transformado a MinIO bucket 'silver'
s3.upload_file(
    Filename=output_path,
    Bucket="silver",
    Key="hotels/reservations_silver.csv"
)

print("✅ Archivo transformado subido a MinIO - bucket: silver / hotels/reservations_silver.csv")