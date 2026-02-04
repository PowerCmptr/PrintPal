#!/usr/bin/env python3
"""
Print progress screen
"""

from ..core.ui_screen import UIScreen
from ..core.ui_component import UIRect
from ..components.containers import UIContainer
from ..components.labels import UILabel
from ..components.progress import UIProgressCircle, UIProgressBar
from ..components.buttons import UIButton
from ..themes.colors import ColorTheme

class ProgressScreen(UIScreen):
    """Screen for print progress monitoring"""
    
    def __init__(self, display_width: int, display_height: int):
        super().__init__("progress", display_width, display_height)
        self.progress = 0.0
        self.filename = ""
        self.print_time = "00:00:00"
        self.remaining_time = "00:00:00"
        self.state = "READY"
        
    def initialize(self):
        """Initialize progress screen"""
        # Header
        header = UIContainer(
            UIRect(0, 0, self.width, 50),
            background_color=ColorTheme.DARK['secondary']
        )
        
        title = UILabel(
            UIRect(0, 0, self.width, 50),
            "PRINT PROGRESS",
            font_key='h2',
            color=ColorTheme.DARK['text_primary'],
            align='center',
            valign='middle'
        )
        header.add_child(title)
        
        # Large progress circle
        self.progress_circle = UIProgressCircle(
            UIRect(self.width // 2 - 70, 60, 140, 140),
            value=0.0,
            thickness=10,
            fill_color=ColorTheme.DARK['accent'],
            show_text=True,
            text_format='{:.0%}'
        )
        
        # Filename label
        self.filename_label = UILabel(
            UIRect(20, 210, self.width - 40, 25),
            "No file selected",
            font_key='body',
            color=ColorTheme.DARK['text_primary'],
            align='center'
        )
        
        # Status label
        self.status_label = UILabel(
            UIRect(20, 235, self.width - 40, 25),
            "READY",
            font_key='h3',
            color=ColorTheme.DARK['success'],
            align='center'
        )
        
        # Time info
        time_container = UIContainer(
            UIRect(20, 260, self.width - 40, 60),
            background_color=ColorTheme.DARK['tertiary'],
            corner_radius=8
        )
        
        self.time_elapsed_label = UILabel(
            UIRect(10, 10, self.width - 60, 20),
            "Elapsed: 00:00:00",
            font_key='small',
            color=ColorTheme.DARK['text_secondary']
        )
        
        self.time_remaining_label = UILabel(
            UIRect(10, 30, self.width - 60, 20),
            "Remaining: 00:00:00",
            font_key='small',
            color=ColorTheme.DARK['text_secondary']
        )
        
        time_container.add_child(self.time_elapsed_label)
        time_container.add_child(self.time_remaining_label)
        
        # Control buttons (simplified)
        control_container = UIContainer(
            UIRect(20, 330, self.width - 40, 40),
            background_color=ColorTheme.DARK['primary']
        )
        
        # Add to root
        self.root.add_child(header)
        self.root.add_child(self.progress_circle)
        self.root.add_child(self.filename_label)
        self.root.add_child(self.status_label)
        self.root.add_child(time_container)
        self.root.add_child(control_container)
        
    def update_progress(self, progress: float, filename: str = None,
                       state: str = None, elapsed: str = None,
                       remaining: str = None):
        """Update progress display"""
        self.progress = max(0.0, min(1.0, progress))
        
        if filename:
            self.filename = filename
            # Truncate long filenames
            if len(filename) > 20:
                display_name = filename[:17] + "..."
            else:
                display_name = filename
            self.filename_label.text = display_name
        
        if state:
            self.state = state
            # Set color based on state
            state_colors = {
                'PRINTING': ColorTheme.DARK['success'],
                'PAUSED': ColorTheme.DARK['warning'],
                'ERROR': ColorTheme.DARK['error'],
                'READY': ColorTheme.DARK['text_primary'],
                'COMPLETE': ColorTheme.DARK['accent']
            }
            self.status_label.color = state_colors.get(state, ColorTheme.DARK['text_primary'])
            self.status_label.text = state
        
        if elapsed:
            self.print_time = elapsed
            self.time_elapsed_label.text = f"Elapsed: {elapsed}"
        
        if remaining:
            self.remaining_time = remaining
            self.time_remaining_label.text = f"Remaining: {remaining}"
        
        # Update progress circle
        if self.initialized:
            self.progress_circle.value = self.progress