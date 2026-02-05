FROM python:3.11-slim

# Metadatos
LABEL maintainer="Data Analysis Team"
LABEL description="HPC Stack for House Price Analysis with Parquet + Apache Arrow"

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements y instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar scripts de la aplicación
COPY generate_data.py .
COPY load_arrow_data.py .
COPY linear_regression.py .
COPY run_pipeline.sh .

# Hacer ejecutable el script de pipeline
RUN chmod +x run_pipeline.sh

# Crear directorio para datos
RUN mkdir -p /app/data

# Exponer volumen para datos persistentes
VOLUME ["/app/data"]

# Comando por defecto
CMD ["python", "generate_data.py"]
