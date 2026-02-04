#!/usr/bin/env python3
"""
Font management utilities
"""

import os
from typing import Dict
from PIL import ImageFont

class FontManager:
    """Manages font loading and caching"""
    
    def __init__(self):
        self.fonts: Dict[str, ImageFont.FreeTypeFont] = {}
        self.font_dirs = [
            '/usr/share/fonts/truetype/inter/',
            '/usr/share/fonts/truetype/dejavu/',
            '/usr/share/fonts/TTF/',
            '/usr/share/fonts/truetype/liberation/',
            './assets/fonts/',
        ]
        self._load_fonts()
    
    def _load_fonts(self):
        """Load available fonts"""
        # Default font as fallback
        default_font = ImageFont.load_default()
        
        # Try to find and load preferred fonts
        font_variants = {
            'h1': self._find_font(28),
            'h2': self._find_font(24),
            'h3': self._find_font(20),
            'body': self._find_font(16),
            'small': self._find_font(13),
            'tiny': self._find_font(11),
        }
        
        # Apply found fonts or use default
        for key, font in font_variants.items():
            self.fonts[key] = font if font else default_font
    
    def _find_font(self, size: int) -> ImageFont.FreeTypeFont:
        """Find a font file and load it"""
        font_names = [
            'Inter-Bold.ttf',
            'Inter-Regular.ttf',
            'DejaVuSans-Bold.ttf',
            'DejaVuSans.ttf',
            'LiberationSans-Bold.ttf',
            'LiberationSans-Regular.ttf',
            'Arial Bold.ttf',
            'Arial.ttf',
        ]
        
        for font_dir in self.font_dirs:
            if os.path.exists(font_dir):
                for font_name in font_names:
                    font_path = os.path.join(font_dir, font_name)
                    if os.path.exists(font_path):
                        try:
                            return ImageFont.truetype(font_path, size)
                        except:
                            continue
        
        return None
    
    def get_font(self, key: str) -> ImageFont.FreeTypeFont:
        """Get font by key"""
        return self.fonts.get(key, self.fonts.get('body'))
    
    def set_font(self, key: str, font: ImageFont.FreeTypeFont):
        """Set custom font"""
        self.fonts[key] = font
    
    def add_font_file(self, key: str, font_path: str, size: int):
        """Add font from file"""
        try:
            font = ImageFont.truetype(font_path, size)
            self.fonts[key] = font
            return True
        except:
            return False