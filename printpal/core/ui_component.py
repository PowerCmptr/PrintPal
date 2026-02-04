#!/usr/bin/env python3
"""
UI Component base class
"""

import time
from typing import Optional, List, Tuple, Dict, Any, Callable
from enum import Enum
from dataclasses import dataclass

class UIEvent(Enum):
    """UI Events that components can respond to"""
    CLICK = "click"
    LONG_PRESS = "long_press"
    ROTATE_CW = "rotate_cw"
    ROTATE_CCW = "rotate_ccw"
    FOCUS = "focus"
    BLUR = "blur"
    VALUE_CHANGE = "value_change"
    ANIMATION_FRAME = "animation_frame"

@dataclass
class UIRect:
    """Rectangle for layout and positioning"""
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    
    @property
    def right(self) -> int:
        return self.x + self.width
    
    @property
    def bottom(self) -> int:
        return self.y + self.height
    
    @property
    def center(self) -> Tuple[int, int]:
        return (self.x + self.width // 2, self.y + self.height // 2)
    
    def contains(self, x: int, y: int) -> bool:
        return (self.x <= x <= self.right and 
                self.y <= y <= self.bottom)
    
    def inflate(self, dx: int, dy: int) -> 'UIRect':
        return UIRect(
            self.x - dx,
            self.y - dy,
            self.width + dx * 2,
            self.height + dy * 2
        )

class UIComponent:
    """Base class for all UI components"""
    
    def __init__(self, rect: UIRect, **kwargs):
        self.rect = rect
        self.id = kwargs.get('id', f"component_{id(self)}")
        self.visible = kwargs.get('visible', True)
        self.enabled = kwargs.get('enabled', True)
        self.z_index = kwargs.get('z_index', 0)
        self.parent = None
        self.children: List['UIComponent'] = []
        self.event_handlers: Dict[UIEvent, List[Callable]] = {}
        self.styles = kwargs.get('styles', {})
        self.tags = kwargs.get('tags', [])
        
        # Animation
        self.animations = {}
        self.animation_progress = 0.0
        
    def add_child(self, child: 'UIComponent'):
        """Add a child component"""
        child.parent = self
        self.children.append(child)
        
    def remove_child(self, child: 'UIComponent'):
        """Remove a child component"""
        if child in self.children:
            child.parent = None
            self.children.remove(child)
    
    def on(self, event: UIEvent, handler: Callable):
        """Register event handler"""
        if event not in self.event_handlers:
            self.event_handlers[event] = []
        self.event_handlers[event].append(handler)
    
    def emit(self, event: UIEvent, *args, **kwargs):
        """Emit event to handlers"""
        if event in self.event_handlers:
            for handler in self.event_handlers[event]:
                try:
                    handler(*args, **kwargs)
                except Exception as e:
                    print(f"Error in event handler: {e}")
    
    def update(self, dt: float):
        """Update component state"""
        # Update animations
        if self.animations:
            self._update_animations(dt)
        
        # Update children
        for child in self.children:
            if child.visible:
                child.update(dt)
    
    def render(self, draw, fonts: Dict):
        """Render component and children"""
        if not self.visible:
            return
        
        # Render self
        self._render_self(draw, fonts)
        
        # Render children sorted by z-index
        for child in sorted(self.children, key=lambda c: c.z_index):
            if child.visible:
                child.render(draw, fonts)
    
    def _render_self(self, draw, fonts: Dict):
        """Override this in subclasses"""
        pass
    
    def _update_animations(self, dt: float):
        """Update active animations"""
        self.animation_progress = (self.animation_progress + dt) % 1.0
        
        # Update property animations
        current_time = time.time()
        to_remove = []
        
        for prop_name, anim in self.animations.items():
            elapsed = current_time - anim['start_time']
            progress = min(1.0, elapsed / anim['duration'])
            
            if progress >= 1.0:
                # Animation complete
                setattr(self, prop_name, anim['to'])
                to_remove.append(prop_name)
            else:
                # Interpolate value
                easing = anim['easing'](progress)
                from_val = anim['from']
                to_val = anim['to']
                
                if isinstance(from_val, (int, float)) and isinstance(to_val, (int, float)):
                    value = from_val + (to_val - from_val) * easing
                    setattr(self, prop_name, value)
                elif isinstance(from_val, tuple) and isinstance(to_val, tuple):
                    value = tuple(
                        f + (t - f) * easing 
                        for f, t in zip(from_val, to_val)
                    )
                    setattr(self, prop_name, value)
        
        # Remove completed animations
        for prop_name in to_remove:
            del self.animations[prop_name]
    
    def animate(self, property_name: str, to_value, 
                duration: float = 1.0, easing: Callable = None):
        """Animate a property"""
        from_value = getattr(self, property_name, None)
        if from_value is None:
            return
            
        self.animations[property_name] = {
            'from': from_value,
            'to': to_value,
            'duration': duration,
            'start_time': time.time(),
            'easing': easing or (lambda x: x)
        }
    
    def hit_test(self, x: int, y: int) -> Optional['UIComponent']:
        """Test if point hits this component"""
        if not self.visible or not self.enabled:
            return None
        
        if self.rect.contains(x, y):
            # Check children in reverse z-order (top to bottom)
            for child in reversed(sorted(self.children, key=lambda c: c.z_index)):
                result = child.hit_test(x, y)
                if result:
                    return result
            return self
        
        return None
    
    def find_by_id(self, component_id: str) -> Optional['UIComponent']:
        """Find component by ID in hierarchy"""
        if self.id == component_id:
            return self
        
        for child in self.children:
            result = child.find_by_id(component_id)
            if result:
                return result
        
        return None
    
    def find_by_tag(self, tag: str) -> List['UIComponent']:
        """Find components by tag"""
        results = []
        
        if tag in self.tags:
            results.append(self)
        
        for child in self.children:
            results.extend(child.find_by_tag(tag))
        
        return results

class UIContainer(UIComponent):
    """Container for organizing components"""
    
    def __init__(self, rect: UIRect, **kwargs):
        super().__init__(rect, **kwargs)
        self.background_color = kwargs.get('background_color')
        self.border_color = kwargs.get('border_color')
        self.border_width = kwargs.get('border_width', 0)
        self.corner_radius = kwargs.get('corner_radius', 0)
        self.padding = kwargs.get('padding', 0)
        
    def _render_self(self, draw, fonts: Dict):
        """Render container background and border"""
        from ..utils.helpers import draw_rounded_rectangle
        
        if self.background_color:
            draw_rounded_rectangle(
                draw,
                (self.rect.x, self.rect.y, 
                 self.rect.right, self.rect.bottom),
                radius=self.corner_radius,
                fill=self.background_color
            )
        
        if self.border_width > 0 and self.border_color:
            draw_rounded_rectangle(
                draw,
                (self.rect.x, self.rect.y, 
                 self.rect.right, self.rect.bottom),
                radius=self.corner_radius,
                outline=self.border_color,
                width=self.border_width
            )