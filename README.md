# SmartBancs App - MVP Transaccional

## Requisitos Previos
* Docker y Docker Compose instalados.
* Git.

## Instrucciones de Ejecución
1. Clonar el repositorio.
2. Ejecutar `docker-compose up --build` en la raíz del proyecto para levantar la infraestructura, la base de datos y los microservicios.
3. El API principal estará disponible en `http://localhost:8000`.

## Componentes del Sistema
* **Backend:** Microservicio principal en FastAPI.
* **Base de Datos:** PostgreSQL con scripts DDL/DML para evitar condiciones de carrera.
* **IA Mock:** Servicio asíncrono no bloqueante.
* **ETL:** Script de transformación de datos para sincronización.