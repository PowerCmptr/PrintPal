#!/usr/bin/env python3
"""
Klipper integration (via Moonraker)
"""

from .moonraker import MoonrakerClient, PrinterStatus

class KlipperClient(MoonrakerClient):
    """Klipper client (extends Moonraker)"""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 7125):
        super().__init__(host, port)
    
    def get_gcode_help(self) -> dict:
        """Get G-code help documentation"""
        if not self.network_available or not self.connected:
            return {}
        
        try:
            response = self.session.get(f"{self.base_url}/printer/gcode/help", timeout=5)
            if response.status_code == 200:
                return response.json().get('result', {})
        except:
            pass
        
        return {}
    
    def emergency_stop(self) -> bool:
        """Emergency stop printer"""
        return self.send_gcode("M112")
    
    def home_all(self) -> bool:
        """Home all axes"""
        return self.send_gcode("G28")
    
    def move_relative(self, x: float = None, y: float = None, 
                     z: float = None, e: float = None) -> bool:
        """Move relative to current position"""
        gcode = "G91\n"  # Relative positioning
        
        moves = []
        if x is not None:
            moves.append(f"X{x}")
        if y is not None:
            moves.append(f"Y{y}")
        if z is not None:
            moves.append(f"Z{z}")
        if e is not None:
            moves.append(f"E{e}")
        
        if moves:
            gcode += f"G1 {' '.join(moves)} F6000\n"
            gcode += "G90"  # Back to absolute positioning
            return self.send_gcode(gcode)
        
        return False
    
    def get_endstops(self) -> dict:
        """Get endstop status"""
        if not self.network_available or not self.connected:
            return {}
        
        try:
            response = self.session.get(
                f"{self.base_url}/printer/objects/query?query_endstops=1",
                timeout=5
            )
            if response.status_code == 200:
                result = response.json()
                return result.get('result', {}).get('status', {}).get('query_endstops', {})
        except:
            pass
        
        return {}