FROM python:3.11-slim

WORKDIR /programas/ingesta

# Dependencias necesarias
RUN pip install --no-cache-dir boto3 PyMySQL

# Copia el script al contenedor
COPY ingesta.py .

# Ejecuta el script
CMD ["python", "ingesta.py"]
