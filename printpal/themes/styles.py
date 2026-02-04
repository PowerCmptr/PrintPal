#!/usr/bin/env python3
"""
Style management system
"""

from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class ComponentStyle:
    """Style definition for a component"""
    background_color: tuple = None
    text_color: tuple = None
    border_color: tuple = None
    border_width: int = 0
    corner_radius: int = 0
    font_key: str = 'body'
    padding: int = 0
    margin: int = 0

class StyleManager:
    """Manages component styles"""
    
    def __init__(self):
        self.styles: Dict[str, ComponentStyle] = {}
        self._load_default_styles()
    
    def _load_default_styles(self):
        """Load default component styles"""
        # Button styles
        self.styles['button.primary'] = ComponentStyle(
            background_color=(47, 129, 247),
            text_color=(255, 255, 255),
            corner_radius=8,
            padding=10
        )
        
        self.styles['button.secondary'] = ComponentStyle(
            background_color=(60, 60, 60),
            text_color=(255, 255, 255),
            corner_radius=8,
            padding=10
        )
        
        self.styles['button.success'] = ComponentStyle(
            background_color=(46, 204, 113),
            text_color=(255, 255, 255),
            corner_radius=8,
            padding=10
        )
        
        # Card styles
        self.styles['card.default'] = ComponentStyle(
            background_color=(33, 38, 45),
            border_color=(48, 54, 61),
            border_width=1,
            corner_radius=12,
            padding=15
        )
        
        # Label styles
        self.styles['label.title'] = ComponentStyle(
            text_color=(240, 246, 252),
            font_key='h1'
        )
        
        self.styles['label.heading'] = ComponentStyle(
            text_color=(240, 246, 252),
            font_key='h2'
        )
        
        self.styles['label.body'] = ComponentStyle(
            text_color=(240, 246, 252),
            font_key='body'
        )
        
        self.styles['label.caption'] = ComponentStyle(
            text_color=(139, 148, 158),
            font_key='small'
        )
    
    def get_style(self, style_name: str) -> ComponentStyle:
        """Get style by name"""
        return self.styles.get(style_name, ComponentStyle())
    
    def apply_style(self, component, style_name: str):
        """Apply style to component"""
        style = self.get_style(style_name)
        
        if hasattr(component, 'background_color') and style.background_color:
            component.background_color = style.background_color
        
        if hasattr(component, 'text_color') and style.text_color:
            component.text_color = style.text_color
        
        if hasattr(component, 'border_color') and style.border_color:
            component.border_color = style.border_color
        
        if hasattr(component, 'border_width') and style.border_width:
            component.border_width = style.border_width
        
        if hasattr(component, 'corner_radius') and style.corner_radius:
            component.corner_radius = style.corner_radius
        
        if hasattr(component, 'font_key') and style.font_key:
            component.font_key = style.font_key
        
        if hasattr(component, 'padding') and style.padding:
            component.padding = style.padding