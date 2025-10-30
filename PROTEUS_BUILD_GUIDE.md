# 🔧 RTS Fan Control - Proteus Circuit Build Guide

## Complete Step-by-Step Instructions

---

## **PART 1: MICROCONTROLLER & POWER SETUP**

### Step 1: Add STM32F103C8 Microcontroller
- [ ] **Search Code:** `STM32F103C8` (or `bluepill`)
- [ ] **Place it** in center of schematic
- [ ] **Label:** U1
- [ ] **Position:** Around coordinates (100, 200)

### Step 2: Add Decoupling Capacitors (Power Supply Bypass)
- [ ] **Search Code:** `02013A1R0CAT2A` (0.1µF capacitor)
- [ ] **Add 2 capacitors** for power filtering
  - [ ] **C1:** Near U1 VCC pin (position: 50, 150)
  - [ ] **C2:** For LM35 sensor (position: 50, 100)
- [ ] **Set value:** `0.1µF` for both

---

## **PART 2: TEMPERATURE SENSOR (LM35)**

### Step 3: Add Temperature Sensor
- [ ] **Search Code:** `LM35`
- [ ] **Place it** (position: 50, 300)
- [ ] **Label:** U2
- [ ] **Connections needed:**
  - [ ] LM35 OUTPUT → U1 PA0 (ADC input)
  - [ ] LM35 VCC → C2 positive
  - [ ] LM35 GND → C2 negative

---

## **PART 3: FAN MOTOR DRIVER (TRANSISTOR)**

### Step 4: Add Base Resistor
- [ ] **Search Code:** `10WATT10K` (10kΩ resistor)
- [ ] **Place it** (position: 125, 250)
- [ ] **Label:** R2
- [ ] **Set value:** `10k`

### Step 5: Add Transistor (Fan Driver)
- [ ] **Search Code:** `2N2222` (NPN BJT transistor)
- [ ] **Place it** (position: 200, 300)
- [ ] **Label:** Q1
- [ ] **Connections:**
  - [ ] U1 PA6 (PWM output) → R2 Pin 1
  - [ ] R2 Pin 2 → Q1 BASE
  - [ ] Q1 COLLECTOR → Motor + (or diode +)
  - [ ] Q1 EMITTER → GND

### Step 6: Add Protection Diode
- [ ] **Search Code:** `1N4007` (power diode)
- [ ] **Place it** (position: 225, 300)
- [ ] **Label:** D1
- [ ] **Orientation:** Positive toward motor, negative to emitter
- [ ] **Connections:**
  - [ ] Q1 COLLECTOR → D1 Anode (+)
  - [ ] D1 Cathode (-) → Q1 EMITTER

---

## **PART 4: CRYSTAL & CLOCK (OPTIONAL BUT RECOMMENDED)**

### Step 7: Add 8MHz Crystal
- [ ] **Search Code:** `8MHz` (or `XTAL` or `CRYSTAL`)
- [ ] **Place it** (position: 100, 350)
- [ ] **Label:** XTAL1
- [ ] **Connections:**
  - [ ] XTAL1 Pin 1 → U1 OSC_IN
  - [ ] XTAL1 Pin 2 → U1 OSC_OUT

### Step 8: Add Crystal Load Capacitors (20pF each)
- [ ] **Search Code:** `02013A1R0CAT2A` (0.1µF, but set to 20pF)
- [ ] **Add 2 capacitors:**
  - [ ] **C3:** Position (150, 150), Value: `20pF`
  - [ ] **C4:** Position (150, 100), Value: `20pF`
- [ ] **Connections:**
  - [ ] C3 Pin 1 → XTAL1 Pin 1
  - [ ] C4 Pin 1 → XTAL1 Pin 2
  - [ ] C3 Pin 2 → GND
  - [ ] C4 Pin 2 → GND

---

## **PART 5: ADDITIONAL RESISTORS (OPTIONAL)**

