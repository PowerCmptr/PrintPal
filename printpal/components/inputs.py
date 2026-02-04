#!/usr/bin/env python3
"""
Input components
"""

from typing import Optional
from PIL import ImageDraw
from ..core.ui_component import UIComponent, UIRect

class UISlider(UIComponent):
    """Slider input component"""
    
    def __init__(self, rect: UIRect, **kwargs):
        super().__init__(rect, **kwargs)
        self.value = kwargs.get('value', 0.5)  # 0.0 to 1.0
        self.min_value = kwargs.get('min_value', 0.0)
        self.max_value = kwargs.get('max_value', 1.0)
        self.step = kwargs.get('step', 0.01)
        self.track_color = kwargs.get('track_color', (60, 60, 60))
        self.fill_color = kwargs.get('fill_color', (0, 122, 255))
        self.thumb_color = kwargs.get('thumb_color', (255, 255, 255))
        self.thumb_radius = kwargs.get('thumb_radius', 10)
        self.show_value = kwargs.get('show_value', True)
        self.value_format = kwargs.get('value_format', '{:.0%}')
        
    def _render_self(self, draw: ImageDraw.ImageDraw, fonts: dict):
        """Render slider"""
        from ..utils.helpers import draw_rounded_rectangle
        
        # Normalize value
        normalized = max(0.0, min(1.0,
            (self.value - self.min_value) / (self.max_value - self.min_value)
        ))
        
        # Track dimensions
        track_height = 6
        track_y = self.rect.center[1] - track_height // 2
        
        # Draw track
        draw_rounded_rectangle(
            draw,
            (self.rect.x, track_y,
             self.rect.right, track_y + track_height),
            radius=track_height // 2,
            fill=self.track_color
        )
        
        # Draw fill
        if normalized > 0:
            fill_width = int(self.rect.width * normalized)
            if fill_width > 0:
                draw_rounded_rectangle(
                    draw,
                    (self.rect.x, track_y,
                     self.rect.x + fill_width, track_y + track_height),
                    radius=track_height // 2,
                    fill=self.fill_color
                )
        
        # Draw thumb
        thumb_x = self.rect.x + int(self.rect.width * normalized)
        draw.ellipse(
            [thumb_x - self.thumb_radius, self.rect.center[1] - self.thumb_radius,
             thumb_x + self.thumb_radius, self.rect.center[1] + self.thumb_radius],
            fill=self.thumb_color
        )
        
        # Draw value
        if self.show_value:
            font = fonts.get('small')
            if font:
                text = self.value_format.format(normalized)
                draw.text(
                    (self.rect.x, self.rect.y - 15),
                    text,
                    font=font,
                    fill=self.fill_color,
                    anchor='lb'
                )

class UITextInput(UIComponent):
    """Text input component"""
    
    def __init__(self, rect: UIRect, **kwargs):
        super().__init__(rect, **kwargs)
        self.text = kwargs.get('text', '')
        self.placeholder = kwargs.get('placeholder', '')
        self.font_key = kwargs.get('font_key', 'body')
        self.text_color = kwargs.get('text_color', (255, 255, 255))
        self.placeholder_color = kwargs.get('placeholder_color', (128, 128, 128))
        self.background_color = kwargs.get('background_color', (40, 40, 40))
        self.border_color = kwargs.get('border_color', (80, 80, 80))
        self.focused_border_color = kwargs.get('focused_border_color', (0, 122, 255))
        self.corner_radius = kwargs.get('corner_radius', 6)
        self.border_width = kwargs.get('border_width', 2)
        self.has_focus = False
        self.cursor_pos = len(self.text)
        self.cursor_blink = 0
        
    def _render_self(self, draw: ImageDraw.ImageDraw, fonts: dict):
        """Render text input"""
        from ..utils.helpers import draw_rounded_rectangle
        
        # Update cursor blink
        self.cursor_blink = (self.cursor_blink + 1) % 60
        
        # Determine border color
        border_color = (self.focused_border_color if self.has_focus 
                       else self.border_color)
        
        # Draw background
        draw_rounded_rectangle(
            draw,
            (self.rect.x, self.rect.y,
             self.rect.right, self.rect.bottom),
            radius=self.corner_radius,
            fill=self.background_color
        )
        
        # Draw border
        draw_rounded_rectangle(
            draw,
            (self.rect.x, self.rect.y,
             self.rect.right, self.rect.bottom),
            radius=self.corner_radius,
            outline=border_color,
            width=self.border_width
        )
        
        # Draw text
        font = fonts.get(self.font_key, fonts.get('body'))
        if font:
            display_text = self.text if self.text else self.placeholder
            text_color = self.text_color if self.text else self.placeholder_color
            
            # Calculate text position
            text_x = self.rect.x + 10
            text_y = self.rect.center[1]
            
            draw.text(
                (text_x, text_y),
                display_text,
                font=font,
                fill=text_color,
                anchor='lm'
            )
            
            # Draw cursor if focused
            if self.has_focus and self.cursor_blink < 30:
                # Calculate cursor position
                if self.cursor_pos > 0:
                    prefix = self.text[:self.cursor_pos]
                    prefix_width = draw.textlength(prefix, font=font)
                else:
                    prefix_width = 0
                
                cursor_x = text_x + prefix_width
                cursor_height = font.size // 2
                
                draw.line(
                    [(cursor_x, text_y - cursor_height),
                     (cursor_x, text_y + cursor_height)],
                    fill=self.text_color,
                    width=2
                )