@echo off
REM Batch script to run Renode simulation for STM32 Fan Control
REM This avoids path issues with PowerShell

echo ======================================
echo Starting Renode Simulation...
echo ======================================
echo.
echo After 5 seconds, check uart_output.txt for data
echo Watch the UART Analyzer window!
echo.

cd /d "%~dp0"
"C:\Program Files\Renode\bin\Renode.exe" -e "include @working_sim.resc"

echo.
echo Simulation ended.
pause
