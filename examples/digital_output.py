#!/usr/bin/env python3
"""
Digital Output Example for NVIDIA Orin Nano

This example demonstrates:
- Setting up a pin for digital output
- Setting pin HIGH and LOW
- Blinking an LED
- Using the DigitalPin wrapper class

Hardware setup:
- Connect an LED with a resistor to pin 18 (or any other available GPIO pin)
- Connect the cathode (short leg) to ground
- Connect the anode (long leg) to the GPIO pin through a 330-ohm resistor

Pin reference for Orin Nano:
- Pin 18 (BOARD) = GPIO pin on 40-pin header
- See README.md for complete pinout
"""

import time
import sys
import os

# Add the src directory to the path to import our library
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from stickbot import DigitalPin, setup_gpio, cleanup_gpio

# Configuration
LED_PIN = 18  # BOARD pin 18
BLINK_DURATION = 0.5  # seconds


def basic_output_example():
    """Basic GPIO output using Jetson.GPIO directly"""
    print("=== Basic Output Example ===")
    
    try:
        import Jetson.GPIO as GPIO
    except ImportError:
        import RPi.GPIO as GPIO
    
    # Setup
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
    
    print(f"Setting pin {LED_PIN} HIGH for 2 seconds...")
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(2)
    
    print(f"Setting pin {LED_PIN} LOW for 2 seconds...")
    GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(2)
    
    print("Basic output example completed\n")


def wrapper_class_example():
    """Example using the DigitalPin wrapper class"""
    print("=== Wrapper Class Example ===")
    
    try:
        import Jetson.GPIO as GPIO
    except ImportError:
        import RPi.GPIO as GPIO
    
    # Create a digital output pin
    led = DigitalPin(LED_PIN, GPIO.OUT, GPIO.LOW)
    print(f"Created: {led}")
    
    # Set high
    print("Setting LED HIGH...")
    led.set_high()
    time.sleep(1)
    
    # Set low
    print("Setting LED LOW...")
    led.set_low()
    time.sleep(1)
    
    # Toggle several times
    print("Toggling LED 5 times...")
    for i in range(5):
        led.toggle()
        state = "ON" if led.get_value() == GPIO.HIGH else "OFF"
        print(f"  Toggle {i+1}: LED is {state}")
        time.sleep(0.5)
    
    # Ensure LED is off
    led.set_low()
    print("Wrapper class example completed\n")


def blinking_pattern_example():
    """More complex blinking patterns"""
    print("=== Blinking Patterns Example ===")
    
    try:
        import Jetson.GPIO as GPIO
    except ImportError:
        import RPi.GPIO as GPIO
    
    led = DigitalPin(LED_PIN, GPIO.OUT, GPIO.LOW)
    
    # Pattern 1: Fast blinks
    print("Pattern 1: Fast blinks (5 times)")
    for i in range(5):
        led.set_high()
        time.sleep(0.1)
        led.set_low()
        time.sleep(0.1)
    
    time.sleep(1)
    
    # Pattern 2: Slow blinks
    print("Pattern 2: Slow blinks (3 times)")
    for i in range(3):
        led.set_high()
        time.sleep(1.0)
        led.set_low()
        time.sleep(1.0)
    
    time.sleep(1)
    
    # Pattern 3: Morse code SOS
    print("Pattern 3: Morse code SOS")
    def short_blink():
        led.set_high()
        time.sleep(0.2)
        led.set_low()
        time.sleep(0.2)
    
    def long_blink():
        led.set_high()
        time.sleep(0.6)
        led.set_low()
        time.sleep(0.2)
    
    # S (3 short)
    for _ in range(3):
        short_blink()
    time.sleep(0.4)
    
    # O (3 long)
    for _ in range(3):
        long_blink()
    time.sleep(0.4)
    
    # S (3 short)
    for _ in range(3):
        short_blink()
    
    print("Blinking patterns example completed\n")


def multiple_pins_example():
    """Control multiple output pins"""
    print("=== Multiple Pins Example ===")
    
    try:
        import Jetson.GPIO as GPIO
    except ImportError:
        import RPi.GPIO as GPIO
    
    # Use multiple pins (make sure these are available on your board)
    pins = [18, 16, 15]  # Adjust based on your hardware setup
    leds = []
    
    # Create multiple LED objects
    for pin in pins:
        try:
            led = DigitalPin(pin, GPIO.OUT, GPIO.LOW)
            leds.append(led)
            print(f"Created LED on pin {pin}")
        except Exception as e:
            print(f"Could not setup pin {pin}: {e}")
    
    if not leds:
        print("No LEDs available for multiple pin example")
        return
    
    # Light up LEDs in sequence
    print("Lighting LEDs in sequence...")
    for i, led in enumerate(leds):
        print(f"  Lighting LED {i+1}")
        led.set_high()
        time.sleep(0.5)
    
    time.sleep(1)
    
    # Turn off LEDs in reverse order
    print("Turning off LEDs in reverse order...")
    for i, led in enumerate(reversed(leds)):
        print(f"  Turning off LED {len(leds)-i}")
        led.set_low()
        time.sleep(0.5)
    
    print("Multiple pins example completed\n")


def main():
    """Main function to run all examples"""
    print("Digital Output Examples for NVIDIA Orin Nano")
    print("=" * 50)
    
    # Setup GPIO
    setup_gpio()
    
    try:
        # Run examples
        basic_output_example()
        # wrapper_class_example()
        # blinking_pattern_example()
        # multiple_pins_example()
        
        print("All examples completed successfully!")
        
    except KeyboardInterrupt:
        print("\nExample interrupted by user")
    except Exception as e:
        print(f"Error running examples: {e}")
    finally:
        # Always cleanup GPIO
        cleanup_gpio()


if __name__ == "__main__":
    main()