#!/usr/bin/env python3
"""
Test UI screens
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from printpal.screens.temperature_screen import TemperatureScreen
from printpal.screens.progress_screen import ProgressScreen
from printpal.screens.settings_screen import SettingsScreen

class TestUIScreens:
    """Test UI screens"""
    
    def setup_method(self):
        """Setup test"""
        self.width = 320
        self.height = 240
    
    def test_temperature_screen(self):
        """Test temperature screen"""
        screen = TemperatureScreen(self.width, self.height)
        assert screen.name == "temperature"
        assert screen.width == 320
        assert screen.height == 240
        
        # Test temperature update
        screen.update_temperatures(60.5, 60, 210.2, 210)
        assert screen.bed_temp == 60.5
        assert screen.bed_target == 60
        assert screen.nozzle_temp == 210.2
        assert screen.nozzle_target == 210
    
    def test_progress_screen(self):
        """Test progress screen"""
        screen = ProgressScreen(self.width, self.height)
        assert screen.name == "progress"
        
        # Test progress update
        screen.update_progress(
            progress=0.75,
            filename="test_print.gcode",
            state="PRINTING",
            elapsed="01:30:00",
            remaining="00:30:00"
        )
        
        assert screen.progress == 0.75
        assert screen.filename == "test_print.gcode"
        assert screen.state == "PRINTING"
        assert screen.print_time == "01:30:00"
        assert screen.remaining_time == "00:30:00"
    
    def test_settings_screen(self):
        """Test settings screen"""
        screen = SettingsScreen(self.width, self.height)
        assert screen.name == "settings"
        
        # Test initialization
        screen.initialize()
        assert screen.initialized == True
        assert hasattr(screen, 'brightness_slider')
        assert hasattr(screen, 'timeout_slider')
        assert hasattr(screen, 'autoconnect_toggle')
        assert hasattr(screen, 'sound_toggle')

if __name__ == "__main__":
    pytest.main([__file__, '-v'])