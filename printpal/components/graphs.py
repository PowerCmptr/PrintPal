#!/usr/bin/env python3
"""
Graph and chart components
"""

from typing import List, Optional, Tuple
from PIL import ImageDraw
from ..core.ui_component import UIComponent, UIRect

class UIGraph(UIComponent):
    """Graph component for visualizing data"""
    
    def __init__(self, rect: UIRect, **kwargs):
        super().__init__(rect, **kwargs)
        self.data: List[float] = kwargs.get('data', [])
        self.max_points = kwargs.get('max_points', 50)
        self.line_color = kwargs.get('line_color', (0, 122, 255))
        self.line_width = kwargs.get('line_width', 2)
        self.fill_color = kwargs.get('fill_color', (0, 122, 255, 64))
        self.show_grid = kwargs.get('show_grid', True)
        self.grid_color = kwargs.get('grid_color', (60, 60, 60, 128))
        self.show_axis = kwargs.get('show_axis', True)
        self.auto_scale = kwargs.get('auto_scale', True)
        self.min_y = kwargs.get('min_y', None)
        self.max_y = kwargs.get('max_y', None)
        
    def add_data_point(self, value: float):
        """Add a new data point"""
        self.data.append(value)
        if len(self.data) > self.max_points:
            self.data.pop(0)
    
    def clear_data(self):
        """Clear all data points"""
        self.data = []
    
    def _render_self(self, draw: ImageDraw.ImageDraw, fonts: dict):
        """Render graph"""
        if len(self.data) < 2:
            return
        
        # Calculate Y range
        if self.auto_scale:
            min_val = min(self.data)
            max_val = max(self.data)
            if min_val == max_val:
                max_val = min_val + 1
        else:
            min_val = self.min_y if self.min_y is not None else min(self.data)
            max_val = self.max_y if self.max_y is not None else max(self.data)
        
        # Draw grid
        if self.show_grid:
            grid_steps = 5
            step_y = self.rect.height // grid_steps
            for i in range(1, grid_steps):
                y = self.rect.y + i * step_y
                draw.line(
                    [(self.rect.x, y), (self.rect.right, y)],
                    fill=self.grid_color,
                    width=1
                )
        
        # Calculate points
        points = []
        for i, value in enumerate(self.data):
            x = self.rect.x + (i / (len(self.data) - 1)) * self.rect.width
            y = self.rect.bottom - ((value - min_val) / (max_val - min_val)) * self.rect.height
            points.append((x, y))
        
        # Draw filled area
        if self.fill_color and len(points) > 1:
            fill_points = points.copy()
            fill_points.append((points[-1][0], self.rect.bottom))
            fill_points.append((points[0][0], self.rect.bottom))
            draw.polygon(fill_points, fill=self.fill_color)
        
        # Draw line
        if len(points) > 1:
            draw.line(points, fill=self.line_color, width=self.line_width)
        
        # Draw axis
        if self.show_axis:
            # X axis
            draw.line(
                [(self.rect.x, self.rect.bottom),
                 (self.rect.right, self.rect.bottom)],
                fill=self.grid_color,
                width=1
            )
            # Y axis
            draw.line(
                [(self.rect.x, self.rect.y),
                 (self.rect.x, self.rect.bottom)],
                fill=self.grid_color,
                width=1
            )

class UISparkline(UIGraph):
    """Minimal sparkline graph"""
    
    def __init__(self, rect: UIRect, **kwargs):
        super().__init__(rect, **kwargs)
        self.line_color = kwargs.get('line_color', (0, 122, 255))
        self.fill_color = kwargs.get('fill_color', None)  # No fill by default
        self.show_grid = False
        self.show_axis = False