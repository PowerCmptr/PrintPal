#!/usr/bin/env python3
"""
Menu navigation screen
"""

from typing import List, Tuple
from ..core.ui_screen import UIScreen
from ..core.ui_component import UIRect
from ..components.containers import UIContainer, UIList
from ..components.labels import UILabel
from ..components.buttons import UIButton, UIIconButton
from ..themes.colors import ColorTheme

class MenuItem:
    """Menu item definition"""
    
    def __init__(self, id: str, label: str, icon: str = None, 
                 screen: str = None, action: callable = None):
        self.id = id
        self.label = label
        self.icon = icon
        self.screen = screen
        self.action = action

class MenuScreen(UIScreen):
    """Menu navigation screen"""
    
    def __init__(self, display_width: int, display_height: int):
        super().__init__("menu", display_width, display_height)
        self.menu_items: List[MenuItem] = []
        self.selected_index = 0
        
    def add_menu_item(self, item: MenuItem):
        """Add menu item"""
        self.menu_items.append(item)
        if self.initialized:
            self._update_menu()
    
    def set_menu_items(self, items: List[MenuItem]):
        """Set all menu items"""
        self.menu_items = items
        if self.initialized:
            self._update_menu()
    
    def initialize(self):
        """Initialize menu screen"""
        # Header
        header = UIContainer(
            UIRect(0, 0, self.width, 50),
            background_color=ColorTheme.DARK['secondary']
        )
        
        title = UILabel(
            UIRect(0, 0, self.width, 50),
            "MENU",
            font_key='h2',
            color=ColorTheme.DARK['text_primary'],
            align='center',
            valign='middle'
        )
        header.add_child(title)
        
        # Menu list container
        self.menu_list = UIList(
            UIRect(20, 60, self.width - 40, self.height - 120),
            spacing=10,
            background_color=ColorTheme.DARK['primary']
        )
        
        # Create menu buttons
        self._update_menu()
        
        # Back button
        back_button = UIButton(
            UIRect(self.width // 2 - 60, self.height - 50, 120, 40),
            text="BACK",
            background_color=ColorTheme.DARK['accent'],
            corner_radius=8
        )
        
        # Add to root
        self.root.add_child(header)
        self.root.add_child(self.menu_list)
        self.root.add_child(back_button)
        
    def _update_menu(self):
        """Update menu items display"""
        # Clear existing items
        self.menu_list.children.clear()
        
        # Create menu items
        for i, item in enumerate(self.menu_items):
            is_selected = (i == self.selected_index)
            
            item_bg = (ColorTheme.DARK['accent'] if is_selected 
                      else ColorTheme.DARK['tertiary'])
            
            item_container = UIContainer(
                UIRect(0, 0, self.width - 40, 60),
                background_color=item_bg,
                corner_radius=12
            )
            
            # Icon placeholder
            if item.icon:
                icon_x = 15
                icon_size = 30
                # Simple icon representation
                # In real implementation, would use actual icons
                icon_label = "●" if not item.icon else item.icon[0].upper()
                
                icon = UILabel(
                    UIRect(icon_x, 15, 30, 30),
                    icon_label,
                    font_key='h3',
                    color=ColorTheme.DARK['text_primary'],
                    align='center',
                    valign='middle'
                )
                item_container.add_child(icon)
            
            # Label
            label_x = 60 if item.icon else 20
            label = UILabel(
                UIRect(label_x, 20, self.width - label_x - 20, 40),
                item.label,
                font_key='body',
                color=ColorTheme.DARK['text_primary'],
                valign='middle'
            )
            item_container.add_child(label)
            
            # Selection indicator
            if is_selected:
                indicator = UILabel(
                    UIRect(self.width - 60, 20, 30, 40),
                    "▶",
                    font_key='body',
                    color=ColorTheme.DARK['text_primary'],
                    valign='middle'
                )
                item_container.add_child(indicator)
            
            self.menu_list.add_child(item_container)
    
    def select_next(self):
        """Select next menu item"""
        if self.menu_items:
            self.selected_index = (self.selected_index + 1) % len(self.menu_items)
            self._update_menu()
    
    def select_prev(self):
        """Select previous menu item"""
        if self.menu_items:
            self.selected_index = (self.selected_index - 1) % len(self.menu_items)
            self._update_menu()
    
    def get_selected_item(self) -> MenuItem:
        """Get currently selected menu item"""
        if self.menu_items and 0 <= self.selected_index < len(self.menu_items):
            return self.menu_items[self.selected_index]
        return None