"""
Script para cargar y manipular datos usando Apache Arrow
Utiliza operaciones zero-copy para máximo rendimiento
"""
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.compute as pc
import pandas as pd
from typing import Optional, Dict, List


class ArrowDataLoader:
    """
    Clase para gestionar datos usando Apache Arrow con operaciones zero-copy
    Proporciona acceso de alto rendimiento a los datos almacenados en Parquet
    """
    
    def __init__(self, parquet_path: str = 'house_data.parquet'):
        """
        Inicializa el cargador de datos Arrow
        
        Args:
            parquet_path: Ruta al archivo Parquet
        """
        self.parquet_path = parquet_path
        self.table = None
        self._load_data()
    
    def _load_data(self):
        """
        Carga los datos desde Parquet usando Apache Arrow
        Utiliza zero-copy para máximo rendimiento
        """
        try:
            # Cargar usando PyArrow (zero-copy cuando sea posible)
            self.table = pq.read_table(self.parquet_path)
            print(f"Datos cargados desde {self.parquet_path}")
            print(f"Total de registros: {len(self.table)}")
            print(f"Columnas: {self.table.column_names}")
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            raise
    
    def get_arrow_table(self) -> pa.Table:
        """
        Retorna la tabla Arrow (zero-copy)
        
        Returns:
            Tabla PyArrow
        """
        return self.table
    
    def get_pandas_dataframe(self, zero_copy: bool = True) -> pd.DataFrame:
        """
        Convierte a Pandas DataFrame
        
        Args:
            zero_copy: Si es True, usa zero-copy cuando sea posible
            
        Returns:
            DataFrame de Pandas
        """
        # Usar zero_copy_only para evitar copias innecesarias
        if zero_copy:
            return self.table.to_pandas(self_destruct=False, split_blocks=True, 
                                        use_threads=True)
        return self.table.to_pandas()
    
    def get_column(self, column_name: str) -> pa.Array:
        """
        Obtiene una columna específica (zero-copy)
        
        Args:
            column_name: Nombre de la columna
            
        Returns:
            Array de PyArrow
        """
        return self.table.column(column_name)
    
    def get_statistics(self) -> Dict:
        """
        Calcula estadísticas básicas usando PyArrow compute
        
        Returns:
            Diccionario con estadísticas
        """
        stats = {}
        
        # Calcular estadísticas para precio
        precio = self.table.column('precio_usd')
        stats['precio_promedio'] = pc.mean(precio).as_py()
        stats['precio_minimo'] = pc.min(precio).as_py()
        stats['precio_maximo'] = pc.max(precio).as_py()
        stats['precio_std'] = pc.stddev(precio).as_py()
        
        # Calcular estadísticas para área
        area = self.table.column('area_m2')
        stats['area_promedio'] = pc.mean(area).as_py()
        stats['area_minima'] = pc.min(area).as_py()
        stats['area_maxima'] = pc.max(area).as_py()
        
        # Total de casas
        stats['total_casas'] = len(self.table)
        
        return stats
    
    def filter_by_price_range(self, min_price: float, max_price: float) -> pa.Table:
        """
        Filtra casas por rango de precio usando PyArrow compute
        
        Args:
            min_price: Precio mínimo
            max_price: Precio máximo
            
        Returns:
            Tabla filtrada
        """
        precio = self.table.column('precio_usd')
        mask = pc.and_(pc.greater_equal(precio, min_price), 
                      pc.less_equal(precio, max_price))
        return self.table.filter(mask)
    
    def filter_by_area_range(self, min_area: float, max_area: float) -> pa.Table:
        """
        Filtra casas por rango de área
        
        Args:
            min_area: Área mínima
            max_area: Área máxima
            
        Returns:
            Tabla filtrada
        """
        area = self.table.column('area_m2')
        mask = pc.and_(pc.greater_equal(area, min_area), 
                      pc.less_equal(area, max_area))
        return self.table.filter(mask)
    
    def sort_by_column(self, column_name: str, ascending: bool = True) -> pa.Table:
        """
        Ordena la tabla por una columna
        
        Args:
            column_name: Nombre de la columna
            ascending: Si es True, orden ascendente
            
        Returns:
            Tabla ordenada
        """
        order = "ascending" if ascending else "descending"
        indices = pc.sort_indices(self.table, sort_keys=[(column_name, order)])
        return pc.take(self.table, indices)
    
    def get_top_n_by_price(self, n: int = 10) -> pd.DataFrame:
        """
        Obtiene las N casas más caras
        
        Args:
            n: Número de casas a retornar
            
        Returns:
            DataFrame con las casas más caras
        """
        sorted_table = self.sort_by_column('precio_usd', ascending=False)
        top_n = sorted_table.slice(0, n)
        return top_n.to_pandas()
    
    def save_to_parquet(self, output_path: str, compression: str = 'snappy'):
        """
        Guarda la tabla en formato Parquet
        
        Args:
            output_path: Ruta del archivo de salida
            compression: Tipo de compresión (snappy, gzip, brotli, lz4)
        """
        pq.write_table(self.table, output_path, compression=compression)
        print(f"Tabla guardada en: {output_path}")


def demonstrate_arrow_operations():
    """
    Demuestra las capacidades de Apache Arrow con operaciones zero-copy
    """
    print("="*60)
    print("DEMOSTRACIÓN DE APACHE ARROW - OPERACIONES ZERO-COPY")
    print("="*60)
    
    # Cargar datos
    loader = ArrowDataLoader('house_data.parquet')
    
    # Mostrar estadísticas
    print("\nEstadísticas (calculadas con PyArrow compute):")
    stats = loader.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:,.2f}")
        else:
            print(f"  {key}: {value}")
    
    # Filtrar por precio
    print("\nFiltrando casas entre $200,000 y $300,000...")
    filtered = loader.filter_by_price_range(200000, 300000)
    print(f"Casas encontradas: {len(filtered)}")
    
    # Top 10 casas más caras
    print("\nTop 10 casas más caras:")
    top_10 = loader.get_top_n_by_price(10)
    print(top_10[['id', 'area_m2', 'habitaciones', 'precio_usd']].to_string(index=False))
    
    # Conversión a Pandas con zero-copy
    print("\nConvirtiendo a Pandas DataFrame (zero-copy)...")
    df = loader.get_pandas_dataframe(zero_copy=True)
    print(f"DataFrame creado con {len(df)} registros")
    print(f"Memoria aproximada: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
    
    print("\n" + "="*60)
    print("¡Demostración completada!")
    print("="*60)


if __name__ == '__main__':
    demonstrate_arrow_operations()
