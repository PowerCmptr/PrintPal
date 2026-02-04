#!/usr/bin/env python3
"""
Button components
"""

from typing import Optional, Tuple
from PIL import ImageDraw
from ..core.ui_component import UIComponent, UIRect

class UIButton(UIComponent):
    """Basic button component"""
    
    def __init__(self, rect: UIRect, text: str = "", **kwargs):
        super().__init__(rect, **kwargs)
        self.text = text
        self.background_color = kwargs.get('background_color', (60, 60, 60))
        self.hover_color = kwargs.get('hover_color', (80, 80, 80))
        self.active_color = kwargs.get('active_color', (100, 100, 100))
        self.text_color = kwargs.get('text_color', (255, 255, 255))
        self.corner_radius = kwargs.get('corner_radius', 8)
        self.is_hovered = False
        self.is_active = False
        self.icon = kwargs.get('icon')
        self.icon_color = kwargs.get('icon_color', self.text_color)
        
    def _render_self(self, draw: ImageDraw.ImageDraw, fonts: dict):
        """Render button"""
        from ..utils.helpers import draw_rounded_rectangle
        
        # Determine color
        if self.is_active:
            color = self.active_color
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.background_color
        
        # Draw button background
        draw_rounded_rectangle(
            draw,
            (self.rect.x, self.rect.y, 
             self.rect.right, self.rect.bottom),
            radius=self.corner_radius,
            fill=color
        )
        
        # Draw icon if present
        if self.icon:
            icon_size = min(self.rect.width, self.rect.height) - 20
            icon_x = self.rect.center[0] - icon_size // 2
            icon_y = self.rect.center[1] - icon_size // 2
            
            # Simple icon drawing (can be replaced with actual icon rendering)
            if self.icon == "home":
                draw.rectangle(
                    [icon_x + 5, icon_y + 5, 
                     icon_x + icon_size - 5, icon_y + icon_size - 5],
                    outline=self.icon_color,
                    width=2
                )
            elif self.icon == "settings":
                draw.ellipse(
                    [icon_x + 5, icon_y + 5,
                     icon_x + icon_size - 5, icon_y + icon_size - 5],
                    outline=self.icon_color,
                    width=2
                )
        
        # Draw text
        if self.text and not self.icon:
            font = fonts.get('body')
            if font:
                draw.text(
                    self.rect.center,
                    self.text,
                    font=font,
                    fill=self.text_color,
                    anchor='mm'
                )

class UIToggleButton(UIButton):
    """Toggle button with on/off state"""
    
    def __init__(self, rect: UIRect, text: str = "", **kwargs):
        super().__init__(rect, text, **kwargs)
        self.is_on = kwargs.get('is_on', False)
        self.on_color = kwargs.get('on_color', (0, 122, 255))
        self.off_color = kwargs.get('off_color', self.background_color)
        
    def _render_self(self, draw: ImageDraw.ImageDraw, fonts: dict):
        """Render toggle button"""
        from ..utils.helpers import draw_rounded_rectangle
        
        # Determine color based on state
        if self.is_on:
            color = self.on_color
        else:
            color = self.off_color
            
        if self.is_active:
            color = tuple(min(255, c + 30) for c in color)
        elif self.is_hovered:
            color = tuple(min(255, c + 20) for c in color)
        
        # Draw button
        draw_rounded_rectangle(
            draw,
            (self.rect.x, self.rect.y,
             self.rect.right, self.rect.bottom),
            radius=self.corner_radius,
            fill=color
        )
        
        # Draw text
        if self.text:
            font = fonts.get('body')
            if font:
                draw.text(
                    self.rect.center,
                    self.text,
                    font=font,
                    fill=self.text_color,
                    anchor='mm'
                )
    
    def toggle(self):
        """Toggle button state"""
        self.is_on = not self.is_on
        self.emit(UIEvent.VALUE_CHANGE, self.is_on)

class UIIconButton(UIButton):
    """Button with icon only"""
    
    def __init__(self, rect: UIRect, icon: str, **kwargs):
        super().__init__(rect, "", **kwargs)
        self.icon = icon
        self.icon_size = kwargs.get('icon_size', 
                                   min(rect.width, rect.height) - 20)
    
    def _render_self(self, draw: ImageDraw.ImageDraw, fonts: dict):
        """Render icon button"""
        from ..utils.helpers import draw_rounded_rectangle
        
        # Determine color
        if self.is_active:
            color = self.active_color
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.background_color
        
        # Draw button background
        draw_rounded_rectangle(
            draw,
            (self.rect.x, self.rect.y,
             self.rect.right, self.rect.bottom),
            radius=self.corner_radius,
            fill=color
        )
        
        # Draw icon (simplified - can be extended)
        icon_x = self.rect.center[0] - self.icon_size // 2
        icon_y = self.rect.center[1] - self.icon_size // 2
        
        if self.icon == "play":
            # Triangle for play
            points = [
                (icon_x + 5, icon_y + 5),
                (icon_x + self.icon_size - 5, icon_y + self.icon_size // 2),
                (icon_x + 5, icon_y + self.icon_size - 5)
            ]
            draw.polygon(points, fill=self.icon_color)
        
        elif self.icon == "pause":
            # Two rectangles for pause
            bar_width = 4
            gap = 3
            left_x = icon_x + (self.icon_size - (bar_width * 2 + gap)) // 2
            draw.rectangle(
                [left_x, icon_y + 5,
                 left_x + bar_width, icon_y + self.icon_size - 5],
                fill=self.icon_color
            )
            draw.rectangle(
                [left_x + bar_width + gap, icon_y + 5,
                 left_x + bar_width + gap + bar_width, icon_y + self.icon_size - 5],
                fill=self.icon_color
            )
        
        elif self.icon == "stop":
            # Square for stop
            draw.rectangle(
                [icon_x + 5, icon_y + 5,
                 icon_x + self.icon_size - 5, icon_y + self.icon_size - 5],
                fill=self.icon_color
            )