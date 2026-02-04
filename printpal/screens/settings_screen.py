#!/usr/bin/env python3
"""
Settings screen
"""

from ..core.ui_screen import UIScreen
from ..core.ui_component import UIRect
from ..components.containers import UIContainer, UIList
from ..components.labels import UILabel
from ..components.buttons import UIButton, UIToggleButton
from ..components.inputs import UISlider
from ..themes.colors import ColorTheme

class SettingsScreen(UIScreen):
    """Settings and configuration screen"""
    
    def __init__(self, display_width: int, display_height: int):
        super().__init__("settings", display_width, display_height)
        
    def initialize(self):
        """Initialize settings screen"""
        # Header
        header = UIContainer(
            UIRect(0, 0, self.width, 50),
            background_color=ColorTheme.DARK['secondary']
        )
        
        title = UILabel(
            UIRect(0, 0, self.width, 50),
            "SETTINGS",
            font_key='h2',
            color=ColorTheme.DARK['text_primary'],
            align='center',
            valign='middle'
        )
        header.add_child(title)
        
        # Settings list
        settings_list = UIList(
            UIRect(20, 60, self.width - 40, self.height - 100),
            spacing=15,
            background_color=ColorTheme.DARK['primary']
        )
        
        # Display settings
        display_card = UIContainer(
            UIRect(0, 0, self.width - 40, 150),
            background_color=ColorTheme.DARK['tertiary'],
            corner_radius=12
        )
        
        display_title = UILabel(
            UIRect(10, 10, self.width - 60, 30),
            "Display Settings",
            font_key='h3',
            color=ColorTheme.DARK['text_primary']
        )
        
        brightness_label = UILabel(
            UIRect(10, 50, 100, 25),
            "Brightness",
            font_key='body',
            color=ColorTheme.DARK['text_secondary']
        )
        
        self.brightness_slider = UISlider(
            UIRect(120, 50, self.width - 180, 25),
            value=0.8,
            fill_color=ColorTheme.DARK['accent']
        )
        
        timeout_label = UILabel(
            UIRect(10, 90, 100, 25),
            "Dim Timeout",
            font_key='body',
            color=ColorTheme.DARK['text_secondary']
        )
        
        self.timeout_slider = UISlider(
            UIRect(120, 90, self.width - 180, 25),
            value=0.5,
            fill_color=ColorTheme.DARK['accent']
        )
        
        display_card.add_child(display_title)
        display_card.add_child(brightness_label)
        display_card.add_child(self.brightness_slider)
        display_card.add_child(timeout_label)
        display_card.add_child(self.timeout_slider)
        
        # Printer settings
        printer_card = UIContainer(
            UIRect(0, 0, self.width - 40, 120),
            background_color=ColorTheme.DARK['tertiary'],
            corner_radius=12
        )
        
        printer_title = UILabel(
            UIRect(10, 10, self.width - 60, 30),
            "Printer Settings",
            font_key='h3',
            color=ColorTheme.DARK['text_primary']
        )
        
        autoconnect_label = UILabel(
            UIRect(10, 50, 120, 25),
            "Auto-connect",
            font_key='body',
            color=ColorTheme.DARK['text_secondary']
        )
        
        self.autoconnect_toggle = UIToggleButton(
            UIRect(self.width - 100, 50, 50, 25),
            is_on=True,
            on_color=ColorTheme.DARK['success'],
            corner_radius=12
        )
        
        sound_label = UILabel(
            UIRect(10, 85, 120, 25),
            "Sound Effects",
            font_key='body',
            color=ColorTheme.DARK['text_secondary']
        )
        
        self.sound_toggle = UIToggleButton(
            UIRect(self.width - 100, 85, 50, 25),
            is_on=True,
            on_color=ColorTheme.DARK['success'],
            corner_radius=12
        )
        
        printer_card.add_child(printer_title)
        printer_card.add_child(autoconnect_label)
        printer_card.add_child(self.autoconnect_toggle)
        printer_card.add_child(sound_label)
        printer_card.add_child(self.sound_toggle)
        
        # Add cards to list
        settings_list.add_child(display_card)
        settings_list.add_child(printer_card)
        
        # Add to root
        self.root.add_child(header)
        self.root.add_child(settings_list)