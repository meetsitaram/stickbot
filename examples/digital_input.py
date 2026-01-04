#!/home/stick/solo_venv/bin/python3
"""
Digital Input Example for NVIDIA Orin Nano

This example demonstrates:
- Setting up a pin for digital input
- Reading pin states (HIGH/LOW)
- Monitoring pin changes
- Using interrupts to detect button presses

Hardware setup:
- Connect a button between pin 16 and ground
- The internal pull-up resistor will be used
- Connect an LED to pin 18 for output indication

Pin reference for Orin Nano:
- Pin 16 (BOARD) = GPIO pin for button input
- Pin 18 (BOARD) = GPIO pin for LED output  
- See README.md for complete pinout
"""

import time
import sys
import os

# Add the src directory to the path to import our library
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from stickbot import DigitalPin, setup_gpio, cleanup_gpio, read_pin_state

# Configuration
BUTTON_PIN = 16   # BOARD pin 16 for button input
LED_PIN = 18      # BOARD pin 18 for LED output


def basic_input_example():
    """Basic GPIO input reading"""
    print("=== Basic Input Example ===")
    
    try:
        import Jetson.GPIO as GPIO
    except ImportError:
        import RPi.GPIO as GPIO
    
    # Setup
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Pull-up for button
    
    print(f"Reading pin {BUTTON_PIN} state for 10 seconds...")
    print("Press and release the button to see state changes")
    print("(Button pressed = LOW, Button released = HIGH)")
    
    start_time = time.time()
    last_state = None
    
    while time.time() - start_time < 10:
        current_state = GPIO.input(BUTTON_PIN)
        
        if current_state != last_state:
            state_str = "LOW (PRESSED)" if current_state == GPIO.LOW else "HIGH (RELEASED)"
            print(f"Pin {BUTTON_PIN} changed to: {state_str}")
            last_state = current_state
        
        time.sleep(0.01)  # Small delay to avoid excessive CPU usage
    
    print("Basic input example completed\n")


def wrapper_class_input_example():
    """Example using DigitalPin wrapper for input"""
    print("=== Wrapper Class Input Example ===")
    
    try:
        import Jetson.GPIO as GPIO
    except ImportError:
        import RPi.GPIO as GPIO
    
    # Create input pin (button) and output pin (LED)
    button = DigitalPin(BUTTON_PIN, GPIO.IN)
    led = DigitalPin(LED_PIN, GPIO.OUT, GPIO.LOW)
    
    print(f"Button: {button}")
    print(f"LED: {led}")
    print("\nPress button to control LED for 15 seconds...")
    
    start_time = time.time()
    last_button_state = None
    
    while time.time() - start_time < 15:
        button_state = button.read()
        
        # Button is pressed when it reads LOW (due to pull-up)
        if button_state == GPIO.LOW and last_button_state != GPIO.LOW:
            print("Button PRESSED - LED ON")
            led.set_high()
        elif button_state == GPIO.HIGH and last_button_state != GPIO.HIGH:
            print("Button RELEASED - LED OFF")
            led.set_low()
        
        last_button_state = button_state
        time.sleep(0.01)
    
    # Ensure LED is off
    led.set_low()
    print("Wrapper class input example completed\n")


def button_counter_example():
    """Count button presses"""
    print("=== Button Counter Example ===")
    
    try:
        import Jetson.GPIO as GPIO
    except ImportError:
        import RPi.GPIO as GPIO
    
    button = DigitalPin(BUTTON_PIN, GPIO.IN)
    led = DigitalPin(LED_PIN, GPIO.OUT, GPIO.LOW)
    
    print("Counting button presses for 20 seconds...")
    print("Each press will blink the LED")
    
    press_count = 0
    last_state = GPIO.HIGH  # Start assuming button is not pressed
    start_time = time.time()
    
    while time.time() - start_time < 20:
        current_state = button.read()
        
        # Detect falling edge (button press)
        if last_state == GPIO.HIGH and current_state == GPIO.LOW:
            press_count += 1
            print(f"Button press #{press_count}")
            
            # Blink LED to indicate button press
            led.set_high()
            time.sleep(0.1)
            led.set_low()
            
            # Debounce delay
            time.sleep(0.1)
        
        last_state = current_state
        time.sleep(0.01)
    
    print(f"Total button presses: {press_count}")
    print("Button counter example completed\n")


