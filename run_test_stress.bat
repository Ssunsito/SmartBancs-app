@echo off
title Prueba de Estres - SmartBancs API
color 0A

echo ==========================================================
echo      SMARTBANCS APP - SIMULACION DE ALTA CONCURRENCIA
echo ==========================================================
echo.
echo Preparando el envio de 50 transacciones simultaneas...
echo Asegurate de tener la ventana de logs visible al lado.
echo.
pause

echo.
echo Ejecutando peticiones concurrentes...
echo.
python backend\tests\stress_test.py

echo.
echo ==========================================================
echo Prueba finalizada. 
echo Demostracion de latencia y bloqueos SQL completada.
echo ==========================================================
pause