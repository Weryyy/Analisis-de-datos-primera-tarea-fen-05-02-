# Análisis de Datos: Precios de Casas

Proyecto de análisis de datos que genera un conjunto de datos artificiales de precios de casas, utiliza **Apache Arrow** para operaciones de alto rendimiento con **zero-copy**, almacena datos en formato **Parquet**, y realiza un análisis de regresión lineal simple.

## 📋 Descripción

Este proyecto crea un conjunto de datos sintético de 500 casas con diversas características (área, habitaciones, baños, antigüedad, etc.) y sus respectivos precios. Los datos se almacenan en formato Parquet optimizado para análisis de alto rendimiento, utilizando Apache Arrow para operaciones zero-copy y máxima eficiencia.

## 🚀 Stack HPC (High-Performance Computing)

- **Apache Arrow**: Framework para operaciones in-memory con zero-copy
- **Parquet**: Formato columnar optimizado para análisis
- **Pandas**: Integración con Arrow para DataFrames eficientes
- **Docker**: Containerización para despliegue fácil y reproducible

## 🛠️ Tecnologías Utilizadas

- **Python 3.11+**: Lenguaje principal del proyecto
- **Apache Arrow (PyArrow)**: Operaciones zero-copy de alto rendimiento
- **Parquet**: Formato de almacenamiento columnar con compresión
- **Docker**: Containerización para despliegue fácil
- **Pandas & NumPy**: Manipulación y generación de datos
- **Scikit-learn**: Implementación de regresión lineal
- **Matplotlib & Seaborn**: Visualización de datos
- **LaTeX**: Generación de documentos profesionales

## 📁 Estructura del Proyecto

```
.
├── Dockerfile                  # Imagen Docker para el entorno de análisis
├── docker-compose.yml          # Configuración del stack HPC
├── requirements.txt            # Dependencias de Python (Arrow, Parquet)
├── generate_data.py           # Generación de datos en formato Parquet
├── load_arrow_data.py         # Cargador con Apache Arrow (zero-copy)
├── linear_regression.py       # Análisis de regresión con Arrow
├── house_data.parquet         # Datos optimizados (creado al ejecutar)
├── house_data.csv             # Datos en CSV (compatibilidad)
├── regression_output.tex      # Salida en formato LaTeX
└── regression_plot.png        # Visualización de la regresión
```

## 🚀 Instalación y Uso

### Prerrequisitos

- Docker y Docker Compose instalados
- Python 3.11 o superior (para ejecución local)
- pip (gestor de paquetes de Python)

### Opción 1: Ejecución con Docker (Recomendado)

```bash
# Construir y ejecutar el contenedor
docker-compose up --build

# El contenedor ejecutará automáticamente:
# 1. Generación de datos en Parquet
# 2. Demostración de operaciones Arrow
# 3. Análisis de regresión lineal
```

### Opción 2: Ejecución Local

#### Paso 1: Clonar el repositorio

```bash
git clone <repository-url>
cd Analisis-de-datos-primera-tarea-fen-05-02-
```

#### Paso 2: Instalar dependencias de Python

```bash
pip install -r requirements.txt
```

#### Paso 3: Ejecutar el pipeline completo

```bash
# Opción A: Usar el script automatizado
./run_pipeline.sh

# Opción B: Ejecutar paso a paso
python generate_data.py        # Genera datos en Parquet
python load_arrow_data.py      # Demuestra operaciones Arrow
python linear_regression.py    # Ejecuta análisis
```

## 📊 Ventajas del Stack HPC

### Apache Arrow - Zero-Copy Operations

Apache Arrow permite operaciones sin copia de memoria:
- **Mayor velocidad**: Acceso directo a la memoria sin copias innecesarias
- **Menor uso de RAM**: Reutilización de buffers de memoria
- **Interoperabilidad**: Formato estándar entre diferentes herramientas

### Formato Parquet

- **Compresión eficiente**: Reduce tamaño de almacenamiento (Snappy compression)
- **Lectura columnar**: Solo lee las columnas necesarias
- **Metadata integrado**: Estadísticas y esquema incluidos
- **Portabilidad**: Formato estándar de la industria

