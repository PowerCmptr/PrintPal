#!/usr/bin/env python3
"""
MINIMAL PrintPal Example
Runs in 30 seconds, no hardware needed
"""

import time
from printpal import UIManager
from printpal.core.ui_screen import UIScreen
from printpal.core.ui_component import UIRect
from printpal.components.containers import UIContainer
from printpal.components.labels import UILabel
from printpal.components.buttons import UIButton
from printpal.themes.colors import ColorTheme

class SimpleScreen(UIScreen):
    def initialize(self):
        # Background
        bg = UIContainer(
            UIRect(0, 0, self.width, self.height),
            background_color=ColorTheme.DARK['primary']
        )
        
        # Title
        title = UILabel(
            UIRect(0, 50, self.width, 40),
            "IT WORKS! 🎉",
            font_key='h1',
            color=ColorTheme.DARK['accent'],
            align='center'
        )
        
        # Instructions
        info = UILabel(
            UIRect(0, 120, self.width, 60),
            "Use arrow keys:\n← → to simulate rotation\nENTER to click",
            font_key='body',
            color=ColorTheme.DARK['text_secondary'],
            align='center'
        )
        
        # Button
        self.button = UIButton(
            UIRect(100, 200, 120, 40),
            text="Click Me",
            background_color=ColorTheme.DARK['accent'],
            corner_radius=8
        )
        
        self.click_count = 0
        def on_click():
            self.click_count += 1
            print(f"Button clicked {self.click_count} times!")
        
        self.button.on('click', on_click)
        
        # Add everything
        bg.add_child(title)
        bg.add_child(info)
        bg.add_child(self.button)
        self.root.add_child(bg)

def main():
    """Run minimal example"""
    print("="*50)
    print("MINIMAL PRINTPAL EXAMPLE")
    print("="*50)
    print("This demo requires NO HARDWARE")
    print("Just keyboard input:")
    print("  A/D or ←/→ : Simulate rotary encoder")
    print("  ENTER/SPACE: Click button")
    print("  Q          : Quit")
    print("="*50)
    
    # Create UI
    ui = UIManager(320, 240)
    
    # Create and register screen
    screen = SimpleScreen("demo", 320, 240)
    ui.register_screen(screen)
    ui.switch_screen("demo")
    
    # Start everything
    ui.start_animation_loop()
    
    # Keep running
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nThanks for trying PrintPal! 👋")

if __name__ == "__main__":
    main()
