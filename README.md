# SmartBancs App - MVP Transaccional (Reto Técnico)

Este repositorio contiene la solución práctica para el caso "SmartBancs App", una plataforma financiera orientada a procesar transacciones en tiempo real con alta concurrencia, integrando un flujo desacoplado para Inteligencia Artificial y sincronización con sistemas legados (Bancs).

## Arquitectura y Stack Tecnológico

La solución implementa una **Arquitectura Orientada a Eventos (EDA)**:
* **Microservicio Principal:** Python (FastAPI) para manejo asíncrono de alto rendimiento.
* **Base de Datos:** PostgreSQL con bloqueos preventivos (`SELECT FOR UPDATE`) para evitar condiciones de carrera.
* **Mensajería Asíncrona:** RabbitMQ para desacoplar el core principal de la IA y el sistema heredado.
* **Workers Automáticos:** Servicios Dockerizados que consumen colas y procesan ETL (Pandas/SQLAlchemy).
* **Infraestructura:** Docker y Docker Compose para despliegue encapsulado (IaC).

---

## ⚙️ 1. Prerrequisitos

Para instalar y ejecutar esta solución, el entorno debe contar con:
* **Docker y Docker Compose** instalados y en ejecución.
* **Python 3.9 o superior** (exclusivamente para ejecutar los scripts locales de prueba).
* **Git** para clonar el repositorio.

---

## 🚀 2. Instalación y Ejecución

La infraestructura y todos los microservicios se levantan mediante un único comando automatizado que instala dependencias locales y orquesta los contenedores.

1. **Clonar el repositorio:**

   git clone <URL_DE_TU_REPOSITORIO>
   cd smartbancs-app


2. **Levantar la solución:**

Doble clic en el archivo `start.bat` o ejecútelo en su consola:

start.bat


*Nota: El script levantará PostgreSQL, RabbitMQ, la API principal, el Worker de IA y el Worker ETL en segundo plano, y anclará la consola a los logs centralizados (Observabilidad).*

---

## 🧪 3. Probar la Solución (Escenarios de Evaluación)

El proyecto incluye un generador de datos dinámico y scripts de simulación automatizados para validar los criterios técnicos del reto. Mantenga abierta la consola de logs (`start.bat`) mientras ejecuta las pruebas para observar la telemetría en tiempo real.

### A. Prueba de Alta Concurrencia y Tiempo de Respuesta

Demuestra que el sistema soporta un pico transaccional resolviendo transferencias en menos de 2 segundos, evitando *race conditions* en base de datos.

* `run_stress_test.bat`

### B. Simulación de Incidente Crítico (Deadlocks)

Inyecta 200 transacciones cruzadas para forzar una colisión de bloqueos en PostgreSQL, permitiendo que la telemetría capture la excepción exacta (DeadlockDetectedError) para su rápido diagnóstico.

* `run_incident.bat`

### C. Validación de IA asíncrona y ETL

* **IA Mock:** Al ejecutar cualquier transferencia, revise los logs. Verá al `ia_worker` atrapando el evento y generando recomendaciones sin bloquear la API HTTP.
* **Proceso ETL:** Cada 1 minuto, el `etl_worker` extrae los datos de PostgreSQL, los estandariza y genera el archivo limpio `dataset_optimizado_ia.json` en la carpeta `etl_process/data/`.

---

## 🛑 4. Detener la Solución

Para apagar de forma segura toda la infraestructura, liberar los puertos y detener los contenedores, ejecute en la raíz del proyecto:

docker-compose down


*(Si desea eliminar también los volúmenes de datos persistentes de la base de datos, agregue el flag `-v`: `docker-compose down -v`)*

---

## 📁 Estructura del Repositorio

smartbancs-app/
├── backend/                  # API principal (FastAPI) y conexión a DB
├── database/                 # Scripts DDL/DML de inicialización SQL
├── docs/                     # Documentación técnica teórica (Arquitectura y Post-mortem)
├── etl_process/              # Worker automatizado para limpieza de datos (Pandas/SQLAlchemy)
├── ia_mock/                  # Worker asíncrono consumidor de RabbitMQ
├── tests/                    # Scripts de estrés, simulación de incidentes y generador de datos
├── AI_USAGE.md               # Declaración del uso de Inteligencia Artificial
├── docker-compose.yml        # Orquestador de infraestructura
├── start.bat                 # Scripts de arranque automatizado
└── README.md                 # Instrucciones principales
