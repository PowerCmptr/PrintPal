#!/usr/bin/env python3
"""
UI Manager - coordinates screens, rendering, and events
"""

import time
import threading
from typing import Dict, Optional
from PIL import Image, ImageDraw
from .ui_screen import UIScreen
from .events import UIEvent
from ..utils.fonts import FontManager

class UIManager:
    """Manages UI state, screens, and rendering"""
    
    def __init__(self, display_width: int, display_height: int):
        self.width = display_width
        self.height = display_height
        self.screens: Dict[str, UIScreen] = {}
        self.current_screen: Optional[UIScreen] = None
        self.previous_screen: Optional[UIScreen] = None
        
        # Fonts
        self.font_manager = FontManager()
        self.fonts = self.font_manager.fonts
        
        # Event handling
        self.focused_component = None
        
        # Animation
        self.animation_thread = None
        self.animation_running = False
        self.last_update_time = time.time()
        self.fps = 30
        
        # Display callback
        self.display_callback = None
        
    def register_screen(self, screen: UIScreen):
        """Register a screen"""
        self.screens[screen.name] = screen
    
    def switch_screen(self, screen_name: str, transition: str = None):
        """Switch to a different screen"""
        if screen_name not in self.screens:
            print(f"Screen '{screen_name}' not found")
            return
        
        # Notify previous screen
        if self.current_screen:
            self.current_screen.on_exit()
            self.previous_screen = self.current_screen
        
        # Switch to new screen
        self.current_screen = self.screens[screen_name]
        self.current_screen.on_enter()
        
        # Handle transition if specified
        if transition:
            self._handle_transition(transition)
    
    def _handle_transition(self, transition: str):
        """Handle screen transition animation"""
        # Implement transition animations here
        print(f"Transition: {transition}")
    
    def render(self) -> Image.Image:
        """Render current screen to image"""
        if not self.current_screen:
            return self._create_blank_image()
        
        # Create image
        image = self._create_blank_image()
        draw = ImageDraw.Draw(image)
        
        # Render screen
        self.current_screen.render(draw, self.fonts)
        
        return image
    
    def _create_blank_image(self) -> Image.Image:
        """Create blank background image"""
        return Image.new('RGB', (self.width, self.height), (13, 17, 23))
    
    def update(self, dt: float = None):
        """Update UI state"""
        if dt is None:
            current_time = time.time()
            dt = current_time - self.last_update_time
            self.last_update_time = current_time
        
        if self.current_screen:
            self.current_screen.update(dt)
    
    def handle_input(self, event: UIEvent, x: int = None, y: int = None, **kwargs):
        """Handle input event"""
        if not self.current_screen:
            return
        
        # Handle focus changes
        if event in [UIEvent.CLICK, UIEvent.LONG_PRESS] and x is not None and y is not None:
            # Find component at position
            hit = self.current_screen.root.hit_test(x, y)
            
            # Update focus
            if hit != self.focused_component:
                if self.focused_component:
                    self.focused_component.emit(UIEvent.BLUR)
                self.focused_component = hit
                if self.focused_component:
                    self.focused_component.emit(UIEvent.FOCUS)
            
            # Send event to component
            if hit:
                hit.emit(event, **kwargs)
        
        # Also send event to screen
        self.current_screen.handle_event(event, **kwargs)
    
    def start_animation_loop(self, fps: int = 30):
        """Start animation update loop"""
        self.animation_running = True
        self.fps = fps
        
        def animation_loop():
            frame_time = 1.0 / fps
            while self.animation_running:
                start_time = time.time()
                self.update(frame_time)
                
                # Render and display if callback is set
                if self.display_callback:
                    image = self.render()
                    self.display_callback(image)
                
                elapsed = time.time() - start_time
                sleep_time = max(0, frame_time - elapsed)
                time.sleep(sleep_time)
        
        self.animation_thread = threading.Thread(target=animation_loop, daemon=True)
        self.animation_thread.start()
    
    def stop_animation_loop(self):
        """Stop animation update loop"""
        self.animation_running = False
        if self.animation_thread:
            self.animation_thread.join(timeout=1.0)
    
    def set_display_callback(self, callback):
        """Set callback for displaying rendered frames"""
        self.display_callback = callback