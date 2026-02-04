#!/usr/bin/env python3
"""
UI Events system
"""

from enum import Enum

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
    SCREEN_ENTER = "screen_enter"
    SCREEN_EXIT = "screen_exit"
    KEY_PRESS = "key_press"
    KEY_RELEASE = "key_release"