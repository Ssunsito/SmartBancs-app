import pandas as pd
import json
import time
import schedule
import os

def ejecutar_etl():
    print("[ETL] Iniciando proceso de extracción y limpieza de datos en lote...")
    
    # Datos simulados sin procesar
    datos_crudos = [
        {"id": 1, "monto": 50.0, "fecha": "2026-10-01", "estado": "COMPLETADA", "moneda": "USD"},
        {"id": 2, "monto": None, "fecha": "01-10-2026", "estado": "PENDIENTE", "moneda": "usd"},
        {"id": 3, "monto": 1500.5, "fecha": "2026-10-02", "estado": "fallida", "moneda": " Usd "}
    ]
    df = pd.DataFrame(datos_crudos)
    
    # Transformación y limpieza
    df = df.dropna(subset=['monto'])
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce').dt.strftime('%Y-%m-%d')
    df['estado'] = df['estado'].str.strip().str.upper()
    df['moneda'] = df['moneda'].str.strip().str.upper()
    
    # Exportación
    os.makedirs("/app/data", exist_ok=True)
    ruta_salida = "/app/data/dataset_optimizado_ia.json"
    
    datos_limpios = df.to_dict(orient="records")
    with open(ruta_salida, "w") as f:
        json.dump(datos_limpios, f, indent=4)
        
    print(f"[ETL] Lote procesado. Dataset exportado en {ruta_salida}.")

if __name__ == "__main__":
    print("[ETL] Orquestador iniciado. Ejecutando primera carga...")
    ejecutar_etl()
    
    # Programa el ETL para ejecutarse cada 1 minuto (ideal para la demostración en video)
    schedule.every(1).minutes.do(ejecutar_etl)
    
    while True:
        schedule.run_pending()
        time.sleep(1)