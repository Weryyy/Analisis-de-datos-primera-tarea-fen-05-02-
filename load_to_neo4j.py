"""
Script para cargar los datos de casas en Neo4j
"""
from neo4j import GraphDatabase
import pandas as pd
import time


class Neo4jLoader:
    def __init__(self, uri: str = "bolt://localhost:7687", 
                 user: str = "neo4j", 
                 password: str = "password123"):
        """
        Inicializa la conexión con Neo4j
        
        Args:
            uri: URI de conexión a Neo4j
            user: Usuario de Neo4j
            password: Contraseña de Neo4j
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        """Cierra la conexión con Neo4j"""
        self.driver.close()
    
    def clear_database(self):
        """Limpia la base de datos"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("Base de datos limpiada")
    
    def create_constraints(self):
        """Crea restricciones e índices en la base de datos"""
        with self.driver.session() as session:
            # Crear constraint para IDs únicos
            try:
                session.run("""
                    CREATE CONSTRAINT house_id_unique IF NOT EXISTS
                    FOR (h:House) REQUIRE h.id IS UNIQUE
                """)
                print("Constraint creado: house_id_unique")
            except Exception as e:
                print(f"Constraint ya existe o error: {e}")
    
    def load_houses(self, csv_path: str = 'house_data.csv'):
        """
        Carga las casas desde el archivo CSV a Neo4j
        
        Args:
            csv_path: Ruta al archivo CSV con los datos
        """
        df = pd.read_csv(csv_path)
        
        with self.driver.session() as session:
            # Crear nodos de casas
            for _, row in df.iterrows():
                session.run("""
                    CREATE (h:House {
                        id: $id,
                        area_m2: $area_m2,
                        habitaciones: $habitaciones,
                        banos: $banos,
                        antiguedad_anos: $antiguedad_anos,
                        distancia_centro_km: $distancia_centro_km,
                        calificacion_vecindario: $calificacion_vecindario,
                        precio_usd: $precio_usd
                    })
                """, 
                    id=int(row['id']),
                    area_m2=float(row['area_m2']),
                    habitaciones=int(row['habitaciones']),
                    banos=int(row['banos']),
                    antiguedad_anos=float(row['antiguedad_anos']),
                    distancia_centro_km=float(row['distancia_centro_km']),
                    calificacion_vecindario=float(row['calificacion_vecindario']),
                    precio_usd=float(row['precio_usd'])
                )
            
            print(f"Cargadas {len(df)} casas en Neo4j")
    
    def get_all_houses(self):
        """
        Recupera todas las casas de Neo4j
        
        Returns:
            DataFrame con todas las casas
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (h:House)
                RETURN h.id as id, 
                       h.area_m2 as area_m2,
                       h.habitaciones as habitaciones,
                       h.banos as banos,
                       h.antiguedad_anos as antiguedad_anos,
                       h.distancia_centro_km as distancia_centro_km,
                       h.calificacion_vecindario as calificacion_vecindario,
                       h.precio_usd as precio_usd
                ORDER BY h.id
            """)
            
            data = [dict(record) for record in result]
            return pd.DataFrame(data)
    
    def get_statistics(self):
        """
        Obtiene estadísticas básicas de la base de datos
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (h:House)
                RETURN count(h) as total_houses,
                       avg(h.precio_usd) as precio_promedio,
                       min(h.precio_usd) as precio_minimo,
                       max(h.precio_usd) as precio_maximo,
                       avg(h.area_m2) as area_promedio
            """)
            
            stats = result.single()
            return dict(stats)


def wait_for_neo4j(max_attempts: int = 30, delay: int = 2):
    """
    Espera a que Neo4j esté disponible
    
    Args:
        max_attempts: Número máximo de intentos
        delay: Segundos entre intentos
    """
    for attempt in range(max_attempts):
        try:
            loader = Neo4jLoader()
            loader.close()
            print("Neo4j está disponible")
            return True
        except Exception as e:
            print(f"Intento {attempt + 1}/{max_attempts}: Esperando a Neo4j...")
            time.sleep(delay)
    
    raise Exception("No se pudo conectar a Neo4j")


if __name__ == '__main__':
    print("Esperando a que Neo4j esté disponible...")
    wait_for_neo4j()
    
    # Crear instancia del loader
    loader = Neo4jLoader()
    
    try:
        # Limpiar base de datos
        print("\nLimpiando base de datos...")
        loader.clear_database()
        
        # Crear constraints
        print("\nCreando constraints...")
        loader.create_constraints()
        
        # Cargar datos
        print("\nCargando datos de casas...")
        loader.load_houses('house_data.csv')
        
        # Mostrar estadísticas
        print("\nEstadísticas de la base de datos:")
        stats = loader.get_statistics()
        for key, value in stats.items():
            if isinstance(value, float):
                print(f"  {key}: {value:,.2f}")
            else:
                print(f"  {key}: {value}")
        
        print("\n¡Datos cargados exitosamente en Neo4j!")
        
    finally:
        loader.close()
