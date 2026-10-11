from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from db import init_db, close_db, procesar_transferencia_db
from rabbitmq import publicar_evento
import time
import logging
import uuid

# Configuración del Logger para la API
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(name)s | %(message)s')
logger = logging.getLogger("SmartBancs-API")

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

async def flujos_asincronos(tx_id: str, request: TransferenciaRequest):
    logger.info(f"[{tx_id}] Despachando eventos asíncronos a IA y Bancos Legacy...")
    payload = {
        "transaccion_id": tx_id,
        "origen": request.cuenta_origen_id,
        "destino": request.cuenta_destino_id,
        "monto": request.monto
    }
    await publicar_evento("cola_inferencia_ia", payload)
    await publicar_evento("cola_sync_bancs", payload)
    logger.info(f"[{tx_id}] Eventos asíncronos publicados con éxito en RabbitMQ.")

@app.post("/api/v1/transferencias")
async def crear_transferencia(req: TransferenciaRequest, bg_tasks: BackgroundTasks):
    trace_id = str(uuid.uuid4())
    start_time = time.time()
    logger.info(f"[{trace_id}] Nueva petición recibida: Origen {req.cuenta_origen_id} -> Destino {req.cuenta_destino_id} | Monto: {req.monto}")
    
    try:
        await procesar_transferencia_db(req.cuenta_origen_id, req.cuenta_destino_id, req.monto, trace_id)
        bg_tasks.add_task(flujos_asincronos, trace_id, req)
        
        elapsed = time.time() - start_time
        logger.info(f"[{trace_id}] Respuesta HTTP 200 enviada en {round(elapsed, 4)} segundos.")
        
        return {
            "mensaje": "Transferencia exitosa", 
            "transaccion_id": trace_id,
            "tiempo_procesamiento_segundos": round(elapsed, 4)
        }
    except ValueError as e:
        logger.warning(f"[{trace_id}] Validación fallida: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"[{trace_id}] Error interno del servidor: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")