# EXACT WIRE CONNECTIONS - FROM YOUR SCHEMATIC

## Your Current Components (as shown in Proteus)

```
U1: STM32F103C8 (Microcontroller)
U2: LM35 (Temperature Sensor)
Q1: 2N2222 (NPN Transistor)
D1: 1N4007 (Diode)
R1, R2, R3: Resistors
C1, C2: Capacitors
X1: RESONATOR (Crystal - you just placed)
```

---

## CRYSTAL (X1) WIRING - EXACT PIN NAMES

From your schematic, the resonator has these pins:

### **X1 Connections (2 wires needed):**

| From | To | Connection |
|------|----|----|
| **X1 Pin 1** | **U1 OSCIN_FD0** (Pin 5 on U1) | Wire these together |
| **X1 Pin 2** | **U1 OSCOUT_FD1** (Pin 6 on U1) | Wire these together |

---

## LOAD CAPACITORS (C3 & C4) - Optional but Recommended

These stabilize the crystal oscillator:

### **C3 Connections:**
| From | To | Note |
|------|----|----|
| **C3 Pin 1** | **X1 Pin 1** | Connects to same pin as X1→U1 OSCIN_FD0 |
| **C3 Pin 2** | **GND** | Ground rail |

### **C4 Connections:**
| From | To | Note |
|------|----|----|
| **C4 Pin 1** | **X1 Pin 2** | Connects to same pin as X1→U1 OSCOUT_FD1 |
| **C4 Pin 2** | **GND** | Ground rail |

---

## VISUAL DIAGRAM (from your schematic)

```
                 ┌─ X1 (RESONATOR) ─┐
                 │   Pin 1    Pin 2  │
                 └─────┬──────┬──────┘
                       │      │
        ┌──────────────┘      └──────────────┐
        │                                     │
        ↓                                     ↓
   U1.OSCIN_FD0                          U1.OSCOUT_FD1
   (U1 Pin 5)                            (U1 Pin 6)


   LOAD CAPACITORS (both to GND):
   
        C3 ──┐      C4 ──┐
             │            │
             └─ to X1 Pin1 │
                           └─ to X1 Pin 2
             
        Both other ends → GND
```

---

## STEP-BY-STEP FOR YOU

### **Step 1: Wire X1 Pin 1 to U1**
1. Click on **X1 Pin 1**
2. Click on **U1 OSCIN_FD0** (Pin 5)
3. Done - you should see a red wire connect

### **Step 2: Wire X1 Pin 2 to U1**
1. Click on **X1 Pin 2**
2. Click on **U1 OSCOUT_FD1** (Pin 6)
3. Done - another red wire should appear

### **Step 3 (Optional): Add C3 load capacitor**
1. Double-click to place C3 capacitor (20pF)
2. Wire **C3 Pin 1** → **X1 Pin 1**
3. Wire **C3 Pin 2** → **GND**

### **Step 4 (Optional): Add C4 load capacitor**
1. Double-click to place C4 capacitor (20pF)
2. Wire **C4 Pin 1** → **X1 Pin 2**
3. Wire **C4 Pin 2** → **GND**

---

## COMPONENT VALUES

```
X1:  8MHz RESONATOR (or XTAL, CRYSTAL)
C3:  20pF Ceramic Capacitor (if adding load caps)
C4:  20pF Ceramic Capacitor (if adding load caps)
```

---

## QUICK REFERENCE TABLE

| Component | Pin | Connects To | Label |
|-----------|-----|------------|-------|
| X1 | 1 | U1 OSCIN_FD0 | Crystal Pin 1 |
| X1 | 2 | U1 OSCOUT_FD1 | Crystal Pin 2 |
| C3 | 1 | X1 Pin 1 | Load Cap 1 |
| C3 | 2 | GND | Load Cap 1 |
| C4 | 1 | X1 Pin 2 | Load Cap 2 |
| C4 | 2 | GND | Load Cap 2 |

---

**THAT'S IT!** Once these two wires (X1→U1) are connected, the crystal is done. The capacitors (C3, C4) are optional but recommended for stable oscillation.

