"""
RTS Fan Control - Proteus Circuit Generator Script
Generates a BASIC script to automate circuit creation in Proteus
"""

import json
from datetime import datetime

class ProteusCircuitGenerator:
    def __init__(self, project_name="RTS_FanControl"):
        self.project_name = project_name
        self.components = []
        self.connections = []
        self.script = []
        
    def add_component(self, reference, part_code, x, y, value="", orientation=0):
        """Add component to circuit"""
        component = {
            "reference": reference,
            "part_code": part_code,
            "x": x,
            "y": y,
            "value": value,
            "orientation": orientation
        }
        self.components.append(component)
        
    def add_connection(self, from_pin, to_pin):
        """Add wire connection between pins"""
        connection = {
            "from": from_pin,
            "to": to_pin
        }
        self.connections.append(connection)
        
    def generate_basic_script(self):
        """Generate Proteus BASIC script"""
        script = []
        
        # Header
        script.append("' ============================================")
        script.append("' RTS Fan Control Circuit - Auto Generated")
        script.append(f"' Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        script.append("' ============================================")
        script.append("")
        
        # Initialize
        script.append("Sub Main()")
        script.append("    Dim objDes")
        script.append("    Dim objSch")
        script.append("    Dim objSym")
        script.append("    Dim objPin")
        script.append("    Dim objWire")
        script.append("")
        
        # Get schematic object
        script.append("    Set objDes = GetObject(, \"PROTEUS.MSO\")")
        script.append("    Set objSch = objDes.GetCurrentSchematic")
        script.append("")
        
        # Add components
        script.append("    ' ===== ADD COMPONENTS =====")
        for i, comp in enumerate(self.components):
            script.append(f"    ' Component {i+1}: {comp['reference']}")
            script.append(f"    Set objSym = objSch.CreateComponent(\"{comp['part_code']}\", {comp['x']}, {comp['y']})")
            script.append(f"    objSym.SetProperty \"Reference\", \"{comp['reference']}\"")
            if comp['value']:
                script.append(f"    objSym.SetProperty \"Value\", \"{comp['value']}\"")
            script.append(f"    objSym.SetProperty \"Orientation\", {comp['orientation']}")
            script.append("")
        
        # Add connections
        script.append("    ' ===== ADD CONNECTIONS =====")
        for i, conn in enumerate(self.connections):
            script.append(f"    ' Connection {i+1}: {conn['from']} -> {conn['to']}")
            script.append(f"    objSch.CreateWire \"{conn['from']}\", \"{conn['to']}\"")
        
        script.append("")
        script.append("End Sub")
        
        return "\n".join(script)
    
    def generate_json_manifest(self):
        """Generate JSON manifest of components"""
        manifest = {
            "project": self.project_name,
            "timestamp": datetime.now().isoformat(),
            "components": self.components,
            "connections": self.connections,
            "total_components": len(self.components),
            "total_connections": len(self.connections)
        }
        return json.dumps(manifest, indent=2)
    
    def save_basic_script(self, filename):
        """Save BASIC script to file"""
        script = self.generate_basic_script()
        with open(filename, 'w') as f:
            f.write(script)
        print(f"✓ BASIC script saved: {filename}")
        return script
    
    def save_manifest(self, filename):
        """Save component manifest"""
        manifest = self.generate_json_manifest()
        with open(filename, 'w') as f:
            f.write(manifest)
        print(f"✓ Manifest saved: {filename}")

# ============================================
# BUILD THE CIRCUIT
# ============================================

def build_rts_fan_control_circuit():
    """Build RTS Fan Control circuit for Proteus"""
    gen = ProteusCircuitGenerator("RTS_FanControl")
    
    # ===== MICROCONTROLLER =====
    gen.add_component("U1", "STM32F103C8", 100, 200, "STM32F103C8", 0)
    
    # ===== POWER SUPPLY & DECOUPLING =====
    gen.add_component("C1", "02013A1R0CAT2A", 50, 150, "0.1uF", 0)
    gen.add_component("C2", "02013A1R0CAT2A", 50, 100, "0.1uF", 0)
    gen.add_component("C3", "02013A1R0CAT2A", 150, 150, "20pF", 0)
    gen.add_component("C4", "02013A1R0CAT2A", 150, 100, "20pF", 0)
    
    # ===== RESISTORS =====
    gen.add_component("R1", "10WATT1K", 75, 250, "1k", 0)
    gen.add_component("R2", "10WATT10K", 125, 250, "10k", 0)
    gen.add_component("R3", "10WATT220R", 175, 250, "220", 0)
    
    # ===== TEMPERATURE SENSOR =====
    gen.add_component("U2", "LM35", 50, 300, "LM35", 0)
    
    # ===== TRANSISTOR (Fan Driver) =====
    gen.add_component("Q1", "2N2222", 200, 300, "2N2222", 0)
    
    # ===== DIODE (Motor Protection) =====
    gen.add_component("D1", "1N4007", 225, 300, "1N4007", 0)
    
    # ===== CRYSTAL (8MHz) =====
    gen.add_component("XTAL1", "8MHz", 100, 350, "8MHz", 0)
    
    # ===== CONNECTIONS =====
    # Power connections
    gen.add_connection("U1.VCC", "C1.+")
    gen.add_connection("U1.GND", "C1.-")
    gen.add_connection("U2.VCC", "C2.+")
    gen.add_connection("U2.GND", "C2.-")
    
    # Temperature Sensor to ADC
    gen.add_connection("U2.OUT", "U1.PA0")
    
    # PWM Output to Transistor Base
    gen.add_connection("U1.PA6", "R2.1")
    gen.add_connection("R2.2", "Q1.BASE")
    
    # Motor connections
    gen.add_connection("Q1.COLLECTOR", "D1.+")
    gen.add_connection("D1.-", "Q1.EMITTER")
    
    # UART connections (for debugging)
    # PA9 = TX, PA10 = RX (optional USB/UART module)
    
    # Crystal connections
    gen.add_connection("XTAL1.1", "U1.OSC_IN")
    gen.add_connection("XTAL1.2", "U1.OSC_OUT")
    gen.add_connection("C3.1", "XTAL1.1")
    gen.add_connection("C4.1", "XTAL1.2")
    
    return gen

# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("RTS Fan Control - Proteus Circuit Generator")
    print("=" * 60)
    print()
    
    # Generate circuit
    print("[*] Building circuit definition...")
    circuit = build_rts_fan_control_circuit()
    
    # Display statistics
    print(f"[✓] Total Components: {len(circuit.components)}")
    print(f"[✓] Total Connections: {len(circuit.connections)}")
    print()
    
    # Save files
    output_dir = "."
    basic_file = f"{output_dir}/proteus_circuit.bas"
    manifest_file = f"{output_dir}/circuit_manifest.json"
    
    print("[*] Generating files...")
    circuit.save_basic_script(basic_file)
    circuit.save_manifest(manifest_file)
    
    print()
    print("=" * 60)
    print("NEXT STEPS:")
    print("=" * 60)
    print("1. Open Proteus ISIS")
    print("2. Create a new schematic")
    print("3. Go to: Tools → Scripting → Run Script")
    print(f"4. Select: {basic_file}")
    print("5. Run the script")
    print()
    print("OR manually copy components using the manifest:")
    print(f"   {manifest_file}")
    print("=" * 60)
