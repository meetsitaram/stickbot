# StickBot - NVIDIA Orin Nano GPIO Project

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive Python library and example collection for working with GPIO pins on the NVIDIA Orin Nano development board.

## 🚀 Features

- **Simple GPIO Control**: Easy-to-use wrapper classes for digital I/O
- **Hardware PWM Support**: Control PWM-capable pins with proper frequency and duty cycle control
- **Comprehensive Examples**: Ready-to-run examples for common GPIO operations
- **Pin Testing Tools**: Utilities to test and validate GPIO functionality
- **Cross-Compatible**: Works with both Jetson.GPIO and RPi.GPIO libraries

## 📋 Hardware Requirements

- NVIDIA Orin Nano development board
- Jumper wires and breadboard (for prototyping)
- LEDs, resistors, buttons, servos (for examples)

## 🔌 GPIO Pin Reference

The NVIDIA Orin Nano uses a 40-pin GPIO header compatible with Raspberry Pi pinout:

### PWM-Capable Pins (Hardware PWM)
- **Pin 15** (BOARD) - PWM capable (may need pinmux config)
- **Pin 33** (BOARD) - PWM capable (may need pinmux config)

### Digital I/O Pins (BOARD numbering)
`7, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 26, 29, 31, 32, 33, 35, 36, 37, 38, 40`

### Power Pins
- **Pins 1, 17**: 3.3V
- **Pins 2, 4**: 5V
- **Pins 6, 9, 14, 20, 25, 30, 34, 39**: Ground

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd stickbot
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the library in development mode:**
   ```bash
   pip install -e .
   ```

## 🛠️ Quick Start

### Digital Output (LED Control)

```python
from stickbot import DigitalPin, setup_gpio, cleanup_gpio
import Jetson.GPIO as GPIO
import time

# Setup
setup_gpio()

# Create LED on pin 18
led = DigitalPin(18, GPIO.OUT, GPIO.LOW)

# Blink LED
for i in range(10):
    led.set_high()
    time.sleep(0.5)
    led.set_low()  
    time.sleep(0.5)

# Cleanup
cleanup_gpio()
```

### Digital Input (Button Reading)

```python
from stickbot import DigitalPin
import Jetson.GPIO as GPIO

# Create button input with pull-up
button = DigitalPin(16, GPIO.IN)

# Read button state
while True:
    if button.read() == GPIO.LOW:  # Button pressed
        print("Button pressed!")
    time.sleep(0.1)
```

### PWM Control (Servo or LED Brightness)

```python
from stickbot import PWMPin

# Create PWM pin at 1kHz
pwm_pin = PWMPin(33, 1000)

# Start PWM at 50% duty cycle
pwm_pin.start(50)

# Change brightness/position
pwm_pin.change_duty_cycle(75)  # 75% duty cycle
pwm_pin.change_frequency(500)  # Change to 500Hz

# Stop PWM
pwm_pin.stop()
```

## 📚 Examples

Run the included examples to learn GPIO programming:

### 1. Digital Output Examples
```bash
python examples/digital_output.py
```
- Basic HIGH/LOW control
- LED blinking patterns
- Multiple pin control
- Morse code SOS pattern

### 2. Digital Input Examples
```bash
python examples/digital_input.py
```
- Button state reading
- Interrupt-driven input
- Button press counting
- Multiple pin monitoring

### 3. PWM Control Examples
```bash
python examples/pwm_control.py
```
- LED brightness control
- Servo motor positioning
- Frequency sweeping
- Multiple PWM pins

### 4. Pin Information and Testing
```bash
# Show board information
python examples/pin_info.py

# Test a specific pin
python examples/pin_info.py --test-pin 18

# Scan all available pins
python examples/pin_info.py --scan-pins

# Show detailed pinout
python examples/pin_info.py --pinout
```

## ⚙️ PWM Pin Configuration

Some PWM pins may require pinmux configuration to enable hardware PWM:

```bash
# Enable PWM on pin 15 (if needed)
sudo busybox devmem 0x02440020 32 0x400

# Enable PWM on pin 33 (if needed)
sudo busybox devmem 0x02434040 32 0x401
```

**Note**: These commands configure the hardware pinmux temporarily (until reboot). For permanent configuration, modify the device tree.

## 🧪 Testing

Run the test suite to verify functionality:

```bash
python -m pytest tests/
```

Or run specific tests:
```bash
python -m unittest tests.test_gpio
```

## 📁 Project Structure

```
stickbot/
├── src/stickbot/           # Main library code
│   ├── __init__.py        # Library exports
│   ├── gpio.py            # GPIO wrapper classes
│   └── utils.py           # Utility functions
├── examples/              # Example scripts
│   ├── digital_output.py  # Digital output examples
│   ├── digital_input.py   # Digital input examples
│   ├── pwm_control.py     # PWM examples
│   └── pin_info.py        # Pin testing utilities
├── tests/                 # Unit tests
├── requirements.txt       # Python dependencies
├── setup.py              # Package setup
└── README.md             # This file
```

## 🔧 Library API Reference

### DigitalPin Class

```python
DigitalPin(pin_number, direction, initial_value=None)
```

**Methods:**
- `set_high()` - Set output pin to HIGH
- `set_low()` - Set output pin to LOW  
- `toggle()` - Toggle pin state
- `read()` - Read current pin value
- `get_value()` - Get last known value
- `cleanup()` - Clean up pin resources

### PWMPin Class

```python
PWMPin(pin_number, frequency=1000)
```

**Methods:**
- `start(duty_cycle)` - Start PWM with duty cycle (0-100%)
- `stop()` - Stop PWM output
- `change_frequency(frequency)` - Change PWM frequency
- `change_duty_cycle(duty_cycle)` - Change duty cycle (0-100%)
- `is_started()` - Check if PWM is running
- `cleanup()` - Clean up PWM resources

### Utility Functions

- `setup_gpio()` - Initialize GPIO library
- `cleanup_gpio()` - Clean up all GPIO resources
- `get_available_pins()` - Get board-specific pin information
- `print_board_info()` - Display board information

## 🐛 Troubleshooting

### Common Issues

1. **Permission Denied**: Run with `sudo` or add user to `gpio` group
2. **PWM Not Working**: Check pinmux configuration commands above
3. **Pin Already in Use**: Call `cleanup_gpio()` or restart Python session
4. **Import Error**: Ensure `Jetson.GPIO` is installed: `pip install Jetson.GPIO`

### Pin Not Working Checklist

1. Verify pin number (use BOARD numbering)
2. Check if pin supports desired function (PWM, etc.)
3. Ensure proper wiring and connections
4. Test with pin_info.py utility
5. Check for conflicting pin usage

## 📖 Learning Resources

- [NVIDIA Jetson GPIO Library Documentation](https://github.com/NVIDIA/jetson-gpio)
- [Jetson Orin Nano Developer Kit User Guide](https://developer.nvidia.com/jetson-orin-nano-developer-kit)
- [GPIO Programming Best Practices](https://www.raspberrypi.org/documentation/usage/gpio/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- NVIDIA for the Jetson.GPIO library
- Raspberry Pi Foundation for GPIO interface standards
- The open-source community for GPIO programming resources

---

**Happy GPIO programming with your NVIDIA Orin Nano!** 🚀