@echo off
echo ==========================================================
echo Configurando entorno y generando datos de prueba...
echo ==========================================================
pip install aiohttp
python backend\tests\generate_test_data.py

echo.
echo ==========================================================
echo Levantando infraestructura de SmartBancs (IaC)...
echo ==========================================================
docker-compose down
docker-compose up --build -d

echo.
echo Servicios en ejecucion. Conectando a la telemetria centralizada...
docker-compose logs -f api ia_worker etl_worker db