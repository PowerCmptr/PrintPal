# PrintPal UI Framework 🎨

*A modern, modular UI framework for the Anycubic Kobra 2 neo ISP display* 

## ⚠️ IMPORTANT: Kobra 2 Neo Specific

This software is specifically designed for the **Anycubic Kobra 2 Neo** with its 320x240 ILI9341 display. It uses the **custom LCD driver** from [Anycubic-Kobra-Go-Neo-LCD-Driver](https://github.com/jokubasver/Anycubic-Kobra-Go-Neo-LCD-Driver) which is a fork of [fbcp-ili9341](https://github.com/juj/fbcp-ili9341) with proper pin mappings for Kobra Neo series printers.

## Kobra 2 Neo LCD Driver Installation

### 1. Install the Custom LCD Driver
```bash
cd ~
git clone https://github.com/jokubasver/Anycubic-Kobra-Go-Neo-LCD-Driver.git
cd Anycubic-Kobra-Go-Neo-LCD-Driver
mkdir build
cd build
cmake -DILI9341=ON -DGPIO_TFT_DATA_CONTROL=25 -DGPIO_TFT_RESET_PIN=24 -DSPI_BUS_CLOCK_DIVISOR=30 ..
make -j4
sudo ./fbcp-ili9341 &
```

**Important**: This driver is specifically configured for Kobra Neo series pinouts:
- GPIO_TFT_DATA_CONTROL = 25 (RS/DC pin)
- GPIO_TFT_RESET_PIN = 24 (Reset pin)
- SPI_BUS_CLOCK_DIVISOR = 30 (optimized for Kobra display)

### 2. Make Driver Start Automatically
```bash
sudo nano /etc/rc.local
```
Add before `exit 0`:
```bash
/home/pi/Anycubic-Kobra-Go-Neo-LCD-Driver/build/fbcp-ili9341 &
```

## Wiring Diagram for Kobra 2 Neo

### Rotary Encoder (Optional but recommended for full functionality):
```
Encoder CLK → GPIO13 (Pin 33)
Encoder DT  → GPIO26 (Pin 37) 
Encoder SW  → GPIO19 (Pin 35)
Encoder +   → 3.3V (Pin 1)
Encoder GND → GND (Pin 6)
```

**Note**: Without rotary encoder, you can still use PrintPal but navigation will be limited. Temperature display and progress monitoring will work, but you won't be able to switch screens or adjust settings.

## 🚀 Quick Start (5 minutes)

```bash
# 1. Clone and install
git clone git.the-wired.eu/cyan/printpal-framework
cd printpal-framework
pip install Pillow numpy

# 2. Run demo (no hardware needed!)
python main.py --demo

# 3. Try the examples
python examples/basic_demo.py
```

## 🎯 What's This For?

PrintPal was only meant to help you build interfaces for **Anycubic Kobra 2 neo's SPI screen**, though I suppose you could use it for other screens if you modify the code. You are welcome to fork this project.

## ✨ Key Features

| Feature | Why It Matters |
|---------|----------------|
| **Component-based** | Build UIs like LEGO blocks |
| **Hardware-agnostic** | Works with framebuffer, SPI, I2C displays |
| **Rotary encoder support** | Perfect for knob-based navigation |
| **Pre-built screens** | Temperature, progress, settings ready to go |
| **Theming system** | Dark/light/high contrast themes |
| **60 FPS animations** | Smooth, hardware-accelerated rendering |

## 📁 Project Structure (Simplified)

```
printpal/
├── core/           # Base framework
├── components/     # UI widgets (buttons, labels, etc.)
├── screens/        # Pre-built screens
├── hardware/       # Display/input drivers
├── examples/       # Working examples
└── main.py         # Main application
```

## 🎮 Basic Example - 10 Lines of Code

```python
from printpal import UIManager
from printpal.screens import TemperatureScreen

# Create UI manager
ui = UIManager(320, 240)

# Create a temperature screen
temp_screen = TemperatureScreen(320, 240)
ui.register_screen(temp_screen)

# Update temperatures
temp_screen.update_temperatures(bed_temp=60.5, nozzle_temp=210.2)

# Start the UI
ui.start_animation_loop()
```

## 📚 Documentation

- **[Quick Start Guide](#-quick-start-guide)** ← Start here!
- [Component Reference](#-component-reference)
- [Building Custom Screens](#-building-custom-screens)
- [Hardware Setup](#-hardware-setup)
- [API Reference](#-api-reference)

## 🛠️ Hardware Support (Anycubic Kobra 2 neo)

| Display Type | Setup | Notes |
|-------------|-------|-------|
| **ILI9341 (SPI)** | `--display ili9341` | 320x240 common |
| **Framebuffer** | `--display fb` | Linux /dev/fb0 |
| **SSD1306 (I2C)** | `--display ssd1306` | 128x64 OLED |
| **Virtual** | `--demo` | No hardware needed |

| Input Type | Setup |
|------------|-------|
| **Rotary Encoder** | GPIO pins 13,26,19 |
| **Keyboard** | Arrow keys + Enter |
| **Touchscreen** | Coming soon |

## 🚧 Development Status

✅ **Stable**: Core framework, components, demos  
✅ **Ready**: Temperature, progress screens  
🔄 **In Progress**: More integrations, documentation  
📅 **Planned**: Plugin system, web interface

## 📄 License

MIT - Free for personal and commercial use.
```

## `QUICK_START.md` - Actually Useful Guide

```markdown
# 🚀 PrintPal Quick Start
## Get running in under 10 minutes

## Step 1: Installation (1 minute)

```bash
# Option A: From GitHub (recommended)
git clone https://git.the-wired.eu/cyan/printpal-framework.git
cd printpal-framework

# Option B: Just the essential files
curl -O https://git.the-wired.eu/cyan/printpal-framework/main/main.py
curl -O https://git.the-wired.eu/cyan/printpal-framework/main/minimal_example.py

# Install dependencies
pip install Pillow numpy
```

## Step 2: Run a Demo (30 seconds)

```bash
# Run the main demo (no hardware needed)
python main.py --demo

# Or run minimal example
python minimal_example.py
```

You should see a terminal interface with simulated rotary encoder input!

## Step 3: Understanding the Structure

### The 5 Core Files You Actually Need:

1. **`main.py`** - The complete application
2. **`printpal/core/ui_manager.py`** - Manages everything
3. **`printpal/core/ui_component.py`** - Base for all UI elements
4. **`printpal/components/buttons.py`** - Example component
5. **`printpal/screens/temperature_screen.py`** - Example screen

### The 3 Key Concepts:

1. **Components** = UI elements (buttons, labels, etc.)
2. **Screens** = Collections of components
3. **Manager** = Coordinates everything

## Step 4: Your First Custom UI (5 minutes)

Create `my_first_ui.py`:

```python
#!/usr/bin/env python3
"""My first PrintPal UI"""

import time
from printpal import UIManager
from printpal.core.ui_component import UIRect
from printpal.components.labels import UILabel
from printpal.components.buttons import UIButton
from printpal.themes.colors import ColorTheme

# 1. Initialize the UI
ui = UIManager(width=320, height=240)

# 2. Create a custom screen
from printpal.core.ui_screen import UIScreen
from printpal.components.containers import UIContainer

class MyScreen(UIScreen):
    def initialize(self):
        # Create a container
        container = UIContainer(
            UIRect(0, 0, self.width, self.height),
            background_color=ColorTheme.DARK['primary']
        )
        
        # Add a title
        title = UILabel(
            UIRect(0, 50, self.width, 40),
            text="MY FIRST UI!",
            font_key='h1',
            color=ColorTheme.DARK['accent'],
            align='center'
        )
        container.add_child(title)
        
        # Add a button
        button = UIButton(
            UIRect(100, 150, 120, 50),
            text="Click Me!",
            background_color=ColorTheme.DARK['accent'],
            corner_radius=8
        )
        
        def on_button_click():
            print("Button was clicked!")
            
        button.on('click', on_button_click)
        container.add_child(button)
        
        self.root.add_child(container)

# 3. Register and show the screen
my_screen = MyScreen("my_screen", 320, 240)
ui.register_screen(my_screen)
ui.switch_screen("my_screen")

# 4. Start the UI
print("Starting UI - press Ctrl+C to exit")
ui.start_animation_loop()

# Keep running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Goodbye!")
```

Run it:
```bash
python my_first_ui.py
```

## Step 5: Connect to Your Printer (2 minutes)

```python
from printpal.integrations.moonraker import MoonrakerClient

# Connect to Moonraker
printer = MoonrakerClient(host="192.168.1.100")  # Your printer IP
if printer.connect():
    print("Connected to printer!")
    
    # Get status
    status = printer.get_printer_status()
    print(f"Bed: {status.bed_temp:.1f}°C")
    print(f"Nozzle: {status.extruder_temp:.1f}°C")
    
    # Send command
    printer.send_gcode("G28")  # Home printer
```

## Step 6: Build a Temperature Monitor (3 minutes)

```python
#!/usr/bin/env python3
"""Simple temperature monitor"""

import time
from printpal import UIManager
from printpal.screens import TemperatureScreen
from printpal.integrations.moonraker import MoonrakerClient

# Setup
ui = UIManager(320, 240)
printer = MoonrakerClient()  # Default: localhost

# Create temperature screen
temp_screen = TemperatureScreen(320, 240)
ui.register_screen(temp_screen)
ui.switch_screen("temperature")

# Start UI
ui.start_animation_loop()

# Update loop
print("Monitoring printer temperatures...")
try:
    while True:
        # Get printer status
        status = printer.get_printer_status()
        
        # Update display
        temp_screen.update_temperatures(
            bed_temp=status.bed_temp,
            bed_target=status.bed_target,
            nozzle_temp=status.extruder_temp,
            nozzle_target=status.extruder_target
        )
        
        time.sleep(2)  # Update every 2 seconds
        
except KeyboardInterrupt:
    print("Monitor stopped")
```

## 🎯 Common Tasks - Cheat Sheet

### Create a Button
```python
button = UIButton(
    UIRect(x, y, width, height),
    text="My Button",
    background_color=(47, 129, 247),  # Blue
    corner_radius=8
)

def on_click():
    print("Clicked!")

button.on('click', on_click)
```

### Create a Progress Bar
```python
progress = UIProgressBar(
    UIRect(x, y, width, height),
    value=0.5,  # 50%
    fill_color=(0, 122, 255)
)
```

### Switch Between Screens
```python
ui.switch_screen("temperature")  # Go to temp screen
ui.switch_screen("progress")     # Go to progress screen
```

### Handle Rotary Encoder
```python
def on_rotate_cw():
    print("Rotated clockwise")
    
def on_rotate_ccw():
    print("Rotated counter-clockwise")

ui.input.on_rotate_cw = on_rotate_cw
ui.input.on_rotate_ccw = on_rotate_ccw
```

## 🚨 Troubleshooting

### Problem: "No module named 'printpal'"
**Solution:** Make sure you're in the project directory, or install it:
```bash
pip install -e .
```

### Problem: Display not working
**Solution:** Run in demo mode first:
```bash
python main.py --demo
```

### Problem: Can't import RPi.GPIO
**Solution:** You're not on a Raspberry Pi. Use demo mode or keyboard input:
```bash
python main.py --demo  # Simulated input
python main.py --input keyboard  # Use keyboard
```

## 📞 Getting Help

1. **Check the examples** in `examples/` directory
2. **Run the tests** to verify everything works:
   ```bash
   python -m pytest tests/ -v
   ```
3. **Look at pre-built screens** in `printpal/screens/`
4. **Examine component code** in `printpal/components/`

## 🎉 Next Steps

1. **Modify an existing screen** - Start with `temperature_screen.py`
2. **Create your own component** - Copy `buttons.py` as a template
3. **Connect to your hardware** - See `hardware/display.py`
4. **Build a complete app** - Use `main.py` as reference

---

**Remember:** The framework is modular. You don't need to understand everything at once. Start with the examples, then customize!

## 🎯 Common Questions

### Q: Do I need to understand all the code?
**A:** NO! Start with the examples, modify them, then explore.

### Q: How do I add a new screen?
**A:** Copy `temperature_screen.py`, rename it, change the UI.

### Q: Can I use this without a 3D printer?
**A:** YES! It's a general UI framework. Remove printer-specific code.

### Q: Is this ready for production?
**A:** For hobby projects: YES. For commercial: Probably, but test thoroughly.
