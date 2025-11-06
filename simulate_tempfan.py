#!/usr/bin/env python3
"""
RTS Fan Control - Temperature to PWM Simulation
Simulates LM35 temperature sensor + STM32F103C8 + 2N2222 motor driver
Uses ngspice for circuit simulation with matplotlib for visualization
"""

import subprocess
import os
import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# NGSPICE NETLIST: LM35 + STM32 + Motor Driver
# ============================================================

NETLIST = """* RTS Fan Control - Temperature to PWM Simulation
* LM35 Sensor (0-100°C) -> STM32F103C8 ADC -> 2N2222 Motor Driver

.title RTS Fan Control Simulation

* ============================================================
* VOLTAGE SOURCES
* ============================================================
VCC 1 0 DC 5V          ; 5V Supply for motor
VDD 2 0 DC 3.3V       ; 3.3V Supply for STM32
VTEMP 3 0 DC 0V       ; Temperature input (0V = 0°C)

* ============================================================
* LM35 TEMPERATURE SENSOR MODEL
* Output: 10mV per °C (0.5V @ 50°C, 1.0V @ 100°C)
* ============================================================
* Temperature sweep: linearly increase from 0°C to 100°C
* Simulates 0V (0°C) to 1.0V (100°C)
RTEMP_SRC 3 4 10k
ETEMP 4 0 5 0 0.01    ; E_out = 0.01 * V_src = 10mV/°C
CTEMP 4 0 100n

* ============================================================
* STM32F103C8 BEHAVIORAL MODEL
* Simplified: ADC input voltage -> PWM output voltage
* Scaling: 0-3.3V input -> 0-5V PWM output
* ============================================================
EADC 5 0 4 0 1.515    ; ADC gain (5V / 3.3V ≈ 1.515)
RADC 5 6 10k          ; ADC input impedance
CADC 6 0 1u           ; Input filter

* Temperature threshold logic:
* IF V_temp < 0.3V (< 30°C): PWM = 0V (motor off)
* IF V_temp >= 0.3V (>= 30°C): PWM proportional to temp
* ============================================================
ETHRESH 7 0 VALUE = {IF(V(4) < 0.3, 0, V(4) * 1.515)}
CPWM 7 8 10u          ; PWM output smoothing
RPWM 8 0 1Meg

* ============================================================
* 2N2222 TRANSISTOR DRIVER + MOTOR LOAD
* Motor model: Resistance + Inductance + Back-EMF
* ============================================================

* Base resistor (STM32 PA6 -> 2N2222 base)
RBASE 8 9 1k

* 2N2222 NPN Transistor
Q1 1 9 10 Q2N2222
RE1 10 0 100

* Motor Load (Equivalent circuit)
RMOTOR 1 11 100       ; Motor winding resistance
LMOTOR 11 12 10m      ; Motor inductance
CMOTOR 12 0 100u      ; Output smoothing

* Freewheeling Diode (1N4007)
D1 12 1 D1N4007

* ============================================================
* COMPONENT MODELS
* ============================================================

* 2N2222 NPN Transistor (Typical small-signal transistor)
.model Q2N2222 NPN (
+ IS=14.34E-15
+ BF=255.9
+ NF=1.307
+ VAF=74.03
+ IKF=0.2847
+ ISE=14.34E-15
+ NE=1.307
+ BR=6.092
+ NR=1
+ VAR=24
+ IKR=0
+ ISC=0
+ NC=2
+ RB=10
+ IRB=0.1
+ RBM=10
+ RE=0
+ RC=1
+ CJE=26.08E-12
+ VJE=0.75
+ MJE=0.377
+ TF=411E-12
+ XTF=3
+ VTF=1.7
+ ITF=0.6
+ PTF=0
+ CJC=7.306E-12
+ VJEC=0.75
+ MNJC=0.3085
+ XCJC=1
+ TR=46.91E-9
+ XTB=1.5
+ EG=1.11
+ XTI=3
+ FC=0.5
)

* 1N4007 Diode (General purpose rectifier)
.model D1N4007 D (
+ IS=5.84E-14
+ RS=0.8
+ N=1.906
+ BV=1000
+ IBV=100E-6
+ CJO=1.0E-11
+ VJ=0.75
+ M=0.333
+ FC=0.5
+ TT=4.761E-9
)

* ============================================================
* TRANSIENT ANALYSIS
* ============================================================

* Temperature sweep: 0 to 100°C over 10 seconds
* Rate: 10°C per second
.control
    alter VTEMP DC 0    ; Start at 0V (0°C)
    tran 0.01 10 0 0.01 ; Simulate 10 seconds with 0.01s steps
    
    * Manually increase temperature source over time
    * At each time point, calculate temperature
    alter VTEMP DC 0.1
    
    * Output results to file
    set wr_singlescale
    set wr_vecnames
    option numdgt=6
    wrdata output.csv v(4) v(8) v(12)
    
.endc

.end
"""

