@echo off
REM Automated Report Generation for STM32 Fan Control Project
REM This script runs Renode simulation and generates a complete report

echo ========================================
echo STM32 Fan Control - Report Generator
echo ========================================
echo.
echo This will:
echo   1. Run Renode simulation
echo   2. Sweep temperature from 25C to 100C
echo   3. Log all UART output to uart_output.txt
echo   4. Save full simulation log to simulation_report.log
echo.
echo Press Ctrl+C to cancel, or
pause

cd /d "%~dp0"

echo.
echo Starting Renode simulation...
echo.

"C:\Program Files\Renode\bin\Renode.exe" -e "i @generate_report.resc"

echo.
echo ========================================
echo Report generation complete!
echo ========================================
echo.
echo Generated files:
echo   - uart_output.txt (UART debug data)
echo   - simulation_report.log (full log)
echo.
pause
