@echo off
title Incidente Critico - SmartBancs API
color 0C

echo ==========================================================
echo    ALERTA: SIMULACION DE INCIDENTE CRITICO (DEADLOCK)
echo ==========================================================
echo.
echo Este script disparara 200 peticiones de transferencias cruzadas
echo para forzar una colision de bloqueos en PostgreSQL.
echo.
pause

echo.
echo Ejecutando simulacro de incidente...
echo.
python simulate_incident.py

echo.
echo ==========================================================
echo Simulacro completado. Verifique el dashboard de telemetria.
echo ==========================================================
pause