#!/usr/bin/env python3
"""
Animation presets and easing functions
"""

import math
from typing import Callable

class AnimationPresets:
    """Animation easing functions"""
    
    @staticmethod
    def linear(t: float) -> float:
        """Linear easing: no acceleration"""
        return t
    
    @staticmethod
    def ease_in_quad(t: float) -> float:
        """Quadratic ease in"""
        return t * t
    
    @staticmethod
    def ease_out_quad(t: float) -> float:
        """Quadratic ease out"""
        return t * (2 - t)
    
    @staticmethod
    def ease_in_out_quad(t: float) -> float:
        """Quadratic ease in/out"""
        return 2 * t * t if t < 0.5 else -1 + (4 - 2 * t) * t
    
    @staticmethod
    def ease_in_cubic(t: float) -> float:
        """Cubic ease in"""
        return t * t * t
    
    @staticmethod
    def ease_out_cubic(t: float) -> float:
        """Cubic ease out"""
        t -= 1
        return t * t * t + 1
    
    @staticmethod
    def ease_in_out_cubic(t: float) -> float:
        """Cubic ease in/out"""
        if t < 0.5:
            return 4 * t * t * t
        else:
            t = 2 * t - 2
            return 0.5 * t * t * t + 1
    
    @staticmethod
    def ease_in_sine(t: float) -> float:
        """Sine ease in"""
        return 1 - math.cos(t * math.pi / 2)
    
    @staticmethod
    def ease_out_sine(t: float) -> float:
        """Sine ease out"""
        return math.sin(t * math.pi / 2)
    
    @staticmethod
    def ease_in_out_sine(t: float) -> float:
        """Sine ease in/out"""
        return -(math.cos(math.pi * t) - 1) / 2
    
    @staticmethod
    def ease_in_back(t: float) -> float:
        """Back ease in (overshoots)"""
        c1 = 1.70158
        c3 = c1 + 1
        return c3 * t * t * t - c1 * t * t
    
    @staticmethod
    def ease_out_back(t: float) -> float:
        """Back ease out (overshoots)"""
        c1 = 1.70158
        c3 = c1 + 1
        t -= 1
        return 1 + c3 * t * t * t + c1 * t * t
    
    @staticmethod
    def bounce_out(t: float) -> float:
        """Bounce ease out"""
        if t < 1 / 2.75:
            return 7.5625 * t * t
        elif t < 2 / 2.75:
            t -= 1.5 / 2.75
            return 7.5625 * t * t + 0.75
        elif t < 2.5 / 2.75:
            t -= 2.25 / 2.75
            return 7.5625 * t * t + 0.9375
        else:
            t -= 2.625 / 2.75
            return 7.5625 * t * t + 0.984375
    
    @staticmethod
    def elastic_out(t: float) -> float:
        """Elastic ease out"""
        if t == 0:
            return 0
        elif t == 1:
            return 1
        else:
            return math.pow(2, -10 * t) * math.sin((t * 10 - 0.75) * (2 * math.pi / 3)) + 1

class AnimationBuilder:
    """Build complex animations"""
    
    def __init__(self):
        self.keyframes = []
    
    def add_keyframe(self, time: float, properties: dict):
        """Add keyframe at specific time (0.0 to 1.0)"""
        self.keyframes.append((time, properties))
        # Sort by time
        self.keyframes.sort(key=lambda x: x[0])
    
    def get_animation(self, duration: float = 1.0) -> Callable[[float], dict]:
        """Get animation function"""
        def anim_func(progress: float) -> dict:
            # Find current and next keyframe
            current = None
            next = None
            
            for time, props in self.keyframes:
                if time <= progress:
                    current = (time, props)
                else:
                    next = (time, props)
                    break
            
            if not current:
                return {}
            if not next:
                return current[1]
            
            # Interpolate between keyframes
            t1, props1 = current
            t2, props2 = next
            
            # Normalize progress between keyframes
            local_progress = (progress - t1) / (t2 - t1)
            
            # Interpolate properties
            result = {}
            for key in set(props1.keys()) | set(props2.keys()):
                val1 = props1.get(key, 0)
                val2 = props2.get(key, 0)
                
                if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                    result[key] = val1 + (val2 - val1) * local_progress
                elif isinstance(val1, tuple) and isinstance(val2, tuple):
                    result[key] = tuple(
                        v1 + (v2 - v1) * local_progress 
                        for v1, v2 in zip(val1, val2)
                    )
            
            return result
        
        return anim_func