### Step 9: Add Pull-up Resistor (Optional)
- [ ] **Search Code:** `10WATT1K` (1kΩ resistor)
- [ ] **Place it** (position: 75, 250)
- [ ] **Label:** R1
- [ ] **Set value:** `1k`

### Step 10: Add Current Limiting Resistor (Optional)
- [ ] **Search Code:** `10WATT220R` (220Ω resistor)
- [ ] **Place it** (position: 175, 250)
- [ ] **Label:** R3
- [ ] **Set value:** `220`

---

## **PART 6: POWER CONNECTIONS**

### Step 11: Add Power Rails
- [ ] **Add +5V rail** (label: VCC or +5V)
- [ ] **Add GND rail** (label: GND or 0V)
- [ ] **Connect all VCC pins** to +5V
- [ ] **Connect all GND pins** to GND

---

## **PART 7: LOAD HEX FILE INTO MICROCONTROLLER**

### Step 12: Program the Microcontroller
1. **Double-click U1 (STM32F103C8)**
2. **Look for "Program File" field**
3. **Browse and select:**
   ```
   .pio/build/bluepill_f103c8/firmware.hex
   ```
4. **Click OK**

---

## **FINAL CHECKLIST**

### All Components Added:
- [ ] U1 - STM32F103C8 (Microcontroller)
- [ ] U2 - LM35 (Temperature Sensor)
- [ ] C1 - 0.1µF (Decoupling)
- [ ] C2 - 0.1µF (Decoupling)
- [ ] C3 - 20pF (Crystal load)
- [ ] C4 - 20pF (Crystal load)
- [ ] R1 - 1kΩ (Optional pull-up)
- [ ] R2 - 10kΩ (Transistor base)
- [ ] R3 - 220Ω (Optional current limiting)
- [ ] Q1 - 2N2222 (Transistor driver)
- [ ] D1 - 1N4007 (Protection diode)
- [ ] XTAL1 - 8MHz (Clock crystal)

### All Connections Made:
- [ ] Temperature sensor output → ADC input (PA0)
- [ ] PWM output (PA6) → Transistor base (via R2)
- [ ] Transistor collector → Motor/Load
- [ ] Diode in reverse bias across motor
- [ ] Crystal connected with load capacitors
- [ ] All power pins connected to VCC and GND

---

## **NEXT STEPS**

1. **Build firmware:**
   ```
   cd RTS_FanControl
   pio run -e bluepill_f103c8
   ```

2. **Program microcontroller** with hex file (Step 12 above)

3. **Run Proteus simulation:**
   - Click the play button ▶️
   - Vary the LM35 input voltage (0-3.3V)
   - Observe PWM duty cycle changes
   - Monitor UART output

---

## **COMPONENT SEARCH REFERENCE**

| Component | Search Code | Value | Quantity |
|-----------|------------|-------|----------|
| Microcontroller | `STM32F103C8` | - | 1 |
| Temperature Sensor | `LM35` | - | 1 |
| Capacitor (Decoupling) | `02013A1R0CAT2A` | 0.1µF | 2 |
| Capacitor (Crystal) | `02013A1R0CAT2A` | 20pF | 2 |
| Resistor (Pull-up) | `10WATT1K` | 1kΩ | 1 |
| Resistor (Base) | `10WATT10K` | 10kΩ | 1 |
| Resistor (Current) | `10WATT220R` | 220Ω | 1 |
| Transistor | `2N2222` | - | 1 |
| Diode | `1N4007` | - | 1 |
| Crystal | `8MHz` or `XTAL` | 8MHz | 1 |

---

## **TROUBLESHOOTING**

| Problem | Solution |
|---------|----------|
| Component not found | Try searching with different keywords (e.g., `RES` for resistor) |
| Wrong capacitor value | After placing, right-click → Edit → Change value to desired µF/pF |
| Wires not connecting | Make sure pin names match exactly (case-sensitive) |
| No simulation | Check that all GND and VCC are connected properly |

---

**Total Time to Build: ~15-20 minutes** ⏱️

**You got this! Let me know if you get stuck on any step!** 🚀
