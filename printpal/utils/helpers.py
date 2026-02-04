#!/usr/bin/env python3
"""
Helper functions for UI rendering
"""

def draw_rounded_rectangle(draw, xy, radius=0, fill=None, outline=None, width=1):
    """Draw a rounded rectangle"""
    x1, y1, x2, y2 = xy
    
    if radius > 0:
        # Draw corners
        draw.ellipse([x1, y1, x1 + radius*2, y1 + radius*2], 
                    fill=fill, outline=outline)
        draw.ellipse([x2 - radius*2, y1, x2, y1 + radius*2], 
                    fill=fill, outline=outline)
        draw.ellipse([x1, y2 - radius*2, x1 + radius*2, y2], 
                    fill=fill, outline=outline)
        draw.ellipse([x2 - radius*2, y2 - radius*2, x2, y2], 
                    fill=fill, outline=outline)
        
        # Draw sides
        draw.rectangle([x1 + radius, y1, x2 - radius, y1 + radius*2], 
                      fill=fill, outline=outline)
        draw.rectangle([x1, y1 + radius, x1 + radius*2, y2 - radius], 
                      fill=fill, outline=outline)
        draw.rectangle([x1 + radius, y2 - radius*2, x2 - radius, y2], 
                      fill=fill, outline=outline)
        draw.rectangle([x2 - radius*2, y1 + radius, x2, y2 - radius], 
                      fill=fill, outline=outline)
        
        # Fill center
        draw.rectangle([x1 + radius, y1 + radius, x2 - radius, y2 - radius], 
                      fill=fill, outline=None)
    else:
        draw.rectangle(xy, fill=fill, outline=outline, width=width)

def blend_colors(color1, color2, ratio):
    """Blend two colors"""
    r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
    g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
    b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
    
    # Handle alpha if present
    if len(color1) == 4 and len(color2) == 4:
        a = int(color1[3] * (1 - ratio) + color2[3] * ratio)
        return (r, g, b, a)
    
    return (r, g, b)

def darken_color(color, factor=0.7):
    """Darken a color"""
    r = int(color[0] * factor)
    g = int(color[1] * factor)
    b = int(color[2] * factor)
    
    if len(color) == 4:
        return (r, g, b, color[3])
    return (r, g, b)

def lighten_color(color, factor=1.3):
    """Lighten a color"""
    r = min(255, int(color[0] * factor))
    g = min(255, int(color[1] * factor))
    b = min(255, int(color[2] * factor))
    
    if len(color) == 4:
        return (r, g, b, color[3])
    return (r, g, b)

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 6:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    elif len(hex_color) == 8:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4, 6))
    return (0, 0, 0)