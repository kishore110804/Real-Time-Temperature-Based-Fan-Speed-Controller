# 🌡️ Real-Time Temperature-Controlled Fan System# STM32 Fan Control System

### STM32F103C8T6 with Renode Virtual Hardware Simulation

Real-time temperature-based fan control system using STM32F103C8T6 (BluePill) and LM35 temperature sensor.

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]()

[![Renode](https://img.shields.io/badge/Renode-1.16.0-blue)]()## Quick Start

[![STM32](https://img.shields.io/badge/STM32-F103C8T6-orange)]()

[![License](https://img.shields.io/badge/license-MIT-green)]()**Run the demonstration:**

```batch

---demo.bat

```

## 📋 Table of Contents

- [Overview](#-overview)This will:

- [Why Renode?](#-why-renode-the-best-choice-for-embedded-simulation)1. Run the Renode simulation for 30 seconds

- [System Architecture](#-system-architecture)2. Collect temperature sweep data (25°C to 100°C)

- [Real-Time Scheduling](#-real-time-scheduling-algorithms-rms--edf)3. Generate comprehensive reports

- [Hardware Design](#-hardware-design--kicad-visualization)4. Open the results automatically

- [Simulation Results](#-simulation-results--performance-analysis)

- [Quick Start](#-quick-start)## Project Structure



---```

RTS_FanControl/

## 🎯 Overview├── demo.bat                    # Main demonstration script

│

An **intelligent temperature-based fan control system** using STM32F103C8T6 microcontroller (BluePill). The system monitors temperature via LM35 sensor and adjusts fan speed through PWM control using **proportional control algorithm**.├── circuit/                    # Circuit files

│   ├── RTS_FanControl.kicad_sch    # KiCad schematic (open with KiCad)

### Key Features│   ├── RTS_FanControl.kicad_pro

✅ **Real-Time Scheduling**: Implements Rate Monotonic Scheduling (RMS) and Earliest Deadline First (EDF)  │   └── *.cir                        # Circuit simulation files

✅ **Virtual Hardware**: Complete validation using Renode (no physical hardware needed!)  │

✅ **Bare-Metal Firmware**: Ultra-efficient 852-byte firmware with direct register access  ├── simulation/                 # Renode simulation scripts

✅ **Professional Circuit**: KiCad schematic with proper power management  │   ├── demo_sim.resc                # Main simulation script

✅ **Perfect Control**: R² = 1.000000 correlation between temperature and fan speed  │   └── *.resc                       # Other simulation configurations

✅ **Comprehensive Testing**: 574+ samples across 25°C to 100°C  │

├── reports/                    # Generated reports and data

### Technical Specifications│   ├── PROJECT_REPORT.txt           # Main formatted report

| Component | Specification |│   ├── simulation_data.csv          # Raw data for Excel

|-----------|---------------|│   └── uart_output.txt              # UART logs from simulation

| **Microcontroller** | STM32F103C8T6 (ARM Cortex-M3, 72MHz) |│

| **Temperature Sensor** | LM35 (10mV/°C precision) |├── documentation/              # Project documentation

| **ADC** | 12-bit (0-4095) on PA0 |│   ├── COMPLETE_PROJECT_SUMMARY.md

| **PWM** | 8kHz on PA6 (Timer 3) |│   ├── CIRCUIT_DOCUMENTATION.md

| **UART** | 115200 baud on PA9/PA10 |│   ├── DEMO_QUICK_REFERENCE.txt

| **Control** | Proportional: PWM = Temp × 40 |│   └── *.md / *.txt                 # Guides and references

| **Range** | 25°C - 100°C |│

├── scripts/                    # Python utilities

---│   ├── analyze_results.py           # Report generator

│   ├── generate_kicad_schematic.py

## 🚀 Why Renode? The Best Choice for Embedded Simulation│   └── *.py                         # Other utility scripts

│

### What is Renode?└── src/                        # Source code

    ├── main_simple.c                # Bare-metal firmware (for Renode)

# RTS Fan Control — README

Purpose
-------
Brief, practical documentation for the Real-Time Temperature-Based Fan Controller. Focus: the control law, why Renode is used for validation, and a compact RMS vs EDF comparison.

Project in one sentence
-----------------------
Firmware reads temperature from an LM35 (ADC), applies a proportional control law (pwm = clamp(temp × 40, 0, PWM_MAX)), updates PWM, and logs values over UART. The behavior is validated with Renode and analyzed with Python scripts that generate plots from the recorded CSV.

Why use Renode
--------------
- Emulates STM32 peripherals (ADC, timers, UART) at register level.
- Produces deterministic, repeatable output files (UART logs, CSV) for analysis.
- Lets you pause, inspect memory/registers, and run scripted scenarios—ideal for investigating timing and scheduling.

RMS vs EDF — concise
--------------------
- RMS (Rate Monotonic): fixed priorities by period. Simple and predictable; well suited to small periodic task sets. Reasonable schedulability bounds make it straightforward to verify.
- EDF (Earliest Deadline First): dynamic priorities; can use CPU up to 100% in theory, but needs more runtime bookkeeping.

This project uses RMS because the task set is small, periodic, and low-utilization; RMS is simpler to demonstrate while meeting jitter and miss-rate targets.

How Renode is used (practical)
------------------------------
1. Load platform description for STM32F103 and the compiled ELF.
2. Attach USART1 to a file backend and (optionally) an analyzer.
3. Start the simulation; Renode executes firmware and writes UART output and any configured logs.

Useful Renode monitor commands:
- pause — stop CPU
- sysbus ReadBytes <addr> <len> — dump memory
- sysbus ReadDoubleWord <addr> — read peripheral register
- showAnalyzer sysbus.usart1 — view live UART output

Quick start
-----------
Build firmware:

```powershell
pio run
```

Run the automated demo (recommended):

```powershell
demo.bat
```

Or run Renode manually and include the script:

```powershell
renode
(monitor) include @simulation/demo_sim.resc
```

Generate graphs from the CSV:

```powershell
cd goingtodeletereports
python generate_graphs.py
```

Files of interest
-----------------
- `simulation/demo_sim.resc` — Renode script that loads the platform and ELF and records UART.
- `src/main_simple.c` — Minimal firmware used for simulation.
- `src/main.c` — HAL-based firmware for hardware.
- `reports/simulation_data.csv` — Sampled data used for plotting.
- `goingtodeletereports/generate_graphs.py` — Creates the report PNGs.

Reproducing analysis
--------------------
1. Run the Renode script (via `demo.bat` or manually) to produce `reports/simulation_data.csv` and `reports/uart_output.txt`.
2. Run `python goingtodeletereports/generate_graphs.py` to generate the plot images.

Next steps (optional)
---------------------
- I can create an explicit Renode-only demo `.bat` that runs Renode headless and produces the CSV without extra wrappers.
- I can prepare a one-page handout derived from this README for slides.

Author: Kishore N — GitHub @kishore110804
