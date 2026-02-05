#!/bin/bash
set -e  # Exit immediately if any command fails

# Script para ejecutar el pipeline completo de análisis

echo "============================================"
echo "Pipeline de Análisis de Precios de Casas"
echo "============================================"
echo ""

# Paso 1: Generar datos
echo "Paso 1: Generando datos artificiales..."
python generate_data.py
if [ $? -ne 0 ]; then
    echo "Error al generar datos"
    exit 1
fi
echo ""

# Paso 2: Cargar datos en Neo4j
echo "Paso 2: Cargando datos en Neo4j..."
python load_to_neo4j.py
if [ $? -ne 0 ]; then
    echo "Error al cargar datos en Neo4j"
    echo "Asegúrate de que Neo4j esté ejecutándose (docker-compose up -d)"
    exit 1
fi
echo ""

# Paso 3: Ejecutar análisis de regresión
echo "Paso 3: Ejecutando análisis de regresión lineal..."
python linear_regression.py
if [ $? -ne 0 ]; then
    echo "Error al ejecutar análisis"
    exit 1
fi
echo ""

echo "============================================"
echo "¡Pipeline completado exitosamente!"
echo "============================================"
echo ""
echo "Archivos generados:"
echo "  - house_data.csv"
echo "  - regression_output.tex"
echo "  - regression_plot.png"
echo ""
