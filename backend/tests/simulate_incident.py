import asyncio
import aiohttp
import time

URL = "http://localhost:8000/api/v1/transferencias"

async def enviar_transferencia(session, origen, destino, monto, idx):
    payload = {"cuenta_origen_id": origen, "cuenta_destino_id": destino, "monto": monto}
    try:
        async with session.post(URL, json=payload) as response:
            estado = response.status
            data = await response.json()
            if estado == 200:
                print(f"[Req {idx}] Exito -> {data.get('transaccion_id')}")
            else:
                print(f"[Req {idx}] FALLO HTTP {estado} | {data.get('detail', 'Error interno')}")
    except Exception as e:
        print(f"[Req {idx}] Error critico de conexion: {str(e)}")

async def main():
    print("Iniciando Simulacro de Incidente: Ataque de transacciones cruzadas...")
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        tareas = []
        # Disparamos 200 transacciones simultaneas cruzadas
        for i in range(200):
            if i % 2 == 0:
                # Transfiere de la cuenta 1 a la 2
                tareas.append(enviar_transferencia(session, 1, 2, 1.0, i))
            else:
                # Transfiere de la cuenta 2 a la 1
                tareas.append(enviar_transferencia(session, 2, 1, 1.0, i))
        
        await asyncio.gather(*tareas)
        
    print(f"Simulacro finalizado en {round(time.time() - start_time, 2)} segundos.")
    print("Revisa los logs del contenedor para ver la deteccion del incidente.")

if __name__ == "__main__":
    asyncio.run(main())