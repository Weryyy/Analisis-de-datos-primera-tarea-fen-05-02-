"""
Script para realizar regresión lineal simple sobre los datos de casas
Analiza la relación entre el área de la casa y su precio
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from load_to_neo4j import Neo4jLoader


def load_data_from_neo4j():
    """
    Carga los datos desde Neo4j
    
    Returns:
        DataFrame con los datos de las casas
    """
    loader = Neo4jLoader()
    try:
        df = loader.get_all_houses()
        print(f"Datos cargados desde Neo4j: {len(df)} casas")
        return df
    finally:
        loader.close()


def perform_simple_linear_regression(df: pd.DataFrame, 
                                     feature: str = 'area_m2',
                                     target: str = 'precio_usd'):
    """
    Realiza regresión lineal simple
    
    Args:
        df: DataFrame con los datos
        feature: Variable independiente (característica)
        target: Variable dependiente (precio)
    
    Returns:
        Modelo entrenado y métricas
    """
    # Preparar datos
    X = df[[feature]].values
    y = df[target].values
    
    # Crear y entrenar modelo
    model = LinearRegression()
    model.fit(X, y)
    
    # Predicciones
    y_pred = model.predict(X)
    
    # Calcular métricas
    mse = mean_squared_error(y, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    
    # Coeficientes
    slope = model.coef_[0]
    intercept = model.intercept_
    
    results = {
        'model': model,
        'X': X,
        'y': y,
        'y_pred': y_pred,
        'slope': slope,
        'intercept': intercept,
        'mse': mse,
        'rmse': rmse,
        'mae': mae,
        'r2': r2,
        'feature': feature,
        'target': target
    }
    
    return results


def print_results(results: dict):
    """
    Imprime los resultados del análisis
    
    Args:
        results: Diccionario con los resultados
    """
    print("\n" + "="*60)
    print("RESULTADOS DE LA REGRESIÓN LINEAL SIMPLE")
    print("="*60)
    print(f"\nVariable independiente (X): {results['feature']}")
    print(f"Variable dependiente (Y): {results['target']}")
    print(f"\nEcuación de la recta:")
    print(f"  Y = {results['slope']:.2f}X + {results['intercept']:.2f}")
    print(f"\nMétricas de evaluación:")
    print(f"  R² (Coeficiente de determinación): {results['r2']:.4f}")
    print(f"  MSE (Error cuadrático medio): {results['mse']:,.2f}")
    print(f"  RMSE (Raíz del error cuadrático medio): {results['rmse']:,.2f}")
    print(f"  MAE (Error absoluto medio): {results['mae']:,.2f}")
    print("\nInterpretación:")
    print(f"  - Por cada unidad adicional de {results['feature']},")
    print(f"    el precio aumenta en ${results['slope']:.2f}")
    print(f"  - El R² de {results['r2']:.4f} indica que el {results['r2']*100:.2f}%")
    print(f"    de la variabilidad del precio es explicada por {results['feature']}")
    print("="*60)


def generate_latex_output(results: dict, output_file: str = 'regression_output.tex'):
    """
    Genera salida en formato LaTeX
    
    Args:
        results: Diccionario con los resultados
        output_file: Archivo de salida
    """
    latex_content = r"""
\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[spanish]{babel}
\usepackage{amsmath}
\usepackage{graphicx}
\usepackage{booktabs}

\title{Análisis de Regresión Lineal: Precio de Casas}
\author{Análisis de Datos}
\date{\today}

\begin{document}

\maketitle

\section{Introducción}
Este documento presenta los resultados de un análisis de regresión lineal simple 
sobre un conjunto de datos artificiales de precios de casas.

\section{Metodología}
Se utilizó regresión lineal simple para modelar la relación entre """ + \
    f"\\textbf{{{results['feature'].replace('_', ' ')}}} " + \
    f"y \\textbf{{{results['target'].replace('_', ' ')}}}.\n\n"
    
    latex_content += r"""\section{Modelo de Regresión}

El modelo de regresión lineal simple tiene la forma:
\begin{equation}
Y = \beta_0 + \beta_1 X + \epsilon
\end{equation}

donde:
\begin{itemize}
\item $Y$ es la variable dependiente (precio en USD)
\item $X$ es la variable independiente (""" + f"{results['feature'].replace('_', ' ')}" + r""")
\item $\beta_0$ es la ordenada al origen (intercepto)
\item $\beta_1$ es la pendiente
\item $\epsilon$ es el término de error
\end{itemize}

\section{Resultados}

Los parámetros estimados del modelo son:

\begin{equation}
Y = """ + f"{results['intercept']:.2f}" + r""" + """ + f"{results['slope']:.2f}" + r"""X
\end{equation}

