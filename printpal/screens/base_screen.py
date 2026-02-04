#!/usr/bin/env python3
"""
Base screen with common functionality
"""

from typing import Optional
from ..core.ui_screen import UIScreen
from ..core.ui_component import UIRect
from ..components.containers import UIContainer
from ..components.labels import UILabel
from ..themes.colors import ColorTheme

class BaseScreen(UIScreen):
    """Base screen with header and common elements"""
    
    def __init__(self, name: str, display_width: int, display_height: int):
        super().__init__(name, display_width, display_height)
        self.header_height = 50
        self.footer_height = 40
        self.content_rect = UIRect(
            0, self.header_height,
            display_width,
            display_height - self.header_height - self.footer_height
        )
        
    def initialize(self):
        """Initialize base screen elements"""
        # Create header
        self.header = UIContainer(
            UIRect(0, 0, self.width, self.header_height),
            background_color=ColorTheme.DARK['secondary']
        )
        
        self.title_label = UILabel(
            UIRect(0, 0, self.width, self.header_height),
            text=self.name.upper(),
            font_key='h2',
            color=ColorTheme.DARK['text_primary'],
            align='center',
            valign='middle'
        )
        self.header.add_child(self.title_label)
        
        # Create content area
        self.content = UIContainer(
            self.content_rect,
            background_color=ColorTheme.DARK['primary']
        )
        
        # Create footer
        self.footer = UIContainer(
            UIRect(0, self.height - self.footer_height, 
                  self.width, self.footer_height),
            background_color=ColorTheme.DARK['secondary']
        )
        
        # Add to root
        self.root.add_child(self.header)
        self.root.add_child(self.content)
        self.root.add_child(self.footer)
        
    def set_title(self, title: str):
        """Update screen title"""
        self.title_label.text = title.upper()
    
    def add_content(self, component):
        """Add component to content area"""
        self.content.add_child(component)