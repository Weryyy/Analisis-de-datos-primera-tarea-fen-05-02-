# Análisis de Datos: Precios de Casas

Proyecto de análisis de datos que genera un conjunto de datos artificiales de precios de casas, los almacena en Neo4j usando Docker, y realiza un análisis de regresión lineal simple.

## 📋 Descripción

Este proyecto crea un conjunto de datos sintético de 500 casas con diversas características (área, habitaciones, baños, antigüedad, etc.) y sus respectivos precios. Los datos se almacenan en una base de datos Neo4j desplegada mediante Docker, y se realiza un análisis de regresión lineal simple para estudiar la relación entre el área de la casa y su precio.

## 🛠️ Tecnologías Utilizadas

- **Python 3.x**: Lenguaje principal del proyecto
- **Neo4j 5.15.0**: Base de datos de grafos para almacenar los datos
- **Docker**: Containerización para despliegue fácil
- **Pandas & NumPy**: Manipulación y generación de datos
- **Scikit-learn**: Implementación de regresión lineal
- **Matplotlib & Seaborn**: Visualización de datos
- **LaTeX**: Generación de documentos profesionales

## 📁 Estructura del Proyecto

```
.
├── docker-compose.yml          # Configuración de Docker para Neo4j
├── requirements.txt            # Dependencias de Python
├── generate_data.py           # Generación de datos artificiales
├── load_to_neo4j.py          # Carga de datos en Neo4j
├── linear_regression.py       # Análisis de regresión lineal
├── house_data.csv            # Datos generados (creado al ejecutar)
├── regression_output.tex      # Salida en formato LaTeX (creado al ejecutar)
└── regression_plot.png        # Visualización de la regresión (creado al ejecutar)
```

## 🚀 Instalación y Uso

### Prerrequisitos

- Docker y Docker Compose instalados
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Clonar el repositorio

```bash
git clone <repository-url>
cd Analisis-de-datos-primera-tarea-fen-05-02-
```

### Paso 2: Instalar dependencias de Python

```bash
pip install -r requirements.txt
```

### Paso 3: Iniciar Neo4j con Docker

```bash
docker-compose up -d
```

Esto iniciará Neo4j en:
- **Browser Neo4j**: http://localhost:7474
- **Bolt Protocol**: bolt://localhost:7687
- **Credenciales**: usuario: `neo4j`, contraseña: `password123`

### Paso 4: Generar datos artificiales

```bash
python generate_data.py
```

Este script genera 500 registros de casas con características aleatorias pero realistas, guardándolos en `house_data.csv`.

### Paso 5: Cargar datos en Neo4j

```bash
python load_to_neo4j.py
```

Este script carga los datos del CSV a la base de datos Neo4j.

### Paso 6: Ejecutar análisis de regresión lineal

```bash
python linear_regression.py
```

Este script:
1. Carga los datos desde Neo4j
2. Realiza regresión lineal simple (área vs precio)
3. Calcula métricas de evaluación (R², MSE, RMSE, MAE)
4. Genera un documento LaTeX con los resultados
5. Crea visualizaciones gráficas

## 📊 Resultados

El análisis genera los siguientes archivos:

1. **regression_output.tex**: Documento LaTeX completo con:
   - Metodología del análisis
   - Ecuación de regresión
   - Métricas de evaluación
   - Interpretación de resultados

2. **regression_plot.png**: Visualización con:
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

Para detener Neo4j:

```bash
docker-compose down
```

Para detener y eliminar todos los datos:

```bash
docker-compose down -v
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

### Cambiar credenciales de Neo4j

Editar `docker-compose.yml`:
```yaml
- NEO4J_AUTH=neo4j/tu_nueva_contraseña
```

Y actualizar en `load_to_neo4j.py` y `linear_regression.py`.

## 📚 Referencias

- [Neo4j Python Driver](https://neo4j.com/docs/python-manual/current/)
- [Scikit-learn Linear Regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html)
- [Docker Compose](https://docs.docker.com/compose/)

## 📄 Licencia

Este proyecto es para fines educativos.

## 👥 Autor

Proyecto creado para el curso de Análisis de Datos - FEN 05/02
