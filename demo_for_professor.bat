@echo off
echo ================================================================================
echo STM32 Fan Control System - Project Demonstration
echo ================================================================================
echo.
echo This demonstration will:
echo 1. Generate KiCad schematic diagram
echo 2. Run the STM32 firmware in Renode simulator
echo 3. Collect temperature sweep data (25C to 100C)
echo 4. Generate comprehensive PROJECT_REPORT.txt
echo 5. Create simulation_data.csv for graphing
echo.
echo Press any key to start the demonstration...
pause >nul

echo.
echo [Step 1/5] Generating KiCad schematic...
echo ----------------------------------------
python generate_kicad_schematic.py
echo.

echo.
echo [Step 2/5] Starting Renode simulation...
echo ----------------------------------------
echo Running STM32F103C8 firmware with temperature sweep algorithm
echo Simulation will run for 30 seconds to collect data
echo.

REM Delete old output file to start fresh
if exist uart_output.txt del uart_output.txt

REM Start Renode simulation in background
start "Renode Simulator" "C:\Program Files\Renode\bin\Renode.exe" -e "include @demo_sim.resc"

echo Waiting for simulation to generate data...
timeout /t 30 /nobreak

echo.
echo [Step 3/5] Stopping simulation...
echo ----------------------------------------
taskkill /FI "WindowTitle eq Renode Simulator*" /T /F >nul 2>&1

echo.
echo [Step 4/5] Generating report from simulation data...
echo ----------------------------------------
python analyze_results.py

echo.
echo [Step 5/5] Opening generated files...
echo ----------------------------------------

echo.
echo ================================================================================
echo DEMONSTRATION COMPLETE!
echo ================================================================================
echo.
echo Generated Files:
echo   - RTS_FanControl.kicad_sch (Circuit schematic)
echo   - PROJECT_REPORT.txt       (Comprehensive formatted report)
echo   - simulation_data.csv      (Raw data for Excel graphing)
echo   - uart_output.txt          (Raw UART output from simulation)
echo.
echo You can now:
echo   1. Open RTS_FanControl.kicad_sch in KiCad to view the circuit
echo   2. Review PROJECT_REPORT.txt for simulation results
echo   3. Import simulation_data.csv into Excel for graphs
echo   4. Show uart_output.txt for raw simulation output
echo.
echo Press any key to open the report and schematic...
pause >nul

REM Open the report and schematic
start PROJECT_REPORT.txt
timeout /t 2 /nobreak >nul
start RTS_FanControl.kicad_sch

echo.
echo Thank you for viewing the demonstration!
pause
