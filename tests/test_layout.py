#!/usr/bin/env python3
"""
Test layout utilities
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from printpal.core.ui_component import UIRect
from printpal.utils.layout import (
    center_rect, distribute_horizontal, distribute_vertical,
    grid_layout, align_left, align_right
)

class TestLayout:
    """Test layout utilities"""
    
    def setup_method(self):
        """Setup test"""
        self.container = UIRect(0, 0, 400, 300)
    
    def test_center_rect(self):
        """Test center positioning"""
        centered = center_rect(self.container, 200, 100)
        assert centered.x == 100  # (400 - 200) / 2
        assert centered.y == 100  # (300 - 100) / 2
        assert centered.width == 200
        assert centered.height == 100
    
    def test_distribute_horizontal(self):
        """Test horizontal distribution"""
        rects = distribute_horizontal(self.container, [50, 100, 50], spacing=20)
        
        assert len(rects) == 3
        
        # Total width = 50 + 100 + 50 + 20*2 = 240
        # Start x = (400 - 240) / 2 = 80
        assert rects[0].x == 80
        assert rects[1].x == 80 + 50 + 20  # 150
        assert rects[2].x == 80 + 50 + 20 + 100 + 20  # 270
        
        assert rects[0].width == 50
        assert rects[1].width == 100
        assert rects[2].width == 50
    
    def test_distribute_vertical(self):
        """Test vertical distribution"""
        rects = distribute_vertical(self.container, [50, 100, 50], spacing=20)
        
        assert len(rects) == 3
        
        # Total height = 50 + 100 + 50 + 20*2 = 240
        # Start y = (300 - 240) / 2 = 30
        assert rects[0].y == 30
        assert rects[1].y == 30 + 50 + 20  # 100
        assert rects[2].y == 30 + 50 + 20 + 100 + 20  # 220
        
        assert rects[0].height == 50
        assert rects[1].height == 100
        assert rects[2].height == 50
    
    def test_grid_layout(self):
        """Test grid layout"""
        grid = grid_layout(self.container, rows=2, cols=3, spacing=10)
        
        assert len(grid) == 2  # 2 rows
        assert len(grid[0]) == 3  # 3 columns
        
        # Cell size calculation
        # width = (400 - 10*2) / 3 = 126.66 ≈ 126
        # height = (300 - 10*1) / 2 = 145
        assert grid[0][0].width == 126
        assert grid[0][0].height == 145
        
        # Check spacing
        assert grid[0][1].x == grid[0][0].x + 126 + 10
        assert grid[1][0].y == grid[0][0].y + 145 + 10
    
    def test_alignment(self):
        """Test alignment functions"""
        # Left alignment
        left = align_left(self.container, 100, 50, margin=20)
        assert left.x == 20
        assert left.y == (300 - 50) // 2  # Center vertically
        
        # Right alignment
        right = align_right(self.container, 100, 50, margin=20)
        assert right.x == 400 - 100 - 20  # 280
        assert right.y == (300 - 50) // 2  # Center vertically

if __name__ == "__main__":
    pytest.main([__file__, '-v'])