# ============================================================
# SIMULATION FUNCTIONS
# ============================================================

def create_netlist_file(filename="tempfan.cir"):
    """Create ngspice netlist file"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(NETLIST)
    print(f"✅ Netlist created: {filename}")
    return filename

def run_ngspice_simulation(netlist_file="tempfan.cir", log_file="ngspice.log"):
    """Run ngspice simulation"""
    print("\n🔄 Running ngspice simulation...")
    try:
        result = subprocess.run(
            ["ngspice", "-b", netlist_file, "-o", log_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"✅ Simulation completed successfully")
            return True
        else:
            print(f"❌ Simulation failed with return code {result.returncode}")
            print(f"Error output:\n{result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ ngspice not found! Install it:")
        print("   Windows: choco install ngspice")
        print("   Linux: sudo apt install ngspice")
        print("   macOS: brew install ngspice")
        return False
    except Exception as e:
        print(f"❌ Error running simulation: {e}")
        return False

def read_simulation_data(csv_file="output.csv"):
    """Read simulation results from CSV"""
    print(f"\n📊 Reading simulation data from {csv_file}")
    
    times = []
    v_temp = []
    v_pwm = []
    v_motor = []
    
    try:
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            # Skip header if present
            next(reader, None)
            
            for row in reader:
                if len(row) >= 3:
                    try:
                        times.append(float(row[0]))
                        v_temp.append(float(row[1]) * 1000)   # Convert to mV
                        v_pwm.append(float(row[2]))
                        v_motor.append(float(row[3]) if len(row) > 3 else 0)
                    except ValueError:
                        continue
        
        print(f"✅ Read {len(times)} data points")
        return times, v_temp, v_pwm, v_motor
        
    except FileNotFoundError:
        print(f"❌ Output file not found: {csv_file}")
        return [], [], [], []

def generate_synthetic_data():
    """Generate synthetic data if ngspice not available"""
    print("\n⚠️  Generating synthetic data (ngspice unavailable)")
    
    times = np.linspace(0, 10, 1000)  # 0-10 seconds
    
    # Temperature ramp: 0°C to 100°C
    temperatures_C = times * 10  # 10°C per second
    v_temp_mV = temperatures_C * 10  # LM35: 10mV per °C
    
    # PWM response with hysteresis
    v_pwm = np.where(v_temp_mV < 300, 0,  # Below 30°C: off
            np.where(v_temp_mV > 1000, 5,  # Above 100°C: full
                    (v_temp_mV - 300) * 5 / 700))  # Linear ramp 30-100°C
    
    # Motor voltage (filtered)
    v_motor = v_pwm * 0.9  # Motor drives at ~90% of PWM
    
    return times, v_temp_mV, v_pwm, v_motor

def create_plots(times, v_temp, v_pwm, v_motor, output_file="fan_simulation.png"):
    """Generate matplotlib plots"""
    print("\n📈 Generating plots...")
    
    # Convert to numpy arrays if needed
    times = np.array(times)
    v_temp = np.array(v_temp)
    v_pwm = np.array(v_pwm)
    v_motor = np.array(v_motor)
    
    # Calculate derived quantities
    temp_celsius = v_temp / 10  # LM35: 10mV per °C
    pwm_percent = (v_pwm / 5) * 100 if len(v_pwm) > 0 else np.zeros_like(times)
    
    # Create figure with subplots
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    fig.suptitle('RTS Fan Control - Temperature to PWM Simulation', fontsize=16, fontweight='bold')
    
    # Plot 1: Temperature over time
    axes[0].plot(times, temp_celsius, 'r-', linewidth=2, label='LM35 Temperature')
    axes[0].axhline(y=30, color='orange', linestyle='--', alpha=0.7, label='Motor ON threshold (30°C)')
    axes[0].axhline(y=50, color='red', linestyle='--', alpha=0.7, label='Motor MAX threshold (50°C)')
    axes[0].set_ylabel('Temperature (°C)', fontweight='bold')
    axes[0].set_ylim([-5, 105])
    axes[0].grid(True, alpha=0.3)
    axes[0].legend(loc='upper left')
    axes[0].set_title('LM35 Temperature Sensor Output')
    
    # Plot 2: PWM output (voltage)
    axes[1].plot(times, v_pwm, 'b-', linewidth=2, label='PWM Voltage (PA6)')
    axes[1].set_ylabel('Voltage (V)', fontweight='bold')
    axes[1].set_ylim([-0.5, 5.5])
    axes[1].grid(True, alpha=0.3)
    axes[1].legend(loc='upper left')
    axes[1].set_title('STM32F103C8 PWM Output (PA6)')
    
    # Plot 3: Motor output and PWM duty cycle
    ax3a = axes[2]
    color = 'tab:green'
    ax3a.set_ylabel('PWM Duty Cycle (%)', color=color, fontweight='bold')
    line1 = ax3a.plot(times, pwm_percent, color=color, linewidth=2, label='PWM Duty Cycle')
    ax3a.tick_params(axis='y', labelcolor=color)
    ax3a.set_ylim([-5, 105])
    ax3a.grid(True, alpha=0.3)
    
    # Secondary y-axis for motor voltage
    ax3b = ax3a.twinx()
    color = 'tab:purple'
    ax3b.set_ylabel('Motor Voltage (V)', color=color, fontweight='bold')
    line2 = ax3b.plot(times, v_motor, color=color, linewidth=2, linestyle='--', label='Motor Output')
    ax3b.tick_params(axis='y', labelcolor=color)
    
    axes[2].set_xlabel('Time (seconds)', fontweight='bold')
    axes[2].set_title('Motor Driver Output')
    
    # Combined legend
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax3a.legend(lines, labels, loc='upper left')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"✅ Plot saved: {output_file}")
    
    plt.show()

def save_data_table(times, v_temp, v_pwm, v_motor, output_file="simulation_results.csv"):
    """Save simulation results as CSV table"""
    print(f"\n📋 Saving results to {output_file}")
    
    temp_celsius = np.array(v_temp) / 10
    pwm_percent = (np.array(v_pwm) / 5) * 100 if len(v_pwm) > 0 else np.zeros_like(times)
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Time(s)', 'Temp(°C)', 'V_Temp(mV)', 'V_PWM(V)', 'PWM_Duty(%)', 'V_Motor(V)'])
        
        for i in range(len(times)):
            writer.writerow([
                f"{times[i]:.3f}",
                f"{temp_celsius[i]:.1f}",
                f"{v_temp[i]:.2f}",
                f"{v_pwm[i]:.3f}",
                f"{pwm_percent[i]:.1f}",
                f"{v_motor[i]:.3f}"
            ])
    
    print(f"✅ Results saved: {output_file}")

# ============================================================
# MAIN EXECUTION
# ============================================================

def main():
    print("="*60)
    print("RTS FAN CONTROL - CIRCUIT SIMULATION")
    print("="*60)
    print()
    
    # Create netlist
    create_netlist_file("tempfan.cir")
    
    # Try to run ngspice
    sim_success = run_ngspice_simulation("tempfan.cir", "ngspice.log")
    
    # Get data
    if sim_success:
        times, v_temp, v_pwm, v_motor = read_simulation_data("output.csv")
    else:
        print("\n⚠️  Using synthetic data for demonstration...")
        times, v_temp, v_pwm, v_motor = generate_synthetic_data()
    
    # If we have data, generate plots
    if len(times) > 0:
        # Create plots
        create_plots(times, v_temp, v_pwm, v_motor, "fan_simulation.png")
        
        # Save CSV results
        save_data_table(times, v_temp, v_pwm, v_motor, "simulation_results.csv")
        
        # Print summary
        print("\n" + "="*60)
        print("SIMULATION SUMMARY")
        print("="*60)
        print(f"Simulation time: {times[-1]:.2f} seconds")
        print(f"Temperature range: {np.array(v_temp)/10:.1f}°C - {np.array(v_temp)/10:.1f}°C")
        print(f"PWM output: {np.min(v_pwm):.2f}V - {np.max(v_pwm):.2f}V")
        print(f"Motor response: {np.min(v_motor):.2f}V - {np.max(v_motor):.2f}V")
        print("="*60)
        print("\n✅ Files generated:")
        print("   • fan_simulation.png - Visualization of results")
        print("   • simulation_results.csv - Data table")
        print("   • ngspice.log - Simulation log")
        print()
    else:
        print("❌ No data to plot!")
        sys.exit(1)

if __name__ == "__main__":
    main()