## 📊 Resultados

El análisis genera los siguientes archivos:

1. **house_data.parquet**: Datos en formato columnar optimizado
   - Compresión Snappy para mejor rendimiento
   - Metadata integrado con estadísticas
   - Soporte para operaciones zero-copy

2. **house_data.csv**: Formato CSV para compatibilidad

3. **regression_output.tex**: Documento LaTeX completo con:
   - Metodología del análisis
   - Ecuación de regresión
   - Métricas de evaluación
   - Interpretación de resultados

4. **regression_plot.png**: Visualización con:
   - Scatter plot de datos reales
   - Línea de regresión ajustada
   - Gráfico de residuos

## 🔍 Características de los Datos

Cada casa en el conjunto de datos tiene las siguientes características:

- **area_m2**: Área en metros cuadrados (50-300 m²)
- **habitaciones**: Número de habitaciones (1-6)
- **banos**: Número de baños (1-4)
- **antiguedad_anos**: Antigüedad de la casa en años (0-50)
- **distancia_centro_km**: Distancia al centro de la ciudad en km (1-30)
- **calificacion_vecindario**: Calificación del vecindario (1-10)
- **precio_usd**: Precio de la casa en dólares

## 📈 Modelo de Regresión

El modelo de regresión lineal simple analiza la relación entre:
- **Variable independiente (X)**: Área de la casa (m²)
- **Variable dependiente (Y)**: Precio de la casa (USD)

La ecuación del modelo es: `Y = β₀ + β₁X`

Donde:
- β₀ es el intercepto (precio base)
- β₁ es la pendiente (incremento de precio por m²)

## 🛑 Detener el Proyecto

Para detener el contenedor Docker:

```bash
docker-compose down
```

## 📝 Compilar el Documento LaTeX

Para compilar el documento LaTeX generado:

```bash
pdflatex regression_output.tex
```

O usar un editor LaTeX online como [Overleaf](https://www.overleaf.com/).

## 🔧 Configuración Avanzada

### Cambiar número de muestras

Editar `generate_data.py` y modificar:
```python
data = generate_house_data(n_samples=1000, random_state=42)  # Genera 1000 casas
```

### Operaciones con Apache Arrow

El script `load_arrow_data.py` demuestra operaciones HPC:

```python
from load_arrow_data import ArrowDataLoader

# Cargar datos con zero-copy
loader = ArrowDataLoader('house_data.parquet')

# Obtener tabla Arrow (zero-copy)
table = loader.get_arrow_table()

# Filtrar por precio (operaciones eficientes)
filtered = loader.filter_by_price_range(200000, 300000)

# Obtener top N casas más caras
top_10 = loader.get_top_n_by_price(10)

# Estadísticas con PyArrow compute
stats = loader.get_statistics()
```

### Comparación de Formatos

| Característica | Parquet + Arrow | CSV |
|---------------|-----------------|-----|
| Tamaño en disco | ~20 KB (comprimido) | ~19 KB |
| Velocidad de lectura | **Muy rápida** | Lenta |
| Lectura columnar | ✅ Sí | ❌ No |
| Zero-copy | ✅ Sí | ❌ No |
| Metadata | ✅ Incluido | ❌ No |
| Compresión | ✅ Snappy/Gzip | ❌ No |

## 📚 Referencias

- [Apache Arrow Documentation](https://arrow.apache.org/docs/python/)
- [Parquet Format Specification](https://parquet.apache.org/docs/)
- [Scikit-learn Linear Regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html)
- [Docker Compose](https://docs.docker.com/compose/)

## 📄 Licencia

Este proyecto es para fines educativos.

## 👥 Autor

Proyecto creado para el curso de Análisis de Datos - FEN 05/02

---

## 🆕 Novedades en esta versión

- ✅ Migración de Neo4j a stack HPC con Parquet + Arrow
- ✅ Operaciones zero-copy para máximo rendimiento
- ✅ Formato columnar optimizado para análisis
- ✅ Sin dependencias de bases de datos externas
- ✅ Solución completa en contenedor Docker
- ✅ Compatible con entornos con restricciones de firewall
