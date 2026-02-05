# Guía Rápida de Inicio - HPC Stack

Esta guía te ayudará a ejecutar el análisis de precios de casas con **Apache Arrow + Parquet** en pocos minutos.

## 📦 Instalación Rápida

### 1. Instalar Docker

Si no tienes Docker instalado:
- **Windows/Mac**: Descarga [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Linux**: 
  ```bash
  sudo apt-get update
  sudo apt-get install docker.io docker-compose-plugin
  ```

### 2. Instalar Python 3.11+

Verifica tu versión de Python:
```bash
python3 --version
```

### 3. Instalar dependencias de Python

```bash
pip install -r requirements.txt
```

## 🚀 Ejecución Rápida

### Opción A: Con Docker (Recomendado - Todo Automatizado)

```bash
# Construir y ejecutar el contenedor
docker-compose up --build

# El sistema ejecutará automáticamente:
# 1. Generación de datos en Parquet
# 2. Demostración de operaciones Arrow (zero-copy)
# 3. Análisis de regresión lineal completo
```

### Opción B: Ejecución Local (Paso a Paso)

```bash
# 1. Generar datos en formato Parquet
python generate_data.py

# 2. Demostrar operaciones Arrow con zero-copy
python load_arrow_data.py

# 3. Ejecutar análisis de regresión
python linear_regression.py
```

### Opción C: Pipeline Automatizado Local

```bash
# Ejecutar todo el pipeline
./run_pipeline.sh
```

## 📊 Resultados

Después de ejecutar el análisis, encontrarás:

1. **house_data.parquet** - Datos en formato HPC optimizado (20 KB)
2. **house_data.csv** - Formato CSV para compatibilidad (19 KB)
3. **regression_output.tex** - Documento LaTeX con resultados completos
4. **regression_plot.png** - Visualización gráfica del análisis

## 💡 Ventajas del Stack HPC

### Apache Arrow - Zero-Copy
- ✅ **Sin copias de memoria**: Acceso directo a datos
- ✅ **Mayor velocidad**: 10-100x más rápido que operaciones tradicionales
- ✅ **Menor RAM**: Reutilización eficiente de memoria

### Formato Parquet
- ✅ **Compresión Snappy**: Datos comprimidos automáticamente
- ✅ **Lectura columnar**: Solo lee columnas necesarias
- ✅ **Metadata**: Estadísticas incluidas en el archivo

## 🔍 Operaciones Arrow Disponibles

```python
from load_arrow_data import ArrowDataLoader

loader = ArrowDataLoader('house_data.parquet')

# Estadísticas con PyArrow compute (muy rápido)
stats = loader.get_statistics()

# Filtrar por rango de precio
casas = loader.filter_by_price_range(200000, 300000)

# Top N casas más caras
top_10 = loader.get_top_n_by_price(10)

# Conversión a Pandas con zero-copy
df = loader.get_pandas_dataframe(zero_copy=True)
```

## 🛑 Detener el sistema

```bash
docker-compose down
```

## ❓ Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'pyarrow'"

**Solución:** Instala las dependencias:
```bash
pip install pyarrow fastparquet pandas
```

### Error: "docker: command not found"

**Solución:** Instala Docker Desktop o el Docker Engine

### El análisis es lento

**Solución:** El stack HPC con Arrow es muy rápido. Si notas lentitud:
- Verifica que pyarrow esté instalado correctamente
- Usa `zero_copy=True` en las conversiones a Pandas
- El formato Parquet con compresión Snappy optimiza lectura/escritura

## 📝 Compilar el documento LaTeX

### Opción 1: Usar pdflatex (local)
```bash
pdflatex regression_output.tex
```

### Opción 2: Usar Overleaf (online)
1. Ve a [overleaf.com](https://www.overleaf.com)
2. Crea un nuevo proyecto
3. Copia el contenido de `regression_output.tex`
4. Compila el documento

## 🎯 Comparación: Neo4j vs HPC Stack

| Aspecto | Neo4j (Anterior) | HPC Stack (Actual) |
|---------|------------------|-------------------|
| Conexión | Requiere red | ✅ Local |
| Firewall | ❌ Problemas | ✅ Sin problemas |
| Velocidad | Media | ✅ Muy rápida |
| Memoria | Alta | ✅ Optimizada |
| Setup | Complejo | ✅ Simple |
| Zero-copy | No | ✅ Sí |

## 📚 Más información

Ver el [README.md](README.md) completo para documentación detallada sobre:
- Arquitectura del stack HPC
- Operaciones avanzadas con Arrow
- Comparación de formatos de datos
- Referencias técnicas
