import asyncio
import aiohttp
import time
import json
import os

URL = "http://localhost:8000/api/v1/transferencias"

async def enviar_transaccion(session, payload, idx):
    try:
        async with session.post(URL, json=payload) as response:
            data = await response.json()
            estado = response.status
            print(f"[{idx}] HTTP {estado} | Monto: {payload['monto']} -> {data.get('mensaje', data)}")
            return estado
    except Exception as e:
        print(f"[{idx}] Error: {str(e)}")
        return 500

async def main():
    ruta_datos = "tests/data/stress_data.json"
    if not os.path.exists(ruta_datos):
        print("Error: No se encontraron los datos de prueba. Ejecute generate_test_data.py primero.")
        return

    with open(ruta_datos, "r") as f:
        payloads = json.load(f)

    print(f"Iniciando prueba de estrés: Leyendo {len(payloads)} transacciones dinámicas desde JSON...")
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        tareas = [enviar_transaccion(session, payload, i) for i, payload in enumerate(payloads)]
        resultados = await asyncio.gather(*tareas)
        
    elapsed = time.time() - start_time
    exitosas = resultados.count(200)
    
    print("-" * 40)
    print(f"Tiempo total para {len(payloads)} peticiones: {round(elapsed, 4)} segundos.")
    print(f"Transacciones exitosas: {exitosas}/{len(payloads)}")

if __name__ == "__main__":
    asyncio.run(main())