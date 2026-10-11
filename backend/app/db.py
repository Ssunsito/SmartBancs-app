import asyncpg
import os
import time
import logging

# Configuración del Logger para la DB
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(name)s | %(message)s')
logger = logging.getLogger("SmartBancs-DB")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://smartbancs_user:supersecretpassword@localhost:5432/smartbancs")
pool = None

async def init_db():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)
    logger.info("Pool de conexiones a PostgreSQL inicializado exitosamente.")

async def close_db():
    await pool.close()
    logger.info("Pool de conexiones cerrado.")

async def procesar_transferencia_db(origen_id: int, destino_id: int, monto: float, trace_id: str):
    start_time = time.time()
    try:
        async with pool.acquire() as connection:
            async with connection.transaction():
                logger.info(f"[{trace_id}] Iniciando transacción SQL con bloqueos (FOR UPDATE).")
                
                origen = await connection.fetchrow('SELECT saldo FROM cuentas WHERE id = $1 FOR UPDATE', origen_id)
                destino = await connection.fetchrow('SELECT saldo FROM cuentas WHERE id = $1 FOR UPDATE', destino_id)

                if not origen or not destino:
                    raise ValueError("Cuenta de origen o destino no encontrada")
                if origen['saldo'] < monto:
                    raise ValueError("Fondos insuficientes")

                await connection.execute('UPDATE cuentas SET saldo = saldo - $1 WHERE id = $2', monto, origen_id)
                await connection.execute('UPDATE cuentas SET saldo = saldo + $1 WHERE id = $2', monto, destino_id)

                tx_internal_id = await connection.fetchval(
                    '''INSERT INTO transacciones (id, cuenta_origen_id, cuenta_destino_id, monto, estado) 
                       VALUES ($1, $2, $3, $4, 'COMPLETADA') RETURNING id''',
                    trace_id, origen_id, destino_id, monto
                )
                
                elapsed = round((time.time() - start_time) * 1000, 2)
                logger.info(f"[{trace_id}] Transacción SQL confirmada en {elapsed} ms.")
                return str(tx_internal_id)

    except asyncpg.exceptions.DeadlockDetectedError as e:
        logger.error(f"[{trace_id}] INCIDENTE CRÍTICO: Deadlock detectado en la base de datos - {str(e)}")
        raise e
    except asyncpg.exceptions.PostgresError as e:
        logger.error(f"[{trace_id}] Error de base de datos (Posible Timeout): {str(e)}")
        raise e