#!/usr/bin/env python3
"""
GPIO management utilities
"""

import time
from typing import Optional, Callable

class GPIOManager:
    """Manage GPIO pins and callbacks"""
    
    def __init__(self):
        self.callbacks = {}
        self.gpio_available = False
        
        try:
            import RPi.GPIO as GPIO
            self.GPIO = GPIO
            self.gpio_available = True
            self.GPIO.setmode(self.GPIO.BCM)
            self.GPIO.setwarnings(False)
        except ImportError:
            print("RPi.GPIO not available")
    
    def setup_input(self, pin: int, pull_up: bool = True, 
                   callback: Optional[Callable] = None,
                   edge: str = 'both'):
        """Setup GPIO pin as input"""
        if not self.gpio_available:
            return False
        
        try:
            pud = self.GPIO.PUD_UP if pull_up else self.GPIO.PUD_DOWN
            self.GPIO.setup(pin, self.GPIO.IN, pull_up_down=pud)
            
            if callback:
                edge_map = {
                    'rising': self.GPIO.RISING,
                    'falling': self.GPIO.FALLING,
                    'both': self.GPIO.BOTH
                }
                gpio_edge = edge_map.get(edge, self.GPIO.BOTH)
                self.GPIO.add_event_detect(pin, gpio_edge, 
                                          callback=callback, 
                                          bouncetime=50)
                self.callbacks[pin] = callback
            
            return True
        except Exception as e:
            print(f"Error setting up GPIO {pin}: {e}")
            return False
    
    def setup_output(self, pin: int, initial: bool = False):
        """Setup GPIO pin as output"""
        if not self.gpio_available:
            return False
        
        try:
            self.GPIO.setup(pin, self.GPIO.OUT)
            self.GPIO.output(pin, initial)
            return True
        except Exception as e:
            print(f"Error setting up GPIO output {pin}: {e}")
            return False
    
    def read(self, pin: int) -> Optional[bool]:
        """Read GPIO pin"""
        if not self.gpio_available:
            return None
        
        try:
            return bool(self.GPIO.input(pin))
        except:
            return None
    
    def write(self, pin: int, value: bool):
        """Write to GPIO pin"""
        if not self.gpio_available:
            return
        
        try:
            self.GPIO.output(pin, value)
        except Exception as e:
            print(f"Error writing to GPIO {pin}: {e}")
    
    def pwm(self, pin: int, frequency: float = 1000):
        """Create PWM on GPIO pin"""
        if not self.gpio_available:
            return None
        
        try:
            return self.GPIO.PWM(pin, frequency)
        except Exception as e:
            print(f"Error creating PWM on GPIO {pin}: {e}")
            return None
    
    def cleanup(self):
        """Cleanup GPIO resources"""
        if self.gpio_available:
            self.GPIO.cleanup()
            self.callbacks.clear()