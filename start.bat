@echo off
echo ==========================================================
echo Instalando dependencias locales para scripts de prueba...
echo ==========================================================
pip install aiohttp

echo.
echo ==========================================================
echo Levantando infraestructura de SmartBancs (IaC)...
echo ==========================================================
docker-compose down
docker-compose up --build -d

echo.
echo Servicios en ejecucion. Conectando a la telemetria centralizada...
docker-compose logs -f api ia_worker etl_worker db