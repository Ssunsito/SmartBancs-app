-- DDL: Creación de tablas
CREATE TABLE cuentas (
    id SERIAL PRIMARY KEY,
    numero_cuenta VARCHAR(20) UNIQUE NOT NULL,
    titular VARCHAR(100) NOT NULL,
    saldo DECIMAL(12, 2) NOT NULL CHECK (saldo >= 0), -- Evita saldos negativos a nivel de DB
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TYPE estado_transaccion AS ENUM ('PENDIENTE', 'COMPLETADA', 'FALLIDA');

CREATE TABLE transacciones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cuenta_origen_id INT REFERENCES cuentas(id),
    cuenta_destino_id INT REFERENCES cuentas(id),
    monto DECIMAL(12, 2) NOT NULL CHECK (monto > 0),
    estado estado_transaccion DEFAULT 'PENDIENTE',
    fecha_transaccion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para optimizar las consultas de validación y evitar cuellos de botella
CREATE INDEX idx_transacciones_cuenta_origen ON transacciones(cuenta_origen_id);
CREATE INDEX idx_transacciones_estado ON transacciones(estado);

-- DML: Datos semilla (Mock data) para probar el MVP sin tener que crear usuarios desde cero
INSERT INTO cuentas (numero_cuenta, titular, saldo) VALUES 
('1000000001', 'Alice Johnson', 5000.00),
('1000000002', 'Bob Smith', 1500.00),
('1000000003', 'Core Legado Bancs', 999999.00);