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

 # RTS Fan Control — README (concise)

 A concise description of the Real-Time Temperature-Based Fan Controller project. This file focuses on the scheduling algorithms used (RMS vs EDF) and how Renode is used to simulate and validate the firmware.

 The aim: practical explanation for a presentation or quick review. For full technical detail see the `documentation/` folder and the simulation scripts.

 ## Contents
 - Overview
 - Why Renode
 - Scheduling: RMS vs EDF (practical summary)
 - How Renode runs and inspects firmware
 - Quick start (build + run simulation)
 - Files of interest
 - Reproduce graphs

 ---

 ## Overview

 This project implements a proportional temperature-to-PWM fan controller for an STM32F103 (BluePill) using an LM35 sensor. The control law used for demonstration is a simple proportional mapping:

 pwm_duty = clamp(Temperature * 40, 0, PWM_MAX)

 The firmware reads ADC samples, updates the PWM duty cycle, and logs values over UART. Validation and data collection are performed with Renode so results are deterministic and reproducible.

 ## Why Renode

 Renode is used because it provides a fast, deterministic, and inspectable environment for embedded firmware:

 - Emulates MCU peripherals (ADC, timers, UART) at the register level.
 - Captures UART and peripheral activity to files for analysis.
 - Allows pausing and introspection (memory, registers), which helps debug timing and scheduling.
 - Integrates in automated workflows (headless runs, reproducible outputs).

 This makes Renode particularly suitable for demonstrations and for validating scheduling/jitter behavior without requiring the physical board.

 ## Scheduling: RMS vs EDF (practical)

 A short, practical comparison for this project.

 Rate Monotonic Scheduling (RMS)
 - Fixed priorities assigned by task period (shorter period → higher priority).
 - Simple and predictable for periodic task sets.
 - Appropriate when tasks are periodic and utilization is low-to-moderate.

 Earliest Deadline First (EDF)
 - Dynamic priorities based on closest deadline.
 - Can schedule up to 100% CPU utilization (theoretical bound U ≤ 1.0) but requires more dynamic bookkeeping.

 Why we use RMS here
 - The project has a small set of periodic tasks (ADC read, PWM update, logging) with low utilization. RMS is simpler to demonstrate and is sufficient given the measured CPU load and jitter targets.

 When to prefer EDF
 - Highly variable or sporadic task sets, or when you need to utilize CPU closer to 100%.

 ## How Renode runs and inspects the firmware

 Typical steps (see `simulation/demo_sim.resc`):
 1. Load an STM32F103 platform description.
 2. Load the compiled firmware ELF into the virtual flash.
 3. Attach USART1 to a file backend and (optionally) an analyzer.
 4. Start the simulation; Renode executes the firmware and records the UART output and any configured logs.

 Useful monitor capabilities:
 - pause: stop CPU and inspect state
 - sysbus ReadBytes <addr> <len>: dump memory
 - sysbus ReadDoubleWord <addr>: read peripheral register
 - showAnalyzer sysbus.usart1: show live UART output

 These capabilities let you verify that register writes, ADC reads, and timer updates behave as expected and also let you measure jitter and missed deadlines deterministically.

 ## Quick start (build and run)

 1) Build firmware (PlatformIO):

 ```powershell
 pio run
 ```

 2) Run the Renode demo (automated):

 ```powershell
 demo.bat
 ```

 Or run Renode interactively and include the script:

 ```powershell
 renode
 (monitor) include @simulation/demo_sim.resc
 ```

 3) Generate graphs from collected CSV:

 ```powershell
 cd goingtodeletereports
 python generate_graphs.py
 ```

 ## Files of interest
 - `simulation/demo_sim.resc` — Renode script that runs the platform and logs UART to file.
 - `src/main_simple.c` — Simplified firmware used during simulation.
 - `src/main.c` — HAL-based firmware for hardware deployment.
 - `reports/simulation_data.csv` — Data used by the plotting scripts.
 - `goingtodeletereports/generate_graphs.py` — Creates PNGs for the report.

 ## Reproduce analysis
 1. Run the Renode script to produce `reports/simulation_data.csv` and `reports/uart_output.txt`.
 2. Run `python goingtodeletereports/generate_graphs.py` to create graphs in `goingtodeletereports/graphs_output/`.

 ## Next steps (optional)
 - I can replace the `demo.bat` call with an explicit, single-step Renode command sequence if you prefer to avoid the batch file.
 - If you want the README pared down further for a slide handout, I can prepare a 1-page summary.

 ---

 Author: Kishore N — GitHub @kishore110804
