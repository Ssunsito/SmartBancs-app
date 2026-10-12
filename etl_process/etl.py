import pandas as pd
import json
import time
import schedule
import os
from sqlalchemy import create_engine

# Captura la URL de conexión inyectada por Docker
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://smartbancs_user:supersecretpassword@localhost:5432/smartbancs")

def ejecutar_etl():
    print("[ETL] Iniciando proceso de extracción y limpieza desde PostgreSQL...")
    try:
        # 1. Extracción: Conexión a la base de datos real
        engine = create_engine(DATABASE_URL)
        query = "SELECT * FROM transacciones;"
        df = pd.read_sql(query, engine)
        
        if df.empty:
            print("[ETL] No hay transacciones en la base de datos para procesar.")
            return

        # 2. Transformación y Limpieza
        print(f"[ETL] Se extrajeron {len(df)} transacciones crudas de la base de datos.")
        
        # Elimina posibles nulos o errores de integridad en el monto
        df = df.dropna(subset=['monto'])
        
        # Estandariza formatos incompatibles con JSON
        if 'fecha_transaccion' in df.columns:
            df['fecha_transaccion'] = pd.to_datetime(df['fecha_transaccion']).dt.strftime('%Y-%m-%d %H:%M:%S')
        
        if 'id' in df.columns:
            df['id'] = df['id'].astype(str) # Los UUID deben ser strings para el JSON

        # 3. Carga: Exportación del Dataset
        os.makedirs("/app/data", exist_ok=True)
        ruta_salida = "/app/data/dataset_optimizado_ia.json"
        
        datos_limpios = df.to_dict(orient="records")
        with open(ruta_salida, "w") as f:
            json.dump(datos_limpios, f, indent=4)
            
        print(f"[ETL] Exito. {len(df)} registros limpios exportados en {ruta_salida}.")

    except Exception as e:
        print(f"[ETL] Error critico de procesamiento: {str(e)}")

if __name__ == "__main__":
    print("[ETL] Orquestador iniciado. Ejecutando primera carga...")
    ejecutar_etl()
    
    # Se ejecutará cada 1 minuto
    schedule.every(1).minutes.do(ejecutar_etl)
    
    while True:
        schedule.run_pending()
        time.sleep(1)