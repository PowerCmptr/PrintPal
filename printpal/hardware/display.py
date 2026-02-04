#!/usr/bin/env python3
"""
Display hardware abstraction
"""

import os
import numpy as np
from PIL import Image
from typing import Optional

class Display:
    """Abstract display interface"""
    
    def __init__(self, width: int = 320, height: int = 240):
        self.width = width
        self.height = height
        self.brightness = 1.0
        self.rotation = 0
        
    def init(self) -> bool:
        """Initialize display"""
        raise NotImplementedError("Subclasses must implement init()")
    
    def clear(self, color: tuple = (0, 0, 0)):
        """Clear display with color"""
        raise NotImplementedError("Subclasses must implement clear()")
    
    def show(self, image: Image.Image):
        """Display image"""
        raise NotImplementedError("Subclasses must implement show()")
    
    def set_brightness(self, brightness: float):
        """Set display brightness (0.0 to 1.0)"""
        self.brightness = max(0.0, min(1.0, brightness))
    
    def get_size(self) -> tuple:
        """Get display dimensions"""
        return (self.width, self.height)
    
    def close(self):
        """Cleanup display resources"""
        pass

class FrameBufferDisplay(Display):
    """Linux framebuffer display"""
    
    def __init__(self, width: int = 320, height: int = 240, 
                 device: str = '/dev/fb0'):
        super().__init__(width, height)
        self.device = device
        self.fb_fd = None
        self.stride = width * 4  # 32-bit BGRA
        
    def init(self) -> bool:
        """Open framebuffer device"""
        try:
            self.fb_fd = os.open(self.device, os.O_RDWR)
            return True
        except:
            print(f"Failed to open framebuffer: {self.device}")
            self.fb_fd = None
            return False
    
    def clear(self, color: tuple = (0, 0, 0)):
        """Clear framebuffer"""
        if not self.fb_fd:
            return
        
        # Create solid color image
        img = Image.new('RGB', (self.width, self.height), color)
        self.show(img)
    
    def show(self, image: Image.Image):
        """Write image to framebuffer"""
        if not self.fb_fd:
            return
        
        try:
            # Ensure correct size
            if image.size != (self.width, self.height):
                image = image.resize((self.width, self.height), Image.BILINEAR)
            
            # Apply brightness
            if self.brightness < 1.0:
                img_array = np.array(image)
                img_array = np.clip(img_array * self.brightness, 0, 255).astype(np.uint8)
                image = Image.fromarray(img_array)
            
            # Convert to BGRA for framebuffer
            img_array = np.array(image)
            
            if len(img_array.shape) == 2:  # Grayscale
                img_array = np.stack([img_array, img_array, img_array], axis=2)
            
            if img_array.shape[2] == 3:  # RGB
                bgra = np.zeros((self.height, self.width, 4), dtype=np.uint8)
                bgra[:, :, 0] = img_array[:, :, 2]  # Blue
                bgra[:, :, 1] = img_array[:, :, 1]  # Green
                bgra[:, :, 2] = img_array[:, :, 0]  # Red
                bgra[:, :, 3] = 255                  # Alpha
            else:  # RGBA
                bgra = np.zeros((self.height, self.width, 4), dtype=np.uint8)
                bgra[:, :, 0] = img_array[:, :, 2]  # Blue
                bgra[:, :, 1] = img_array[:, :, 1]  # Green
                bgra[:, :, 2] = img_array[:, :, 0]  # Red
                bgra[:, :, 3] = img_array[:, :, 3]  # Alpha
            
            # Write to framebuffer
            os.lseek(self.fb_fd, 0, os.SEEK_SET)
            os.write(self.fb_fd, bgra.tobytes())
            
        except Exception as e:
            print(f"Display error: {e}")
    
    def close(self):
        """Close framebuffer"""
        if self.fb_fd:
            os.close(self.fb_fd)
            self.fb_fd = None

class MockDisplay(Display):
    """Mock display for testing"""
    
    def __init__(self, width: int = 320, height: int = 240):
        super().__init__(width, height)
        self.current_image = None
        print(f"Mock Display: {width}x{height}")
    
    def init(self) -> bool:
        print("Mock Display initialized")
        return True
    
    def clear(self, color: tuple = (0, 0, 0)):
        print(f"Mock Display clear: {color}")
        self.current_image = Image.new('RGB', (self.width, self.height), color)
    
    def show(self, image: Image.Image):
        self.current_image = image.copy()
        print(f"Mock Display show: {image.size}")
    
    def save_current(self, filename: str = "display_output.png"):
        """Save current image to file (for testing)"""
        if self.current_image:
            self.current_image.save(filename)
            print(f"Saved to {filename}")