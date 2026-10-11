import asyncpg
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://smartbancs_user:supersecretpassword@localhost:5432/smartbancs")
pool = None

async def init_db():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)

async def close_db():
    await pool.close()

async def procesar_transferencia_db(origen_id: int, destino_id: int, monto: float):
    async with pool.acquire() as connection:
        # Inicia la transacción ACID
        async with connection.transaction():
            # SELECT FOR UPDATE bloquea las filas consultadas para evitar race conditions
            origen = await connection.fetchrow(
                'SELECT saldo FROM cuentas WHERE id = $1 FOR UPDATE', origen_id
            )
            destino = await connection.fetchrow(
                'SELECT saldo FROM cuentas WHERE id = $1 FOR UPDATE', destino_id
            )

            if not origen or not destino:
                raise ValueError("Cuenta de origen o destino no encontrada")
            if origen['saldo'] < monto:
                raise ValueError("Fondos insuficientes")

            # Actualiza los saldos
            await connection.execute(
                'UPDATE cuentas SET saldo = saldo - $1 WHERE id = $2', monto, origen_id
            )
            await connection.execute(
                'UPDATE cuentas SET saldo = saldo + $1 WHERE id = $2', monto, destino_id
            )

            # Registra la transacción
            tx_id = await connection.fetchval(
                '''INSERT INTO transacciones (cuenta_origen_id, cuenta_destino_id, monto, estado) 
                   VALUES ($1, $2, $3, 'COMPLETADA') RETURNING id''',
                origen_id, destino_id, monto
            )
            return str(tx_id)