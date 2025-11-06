# KiCad Setup - Quick Start Guide

## What I Created For You

```
✅ RTS_FanControl.kicad_pro     - KiCad Project file
✅ RTS_FanControl.kicad_sch     - Schematic (all components pre-wired)
✅ RTS_FanControl.cir           - ngspice simulation file (ready to run)
✅ KiCad_SETUP_GUIDE.md         - This file
```

---

## Step 1: Open the KiCad Project

**Option A: From File Explorer**
1. Open: `c:\Users\Kishore N\Documents\PlatformIO\Projects\RTS_FanControl\`
2. Double-click: `RTS_FanControl.kicad_pro`
3. KiCad opens automatically

**Option B: From KiCad App**
1. Launch KiCad
2. File → Open Project
3. Select `RTS_FanControl.kicad_pro`

---

## Step 2: View Your Schematic

1. In KiCad, click: **Schematic Editor** (left panel)
2. You'll see your circuit:
   - **U1** = STM32F103C8 (Microcontroller)
   - **U2** = LM35 (Temperature Sensor)
   - **Q1** = 2N2222 (Motor Driver)
   - **D1** = 1N4007 (Protection Diode)
   - **C1-C4** = Capacitors
   - **R1-R3** = Resistors
   - **X1** = 8MHz Crystal

---

## Step 3: Run Simulation with ngspice

### **Option A: Command Line (Recommended)**

1. Open **PowerShell** in workspace folder
2. Run this command:
   ```
   ngspice RTS_FanControl.cir
   ```
3. You should see:
   ```
   ngspice 1 — Circuit Simulator
   ...
   Simulation complete
   ```

### **Option B: From KiCad GUI**

1. In KiCad Schematic Editor
2. Click: **Simulate** (or Tools → Simulator)
3. Click: **Load Netlist** → Select `RTS_FanControl.cir`
4. Click: **Run Simulation**

---

## Step 4: Understand the Simulation

The `.cir` file does this:

| Input | Process | Output |
|-------|---------|--------|
| Temperature (0-110°C) | LM35 Sensor | ADC Voltage (0-1.1V) |
| ADC Voltage | STM32 ADC | Digital Count (0-4095) |
| ADC Count | STM32 PWM | PWM on PA6 (0-3.3V) |
| PWM Signal | 2N2222 + Motor | Motor Speed Control |

---

## Step 5: Verify Circuit Connections

The `.kicad_sch` includes all these connections:

### **Power:**
- VCC = 5V (Motor supply)
- VDD = 3.3V (STM32 core)
- GND = Ground

### **Temperature Sensing:**
- LM35 Vout → U1 PA0 (ADC Channel 0)
- LM35 VCC → 5V
- LM35 GND → GND

### **PWM Output:**
- U1 PA6 → R3 → Q1 Base
- Q1 Collector → Motor + D1 Anode
- Q1 Emitter → GND
- D1 Cathode → VCC (freewheeling)

### **Crystal Oscillator:**
- X1 Pin 1 → U1 OSCIN (OSC_IN)
- X1 Pin 2 → U1 OSCOUT (OSC_OUT)
- C3 (20pF) across Pin 1 to GND
- C4 (20pF) across Pin 2 to GND

### **Decoupling:**
- C1 (0.1µF) on U1 VDD → GND
- C2 (0.1µF) on VCC → GND

---

## Step 6: Load Your Firmware

To run your actual STM32 code in simulation:

1. **Export HEX file from PlatformIO:**
   - Build: `pio run -e bluepill_f103c8`
   - Locate: `.pio/build/bluepill_f103c8/firmware.hex`

2. **In ngspice simulation:**
   - The STM32 model includes ADC → PWM transfer function
   - Your firmware is abstracted as behavioral model
   - Temperature input on PA0 → PWM output on PA6

---

## Step 7: Test Temperature Response

**Manual Test:**

1. In simulation, vary VIN_TEMP (temperature input)
2. Observe PA0 voltage (ADC input)
3. Observe PA6 voltage (PWM output)

**Expected Behavior:**
- VIN_TEMP = 0V (0°C) → PA6 ≈ 0V (Motor off)
- VIN_TEMP = 0.33V (33°C) → PA6 ≈ 1.0V (Motor ~30% speed)
- VIN_TEMP = 0.66V (66°C) → PA6 ≈ 2.0V (Motor ~60% speed)
- VIN_TEMP = 1.1V (110°C) → PA6 ≈ 3.3V (Motor full speed)

---

## Troubleshooting

### **Problem: ngspice command not found**
**Solution:** Install ngspice
```powershell
# Using Windows package manager (if installed)
scoop install ngspice

# OR download from: http://ngspice.sourceforge.net/
```

### **Problem: KiCad shows empty schematic**
**Solution:** 
- Wait for symbols to load (may take 10-20 sec)
- Press F5 to refresh
- Or re-open the file

### **Problem: Simulation shows no output**
**Solution:**
- Check ngspice is installed: `ngspice --version`
- Run simulation with verbose: `ngspice -b RTS_FanControl.cir -o sim.log`
- Check output file: `type sim.log`

---

## Next Steps

1. ✅ **Done:** KiCad project created
2. ✅ **Done:** Schematic pre-wired
3. ✅ **Done:** Simulation ready
4. 📍 **Now:** Open KiCad and verify schematic
5. 📍 **Then:** Run ngspice simulation
6. 📍 **Finally:** Verify temperature → PWM response

---

## Files Reference

| File | Purpose | Open With |
|------|---------|-----------|
| `RTS_FanControl.kicad_pro` | Project file | KiCad (double-click) |
| `RTS_FanControl.kicad_sch` | Schematic diagram | KiCad (auto-opens) |
| `RTS_FanControl.cir` | SPICE simulation | ngspice or text editor |
| `KiCad_SETUP_GUIDE.md` | This guide | Any text editor |

---

**Ready? Let's go!** 🚀

Next: Open `RTS_FanControl.kicad_pro` and tell me what you see!
