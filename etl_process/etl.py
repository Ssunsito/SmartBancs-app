import pandas as pd
import json

def ejecutar_etl():
    print("[ETL] Iniciando proceso de extracción y limpieza de datos...")
    
    # 1. Extracción: Simulamos datos crudos extraídos con ruido y valores nulos
    datos_crudos = [
        {"id": 1, "monto": 50.0, "fecha": "2026-10-01", "estado": "COMPLETADA", "moneda": "USD"},
        {"id": 2, "monto": None, "fecha": "01-10-2026", "estado": "PENDIENTE", "moneda": "usd"},
        {"id": 3, "monto": 1500.5, "fecha": "2026-10-02", "estado": "fallida", "moneda": " Usd "}
    ]
    df = pd.DataFrame(datos_crudos)
    
    # 2. Transformación y Limpieza
    # a. Eliminar transacciones sin monto (manejo de nulos)
    df = df.dropna(subset=['monto'])
    
    # b. Estandarizar fechas al formato YYYY-MM-DD
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce').dt.strftime('%Y-%m-%d')
    
    # c. Estandarizar strings (estado y moneda) a mayúsculas sin espacios
    df['estado'] = df['estado'].str.strip().str.upper()
    df['moneda'] = df['moneda'].str.strip().str.upper()
    
    # 3. Carga: Exportar a un formato optimizado (ej. JSON estructurado)
    datos_limpios = df.to_dict(orient="records")
    with open("dataset_optimizado_ia.json", "w") as f:
        json.dump(datos_limpios, f, indent=4)
        
    print("[ETL] Proceso finalizado. Dataset optimizado exportado como 'dataset_optimizado_ia.json'.")

if __name__ == "__main__":
    ejecutar_etl()