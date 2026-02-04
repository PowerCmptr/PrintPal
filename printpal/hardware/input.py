#!/usr/bin/env python3
"""
Input device handling
"""

import time
import threading
from typing import Optional, Callable
from ..core.events import UIEvent

class InputHandler:
    """Abstract input handler"""
    
    def __init__(self):
        self.on_click: Optional[Callable] = None
        self.on_long_press: Optional[Callable] = None
        self.on_rotate_cw: Optional[Callable] = None
        self.on_rotate_ccw: Optional[Callable] = None
        self.running = False
        self.poll_thread = None
    
    def start(self):
        """Start input polling"""
        self.running = True
        self.poll_thread = threading.Thread(target=self._poll_loop, daemon=True)
        self.poll_thread.start()
    
    def stop(self):
        """Stop input polling"""
        self.running = False
        if self.poll_thread:
            self.poll_thread.join(timeout=1.0)
    
    def _poll_loop(self):
        """Polling loop - implement in subclasses"""
        raise NotImplementedError("Subclasses must implement _poll_loop()")
    
    def emit_event(self, event: UIEvent, **kwargs):
        """Emit input event"""
        handlers = {
            UIEvent.CLICK: self.on_click,
            UIEvent.LONG_PRESS: self.on_long_press,
            UIEvent.ROTATE_CW: self.on_rotate_cw,
            UIEvent.ROTATE_CCW: self.on_rotate_ccw,
        }
        
        handler = handlers.get(event)
        if handler:
            try:
                handler(**kwargs)
            except Exception as e:
                print(f"Error in input handler: {e}")

class RotaryEncoderInput(InputHandler):
    """Rotary encoder with button input"""
    
    def __init__(self, clk_pin: int = 13, dt_pin: int = 26, 
                 sw_pin: int = 19, pull_up: bool = True):
        super().__init__()
        self.clk_pin = clk_pin
        self.dt_pin = dt_pin
        self.sw_pin = sw_pin
        self.pull_up = pull_up
        
        self.last_clk = 1
        self.last_sw = 1
        self.btn_press_time = 0
        self.long_press_fired = False
        
        # Debouncing
        self.rotation_debounce = 0
        self.click_debounce = 0
        
        # Try to import GPIO
        self.gpio_available = False
        try:
            import RPi.GPIO as GPIO
            self.GPIO = GPIO
            self.gpio_available = True
        except ImportError:
            print("RPi.GPIO not available - using mock input")
    
    def _poll_loop(self):
        """Poll rotary encoder"""
        if not self.gpio_available:
            self._mock_poll()
            return
        
        try:
            # Setup GPIO
            self.GPIO.setmode(self.GPIO.BCM)
            self.GPIO.setup(self.clk_pin, self.GPIO.IN, 
                           pull_up_down=self.GPIO.PUD_UP if self.pull_up else self.GPIO.PUD_DOWN)
            self.GPIO.setup(self.dt_pin, self.GPIO.IN,
                           pull_up_down=self.GPIO.PUD_UP if self.pull_up else self.GPIO.PUD_DOWN)
            self.GPIO.setup(self.sw_pin, self.GPIO.IN,
                           pull_up_down=self.GPIO.PUD_UP if self.pull_up else self.GPIO.PUD_DOWN)
            
            self.last_clk = self.GPIO.input(self.clk_pin)
            self.last_sw = self.GPIO.input(self.sw_pin)
            
            while self.running:
                self._poll_encoder()
                time.sleep(0.01)  # 100Hz polling
                
        except Exception as e:
            print(f"GPIO error: {e}")
            self._mock_poll()
    
    def _poll_encoder(self):
        """Poll encoder with debouncing"""
        current_time = time.time()
        
        # Rotation detection
        if current_time - self.rotation_debounce > 0.01:  # 100ms debounce
            clk = self.GPIO.input(self.clk_pin)
            if clk != self.last_clk:
                dt = self.GPIO.input(self.dt_pin)
                if dt != clk:
                    self.emit_event(UIEvent.ROTATE_CW)
                else:
                    self.emit_event(UIEvent.ROTATE_CCW)
                self.rotation_debounce = current_time
                self.last_clk = clk
        
        # Button detection
        if current_time - self.click_debounce > 0.05:  # 50ms debounce
            sw = self.GPIO.input(self.sw_pin)
            
            if sw == 0 and self.last_sw == 1:  # Button pressed
                self.btn_press_time = current_time
                self.long_press_fired = False
                
            elif sw == 1 and self.last_sw == 0:  # Button released
                press_duration = current_time - self.btn_press_time
                
                if not self.long_press_fired:
                    if press_duration < 0.5:  # Short click
                        self.emit_event(UIEvent.CLICK)
                        self.click_debounce = current_time
                    elif press_duration >= 1.0:  # Long press
                        self.emit_event(UIEvent.LONG_PRESS)
                        self.long_press_fired = True
            
            elif sw == 0:  # Button held
                press_duration = current_time - self.btn_press_time
                if press_duration >= 1.0 and not self.long_press_fired:
                    self.emit_event(UIEvent.LONG_PRESS)
                    self.long_press_fired = True
            
            self.last_sw = sw
    
    def _mock_poll(self):
        """Mock polling for development"""
        import random
        
        print("Using mock input (press Ctrl+C to exit)")
        
        event_sequence = [
            (UIEvent.ROTATE_CW, 2),
            (UIEvent.CLICK, 1),
            (UIEvent.ROTATE_CCW, 2),
            (UIEvent.LONG_PRESS, 3),
        ]
        
        event_index = 0
        
        while self.running:
            event, wait_time = event_sequence[event_index]
            
            time.sleep(wait_time)
            
            print(f"Mock event: {event}")
            self.emit_event(event)
            
            event_index = (event_index + 1) % len(event_sequence)

