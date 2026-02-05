"""
Script de comparación de rendimiento: CSV vs Parquet + Arrow
Demuestra las ventajas del stack HPC
"""
import time
import pandas as pd
import pyarrow.parquet as pq
from load_arrow_data import ArrowDataLoader


def benchmark_csv_loading():
    """Benchmark de carga desde CSV"""
    print("\n" + "="*60)
    print("BENCHMARK: Carga desde CSV (tradicional)")
    print("="*60)
    
    start_time = time.time()
    df = pd.read_csv('house_data.csv')
    load_time = time.time() - start_time
    
    print(f"Tiempo de carga: {load_time*1000:.2f} ms")
    print(f"Registros cargados: {len(df)}")
    print(f"Memoria usada: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
    
    return load_time, df


def benchmark_parquet_loading():
    """Benchmark de carga desde Parquet"""
    print("\n" + "="*60)
    print("BENCHMARK: Carga desde Parquet (tradicional)")
    print("="*60)
    
    start_time = time.time()
    df = pd.read_parquet('house_data.parquet')
    load_time = time.time() - start_time
    
    print(f"Tiempo de carga: {load_time*1000:.2f} ms")
    print(f"Registros cargados: {len(df)}")
    print(f"Memoria usada: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
    
    return load_time, df


def benchmark_arrow_loading():
    """Benchmark de carga con Apache Arrow (zero-copy)"""
    print("\n" + "="*60)
    print("BENCHMARK: Carga con Apache Arrow (zero-copy)")
    print("="*60)
    
    start_time = time.time()
    loader = ArrowDataLoader('house_data.parquet')
    df = loader.get_pandas_dataframe(zero_copy=True)
    load_time = time.time() - start_time
    
    print(f"Tiempo de carga: {load_time*1000:.2f} ms")
    print(f"Registros cargados: {len(df)}")
    print(f"Memoria usada: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
    
    return load_time, df, loader


def benchmark_filtering():
    """Benchmark de operaciones de filtrado"""
    print("\n" + "="*60)
    print("BENCHMARK: Operaciones de filtrado")
    print("="*60)
    
    # CSV/Pandas tradicional
    df_csv = pd.read_csv('house_data.csv')
    start_time = time.time()
    filtered_pandas = df_csv[(df_csv['precio_usd'] >= 200000) & 
                             (df_csv['precio_usd'] <= 300000)]
    pandas_time = time.time() - start_time
    print(f"Pandas (CSV): {pandas_time*1000:.2f} ms - {len(filtered_pandas)} registros")
    
    # Arrow con PyArrow compute
    loader = ArrowDataLoader('house_data.parquet')
    start_time = time.time()
    filtered_arrow = loader.filter_by_price_range(200000, 300000)
    arrow_time = time.time() - start_time
    print(f"Arrow (Parquet): {arrow_time*1000:.2f} ms - {len(filtered_arrow)} registros")
    
    speedup = pandas_time / arrow_time if arrow_time > 0 else float('inf')
    print(f"\n⚡ Arrow es {speedup:.1f}x más rápido")


def benchmark_statistics():
    """Benchmark de cálculo de estadísticas"""
    print("\n" + "="*60)
    print("BENCHMARK: Cálculo de estadísticas")
    print("="*60)
    
    # Pandas tradicional
    df = pd.read_csv('house_data.csv')
    start_time = time.time()
    pandas_stats = {
        'mean': df['precio_usd'].mean(),
        'min': df['precio_usd'].min(),
        'max': df['precio_usd'].max(),
        'std': df['precio_usd'].std()
    }
    pandas_time = time.time() - start_time
    print(f"Pandas: {pandas_time*1000:.2f} ms")
    
    # Arrow compute
    loader = ArrowDataLoader('house_data.parquet')
    start_time = time.time()
    arrow_stats = loader.get_statistics()
    arrow_time = time.time() - start_time
    print(f"Arrow: {arrow_time*1000:.2f} ms")
    
    speedup = pandas_time / arrow_time if arrow_time > 0 else float('inf')
    print(f"\n⚡ Arrow es {speedup:.1f}x más rápido")


def compare_file_sizes():
    """Compara tamaños de archivo"""
    print("\n" + "="*60)
    print("COMPARACIÓN: Tamaños de archivo")
    print("="*60)
    
    import os
    
    csv_size = os.path.getsize('house_data.csv')
    parquet_size = os.path.getsize('house_data.parquet')
    
    print(f"CSV: {csv_size:,} bytes ({csv_size/1024:.2f} KB)")
    print(f"Parquet (comprimido): {parquet_size:,} bytes ({parquet_size/1024:.2f} KB)")
    
    compression_ratio = csv_size / parquet_size
    print(f"\nRatio de compresión: {compression_ratio:.2f}x")


def main():
    """Ejecuta todos los benchmarks"""
    print("\n" + "="*70)
    print("SUITE DE BENCHMARKS: HPC Stack vs Enfoque Tradicional")
    print("="*70)
    
    # Generar datos si no existen
    try:
        with open('house_data.csv'):
            pass
    except FileNotFoundError:
        print("\nGenerando datos de prueba...")
        import subprocess
        subprocess.run(['python', 'generate_data.py'])
    
    # Ejecutar benchmarks
    csv_time, _ = benchmark_csv_loading()
    parquet_time, _ = benchmark_parquet_loading()
    arrow_time, _, _ = benchmark_arrow_loading()
    
    # Benchmarks de operaciones
    benchmark_filtering()
    benchmark_statistics()
    compare_file_sizes()
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN DE RENDIMIENTO")
    print("="*70)
    print(f"\n📊 Tiempo de carga:")
    print(f"   CSV:     {csv_time*1000:.2f} ms")
    print(f"   Parquet: {parquet_time*1000:.2f} ms ({csv_time/parquet_time:.1f}x más rápido)")
    print(f"   Arrow:   {arrow_time*1000:.2f} ms ({csv_time/arrow_time:.1f}x más rápido)")
    
    print(f"\n🚀 Conclusión:")
    print(f"   El stack HPC (Parquet + Arrow) es significativamente más rápido")
    print(f"   para operaciones de lectura, filtrado y análisis de datos.")
    print(f"   Ideal para entornos sin acceso a red/bases de datos externas.")
    
    print("\n" + "="*70)


if __name__ == '__main__':
    main()
