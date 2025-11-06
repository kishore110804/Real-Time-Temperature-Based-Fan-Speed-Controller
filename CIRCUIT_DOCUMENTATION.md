# Circuit Schematic Documentation
## STM32F103C8 Temperature-Controlled Fan System

### Generated Files
- **RTS_FanControl.kicad_sch** - Main KiCad schematic file (open in KiCad 7.x)
- **report_outputs/** - Directory for exported PDF/SVG files

---

## Circuit Components

### U1 - STM32F103C8T6 Microcontroller
- **Type:** 32-bit ARM Cortex-M3
- **Clock:** 72 MHz
- **Package:** LQFP-48
- **Function:** Main controller running temperature control algorithm

**Pin Connections:**
- **PA0 (Pin 10):** ADC input - Temperature sensor reading (currently simulated in software)
- **PA6 (Pin 16):** PWM output - TIM3_CH1 @ 8kHz, drives transistor base through R1
- **PA9 (Pin 30):** UART TX - Debug output @ 115200 baud
- **PA10 (Pin 31):** UART RX - Debug input @ 115200 baud
- **VDD (Pin 1):** +5V power supply
- **VSS (Pin 2):** Ground

---

### U2 - LM35 Temperature Sensor
- **Type:** Precision analog temperature sensor
- **Output:** 10mV per °C (linear)
- **Range:** 0°C to 100°C
- **Package:** TO-92

**Pin Connections:**
- **Pin 1 (VCC):** +5V power
- **Pin 2 (OUT):** Analog output → connects to PA0 (ADC input)
- **Pin 3 (GND):** Ground

**Note:** In the current firmware (main_simple.c), temperature is simulated in software for Renode compatibility. For real hardware, this sensor provides actual temperature readings.

---

### Q1 - 2N2222 NPN Transistor
- **Type:** NPN switching transistor
- **Function:** Motor driver switch
- **Max Collector Current:** 800 mA
- **Package:** TO-92

**Pin Connections:**
- **Base (Pin 1):** PWM signal from PA6 through R1 (1kΩ resistor)
- **Emitter (Pin 2):** Ground
- **Collector (Pin 3):** Motor negative terminal (switches motor on/off)

**Operation:**
- PWM signal from PA6 switches transistor on/off rapidly
- Duty cycle determines average current through motor
- Higher duty cycle = faster fan speed

---

### R1 - Base Resistor
- **Value:** 1kΩ (1000 Ω)
- **Power Rating:** 1/4 W (0.25W)
- **Function:** Current limiting resistor for transistor base

**Calculation:**
- PWM output: 3.3V (STM32 logic level)
- Base-Emitter voltage: ~0.7V
- Base current: (3.3V - 0.7V) / 1kΩ = 2.6 mA
- Safe for 2N2222 (max base current: 5 mA)

---

### D1 - 1N4007 Flyback Diode
- **Type:** Rectifier diode
- **Function:** Motor flyback protection
- **Ratings:** 1A, 1000V

**Connection:** Connected in reverse across motor (cathode to +5V, anode to collector)

**Purpose:**
- Protects transistor from voltage spikes when motor turns off
- Motor coil generates back-EMF when power is cut
- Diode provides path for inductive current to dissipate safely

---

### M1 - DC Cooling Fan
- **Type:** 5V DC brushed motor
- **Typical Current:** 100-300 mA
- **Speed Control:** PWM @ 8 kHz

**Pin Connections:**
- **Positive (+):** +5V power rail
- **Negative (-):** Collector of Q1 (switched to ground)

**Control Method:**
- Transistor Q1 rapidly switches motor connection to ground
- PWM frequency: 8 kHz (inaudible, smooth operation)
- Duty cycle: 0-100% (proportional to temperature)

---

## Power Supply

### +5V Rail
- Powers all components: STM32, LM35, and motor
- Recommended supply: 5V @ 500mA minimum
- Can use USB power (5V) or regulated power supply

### GND Rail
- Common ground for all components
- Ensure solid ground connection to prevent noise

---

## Control Algorithm

### Proportional Control
```
PWM_Duty_Cycle = Temperature × 40
```

**Example Operation:**
- 25°C → PWM: 1000 (25% duty) → Fan runs at 25% speed
- 50°C → PWM: 2000 (50% duty) → Fan runs at 50% speed
- 75°C → PWM: 3000 (75% duty) → Fan runs at 75% speed
- 100°C → PWM: 4000 (100% duty) → Fan runs at maximum speed

**Range:**
- PWM duty cycle: 0 to 4000 (16-bit timer, scaled to 0-100%)
- Temperature: 25°C to 100°C (auto-cycling in simulation)
- Update rate: 2 Hz (every 500ms)

---

## Signal Flow

1. **Temperature Sensing:**
   - LM35 outputs analog voltage (10mV/°C)
   - STM32 ADC1 (PA0) reads voltage
   - Software converts to temperature in °C

2. **Control Processing:**
   - STM32 calculates PWM duty cycle
   - Formula: PWM = Temperature × 40
   - Limits: 0 ≤ PWM ≤ 4000

3. **Motor Drive:**
   - TIM3_CH1 (PA6) generates 8kHz PWM signal
   - PWM drives transistor base through 1kΩ resistor
   - Transistor switches motor ground connection

4. **Debug Output:**
   - USART1 (PA9) transmits data @ 115200 baud
   - Format: "Temp: XX C | ADC: XXX | PWM: XXXX | Fan: XX%"
   - Update rate: Every 500ms

---

## Schematic Layout

**Left Side - Temperature Sensor:**
- LM35 positioned on left
- Clear power and output connections
- Label: "Temperature Sensor (Software Simulated)"

**Center - Microcontroller:**
- STM32F103C8T6 main processor
- All GPIO pins labeled
- Power connections shown
- Label: "STM32 Controller - 72MHz ARM Cortex-M3"

**Right Side - Motor Driver:**
- Transistor driver circuit
- Base resistor
- Flyback diode protection
- DC fan motor
- Label: "Fan Driver Circuit - PWM @ 8kHz"

**Bottom - Pin Function Notes:**
- PA0: ADC Input (Temperature)
- PA6: PWM Output (TIM3_CH1)
- PA9/PA10: UART Debug @ 115200

---

## Opening the Schematic

### Using KiCad:
1. Install KiCad 7.x or later (free, open-source)
2. Open KiCad
3. File → Open → Select `RTS_FanControl.kicad_sch`
4. View the complete circuit diagram

### Exporting for Reports:
1. In KiCad schematic editor: File → Plot
2. Select PDF or PNG format
3. Choose output directory (e.g., report_outputs/)
4. Click "Plot All Pages"
5. Use exported image in your project documentation

### Alternative Method (KiCad CLI):
If KiCad CLI is installed in PATH:
```bash
kicad-cli sch export pdf RTS_FanControl.kicad_sch -o report_outputs/
kicad-cli sch export svg RTS_FanControl.kicad_sch -o report_outputs/
```

---

## Implementation Notes

### Current Firmware (main_simple.c):
- **Framework:** Bare-metal CMSIS (no HAL)
- **Size:** 852 bytes Flash, 28 bytes RAM
- **Temperature:** Software-simulated (25°C to 100°C sweep)
- **Purpose:** Renode simulator compatibility

### Future Hardware Implementation:
- Use full HAL firmware (src/main.c)
- Enable real ADC reading from LM35 on PA0
- Enable TIM3 hardware PWM on PA6
- Upload to real STM32F103C8 BluePill board
- Connect actual LM35 sensor and DC fan

### Renode Simulation:
- Current setup works perfectly in Renode
- Generates realistic temperature sweep data
- Demonstrates control algorithm
- UART output shows all parameters
- No actual hardware required for testing

---

## Safety Considerations

1. **Transistor Heat:**
   - 2N2222 can dissipate ~500mW without heatsink
   - At 300mA motor current and switching: minimal heat
   - No heatsink required for typical fan loads

2. **Flyback Protection:**
   - Always include D1 (1N4007) across motor
   - Prevents voltage spikes from damaging transistor
   - Critical for inductive loads (motors, relays, solenoids)

3. **Power Supply:**
   - Ensure 5V supply can handle total current:
     - STM32: ~50mA
     - LM35: ~60µA (negligible)
     - Motor: 100-300mA
     - Total: ~400mA peak
   - Use 500mA or 1A supply for safety margin

4. **Decoupling:**
   - Add 100nF ceramic capacitor near STM32 VDD pin
   - Add 10µF electrolytic across motor for noise suppression
   - Prevents reset issues from motor transients

---

## Testing Procedure

### Simulation Testing (Current):
1. Run `demo_for_professor.bat`
2. Observe Renode output showing temperature sweep
3. Check UART output for correct PWM calculation
4. Verify linear relationship: Temp vs Fan Speed

### Hardware Testing (Future):
1. Assemble circuit on breadboard per schematic
2. Upload firmware to STM32 using ST-Link
3. Connect UART (PA9/PA10) to USB-Serial adapter
4. Open serial monitor @ 115200 baud
5. Heat LM35 sensor (warm hand, hair dryer, etc.)
6. Observe fan speed increase with temperature
7. Verify PWM duty cycle calculation
8. Monitor temperature range 25°C to 100°C

---

## Troubleshooting

**Motor doesn't run:**
- Check transistor connections (BCE pins)
- Verify PWM signal on PA6 with oscilloscope
- Ensure base resistor R1 is 1kΩ (not 10kΩ or higher)
- Test transistor with multimeter (should show ~0.7V Vbe when on)

**Erratic fan behavior:**
- Add 10µF capacitor across motor terminals
- Check for loose ground connections
- Ensure flyback diode D1 orientation is correct
- Verify 5V power supply is stable under load

**Temperature reading wrong:**
- Check LM35 connections (VCC, OUT, GND)
- Verify ADC reference voltage (should be 3.3V)
- Calibrate ADC reading in software
- Ensure analog input pin PA0 is configured correctly

**STM32 resets randomly:**
- Add 100nF capacitor between VDD and VSS
- Separate motor power from microcontroller power if possible
- Ensure flyback diode is installed
- Check for proper grounding

---

## Files in This Project

- **RTS_FanControl.kicad_sch** - KiCad schematic (this circuit)
- **src/main_simple.c** - Simplified firmware for Renode
- **src/main.c** - Full HAL firmware for real hardware
- **demo_sim.resc** - Renode simulation script
- **PROJECT_REPORT.txt** - Simulation results report
- **simulation_data.csv** - Raw data for graphing
- **generate_kicad_schematic.py** - Python script that generated this schematic
- **demo_for_professor.bat** - Complete demonstration script

---

## References

- STM32F103C8T6 Datasheet: [ST Microelectronics](https://www.st.com/)
- LM35 Datasheet: [Texas Instruments](https://www.ti.com/)
- 2N2222 Datasheet: Standard NPN transistor specifications
- KiCad Documentation: [https://docs.kicad.org/](https://docs.kicad.org/)
- STM32 Reference Manual: RM0008

---

**Generated:** November 7, 2025  
**Project:** Real-Time Systems - Temperature Controlled Fan  
**Microcontroller:** STM32F103C8T6 (ARM Cortex-M3)