\subsection{Métricas de Evaluación}

\begin{table}[h]
\centering
\begin{tabular}{@{}lc@{}}
\toprule
Métrica & Valor \\
\midrule
$R^2$ (Coeficiente de determinación) & """ + f"{results['r2']:.4f}" + r""" \\
MSE (Error cuadrático medio) & """ + f"{results['mse']:,.2f}" + r""" \\
RMSE (Raíz del error cuadrático medio) & """ + f"{results['rmse']:,.2f}" + r""" \\
MAE (Error absoluto medio) & """ + f"{results['mae']:,.2f}" + r""" \\
\bottomrule
\end{tabular}
\caption{Métricas de evaluación del modelo}
\end{table}

\subsection{Interpretación}

\begin{itemize}
\item La pendiente $\beta_1 = """ + f"{results['slope']:.2f}" + r"""$ indica que por cada unidad adicional 
de """ + f"{results['feature'].replace('_', ' ')}" + r""", el precio aumenta en \$""" + f"{results['slope']:.2f}" + r""".

\item El coeficiente de determinación $R^2 = """ + f"{results['r2']:.4f}" + r"""$ indica que 
aproximadamente el """ + f"{results['r2']*100:.2f}" + r"""\% de la variabilidad en el precio 
es explicada por """ + f"{results['feature'].replace('_', ' ')}" + r""".

\item El RMSE de \$""" + f"{results['rmse']:,.2f}" + r""" representa el error promedio de las predicciones.
\end{itemize}

\section{Conclusiones}

El análisis de regresión lineal simple muestra una relación """ + \
    ("fuerte" if results['r2'] > 0.7 else "moderada" if results['r2'] > 0.4 else "débil") + \
    r""" entre """ + f"{results['feature'].replace('_', ' ')}" + r""" y el precio de las casas. 
El modelo puede ser utilizado para predecir precios basándose en esta característica.

\end{document}
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(latex_content)
    
    print(f"\nArchivo LaTeX generado: {output_file}")


def create_visualization(results: dict, output_file: str = 'regression_plot.png'):
    """
    Crea visualización de la regresión
    
    Args:
        results: Diccionario con los resultados
        output_file: Archivo de salida para la gráfica
    """
    # Configurar estilo
    sns.set_style("whitegrid")
    
    # Crear subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Gráfico 1: Scatter plot con línea de regresión
    ax1.scatter(results['X'], results['y'], alpha=0.5, s=50, label='Datos reales')
    ax1.plot(results['X'], results['y_pred'], 'r-', linewidth=2, label='Línea de regresión')
    ax1.set_xlabel(results['feature'].replace('_', ' ').title(), fontsize=12)
    ax1.set_ylabel(results['target'].replace('_', ' ').title(), fontsize=12)
    ax1.set_title('Regresión Lineal Simple', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Añadir ecuación a la gráfica
    equation_text = f"Y = {results['slope']:.2f}X + {results['intercept']:.2f}\n$R^2$ = {results['r2']:.4f}"
    ax1.text(0.05, 0.95, equation_text, transform=ax1.transAxes,
             fontsize=11, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Gráfico 2: Residuos
    residuals = results['y'] - results['y_pred']
    ax2.scatter(results['y_pred'], residuals, alpha=0.5, s=50)
    ax2.axhline(y=0, color='r', linestyle='--', linewidth=2)
    ax2.set_xlabel('Valores Predichos', fontsize=12)
    ax2.set_ylabel('Residuos', fontsize=12)
    ax2.set_title('Gráfico de Residuos', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Gráfico guardado: {output_file}")
    plt.close()


if __name__ == '__main__':
    print("="*60)
    print("ANÁLISIS DE REGRESIÓN LINEAL - PRECIO DE CASAS")
    print("="*60)
    
    # Cargar datos desde Neo4j
    print("\nCargando datos desde Neo4j...")
    df = load_data_from_neo4j()
    
    # Realizar regresión lineal simple (área vs precio)
    print("\nRealizando regresión lineal simple...")
    results = perform_simple_linear_regression(df, feature='area_m2', target='precio_usd')
    
    # Imprimir resultados
    print_results(results)
    
    # Generar salida LaTeX
    print("\nGenerando salida LaTeX...")
    generate_latex_output(results, 'regression_output.tex')
    
    # Crear visualización
    print("\nCreando visualizaciones...")
    create_visualization(results, 'regression_plot.png')
    
    print("\n" + "="*60)
    print("¡Análisis completado exitosamente!")
    print("="*60)
    print("\nArchivos generados:")
    print("  - regression_output.tex (documento LaTeX)")
    print("  - regression_plot.png (visualización)")
