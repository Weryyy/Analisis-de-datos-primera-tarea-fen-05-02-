# Guía Rápida de Inicio

Esta guía te ayudará a ejecutar el análisis de precios de casas en pocos minutos.

## 📦 Instalación Rápida

### 1. Instalar Docker

Si no tienes Docker instalado:
- **Windows/Mac**: Descarga [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Linux**: 
  ```bash
  sudo apt-get update
  sudo apt-get install docker.io docker-compose-plugin
  ```

### 2. Instalar Python 3.8+

Verifica tu versión de Python:
```bash
python3 --version
```

### 3. Instalar dependencias de Python

```bash
pip install -r requirements.txt
```

## 🚀 Ejecución Rápida (3 pasos)

### Opción A: Ejecutar todo automáticamente

```bash
# 1. Iniciar Neo4j
docker compose up -d

# 2. Esperar 30 segundos para que Neo4j inicie completamente
sleep 30

# 3. Ejecutar el pipeline completo
./run_pipeline.sh
```

### Opción B: Ejecutar paso a paso

```bash
# 1. Iniciar Neo4j
docker compose up -d

# 2. Esperar a que Neo4j esté listo (30 segundos)
sleep 30

# 3. Generar datos artificiales
python generate_data.py

# 4. Cargar datos en Neo4j
python load_to_neo4j.py

# 5. Ejecutar análisis de regresión
python linear_regression.py
```

## 📊 Resultados

Después de ejecutar el análisis, encontrarás:

1. **house_data.csv** - 500 casas con características aleatorias
2. **regression_output.tex** - Documento LaTeX con resultados completos
3. **regression_plot.png** - Visualización gráfica del análisis

## 🌐 Acceder a Neo4j Browser

Abre tu navegador y ve a: http://localhost:7474

**Credenciales:**
- Usuario: `neo4j`
- Contraseña: `password123`

## 🔍 Consultas Neo4j útiles

```cypher
// Ver todas las casas
MATCH (h:House) RETURN h LIMIT 25

// Casas más caras
MATCH (h:House) 
RETURN h.id, h.precio_usd, h.area_m2 
ORDER BY h.precio_usd DESC 
LIMIT 10

// Casas más baratas
MATCH (h:House) 
RETURN h.id, h.precio_usd, h.area_m2 
ORDER BY h.precio_usd ASC 
LIMIT 10

// Precio promedio por número de habitaciones
MATCH (h:House) 
RETURN h.habitaciones, avg(h.precio_usd) as precio_promedio 
ORDER BY h.habitaciones
```

## 🛑 Detener el sistema

```bash
docker compose down
```

## ❓ Solución de Problemas

### Error: "No se pudo conectar a Neo4j"

**Solución:** Neo4j necesita tiempo para iniciar. Espera 30-60 segundos después de `docker compose up -d`

### Error: "ModuleNotFoundError"

**Solución:** Instala las dependencias:
```bash
pip install numpy pandas matplotlib scikit-learn seaborn neo4j
```

### Error: "docker: command not found"

**Solución:** Instala Docker Desktop o el Docker Engine

### Error: "Puerto 7474 o 7687 ya en uso"

**Solución:** Otro proceso está usando esos puertos. Detén otros servicios Neo4j o cambia los puertos en `docker-compose.yml`

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

## 📚 Más información

Ver el [README.md](README.md) completo para documentación detallada.
