"""
Script para generar datos artificiales de precios de casas
Genera un conjunto de datos sintético con características de casas y sus precios
"""
import numpy as np
import pandas as pd
from typing import Tuple


def generate_house_data(n_samples: int = 500, random_state: int = 42) -> pd.DataFrame:
    """
    Genera datos artificiales de casas con sus características y precios
    
    Args:
        n_samples: Número de casas a generar
        random_state: Semilla para reproducibilidad
    
    Returns:
        DataFrame con los datos generados
    """
    np.random.seed(random_state)
    
    # Características de las casas
    # Área en metros cuadrados (50-300 m²)
    area = np.random.normal(150, 50, n_samples)
    area = np.clip(area, 50, 300)
    
    # Número de habitaciones (1-6)
    habitaciones = np.random.randint(1, 7, n_samples)
    
    # Número de baños (1-4)
    banos = np.random.randint(1, 5, n_samples)
    
    # Antigüedad de la casa en años (0-50)
    antiguedad = np.random.exponential(15, n_samples)
    antiguedad = np.clip(antiguedad, 0, 50)
    
    # Distancia al centro en km (1-30)
    distancia_centro = np.random.gamma(3, 3, n_samples)
    distancia_centro = np.clip(distancia_centro, 1, 30)
    
    # Calificación del vecindario (1-10)
    calificacion_vecindario = np.random.normal(7, 1.5, n_samples)
    calificacion_vecindario = np.clip(calificacion_vecindario, 1, 10)
    
    # Generar precio basado en una relación lineal con ruido
    # Precio base
    precio = 50000  # Precio base
    
    # Factores que influyen en el precio
    precio += area * 800  # $800 por m²
    precio += habitaciones * 15000  # $15,000 por habitación
    precio += banos * 10000  # $10,000 por baño
    precio -= antiguedad * 1000  # -$1,000 por año de antigüedad
    precio -= distancia_centro * 2000  # -$2,000 por km de distancia
    precio += calificacion_vecindario * 5000  # $5,000 por punto de calificación
    
    # Agregar ruido aleatorio (±10%)
    ruido = np.random.normal(0, precio * 0.1, n_samples)
    precio += ruido
    
    # Asegurar precios positivos
    precio = np.clip(precio, 30000, None)
    
    # Crear DataFrame
    df = pd.DataFrame({
        'id': range(1, n_samples + 1),
        'area_m2': np.round(area, 2),
        'habitaciones': habitaciones,
        'banos': banos,
        'antiguedad_anos': np.round(antiguedad, 1),
        'distancia_centro_km': np.round(distancia_centro, 2),
        'calificacion_vecindario': np.round(calificacion_vecindario, 1),
        'precio_usd': np.round(precio, 2)
    })
    
    return df


def save_data(df: pd.DataFrame, output_path: str = 'house_data.parquet'):
    """
    Guarda los datos generados en formato Parquet usando Apache Arrow
    
    Args:
        df: DataFrame con los datos
        output_path: Ruta del archivo de salida
    """
    # Guardar en formato Parquet con compresión snappy para mejor rendimiento
    df.to_parquet(output_path, engine='pyarrow', compression='snappy', index=False)
    print(f"Datos guardados en formato Parquet: {output_path}")
    print(f"Total de registros: {len(df)}")
    print(f"\nEstadísticas básicas:")
    print(df.describe())


if __name__ == '__main__':
    # Generar 500 casas
    print("Generando datos artificiales de casas...")
    data = generate_house_data(n_samples=500, random_state=42)
    
    # Guardar datos en formato Parquet
    save_data(data, 'house_data.parquet')
    
    # También guardar en CSV para compatibilidad
    data.to_csv('house_data.csv', index=False)
    print("\nTambién guardado en CSV para compatibilidad: house_data.csv")
    
    print("\n¡Datos generados exitosamente!")
