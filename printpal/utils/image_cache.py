#!/usr/bin/env python3
"""
Image caching system for performance
"""

import os
import time
from typing import Dict, Optional
from PIL import Image

class ImageCache:
    """Cache for images to improve performance"""
    
    def __init__(self, max_size: int = 100):
        self.cache: Dict[str, dict] = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str) -> Optional[Image.Image]:
        """Get image from cache"""
        if key in self.cache:
            self.cache[key]['last_used'] = time.time()
            self.hits += 1
            return self.cache[key]['image']
        
        self.misses += 1
        return None
    
    def set(self, key: str, image: Image.Image):
        """Add image to cache"""
        # Remove oldest if cache is full
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.cache.keys(), 
                           key=lambda k: self.cache[k]['last_used'])
            del self.cache[oldest_key]
        
        self.cache[key] = {
            'image': image.copy(),
            'last_used': time.time(),
            'created': time.time()
        }
    
    def load_image(self, filepath: str) -> Optional[Image.Image]:
        """Load image with caching"""
        # Use absolute path as key
        abs_path = os.path.abspath(filepath)
        
        # Check cache first
        cached = self.get(abs_path)
        if cached:
            return cached
        
        # Load from disk
        try:
            image = Image.open(filepath)
            self.set(abs_path, image)
            return image
        except:
            return None
    
    def clear(self):
        """Clear cache"""
        self.cache.clear()
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': f"{hit_rate:.1f}%",
            'total_requests': total,
        }