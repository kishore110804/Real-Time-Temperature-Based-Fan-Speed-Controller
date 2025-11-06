#!/usr/bin/env python3
"""
STM32 Fan Control - Report Analyzer
Parses UART output from Renode simulation and generates a formatted report
"""

import re
import csv
from datetime import datetime

def parse_uart_output(filename="uart_output.txt"):
    """Parse UART output file and extract temperature, ADC, and PWM data"""
    data = []
    
    try:
        with open(filename, 'r') as f:
            for line in f:
                # Match pattern: "Temp: XX C | ADC: XXXX | PWM: XXXX | Fan: XX%"
                match = re.search(r'Temp:\s*(\d+)\s*C\s*\|\s*ADC:\s*(\d+)\s*\|\s*PWM:\s*(\d+)', line)
                if match:
                    temp = int(match.group(1))
                    adc = int(match.group(2))
                    pwm = int(match.group(3))
                    data.append({'temp': temp, 'adc': adc, 'pwm': pwm})
    except FileNotFoundError:
        print(f"Error: {filename} not found. Run the simulation first.")
        return []
    
    return data

def calculate_stats(data):
    """Calculate statistics from the data"""
    if not data:
        return None
    
    temps = [d['temp'] for d in data]
    adcs = [d['adc'] for d in data]
    pwms = [d['pwm'] for d in data]
    
    return {
        'temp_min': min(temps),
        'temp_max': max(temps),
        'temp_avg': sum(temps) / len(temps),
        'adc_min': min(adcs),
        'adc_max': max(adcs),
        'adc_avg': sum(adcs) / len(adcs),
        'pwm_min': min(pwms),
        'pwm_max': max(pwms),
        'pwm_avg': sum(pwms) / len(pwms),
        'samples': len(data)
    }

def generate_report(data, stats):
    """Generate a formatted text report"""
    report = []
    report.append("=" * 80)
    report.append("STM32F103C8 FAN CONTROL SYSTEM - SIMULATION REPORT")
    report.append("=" * 80)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Project: Real-Time Fan Control using LM35 Temperature Sensor")
    report.append("")
    
    report.append("SYSTEM SPECIFICATIONS:")
    report.append("-" * 80)
    report.append("  Microcontroller: STM32F103C8T6 (BluePill)")
    report.append("  Clock Speed:     72 MHz")
    report.append("  RAM:             20 KB")
    report.append("  Flash:           64 KB")
    report.append("")
    report.append("  Temperature Sensor: LM35 (10mV/°C)")
    report.append("  ADC:                12-bit, PA0 (ADC1_IN0)")
    report.append("  PWM Output:         TIM3_CH1, PA6, 8kHz")
    report.append("  Motor Driver:       2N2222 NPN Transistor")
    report.append("  UART Debug:         115200 baud, PA9/PA10")
    report.append("")
    
    if stats:
        report.append("SIMULATION STATISTICS:")
        report.append("-" * 80)
        report.append(f"  Total Samples:      {stats['samples']}")
        report.append(f"  Temperature Range:  {stats['temp_min']}°C - {stats['temp_max']}°C")
        report.append(f"  Average Temp:       {stats['temp_avg']:.1f}°C")
        report.append("")
        report.append(f"  ADC Range:          {stats['adc_min']} - {stats['adc_max']} (0-4095)")
        report.append(f"  Average ADC:        {stats['adc_avg']:.0f}")
        report.append("")
        report.append(f"  PWM Duty Range:     {stats['pwm_min']} - {stats['pwm_max']} (0-4000)")
        report.append(f"  Average PWM:        {stats['pwm_avg']:.0f}")
        report.append(f"  PWM Utilization:    {(stats['pwm_avg']/4000)*100:.1f}%")
        report.append("")
    
    report.append("DETAILED MEASUREMENTS:")
    report.append("-" * 80)
    report.append(f"{'Temperature (°C)':<20} {'ADC Value':<15} {'PWM Duty':<15} {'Fan Speed %':<15}")
    report.append("-" * 80)
    
    # Group data by temperature for cleaner output
    temp_groups = {}
    for d in data:
        temp = d['temp']
        if temp not in temp_groups:
            temp_groups[temp] = []
        temp_groups[temp].append(d)
    
    for temp in sorted(temp_groups.keys()):
        samples = temp_groups[temp]
        avg_adc = sum(s['adc'] for s in samples) / len(samples)
        avg_pwm = sum(s['pwm'] for s in samples) / len(samples)
        fan_speed = (avg_pwm / 4000) * 100
        
        report.append(f"{temp:<20} {avg_adc:<15.0f} {avg_pwm:<15.0f} {fan_speed:<15.1f}")
    
    report.append("")
    report.append("=" * 80)
    report.append("CONTROL ALGORITHM ANALYSIS:")
    report.append("-" * 80)
    report.append("The fan control system uses proportional control:")
    report.append("  - PWM Duty Cycle is proportional to ADC reading")
    report.append("  - Formula: PWM = (ADC_Value / 4095) * 4000")
    report.append("  - Linear relationship between temperature and fan speed")
    report.append("")
    report.append("Expected Behavior:")
    report.append("  - At 25°C:  Fan runs at ~30% speed (low cooling)")
    report.append("  - At 50°C:  Fan runs at ~60% speed (medium cooling)")
    report.append("  - At 75°C:  Fan runs at ~90% speed (high cooling)")
    report.append("  - At 100°C: Fan runs at 100% speed (maximum cooling)")
    report.append("")
    report.append("=" * 80)
    report.append("END OF REPORT")
    report.append("=" * 80)
    
    return "\n".join(report)

def save_csv(data, filename="simulation_data.csv"):
    """Save data to CSV file for further analysis"""
    if not data:
        return
    
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['temp', 'adc', 'pwm'])
        writer.writeheader()
        writer.writerows(data)
    
    print(f"✓ CSV data saved to: {filename}")

def main():
    print("Parsing UART output...")
    data = parse_uart_output()
    
    if not data:
        print("No data found. Make sure you've run the simulation first.")
        return
    
    print(f"✓ Parsed {len(data)} data samples")
    
    print("Calculating statistics...")
    stats = calculate_stats(data)
    
    print("Generating report...")
    report = generate_report(data, stats)
    
    # Save report to file
    report_filename = "PROJECT_REPORT.txt"
    with open(report_filename, 'w') as f:
        f.write(report)
    
    print(f"✓ Report saved to: {report_filename}")
    
    # Save CSV
    save_csv(data)
    
    # Print report to console
    print("\n" + report)
    
    print(f"\n✓ Report generation complete!")
    print(f"\nGenerated files:")
    print(f"  - {report_filename} (formatted report)")
    print(f"  - simulation_data.csv (raw data for Excel/analysis)")

if __name__ == "__main__":
    main()
