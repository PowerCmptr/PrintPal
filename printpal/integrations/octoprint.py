#!/usr/bin/env python3
"""
OctoPrint integration
"""

import time
import json
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class OctoPrintStatus:
    """OctoPrint status container"""
    state: str = "Offline"
    progress: float = 0.0
    filename: str = ""
    print_time: float = 0.0
    print_time_left: float = 0.0
    bed_temp: float = 0.0
    bed_target: float = 0.0
    tool_temp: float = 0.0
    tool_target: float = 0.0

class OctoPrintClient:
    """OctoPrint API client"""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 5000, 
                 api_key: str = ""):
        self.base_url = f"http://{host}:{port}"
        self.api_key = api_key
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
        """Connect to OctoPrint"""
        if not self.network_available:
            self.connected = True  # Demo mode
            return True
        
        try:
            self.session = self.requests.Session()
            self.session.headers.update({
                'X-Api-Key': self.api_key,
                'Content-Type': 'application/json'
            })
            
            response = self.session.get(f"{self.base_url}/api/version", timeout=5)
            self.connected = response.status_code == 200
            return self.connected
        except Exception as e:
            self.last_error = str(e)
            self.connected = False
            return False
    
    def disconnect(self):
        """Disconnect from OctoPrint"""
        if self.session:
            self.session.close()
            self.session = None
        self.connected = False
    
    def get_status(self) -> OctoPrintStatus:
        """Get printer status"""
        if not self.network_available or not self.connected:
            return self._get_demo_status()
        
        try:
            # Get connection status
            conn_response = self.session.get(f"{self.base_url}/api/connection", timeout=5)
            conn_data = conn_response.json()
            
            # Get job status
            job_response = self.session.get(f"{self.base_url}/api/job", timeout=5)
            job_data = job_response.json()
            
            # Get printer status
            printer_response = self.session.get(f"{self.base_url}/api/printer", timeout=5)
            printer_data = printer_response.json()
            
            return self._parse_status(conn_data, job_data, printer_data)
            
        except Exception as e:
            self.last_error = str(e)
            self.connected = False
            return OctoPrintStatus(state="Error")
    
    def _parse_status(self, conn_data: Dict, job_data: Dict, 
                     printer_data: Dict) -> OctoPrintStatus:
        """Parse OctoPrint response"""
        try:
            # Connection state
            conn_state = conn_data.get('current', {}).get('state', 'Closed')
            
            # Job info
            job = job_data.get('job', {})
            progress = job_data.get('progress', {})
            
            filename = job.get('file', {}).get('name', '')
            print_progress = progress.get('completion', 0.0)
            print_time = progress.get('printTime', 0.0)
            print_time_left = progress.get('printTimeLeft', 0.0)
            
            # Printer temperatures
            temp_data = printer_data.get('temperature', {})
            bed_temp = temp_data.get('bed', {}).get('actual', 0.0)
            bed_target = temp_data.get('bed', {}).get('target', 0.0)
            
            # Tool temperature (first tool)
            tool_temp = 0.0
            tool_target = 0.0
            for key in temp_data.keys():
                if key.startswith('tool'):
                    tool_temp = temp_data[key].get('actual', 0.0)
                    tool_target = temp_data[key].get('target', 0.0)
                    break
            
            return OctoPrintStatus(
                state=conn_state,
                progress=print_progress,
                filename=filename,
                print_time=print_time,
                print_time_left=print_time_left,
                bed_temp=bed_temp,
                bed_target=bed_target,
                tool_temp=tool_temp,
                tool_target=tool_target
            )
            
        except Exception as e:
            print(f"Status parse error: {e}")
            return OctoPrintStatus(state="Error")
    
    def _get_demo_status(self) -> OctoPrintStatus:
        """Generate demo status"""
        import random
        import math
        
        current_time = time.time()
        
        # Cycle states
        states = ["Printing", "Operational", "Paused", "Offline"]
        state = states[int(current_time / 10) % len(states)]
        
        # Simulate progress
        if state == "Printing":
            progress = (current_time % 600) / 600.0 * 100  # 10 minute cycle
            print_time = current_time % 600
            print_time_left = 600 - print_time
        else:
            progress = 0.0
            print_time = 0.0
            print_time_left = 0.0
        
        # Simulate temperatures
        base_temp = 25 + math.sin(current_time / 10) * 5
        
        return OctoPrintStatus(
            state=state,
            progress=progress,
            filename="demo.gcode" if state == "Printing" else "",
            print_time=print_time,
            print_time_left=print_time_left,
            bed_temp=60 + base_temp + random.uniform(-2, 2),
            bed_target=60.0,
            tool_temp=210 + base_temp + random.uniform(-5, 5),
            tool_target=210.0
        )
    
    def send_command(self, command: str, **kwargs) -> bool:
        """Send OctoPrint API command"""
        if not self.network_available or not self.connected:
            print(f"Demo: Sending command: {command}")
            return True
        
        try:
            url = f"{self.base_url}/api/{command}"
            if kwargs:
                response = self.session.post(url, json=kwargs, timeout=5)
            else:
                response = self.session.post(url, timeout=5)
            
            return response.status_code in [200, 204]
        except Exception as e:
            self.last_error = str(e)
            return False