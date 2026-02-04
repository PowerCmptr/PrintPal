#!/usr/bin/env python3
"""
Label components
"""

from typing import Dict
from PIL import ImageDraw
from ..core.ui_component import UIComponent, UIRect

class UILabel(UIComponent):
    """Text label component"""
    
    def __init__(self, rect: UIRect, text: str = "", **kwargs):
        super().__init__(rect, **kwargs)
        self.text = text
        self.font_key = kwargs.get('font_key', 'body')
        self.color = kwargs.get('color', (255, 255, 255))
        self.align = kwargs.get('align', 'left')
        self.valign = kwargs.get('valign', 'top')
        self.max_width = kwargs.get('max_width')
        self.truncate = kwargs.get('truncate', False)
        self.wrap = kwargs.get('wrap', False)
        
    def _render_self(self, draw: ImageDraw.ImageDraw, fonts: Dict):
        """Render text label"""
        if not self.text:
            return
        
        font = fonts.get(self.font_key, fonts.get('body'))
        if not font:
            return
        
        # Handle text wrapping/truncation
        text_to_render = self.text
        if self.max_width and self.truncate:
            # Truncate with ellipsis
            text_width = draw.textlength(self.text, font=font)
            if text_width > self.max_width:
                # Simple truncation
                chars_per_pixel = len(self.text) / text_width
                max_chars = int(self.max_width * chars_per_pixel) - 3
                if max_chars > 0:
                    text_to_render = self.text[:max_chars] + "..."
        
        # Calculate position based on alignment
        if self.align == 'center':
            anchor = 'mm' if self.valign == 'middle' else 'mt'
            x = self.rect.center[0]
        elif self.align == 'right':
            anchor = 'rm' if self.valign == 'middle' else 'rt'
            x = self.rect.right - 5
        else:  # left
            anchor = 'lm' if self.valign == 'middle' else 'lt'
            x = self.rect.x + 5
        
        if self.valign == 'middle':
            y = self.rect.center[1]
        elif self.valign == 'bottom':
            y = self.rect.bottom - 5
        else:  # top
            y = self.rect.y + 5
        
        draw.text((x, y), text_to_render, font=font, fill=self.color, anchor=anchor)