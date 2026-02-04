#!/usr/bin/env python3
"""
PrintPal - Main Application
Modern UI for 3D Printer Displays
"""

import sys
import os
import time
import signal
import argparse
from typing import Optional

# Add current directory to path for development
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='PrintPal - 3D Printer UI')
    parser.add_argument('--demo', action='store_true', help='Demo mode without hardware')
    parser.add_argument('--test', action='store_true', help='Run tests')
    parser.add_argument('--config', type=str, default='config/default.yaml', help='Config file')
    parser.add_argument('--width', type=int, default=320, help='Display width')
    parser.add_argument('--height', type=int, default=240, help='Display height')
    parser.add_argument('--debug', action='store_true', help='Debug mode')
    
    args = parser.parse_args()
    
    if args.test:
        run_tests()
        return
    
    # Hide cursor
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()
    
    try:
        app = PrintPalApp(args)
        app.run()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Show cursor
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

def run_tests():
    """Run test suite"""
    import pytest
    exit_code = pytest.main(['tests/', '-v'])
    sys.exit(exit_code)

class PrintPalApp:
    """Main application class"""
    
    def __init__(self, args):
        self.args = args
        self.running = False
        
        # Import here to avoid circular imports
        from printpal.core.ui_manager import UIManager
        from printpal.hardware.display import FrameBufferDisplay, MockDisplay
        from printpal.hardware.input import RotaryEncoderInput, KeyboardInput
        from printpal.screens.temperature_screen import TemperatureScreen
        from printpal.screens.progress_screen import ProgressScreen
        from printpal.screens.settings_screen import SettingsScreen
        from printpal.screens.menu_screen import MenuScreen, MenuItem
        
        # Initialize display
        if args.demo:
            self.display = MockDisplay(args.width, args.height)
        else:
            self.display = FrameBufferDisplay(args.width, args.height)
        
        if not self.display.init():
            print("Display initialization failed")
            sys.exit(1)
        
        # Initialize UI manager
        self.ui = UIManager(args.width, args.height)
        
        # Setup display callback
        self.ui.set_display_callback(self.display.show)
        
        # Register screens
        temp_screen = TemperatureScreen(args.width, args.height)
        progress_screen = ProgressScreen(args.width, args.height)
        settings_screen = SettingsScreen(args.width, args.height)
        
        menu_screen = MenuScreen(args.width, args.height)
        menu_screen.set_menu_items([
            MenuItem("temperature", "Temperature", "thermometer", "temperature"),
            MenuItem("progress", "Print Progress", "progress", "progress"),
            MenuItem("settings", "Settings", "settings", "settings"),
            MenuItem("files", "File Browser", "folder"),
            MenuItem("control", "Manual Control", "joystick"),
            MenuItem("system", "System Info", "info"),
        ])
        
        self.ui.register_screen(temp_screen)
        self.ui.register_screen(progress_screen)
        self.ui.register_screen(settings_screen)
        self.ui.register_screen(menu_screen)
        
        # Start with temperature screen
        self.ui.switch_screen("temperature")
        
        # Initialize input
        if args.demo:
            self.input = KeyboardInput()
        else:
            self.input = RotaryEncoderInput()
        
        # Setup input callbacks
        self.input.on_click = self.on_click
        self.input.on_long_press = self.on_long_press
        self.input.on_rotate_cw = self.on_rotate_cw
        self.input.on_rotate_ccw = self.on_rotate_ccw
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)
        
        print("PrintPal initialized")
        print(f"Display: {args.width}x{args.height}")
        print(f"Mode: {'Demo' if args.demo else 'Production'}")
    
    def on_click(self):
        """Handle click event"""
        print("Click")
        self.ui.handle_input('click', x=160, y=120)  # Center of screen
    
    def on_long_press(self):
        """Handle long press event"""
        print("Long press")
        self.ui.handle_input('long_press', x=160, y=120)
    
    def on_rotate_cw(self):
        """Handle clockwise rotation"""
        print("Rotate CW")
        self.ui.handle_input('rotate_cw')
    
    def on_rotate_ccw(self):
        """Handle counter-clockwise rotation"""
        print("Rotate CCW")
        self.ui.handle_input('rotate_ccw')
    
    def run(self):
        """Main application loop"""
        print("\n" + "="*60)
        print("PRINTPAL")
        print("="*60)
        print("Controls:")
        print("  Rotate: Navigate")
        print("  Click: Select")
        print("  Long press (1s): Back/Special")
        print("="*60 + "\n")
        
        # Show startup screen
        self.show_startup()
        
        # Start input polling
        self.input.start()
        
        # Start UI animation loop
        self.ui.start_animation_loop(fps=30)
        
        # Main loop
        self.running = True
        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        
        self.shutdown()
    
    def show_startup(self):
        """Show startup screen"""
        from PIL import Image, ImageDraw
        from printpal.themes.colors import ColorTheme
        
        # Create startup image
        img = Image.new('RGB', (self.display.width, self.display.height), 
                       ColorTheme.DARK['primary'])
        draw = ImageDraw.Draw(img)
        
        # Draw logo/text
        draw.text(
            (self.display.width // 2, self.display.height // 2 - 20),
            "PRINTPAL",
            fill=ColorTheme.DARK['accent'],
            font=None,  # Would use actual font in real implementation
            anchor='mm'
        )
        
        draw.text(
            (self.display.width // 2, self.display.height // 2 + 20),
            "v0.1.0",
            fill=ColorTheme.DARK['text_secondary'],
            font=None,
            anchor='mm'
        )
        
        # Show image
        self.display.show(img)
        time.sleep(1.5)
    
    def shutdown(self, signum=None, frame=None):
        """Clean shutdown"""
        if not self.running:
            return
        
        print("\nShutting down...")
        self.running = False
        
        # Stop input
        self.input.stop()
        
        # Stop UI
        self.ui.stop_animation_loop()
        
        # Clear display
        self.display.clear()
        self.display.close()
        
        print("Goodbye!")

if __name__ == "__main__":
    main()