class KeyboardInput(InputHandler):
    """Keyboard input for development"""
    
    def __init__(self):
        super().__init__()
        print("Keyboard controls:")
        print("  Right Arrow / 'd': Rotate CW")
        print("  Left Arrow / 'a': Rotate CCW")
        print("  Space / Enter: Click")
        print("  'l': Long press")
        print("  'q': Quit")
    
    def _poll_loop(self):
        """Poll keyboard input"""
        try:
            import tty
            import sys
            import termios
            
            # Save terminal settings
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            
            try:
                tty.setraw(sys.stdin.fileno())
                
                while self.running:
                    ch = sys.stdin.read(1)
                    
                    if ch == 'q' or ch == '\x03':  # q or Ctrl+C
                        break
                    elif ch == '\x1b':  # Escape sequence
                        # Check for arrow keys
                        ch2 = sys.stdin.read(1)
                        if ch2 == '[':
                            ch3 = sys.stdin.read(1)
                            if ch3 == 'C':  # Right arrow
                                self.emit_event(UIEvent.ROTATE_CW)
                            elif ch3 == 'D':  # Left arrow
                                self.emit_event(UIEvent.ROTATE_CCW)
                    elif ch == 'd' or ch == 'D':
                        self.emit_event(UIEvent.ROTATE_CW)
                    elif ch == 'a' or ch == 'A':
                        self.emit_event(UIEvent.ROTATE_CCW)
                    elif ch == ' ' or ch == '\n' or ch == '\r':
                        self.emit_event(UIEvent.CLICK)
                    elif ch == 'l' or ch == 'L':
                        self.emit_event(UIEvent.LONG_PRESS)
                    
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                
        except ImportError:
            # Fallback for Windows or systems without tty
            import msvcrt  # Windows
            
            while self.running:
                if msvcrt.kbhit():
                    ch = msvcrt.getch().decode('utf-8', errors='ignore')
                    
                    if ch == 'q' or ch == '\x03':
                        break
                    elif ch == 'd' or ch == 'D':
                        self.emit_event(UIEvent.ROTATE_CW)
                    elif ch == 'a' or ch == 'A':
                        self.emit_event(UIEvent.ROTATE_CCW)
                    elif ch == ' ' or ch == '\r':
                        self.emit_event(UIEvent.CLICK)
                    elif ch == 'l' or ch == 'L':
                        self.emit_event(UIEvent.LONG_PRESS)
                
                time.sleep(0.1)