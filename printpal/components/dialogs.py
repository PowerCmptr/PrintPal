#!/usr/bin/env python3
"""
Dialog and modal components
"""

from typing import List, Optional
from PIL import ImageDraw
from ..core.ui_component import UIContainer, UIRect, UIComponent
from .buttons import UIButton
from .labels import UILabel

class UIDialog(UIContainer):
    """Dialog box component"""
    
    def __init__(self, rect: UIRect, **kwargs):
        super().__init__(rect, **kwargs)
        self.title = kwargs.get('title', '')
        self.message = kwargs.get('message', '')
        self.buttons = kwargs.get('buttons', ['OK'])
        self.background_color = kwargs.get('background_color', (33, 38, 45, 240))
        self.corner_radius = kwargs.get('corner_radius', 12)
        self.on_button_click = kwargs.get('on_button_click')
        
        # Auto-initialize if components provided
        if self.title or self.message:
            self._initialize_dialog()
    
    def _initialize_dialog(self):
        """Initialize dialog components"""
        # Title
        if self.title:
            title_label = UILabel(
                UIRect(20, 20, self.rect.width - 40, 30),
                text=self.title,
                font_key='h2',
                color=(255, 255, 255),
                align='center'
            )
            self.add_child(title_label)
        
        # Message
        if self.message:
            message_label = UILabel(
                UIRect(20, 60, self.rect.width - 40, self.rect.height - 140),
                text=self.message,
                font_key='body',
                color=(200, 200, 200),
                align='center',
                valign='top'
            )
            self.add_child(message_label)
        
        # Buttons
        button_width = 80
        button_height = 40
        total_width = len(self.buttons) * button_width + (len(self.buttons) - 1) * 10
        start_x = (self.rect.width - total_width) // 2
        
        for i, button_text in enumerate(self.buttons):
            button = UIButton(
                UIRect(
                    start_x + i * (button_width + 10),
                    self.rect.height - 70,
                    button_width,
                    button_height
                ),
                text=button_text,
                background_color=(47, 129, 247),
                corner_radius=8
            )
            
            # Store button index for callback
            button_idx = i
            button.on('click', lambda idx=button_idx: self._on_button_click(idx))
            
            self.add_child(button)
    
    def _on_button_click(self, button_index: int):
        """Handle button click"""
        if self.on_button_click:
            self.on_button_click(button_index, self.buttons[button_index])

class UIModal(UIDialog):
    """Modal dialog that blocks interaction"""
    
    def __init__(self, rect: UIRect, **kwargs):
        super().__init__(rect, **kwargs)
        self.block_background = kwargs.get('block_background', True)
        self.background_opacity = kwargs.get('background_opacity', 180)
        
    def _render_self(self, draw: ImageDraw.ImageDraw, fonts: dict):
        """Render modal with background overlay"""
        # Draw semi-transparent overlay
        if self.block_background:
            overlay = Image.new('RGBA', 
                              (self.rect.width, self.rect.height),
                              (0, 0, 0, self.background_opacity))
            # Simplified overlay - in real implementation, would composite
            draw.rectangle(
                (self.rect.x, self.rect.y, 
                 self.rect.right, self.rect.bottom),
                fill=(0, 0, 0, self.background_opacity)
            )
        
        # Render dialog
        super()._render_self(draw, fonts)

class UIToast(UIComponent):
    """Toast notification component"""
    
    def __init__(self, rect: UIRect, **kwargs):
        super().__init__(rect, **kwargs)
        self.message = kwargs.get('message', '')
        self.duration = kwargs.get('duration', 3.0)  # seconds
        self.type = kwargs.get('type', 'info')  # info, success, warning, error
        self.created_time = time.time()
        
        # Type colors
        self.type_colors = {
            'info': (52, 152, 219),
            'success': (46, 204, 113),
            'warning': (241, 196, 15),
            'error': (231, 76, 60)
        }
        
    def _render_self(self, draw: ImageDraw.ImageDraw, fonts: dict):
        """Render toast"""
        from ..utils.helpers import draw_rounded_rectangle
        
        # Check if expired
        if time.time() - self.created_time > self.duration:
            self.visible = False
            return
        
        # Get color based on type
        bg_color = self.type_colors.get(self.type, self.type_colors['info'])
        
        # Draw toast background
        draw_rounded_rectangle(
            draw,
            (self.rect.x, self.rect.y,
             self.rect.right, self.rect.bottom),
            radius=8,
            fill=bg_color
        )
        
        # Draw message
        if self.message:
            font = fonts.get('body')
            if font:
                draw.text(
                    self.rect.center,
                    self.message,
                    font=font,
                    fill=(255, 255, 255),
                    anchor='mm'
                )