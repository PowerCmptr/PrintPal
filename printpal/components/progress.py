#!/usr/bin/env python3
"""
Progress indicator components
"""

import math
from typing import Dict
from PIL import ImageDraw
from ..core.ui_component import UIComponent, UIRect

class UIProgressBar(UIComponent):
    """Progress bar component"""
    
    def __init__(self, rect: UIRect, **kwargs):
        super().__init__(rect, **kwargs)
        self.value = kwargs.get('value', 0.0)  # 0.0 to 1.0
        self.min_value = kwargs.get('min_value', 0.0)
        self.max_value = kwargs.get('max_value', 1.0)
        self.background_color = kwargs.get('background_color', (40, 40, 40))
        self.fill_color = kwargs.get('fill_color', (0, 122, 255))
        self.corner_radius = kwargs.get('corner_radius', 4)
        self.show_text = kwargs.get('show_text', True)
        self.text_format = kwargs.get('text_format', '{:.1%}')
        self.text_color = kwargs.get('text_color', (255, 255, 255))
        
    def _render_self(self, draw: ImageDraw.ImageDraw, fonts: Dict):
        """Render progress bar"""
        from ..utils.helpers import draw_rounded_rectangle
        
        # Normalize value
        normalized = max(0.0, min(1.0, 
            (self.value - self.min_value) / (self.max_value - self.min_value)
        ))
        
        # Draw background
        draw_rounded_rectangle(
            draw,
            (self.rect.x, self.rect.y, 
             self.rect.right, self.rect.bottom),
            radius=self.corner_radius,
            fill=self.background_color
        )
        
        # Draw fill
        if normalized > 0:
            fill_width = int(self.rect.width * normalized)
            if fill_width > 0:
                # Handle rounded corners on fill
                if fill_width >= self.rect.width - self.corner_radius * 2:
                    # Fill is wide enough for full rounding
                    draw_rounded_rectangle(
                        draw,
                        (self.rect.x, self.rect.y, 
                         self.rect.x + fill_width, self.rect.bottom),
                        radius=self.corner_radius,
                        fill=self.fill_color
                    )
                else:
                    # Partial fill with square corners
                    draw.rectangle(
                        (self.rect.x, self.rect.y,
                         self.rect.x + fill_width, self.rect.bottom),
                        fill=self.fill_color
                    )
        
        # Draw text
        if self.show_text:
            font = fonts.get('small')
            if font:
                text = self.text_format.format(normalized)
                draw.text(
                    self.rect.center,
                    text,
                    font=font,
                    fill=self.text_color,
                    anchor='mm'
                )

class UIProgressCircle(UIComponent):
    """Circular progress indicator"""
    
    def __init__(self, rect: UIRect, **kwargs):
        super().__init__(rect, **kwargs)
        self.value = kwargs.get('value', 0.0)  # 0.0 to 1.0
        self.thickness = kwargs.get('thickness', 8)
        self.background_color = kwargs.get('background_color', (40, 40, 40))
        self.fill_color = kwargs.get('fill_color', (0, 122, 255))
        self.show_text = kwargs.get('show_text', True)
        self.text_format = kwargs.get('text_format', '{:.1%}')
        self.text_color = kwargs.get('text_color', (255, 255, 255))
        
    def _render_self(self, draw: ImageDraw.ImageDraw, fonts: Dict):
        """Render circular progress"""
        # Calculate circle parameters
        center = self.rect.center
        radius = min(self.rect.width, self.rect.height) // 2 - self.thickness
        
        # Draw background circle
        draw.ellipse(
            [center[0] - radius, center[1] - radius,
             center[0] + radius, center[1] + radius],
            outline=self.background_color,
            width=self.thickness
        )
        
        # Draw progress arc
        if self.value > 0:
            end_angle = 360 * self.value
            
            # Draw arc using pie slice method
            bbox = [
                center[0] - radius, center[1] - radius,
                center[0] + radius, center[1] + radius
            ]
            
            # PIL's arc doesn't support thickness, so we draw a thick arc manually
            # Simplified version: draw multiple lines
            steps = int(end_angle / 3)  # 3 degree steps
            for i in range(steps):
                angle1 = math.radians(i * 3 - 90)
                angle2 = math.radians((i + 1) * 3 - 90)
                
                x1 = center[0] + radius * math.cos(angle1)
                y1 = center[1] + radius * math.sin(angle1)
                x2 = center[0] + radius * math.cos(angle2)
                y2 = center[1] + radius * math.sin(angle2)
                
                draw.line([(x1, y1), (x2, y2)], 
                         fill=self.fill_color, 
                         width=self.thickness)
        
        # Draw text
        if self.show_text:
            font = fonts.get('body')
            if font:
                text = self.text_format.format(self.value)
                draw.text(
                    center,
                    text,
                    font=font,
                    fill=self.text_color,
                    anchor='mm'
                )