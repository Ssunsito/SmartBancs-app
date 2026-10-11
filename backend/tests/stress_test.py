import asyncio
import aiohttp
import time

URL = "http://localhost:8000/api/v1/transferencias"
PAYLOAD = {"cuenta_origen_id": 1, "cuenta_destino_id": 2, "monto": 10.0}

async def enviar_transaccion(session, idx):
    try:
        async with session.post(URL, json=PAYLOAD) as response:
            data = await response.json()
            estado = response.status
            print(f"[{idx}] HTTP {estado} | {data.get('mensaje', data)}")
            return estado
    except Exception as e:
        print(f"[{idx}] Error: {str(e)}")
        return 500

async def main():
    print("Iniciando prueba de estrés: 50 transacciones concurrentes...")
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        # Creamos 50 tareas para ejecutarse simultáneamente
        tareas = [enviar_transaccion(session, i) for i in range(50)]
        resultados = await asyncio.gather(*tareas)
        
    elapsed = time.time() - start_time
    exitosas = resultados.count(200)
    
    print("-" * 40)
    print(f"Tiempo total para 50 peticiones concurrentes: {round(elapsed, 4)} segundos.")
    print(f"Transacciones exitosas: {exitosas}/50")
    print("Revisa los logs del contenedor 'api' para ver los bloqueos de DB en acción.")

if __name__ == "__main__":
    asyncio.run(main())