@echo off
echo ================================================================================
echo STM32 Fan Control System - Demonstration
echo ================================================================================
echo.
echo This will:
echo   1. Run STM32 firmware simulation in Renode (30 seconds)
echo   2. Collect temperature sweep data (25C to 100C)
echo   3. Generate comprehensive report
echo   4. Open results automatically
echo.
echo Press any key to start...
pause >nul

echo.
echo [Step 1/3] Starting Renode simulation...
echo ----------------------------------------
echo Running STM32F103C8 firmware with temperature control algorithm
echo Collecting data for 30 seconds...
echo.

REM Delete old output to start fresh
if exist "reports\uart_output.txt" del "reports\uart_output.txt"

REM Start Renode simulation
start "Renode Simulator" "C:\Program Files\Renode\bin\Renode.exe" -e "include @simulation\demo_sim.resc"

echo Simulation running... Please wait 30 seconds
timeout /t 30 /nobreak

echo.
echo [Step 2/3] Stopping simulation...
echo ----------------------------------------
taskkill /FI "WindowTitle eq Renode Simulator*" /T /F >nul 2>&1

echo.
echo [Step 3/3] Generating report...
echo ----------------------------------------
python scripts\analyze_results.py

echo.
echo ================================================================================
echo DEMONSTRATION COMPLETE!
echo ================================================================================
echo.
echo Generated Files:
echo   - reports\PROJECT_REPORT.txt       (Comprehensive report with statistics)
echo   - reports\simulation_data.csv      (Raw data for Excel graphs)
echo   - reports\uart_output.txt          (Raw UART output)
echo.
echo Circuit Schematic:
echo   - circuit\RTS_FanControl.kicad_sch (Open in KiCad to view)
echo.
echo Press any key to open the report...
pause >nul

start reports\PROJECT_REPORT.txt

echo.
echo Thank you!
pause
