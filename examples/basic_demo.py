#!/usr/bin/env python3
"""
Basic PrintPal Demo
Shows multiple components working together
"""

import time
import random
from printpal import UIManager
from printpal.core.ui_screen import UIScreen
from printpal.core.ui_component import UIRect
from printpal.components.containers import UIContainer, UIList
from printpal.components.labels import UILabel
from printpal.components.buttons import UIButton
from printpal.components.progress import UIProgressBar
from printpal.components.graphs import UIGraph
from printpal.themes.colors import ColorTheme

class DashboardScreen(UIScreen):
    def __init__(self, name, width, height):
        super().__init__(name, width, height)
        self.cpu_usage = 50.0
        self.temperature = 25.0
        self.graph_data = []
        
    def initialize(self):
        # Create dashboard layout
        dashboard = UIContainer(
            UIRect(0, 0, self.width, self.height),
            background_color=ColorTheme.DARK['primary']
        )
        
        # Header
        header = UIContainer(
            UIRect(0, 0, self.width, 60),
            background_color=ColorTheme.DARK['secondary']
        )
        
        title = UILabel(
            UIRect(0, 0, self.width, 60),
            "DASHBOARD DEMO",
            font_key='h2',
            color=ColorTheme.DARK['accent'],
            align='center',
            valign='middle'
        )
        header.add_child(title)
        
        # Stats row
        stats = UIContainer(
            UIRect(20, 70, self.width - 40, 80),
            background_color=ColorTheme.DARK['tertiary'],
            corner_radius=12
        )
        
        # CPU Usage
        self.cpu_label = UILabel(
            UIRect(20, 15, 100, 30),
            "CPU: 50%",
            font_key='body',
            color=ColorTheme.DARK['text_primary']
        )
        
        self.cpu_progress = UIProgressBar(
            UIRect(20, 45, self.width - 80, 20),
            value=0.5,
            fill_color=ColorTheme.DARK['accent']
        )
        
        # Temperature
        self.temp_label = UILabel(
            UIRect(180, 15, 100, 30),
            "Temp: 25°C",
            font_key='body',
            color=ColorTheme.DARK['text_primary']
        )
        
        # Graph
        self.graph = UIGraph(
            UIRect(20, 160, self.width - 40, 100),
            line_color=ColorTheme.DARK['accent'],
            fill_color=ColorTheme.DARK['accent'] + (64,),
            max_points=20
        )
        
        # Buttons
        button_container = UIContainer(
            UIRect(20, 270, self.width - 40, 50),
            background_color=ColorTheme.DARK['primary']
        )
        
        refresh_btn = UIButton(
            UIRect(0, 0, 120, 40),
            text="Refresh Data",
            background_color=ColorTheme.DARK['accent'],
            corner_radius=8
        )
        
        def on_refresh():
            self.update_data()
            
        refresh_btn.on('click', on_refresh)
        
        # Build hierarchy
        stats.add_child(self.cpu_label)
        stats.add_child(self.cpu_progress)
        stats.add_child(self.temp_label)
        
        button_container.add_child(refresh_btn)
        
        dashboard.add_child(header)
        dashboard.add_child(stats)
        dashboard.add_child(self.graph)
        dashboard.add_child(button_container)
        
        self.root.add_child(dashboard)
        
    def update_data(self):
        """Update demo data"""
        # Simulate data changes
        self.cpu_usage = random.uniform(10, 90)
        self.temperature = random.uniform(20, 40)
        
        # Update components
        if hasattr(self, 'cpu_label'):
            self.cpu_label.text = f"CPU: {self.cpu_usage:.1f}%"
            self.cpu_progress.value = self.cpu_usage / 100.0
            self.temp_label.text = f"Temp: {self.temperature:.1f}°C"
            
            # Add to graph
            self.graph.add_data_point(self.cpu_usage)

def main():
    """Run dashboard demo"""
    print("="*50)
    print("BASIC DASHBOARD DEMO")
    print("="*50)
    
    # Create UI
    ui = UIManager(320, 240)
    
    # Create dashboard
    dashboard = DashboardScreen("dashboard", 320, 240)
    ui.register_screen(dashboard)
    ui.switch_screen("dashboard")
    
    # Start UI
    ui.start_animation_loop()
    
    # Auto-update data every 2 seconds
    print("Dashboard running - data updates every 2 seconds")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            dashboard.update_data()
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nDemo complete!")

if __name__ == "__main__":
    main()
