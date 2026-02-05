#!/bin/bash
set -e  # Exit immediately if any command fails

# Script para ejecutar el pipeline completo de análisis con HPC Stack

echo "============================================"
echo "Pipeline de Análisis de Precios de Casas"
echo "HPC Stack: Parquet + Apache Arrow"
echo "============================================"
echo ""

# Paso 1: Generar datos
echo "Paso 1: Generando datos artificiales en formato Parquet..."
python generate_data.py
if [ $? -ne 0 ]; then
    echo "Error al generar datos"
    exit 1
fi
echo ""

# Paso 2: Demostrar operaciones Arrow
echo "Paso 2: Demostrando operaciones Arrow (zero-copy)..."
python load_arrow_data.py
if [ $? -ne 0 ]; then
    echo "Error al cargar datos con Arrow"
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
echo "  - house_data.parquet (formato HPC optimizado)"
echo "  - house_data.csv (compatibilidad)"
echo "  - regression_output.tex"
echo "  - regression_plot.png"
echo ""
