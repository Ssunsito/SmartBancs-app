import asyncio
import aiohttp
import time
import json
import os

URL = "http://localhost:8000/api/v1/transferencias"

async def enviar_transferencia(session, payload, idx):
    try:
        async with session.post(URL, json=payload) as response:
            estado = response.status
            data = await response.json()
            if estado == 200:
                print(f"[Req {idx}] Exito -> {data.get('transaccion_id')}")
            else:
                print(f"[Req {idx}] FALLO HTTP {estado} | {data.get('detail', 'Error interno')}")
    except Exception as e:
        print(f"[Req {idx}] Error critico: {str(e)}")

async def main():
    ruta_datos = "tests/data/incident_data.json"
    if not os.path.exists(ruta_datos):
        print("Error: No se encontraron los datos de prueba. Ejecute generate_test_data.py primero.")
        return

    with open(ruta_datos, "r") as f:
        payloads = json.load(f)

    print(f"Iniciando Simulacro de Incidente: Inyectando {len(payloads)} transacciones cruzadas desde JSON...")
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        tareas = [enviar_transferencia(session, payload, i) for i, payload in enumerate(payloads)]
        await asyncio.gather(*tareas)
        
    print(f"Simulacro finalizado en {round(time.time() - start_time, 2)} segundos.")
    print("Revisa los logs del contenedor de la base de datos para ver la detección del Deadlock.")

if __name__ == "__main__":
    asyncio.run(main())