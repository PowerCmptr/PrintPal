#!/usr/bin/env python3
"""
Temperature monitoring screen
"""

import time
from ..core.ui_screen import UIScreen
from ..core.ui_component import UIRect
from ..components.containers import UIContainer, UIList
from ..components.labels import UILabel
from ..components.progress import UIProgressCircle
from ..components.graphs import UIGraph
from ..themes.colors import ColorTheme

class TemperatureScreen(UIScreen):
    """Screen for temperature monitoring"""
    
    def __init__(self, display_width: int, display_height: int):
        super().__init__("temperature", display_width, display_height)
        self.bed_temp = 0.0
        self.bed_target = 0.0
        self.nozzle_temp = 0.0
        self.nozzle_target = 0.0
        self.temp_history = []
        self.max_history = 30
        
    def initialize(self):
        """Initialize temperature screen"""
        # Header
        header = UIContainer(
            UIRect(0, 0, self.width, 50),
            background_color=ColorTheme.DARK['secondary']
        )
        
        title = UILabel(
            UIRect(0, 0, self.width, 50),
            "TEMPERATURES",
            font_key='h2',
            color=ColorTheme.DARK['text_primary'],
            align='center',
            valign='middle'
        )
        header.add_child(title)
        
        # Temperature cards container
        cards_container = UIContainer(
            UIRect(0, 60, self.width, 120),
            background_color=ColorTheme.DARK['primary']
        )
        
        # Bed temperature card
        bed_card = UIContainer(
            UIRect(20, 0, 130, 100),
            background_color=ColorTheme.DARK['tertiary'],
            corner_radius=12
        )
        
        bed_label = UILabel(
            UIRect(10, 15, 110, 25),
            "BED",
            font_key='body',
            color=ColorTheme.DARK['text_secondary']
        )
        
        self.bed_temp_label = UILabel(
            UIRect(10, 40, 110, 40),
            "0°C",
            font_key='h3',
            color=ColorTheme.DARK['text_primary'],
            align='center'
        )
        
        self.bed_target_label = UILabel(
            UIRect(10, 75, 110, 20),
            "Target: 0°C",
            font_key='small',
            color=ColorTheme.DARK['text_secondary'],
            align='center'
        )
        
        bed_card.add_child(bed_label)
        bed_card.add_child(self.bed_temp_label)
        bed_card.add_child(self.bed_target_label)
        
        # Nozzle temperature card
        nozzle_card = UIContainer(
            UIRect(170, 0, 130, 100),
            background_color=ColorTheme.DARK['tertiary'],
            corner_radius=12
        )
        
        nozzle_label = UILabel(
            UIRect(10, 15, 110, 25),
            "NOZZLE",
            font_key='body',
            color=ColorTheme.DARK['text_secondary']
        )
        
        self.nozzle_temp_label = UILabel(
            UIRect(10, 40, 110, 40),
            "0°C",
            font_key='h3',
            color=ColorTheme.DARK['text_primary'],
            align='center'
        )
        
        self.nozzle_target_label = UILabel(
            UIRect(10, 75, 110, 20),
            "Target: 0°C",
            font_key='small',
            color=ColorTheme.DARK['text_secondary'],
            align='center'
        )
        
        nozzle_card.add_child(nozzle_label)
        nozzle_card.add_child(self.nozzle_temp_label)
        nozzle_card.add_child(self.nozzle_target_label)
        
        cards_container.add_child(bed_card)
        cards_container.add_child(nozzle_card)
        
        # Temperature graph
        self.temp_graph = UIGraph(
            UIRect(20, 190, self.width - 40, 100),
            line_color=ColorTheme.DARK['bed_color'],
            fill_color=ColorTheme.DARK['bed_color'] + (64,),
            max_points=20
        )
        
        # Add all to root
        self.root.add_child(header)
        self.root.add_child(cards_container)
        self.root.add_child(self.temp_graph)
        
    def update_temperatures(self, bed_temp: float, bed_target: float,
                           nozzle_temp: float, nozzle_target: float):
        """Update temperature displays"""
        self.bed_temp = bed_temp
        self.bed_target = bed_target
        self.nozzle_temp = nozzle_temp
        self.nozzle_target = nozzle_target
        
        if self.initialized:
            # Update labels
            self.bed_temp_label.text = f"{bed_temp:.1f}°C"
            self.bed_target_label.text = f"Target: {bed_target:.0f}°C"
            self.nozzle_temp_label.text = f"{nozzle_temp:.1f}°C"
            self.nozzle_target_label.text = f"Target: {nozzle_target:.0f}°C"
            
            # Add to history for graph
            self.temp_history.append({
                'time': time.time(),
                'bed': bed_temp,
                'nozzle': nozzle_temp
            })
            
            # Keep history manageable
            if len(self.temp_history) > self.max_history:
                self.temp_history.pop(0)
            
            # Update graph with bed temperature
            if self.temp_history:
                self.temp_graph.add_data_point(bed_temp)