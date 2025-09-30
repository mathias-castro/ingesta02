import os
import csv
import boto3
import pymysql

# --- Nombre de archivo local y bucket (igual que en tu ejemplo) ---
ficheroUpload = "data.csv"
nombreBucket  = "gcr-output-01"   # cámbialo si usas otro bucket

# --- Parámetros MySQL (puedes sobreescribir con variables de entorno) ---
dbHost  = os.getenv("DB_HOST", "host.docker.internal")  # "mysql" si usas docker-compose
dbPort  = int(os.getenv("DB_PORT", "3306"))
dbUser  = os.getenv("DB_USER", "root")
dbPass  = os.getenv("DB_PASS", "tu_password")
dbName  = os.getenv("DB_NAME", "test")
dbTabla = os.getenv("DB_TABLE", "items")

def exportar_mysql_a_csv():
    """Lee toda la tabla y la guarda como data.csv en el directorio actual."""
    conn = pymysql.connect(
        host=dbHost, port=dbPort, user=dbUser, password=dbPass,
        database=dbName, charset="utf8mb4", cursorclass=pymysql.cursors.Cursor
    )
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM `{dbTabla}`")
            filas = cur.fetchall()
            headers = [d[0] for d in cur.description]

        with open(ficheroUpload, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(headers)
            w.writerows(filas)

        print(f"CSV generado: {ficheroUpload} ({len(filas)} filas)")
    finally:
        conn.close()

def subir_a_s3():
    s3 = boto3.client('s3')
    # sube con el mismo nombre como key en S3
    resp = s3.upload_file(ficheroUpload, nombreBucket, ficheroUpload)
    return resp  # None si fue exitoso

if __name__ == "__main__":
    exportar_mysql_a_csv()
    response = subir_a_s3()
    print(response)  # boto3.upload_file devuelve None en éxito
    print("Ingesta completada")
