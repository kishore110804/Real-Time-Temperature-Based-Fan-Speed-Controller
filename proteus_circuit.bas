' ============================================
' RTS Fan Control Circuit - Auto Generated
' Generated: 2025-10-30 21:59:55
' ============================================

Sub Main()
    Dim objDes
    Dim objSch
    Dim objSym
    Dim objPin
    Dim objWire

    Set objDes = GetObject(, "PROTEUS.MSO")
    Set objSch = objDes.GetCurrentSchematic

    ' ===== ADD COMPONENTS =====
    ' Component 1: U1
    Set objSym = objSch.CreateComponent("STM32F103C8", 100, 200)
    objSym.SetProperty "Reference", "U1"
    objSym.SetProperty "Value", "STM32F103C8"
    objSym.SetProperty "Orientation", 0

    ' Component 2: C1
    Set objSym = objSch.CreateComponent("02013A1R0CAT2A", 50, 150)
    objSym.SetProperty "Reference", "C1"
    objSym.SetProperty "Value", "0.1uF"
    objSym.SetProperty "Orientation", 0

    ' Component 3: C2
    Set objSym = objSch.CreateComponent("02013A1R0CAT2A", 50, 100)
    objSym.SetProperty "Reference", "C2"
    objSym.SetProperty "Value", "0.1uF"
    objSym.SetProperty "Orientation", 0

    ' Component 4: C3
    Set objSym = objSch.CreateComponent("02013A1R0CAT2A", 150, 150)
    objSym.SetProperty "Reference", "C3"
    objSym.SetProperty "Value", "20pF"
    objSym.SetProperty "Orientation", 0

    ' Component 5: C4
    Set objSym = objSch.CreateComponent("02013A1R0CAT2A", 150, 100)
    objSym.SetProperty "Reference", "C4"
    objSym.SetProperty "Value", "20pF"
    objSym.SetProperty "Orientation", 0

    ' Component 6: R1
    Set objSym = objSch.CreateComponent("10WATT1K", 75, 250)
    objSym.SetProperty "Reference", "R1"
    objSym.SetProperty "Value", "1k"
    objSym.SetProperty "Orientation", 0

    ' Component 7: R2
    Set objSym = objSch.CreateComponent("10WATT10K", 125, 250)
    objSym.SetProperty "Reference", "R2"
    objSym.SetProperty "Value", "10k"
    objSym.SetProperty "Orientation", 0

    ' Component 8: R3
    Set objSym = objSch.CreateComponent("10WATT220R", 175, 250)
    objSym.SetProperty "Reference", "R3"
    objSym.SetProperty "Value", "220"
    objSym.SetProperty "Orientation", 0

    ' Component 9: U2
    Set objSym = objSch.CreateComponent("LM35", 50, 300)
    objSym.SetProperty "Reference", "U2"
    objSym.SetProperty "Value", "LM35"
    objSym.SetProperty "Orientation", 0

    ' Component 10: Q1
    Set objSym = objSch.CreateComponent("2N2222", 200, 300)
    objSym.SetProperty "Reference", "Q1"
    objSym.SetProperty "Value", "2N2222"
    objSym.SetProperty "Orientation", 0

    ' Component 11: D1
    Set objSym = objSch.CreateComponent("1N4007", 225, 300)
    objSym.SetProperty "Reference", "D1"
    objSym.SetProperty "Value", "1N4007"
    objSym.SetProperty "Orientation", 0

    ' Component 12: XTAL1
    Set objSym = objSch.CreateComponent("8MHz", 100, 350)
    objSym.SetProperty "Reference", "XTAL1"
    objSym.SetProperty "Value", "8MHz"
    objSym.SetProperty "Orientation", 0

    ' ===== ADD CONNECTIONS =====
    ' Connection 1: U1.VCC -> C1.+
    objSch.CreateWire "U1.VCC", "C1.+"
    ' Connection 2: U1.GND -> C1.-
    objSch.CreateWire "U1.GND", "C1.-"
    ' Connection 3: U2.VCC -> C2.+
    objSch.CreateWire "U2.VCC", "C2.+"
    ' Connection 4: U2.GND -> C2.-
    objSch.CreateWire "U2.GND", "C2.-"
    ' Connection 5: U2.OUT -> U1.PA0
    objSch.CreateWire "U2.OUT", "U1.PA0"
    ' Connection 6: U1.PA6 -> R2.1
    objSch.CreateWire "U1.PA6", "R2.1"
    ' Connection 7: R2.2 -> Q1.BASE
    objSch.CreateWire "R2.2", "Q1.BASE"
    ' Connection 8: Q1.COLLECTOR -> D1.+
    objSch.CreateWire "Q1.COLLECTOR", "D1.+"
    ' Connection 9: D1.- -> Q1.EMITTER
    objSch.CreateWire "D1.-", "Q1.EMITTER"
    ' Connection 10: XTAL1.1 -> U1.OSC_IN
    objSch.CreateWire "XTAL1.1", "U1.OSC_IN"
    ' Connection 11: XTAL1.2 -> U1.OSC_OUT
    objSch.CreateWire "XTAL1.2", "U1.OSC_OUT"
    ' Connection 12: C3.1 -> XTAL1.1
    objSch.CreateWire "C3.1", "XTAL1.1"
    ' Connection 13: C4.1 -> XTAL1.2
    objSch.CreateWire "C4.1", "XTAL1.2"

End Sub