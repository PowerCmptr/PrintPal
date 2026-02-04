#!/usr/bin/env python3
"""
Container components for layout
"""

from typing import List
from ..core.ui_component import UIContainer, UIRect, UIComponent

class UIList(UIContainer):
    """Vertical list container"""
    
    def __init__(self, rect: UIRect, **kwargs):
        super().__init__(rect, **kwargs)
        self.spacing = kwargs.get('spacing', 10)
        self.scroll_offset = 0
        self.max_scroll = 0
        
    def add_child(self, child: UIComponent):
        """Add child with automatic positioning"""
        super().add_child(child)
        self._update_layout()
    
    def remove_child(self, child: UIComponent):
        """Remove child and update layout"""
        super().remove_child(child)
        self._update_layout()
    
    def _update_layout(self):
        """Update child positions"""
        current_y = self.scroll_offset
        for child in self.children:
            child.rect.y = self.rect.y + current_y
            child.rect.x = self.rect.x + self.padding
            child.rect.width = self.rect.width - self.padding * 2
            current_y += child.rect.height + self.spacing
        
        # Calculate max scroll
        total_height = current_y - self.scroll_offset
        self.max_scroll = max(0, total_height - self.rect.height)

class UIGrid(UIContainer):
    """Grid layout container"""
    
    def __init__(self, rect: UIRect, **kwargs):
        super().__init__(rect, **kwargs)
        self.columns = kwargs.get('columns', 2)
        self.row_height = kwargs.get('row_height', 50)
        self.spacing = kwargs.get('spacing', 10)
        self.items: List[UIComponent] = []
        
    def add_item(self, item: UIComponent):
        """Add item to grid"""
        self.items.append(item)
        self._update_layout()
    
    def _update_layout(self):
        """Update grid layout"""
        if not self.items:
            return
        
        col_width = (self.rect.width - self.padding * 2 - 
                    self.spacing * (self.columns - 1)) // self.columns
        
        for i, item in enumerate(self.items):
            row = i // self.columns
            col = i % self.columns
            
            item.rect.x = self.rect.x + self.padding + col * (col_width + self.spacing)
            item.rect.y = self.rect.y + self.padding + row * (self.row_height + self.spacing)
            item.rect.width = col_width
            item.rect.height = self.row_height