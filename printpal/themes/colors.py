#!/usr/bin/env python3
"""
Color themes for UI
"""

class ColorTheme:
    """Color themes for UI components"""
    
    # Dark theme (GitHub Dark inspired)
    DARK = {
        'primary': (13, 17, 23),
        'secondary': (22, 27, 34),
        'tertiary': (33, 38, 45),
        'quaternary': (48, 54, 61),
        
        'accent': (47, 129, 247),
        'accent_light': (88, 166, 255),
        'accent_dark': (29, 78, 216),
        
        'success': (46, 204, 113),
        'warning': (241, 196, 15),
        'error': (231, 76, 60),
        'info': (52, 152, 219),
        
        'text_primary': (240, 246, 252),
        'text_secondary': (139, 148, 158),
        'text_disabled': (87, 96, 106),
        
        'border': (48, 54, 61),
        'border_light': (33, 38, 45),
        
        # Printer-specific
        'bed_color': (52, 152, 219),      # Light blue
        'nozzle_color': (230, 126, 34),   # Orange
        'fan_color': (155, 89, 182),      # Purple
        'speed_color': (46, 204, 113),    # Green
    }
    
    # Light theme
    LIGHT = {
        'primary': (255, 255, 255),
        'secondary': (242, 242, 247),
        'tertiary': (229, 229, 234),
        'quaternary': (209, 209, 214),
        
        'accent': (0, 122, 255),
        'accent_light': (90, 200, 250),
        'accent_dark': (10, 132, 255),
        
        'success': (52, 199, 89),
        'warning': (255, 149, 0),
        'error': (255, 59, 48),
        'info': (0, 122, 255),
        
        'text_primary': (0, 0, 0),
        'text_secondary': (60, 60, 67),
        'text_disabled': (142, 142, 147),
        
        'border': (209, 209, 214),
        'border_light': (229, 229, 234),
        
        # Printer-specific
        'bed_color': (0, 122, 255),
        'nozzle_color': (255, 149, 0),
        'fan_color': (175, 82, 222),
        'speed_color': (52, 199, 89),
    }
    
    # High contrast theme
    HIGH_CONTRAST = {
        'primary': (0, 0, 0),
        'secondary': (20, 20, 20),
        'tertiary': (40, 40, 40),
        'quaternary': (60, 60, 60),
        
        'accent': (255, 255, 0),
        'accent_light': (255, 255, 100),
        'accent_dark': (200, 200, 0),
        
        'success': (0, 255, 0),
        'warning': (255, 255, 0),
        'error': (255, 0, 0),
        'info': (0, 255, 255),
        
        'text_primary': (255, 255, 255),
        'text_secondary': (200, 200, 200),
        'text_disabled': (128, 128, 128),
        
        'border': (255, 255, 255),
        'border_light': (200, 200, 200),
        
        # Printer-specific
        'bed_color': (0, 255, 255),
        'nozzle_color': (255, 165, 0),
        'fan_color': (255, 0, 255),
        'speed_color': (0, 255, 0),
    }
    
    @classmethod
    def get_theme(cls, theme_name: str = "dark"):
        """Get theme by name"""
        themes = {
            'dark': cls.DARK,
            'light': cls.LIGHT,
            'high_contrast': cls.HIGH_CONTRAST,
        }
        return themes.get(theme_name.lower(), cls.DARK)