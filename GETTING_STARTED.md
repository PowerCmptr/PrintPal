# 🤔 What Should I Do First?

## If You Just Want to Try It:

1. **Run the minimal example** (30 seconds):
   ```bash
   python examples/minimal_example.py
   ```

2. **Play with the dashboard** (2 minutes):
   ```bash
   python examples/basic_demo.py
   ```

3. **Run the full demo** (5 minutes):
   ```bash
   python main.py --demo
   ```

## If You Want to Build Something:

### Option A: Modify an Existing Screen (Easiest)

1. Copy `printpal/screens/temperature_screen.py`
2. Rename it to `my_screen.py`
3. Change the `initialize()` method
4. Run it with a simple test script

### Option B: Create a New Component

1. Copy `printpal/components/buttons.py`
2. Rename it to `my_component.py`
3. Change the class name and `_render_self()` method
4. Test it in a minimal example

### Option C: Connect to Real Hardware

1. **For Raspberry Pi with ILI9341**:
   ```bash
   # Install dependencies
   sudo apt-get install python3-rpi.gpio
   pip install RPi.GPIO
   
   # Run with hardware
   python main.py --display ili9341
   ```

2. **For Linux with framebuffer**:
   ```bash
   # Just run it
   python main.py --display fb
   ```
