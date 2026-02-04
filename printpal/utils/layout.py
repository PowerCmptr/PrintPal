#!/usr/bin/env python3
"""
Layout utilities for positioning components
"""

from typing import List, Tuple
from ..core.ui_component import UIRect

def center_rect(container: UIRect, width: int, height: int) -> UIRect:
    """Center a rectangle within a container"""
    x = container.x + (container.width - width) // 2
    y = container.y + (container.height - height) // 2
    return UIRect(x, y, width, height)

def distribute_horizontal(container: UIRect, widths: List[int], 
                         spacing: int = 10) -> List[UIRect]:
    """Distribute rectangles horizontally with equal spacing"""
    total_width = sum(widths) + spacing * (len(widths) - 1)
    start_x = container.x + (container.width - total_width) // 2
    
    rects = []
    current_x = start_x
    
    for width in widths:
        rects.append(UIRect(
            current_x,
            container.y + (container.height - max(widths)) // 2,
            width,
            container.height
        ))
        current_x += width + spacing
    
    return rects

def distribute_vertical(container: UIRect, heights: List[int],
                       spacing: int = 10) -> List[UIRect]:
    """Distribute rectangles vertically with equal spacing"""
    total_height = sum(heights) + spacing * (len(heights) - 1)
    start_y = container.y + (container.height - total_height) // 2
    
    rects = []
    current_y = start_y
    
    for height in heights:
        rects.append(UIRect(
            container.x + (container.width - max(heights)) // 2,
            current_y,
            container.width,
            height
        ))
        current_y += height + spacing
    
    return rects

def grid_layout(container: UIRect, rows: int, cols: int,
               spacing: int = 10) -> List[List[UIRect]]:
    """Create a grid of rectangles"""
    cell_width = (container.width - spacing * (cols - 1)) // cols
    cell_height = (container.height - spacing * (rows - 1)) // rows
    
    grid = []
    
    for row in range(rows):
        row_rects = []
        for col in range(cols):
            x = container.x + col * (cell_width + spacing)
            y = container.y + row * (cell_height + spacing)
            row_rects.append(UIRect(x, y, cell_width, cell_height))
        grid.append(row_rects)
    
    return grid

def align_left(container: UIRect, width: int, height: int, 
              margin: int = 10) -> UIRect:
    """Align rectangle to left of container"""
    return UIRect(
        container.x + margin,
        container.y + (container.height - height) // 2,
        width,
        height
    )

def align_right(container: UIRect, width: int, height: int,
               margin: int = 10) -> UIRect:
    """Align rectangle to right of container"""
    return UIRect(
        container.right - width - margin,
        container.y + (container.height - height) // 2,
        width,
        height
    )

def align_top(container: UIRect, width: int, height: int,
             margin: int = 10) -> UIRect:
    """Align rectangle to top of container"""
    return UIRect(
        container.x + (container.width - width) // 2,
        container.y + margin,
        width,
        height
    )

def align_bottom(container: UIRect, width: int, height: int,
                margin: int = 10) -> UIRect:
    """Align rectangle to bottom of container"""
    return UIRect(
        container.x + (container.width - width) // 2,
        container.bottom - height - margin,
        width,
        height
    )