def interrupt_example():
    """Example using GPIO interrupts (event detection)"""
    print("=== Interrupt Example ===")
    
    try:
        import Jetson.GPIO as GPIO
    except ImportError:
        import RPi.GPIO as GPIO
    
    # Global variables for interrupt callback
    press_count = [0]  # Use list to make it mutable in callback
    led = None
    
    def button_callback(channel):
        """Callback function for button press interrupt"""
        press_count[0] += 1
        print(f"Interrupt! Button press #{press_count[0]} on pin {channel}")
        if led:
            # Quick LED flash
            led.set_high()
            time.sleep(0.05)
            led.set_low()
    
    # Setup pins
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    led = DigitalPin(LED_PIN, GPIO.OUT, GPIO.LOW)
    
    # Setup interrupt on falling edge (button press)
    GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=200)
    
    print("Interrupt-based button detection active for 15 seconds...")
    print("Press the button multiple times")
    
    try:
        # Just wait while interrupts handle button presses
        time.sleep(15)
    except KeyboardInterrupt:
        print("Interrupted by user")
    
    # Remove event detection
    GPIO.remove_event_detect(BUTTON_PIN)
    led.set_low()
    
    print(f"Total interrupts detected: {press_count[0]}")
    print("Interrupt example completed\n")


def analog_like_reading_example():
    """Simulate analog-like reading by sampling rapidly"""
    print("=== Rapid Sampling Example ===")
    
    try:
        import Jetson.GPIO as GPIO
    except ImportError:
        import RPi.GPIO as GPIO
    
    button = DigitalPin(BUTTON_PIN, GPIO.IN)
    
    print("Taking 1000 rapid samples to show pin state distribution...")
    print("Hold button pressed or released during sampling")
    
    samples = []
    for i in range(1000):
        samples.append(button.read())
        time.sleep(0.001)  # 1ms between samples
    
    high_count = samples.count(GPIO.HIGH)
    low_count = samples.count(GPIO.LOW)
    
    print(f"Sample results:")
    print(f"  HIGH samples: {high_count} ({high_count/10:.1f}%)")
    print(f"  LOW samples: {low_count} ({low_count/10:.1f}%)")
    
    if high_count > low_count:
        print("  Button was mostly RELEASED during sampling")
    else:
        print("  Button was mostly PRESSED during sampling")
    
    print("Rapid sampling example completed\n")


def pin_monitoring_example():
    """Monitor multiple input pins"""
    print("=== Pin Monitoring Example ===")
    
    try:
        import Jetson.GPIO as GPIO
    except ImportError:
        import RPi.GPIO as GPIO
    
    # Monitor multiple pins (adjust based on your hardware)
    input_pins = [BUTTON_PIN, 15]  # Add more pins if available
    pins = []
    
    # Setup input pins
    for pin_num in input_pins:
        try:
            pin = DigitalPin(pin_num, GPIO.IN)
            pins.append((pin_num, pin))
            print(f"Monitoring pin {pin_num}")
        except Exception as e:
            print(f"Could not setup pin {pin_num}: {e}")
    
    if not pins:
        print("No pins available for monitoring")
        return
    
    print("Monitoring pins for 10 seconds...")
    last_states = {}
    start_time = time.time()
    
    while time.time() - start_time < 10:
        for pin_num, pin in pins:
            current_state = pin.read()
            
            if pin_num not in last_states or last_states[pin_num] != current_state:
                state_str = "HIGH" if current_state == GPIO.HIGH else "LOW"
                print(f"Pin {pin_num}: {state_str}")
                last_states[pin_num] = current_state
        
        time.sleep(0.01)
    
    print("Pin monitoring example completed\n")


def main():
    """Main function to run all examples"""
    print("Digital Input Examples for NVIDIA Orin Nano")
    print("=" * 50)
    print("Make sure to connect a button to pin 16 (with pull-up)")
    print("and an LED to pin 18 for the best experience!\n")
    
    # Setup GPIO
    setup_gpio()
    
    try:
        # Run examples
        basic_input_example()
        wrapper_class_input_example()
        button_counter_example()
        interrupt_example()
        analog_like_reading_example()
        pin_monitoring_example()
        
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