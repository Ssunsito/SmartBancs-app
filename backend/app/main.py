from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from db import init_db, close_db, procesar_transferencia_db
from rabbitmq import publicar_evento
import time

app = FastAPI(title="SmartBancs API")

class TransferenciaRequest(BaseModel):
    cuenta_origen_id: int
    cuenta_destino_id: int
    monto: float

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()

# Tarea en segundo plano para manejar los flujos asíncronos
async def flujos_asincronos(tx_id: str, request: TransferenciaRequest):
    payload_evento = {
        "transaccion_id": tx_id,
        "origen": request.cuenta_origen_id,
        "destino": request.cuenta_destino_id,
        "monto": request.monto
    }
    # Encola a la IA y a Bancs (No bloquea la respuesta HTTP)
    await publicar_evento("cola_inferencia_ia", payload_evento)
    await publicar_evento("cola_sync_bancs", payload_evento)

@app.post("/api/v1/transferencias")
async def crear_transferencia(req: TransferenciaRequest, bg_tasks: BackgroundTasks):
    start_time = time.time()
    try:
        # Ejecuta la transacción ACID (Síncrono y Crítico)
        tx_id = await procesar_transferencia_db(req.cuenta_origen_id, req.cuenta_destino_id, req.monto)
        
        # Despacha a IA y Bancs sin esperar que procesen (Asíncrono)
        bg_tasks.add_task(flujos_asincronos, tx_id, req)
        
        elapsed = time.time() - start_time
        return {
            "mensaje": "Transferencia exitosa", 
            "transaccion_id": tx_id,
            "tiempo_procesamiento_segundos": round(elapsed, 4)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")