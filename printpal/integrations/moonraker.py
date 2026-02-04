#!/usr/bin/env python3
"""
Moonraker API integration
"""

import time
import json
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum

class PrinterState(Enum):
    """Printer states"""
    OFF = "off"
    STARTUP = "startup"
    READY = "ready"
    PRINTING = "printing"
    PAUSED = "paused"
    COMPLETE = "complete"
    ERROR = "error"
    CANCELLING = "cancelling"
    STAND_BY = "standby"

@dataclass
class PrinterStatus:
    """Printer status container"""
    state: PrinterState = PrinterState.OFF
    filename: str = ""
    progress: float = 0.0
    print_duration: float = 0.0
    total_duration: float = 0.0
    bed_temp: float = 0.0
    bed_target: float = 0.0
    extruder_temp: float = 0.0
    extruder_target: float = 0.0
    speed_factor: int = 100
    fan_speed: int = 0
    last_update: float = 0.0
    
    @property
    def is_printing(self) -> bool:
        return self.state in [PrinterState.PRINTING, PrinterState.PAUSED]
    
    @property
    def is_heating(self) -> bool:
        return (self.extruder_target > 0 and self.extruder_temp < self.extruder_target - 2) or \
               (self.bed_target > 0 and self.bed_temp < self.bed_target - 2)

class MoonrakerClient:
    """Moonraker API client"""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 7125):
        self.base_url = f"http://{host}:{port}"
        self.session = None
        self.connected = False
        self.last_error = ""
        
        # Try to import requests
        try:
            import requests
            self.requests = requests
            self.network_available = True
        except ImportError:
            self.network_available = False
            print("requests module not available - using demo mode")
    
    def connect(self) -> bool:
        """Connect to Moonraker"""
        if not self.network_available:
            self.connected = True  # Demo mode
            return True
        
        try:
            self.session = self.requests.Session()
            response = self.session.get(f"{self.base_url}/printer/info", timeout=5)
            self.connected = response.status_code == 200
            return self.connected
        except Exception as e:
            self.last_error = str(e)
            self.connected = False
            return False
    
    def disconnect(self):
        """Disconnect from Moonraker"""
        if self.session:
            self.session.close()
            self.session = None
        self.connected = False
    
    def get_printer_status(self) -> PrinterStatus:
        """Get comprehensive printer status"""
        if not self.network_available or not self.connected:
            return self._get_demo_status()
        
        try:
            # Query all necessary objects
            query = {
                'print_stats': None,
                'heater_bed': ['temperature', 'target'],
                'extruder': ['temperature', 'target'],
                'gcode_move': ['speed_factor'],
                'fan': ['speed'],
                'display_status': ['progress']
            }
            
            # Build query string
            query_str = '&'.join([f'{obj}=1' for obj in query.keys()])
            url = f"{self.base_url}/printer/objects/query?{query_str}"
            
            response = self.session.get(url, timeout=5)
            response.raise_for_status()
            
            result = response.json()
            return self._parse_status(result)
            
        except Exception as e:
            self.last_error = str(e)
            self.connected = False
            return PrinterStatus(state=PrinterState.ERROR)
    
    def _parse_status(self, data: Dict) -> PrinterStatus:
        """Parse Moonraker response"""
        try:
            status = data.get('result', {}).get('status', {})
            
            # Printer state
            print_stats = status.get('print_stats', {})
            state_str = print_stats.get('state', 'standby').lower()
            
            state_map = {
                'printing': PrinterState.PRINTING,
                'paused': PrinterState.PAUSED,
                'complete': PrinterState.COMPLETE,
                'cancelled': PrinterState.COMPLETE,
                'error': PrinterState.ERROR,
                'standby': PrinterState.STAND_BY,
                'ready': PrinterState.READY,
            }
            
            state = state_map.get(state_str, PrinterState.STAND_BY)
            
            # Extract data
            filename = print_stats.get('filename', '')
            print_duration = print_stats.get('print_duration', 0.0)
            
            # Temperatures
            bed_temp = status.get('heater_bed', {}).get('temperature', 0.0)
            bed_target = status.get('heater_bed', {}).get('target', 0.0)
            extruder_temp = status.get('extruder', {}).get('temperature', 0.0)
            extruder_target = status.get('extruder', {}).get('target', 0.0)
            
            # Other stats
            speed_factor = int(status.get('gcode_move', {}).get('speed_factor', 100) * 100)
            fan_speed = int(status.get('fan', {}).get('speed', 0) * 100)
            
            # Progress
            progress = status.get('display_status', {}).get('progress', 0.0) * 100
            if progress <= 0 and print_stats.get('filename'):
                # Fallback calculation
                progress = min(100, (print_duration / 3600) * 10)
            
            return PrinterStatus(
                state=state,
                filename=filename,
                progress=progress,
                print_duration=print_duration,
                bed_temp=bed_temp,
                bed_target=bed_target,
                extruder_temp=extruder_temp,
                extruder_target=extruder_target,
                speed_factor=speed_factor,
                fan_speed=fan_speed,
                last_update=time.time()
            )
            
        except Exception as e:
            print(f"Status parse error: {e}")
            return PrinterStatus(state=PrinterState.ERROR)
    
    def send_gcode(self, gcode: str) -> bool:
        """Send G-code command"""
        if not self.network_available or not self.connected:
            print(f"Demo: Sending G-code: {gcode}")
            return True
        
        try:
            response = self.session.post(
                f"{self.base_url}/printer/gcode/script",
                json={'script': gcode},
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            self.last_error = str(e)
            return False
    
    def set_temperature(self, heater: str, temp: float) -> bool:
        """Set temperature for heater"""
        if heater == "bed":
            gcode = f"M140 S{temp}"
        elif heater == "extruder":
            gcode = f"M104 S{temp}"
        else:
            return False
        return self.send_gcode(gcode)
    
    def set_speed(self, speed: int) -> bool:
        """Set print speed percentage"""
        return self.send_gcode(f"M220 S{speed}")
    
    def _get_demo_status(self) -> PrinterStatus:
        """Generate demo status"""
        import random
        import math
        
        # Cycle through states
        current_time = time.time()
        cycle = int(current_time / 10) % 4
        
        states = [PrinterState.PRINTING, PrinterState.PAUSED, 
                  PrinterState.READY, PrinterState.STAND_BY]
        state = states[cycle]
        
        # Simulate temperature changes
        base_temp = 25 + math.sin(current_time / 10) * 5
        
        # Simulate progress for printing state
        if state == PrinterState.PRINTING:
            progress = (current_time % 100) / 100.0
            print_duration = current_time % 3600
        else:
            progress = 0.0
            print_duration = 0.0
        
        return PrinterStatus(
            state=state,
            filename="demo_print.gcode" if state == PrinterState.PRINTING else "",
            progress=progress * 100,
            print_duration=print_duration,
            bed_temp=60 + base_temp + random.uniform(-2, 2),
            bed_target=60.0,
            extruder_temp=210 + base_temp + random.uniform(-5, 5),
            extruder_target=210.0,
            speed_factor=100,
            fan_speed=50 if state == PrinterState.PRINTING else 0,
            last_update=current_time
        )