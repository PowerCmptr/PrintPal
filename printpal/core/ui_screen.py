#!/usr/bin/env python3
"""
UI Screen base class
"""

from typing import Optional, Dict
from PIL import Image, ImageDraw
from .ui_component import UIContainer, UIRect

class UIScreen:
    """Base class for application screens"""
    
    def __init__(self, name: str, display_width: int, display_height: int):
        self.name = name
        self.width = display_width
        self.height = display_height
        self.root = UIContainer(UIRect(0, 0, display_width, display_height))
        self.initialized = False
        self.is_active = False
        
    def initialize(self):
        """Initialize screen components - override in subclasses"""
        pass
    
    def update(self, dt: float):
        """Update screen state"""
        if not self.initialized:
            self.initialize()
            self.initialized = True
        
        self.root.update(dt)
    
    def render(self, draw: ImageDraw.ImageDraw, fonts: Dict) -> None:
        """Render screen to image"""
        self.root.render(draw, fonts)
    
    def handle_event(self, event, *args, **kwargs):
        """Handle UI events - override in subclasses"""
        pass
    
    def on_enter(self):
        """Called when screen becomes active"""
        self.is_active = True
        print(f"Entering screen: {self.name}")
    
    def on_exit(self):
        """Called when screen becomes inactive"""
        self.is_active = False
        print(f"Exiting screen: {self.name}")
    
    def find_component(self, component_id: str):
        """Find component by ID in screen"""
        return self.root.find_by_id(component_id)
    
    def find_components_by_tag(self, tag: str):
        """Find components by tag in screen"""
        return self.root.find_by_tag(tag)