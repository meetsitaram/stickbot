#!/home/stick/solo_venv/bin/python3
"""
PWM Control Example for NVIDIA Orin Nano

This example demonstrates:
- Setting up hardware PWM pins
- Controlling PWM duty cycle and frequency
- Creating smooth LED brightness control
- Servo motor control basics
- Using the PWMPin wrapper class

Hardware setup:
- Connect an LED with resistor to pin 33 (PWM capable pin)
- Or connect a servo motor to pin 33
- See pinout reference for PWM-capable pins on your board

Important notes:
- Only hardware PWM pins are supported (not software PWM)
- NVIDIA Orin Nano supports PWM on pins 15 and 33 (may need pinmux configuration)
- Some pins may require boot-time pinmux configuration to enable PWM

Pin reference for Orin Nano:
- Pin 33 (BOARD) = Hardware PWM capable
- Pin 15 (BOARD) = Hardware PWM capable (may need configuration)
"""

import time
import sys
import os

# Add the src directory to the path to import our library
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from stickbot import PWMPin, setup_gpio, cleanup_gpio

# Configuration - Use PWM-capable pins for Orin Nano
PWM_PIN = 33      # Primary PWM pin for Orin Nano
PWM_FREQUENCY = 1000  # 1 kHz default frequency


def basic_pwm_example():
    """Basic PWM control using Jetson.GPIO directly"""
    print("=== Basic PWM Example ===")
    
    try:
        import Jetson.GPIO as GPIO
    except ImportError:
        import RPi.GPIO as GPIO
    
    # Check if this board supports PWM
    if hasattr(GPIO, 'model'):
        model = GPIO.model
        if model not in ['JETSON_ORIN_NANO', 'JETSON_ORIN_NX', 'JETSON_ORIN']:
            print(f"Warning: PWM support not confirmed for {model}")
    
    # Setup
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PWM_PIN, GPIO.OUT, initial=GPIO.LOW)
    
    try:
        # Create PWM object
        pwm = GPIO.PWM(PWM_PIN, PWM_FREQUENCY)
        
        print(f"Starting PWM on pin {PWM_PIN} at {PWM_FREQUENCY} Hz")
        pwm.start(0)  # Start with 0% duty cycle
        
        # Gradually increase duty cycle
        print("Increasing duty cycle from 0% to 100%...")
        for duty_cycle in range(0, 101, 5):
            print(f"  Duty cycle: {duty_cycle}%")
            pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(0.1)
        
        time.sleep(1)
        
        # Gradually decrease duty cycle
        print("Decreasing duty cycle from 100% to 0%...")
        for duty_cycle in range(100, -1, -5):
            print(f"  Duty cycle: {duty_cycle}%")
            pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(0.1)
        
        pwm.stop()
        print("Basic PWM example completed\n")
        
    except Exception as e:
        print(f"PWM error (pin {PWM_PIN} may not support PWM): {e}")
        print("Try checking pinmux configuration or using a different pin\n")


def wrapper_class_pwm_example():
    """Example using PWMPin wrapper class"""
    print("=== PWM Wrapper Class Example ===")
    
    try:
        # Create PWM pin object
        pwm_led = PWMPin(PWM_PIN, PWM_FREQUENCY)
        print(f"Created: {pwm_led}")
        
        # Start PWM
        print("Starting PWM with 25% duty cycle...")
        pwm_led.start(25)
        time.sleep(2)
        
        # Change duty cycle
        print("Changing to 75% duty cycle...")
        pwm_led.change_duty_cycle(75)
        time.sleep(2)
        
        # Change frequency
        print("Changing frequency to 500 Hz...")
        pwm_led.change_frequency(500)
        time.sleep(2)
        
        # Stop PWM
        print("Stopping PWM...")
        pwm_led.stop()
        
        print(f"Final state: {pwm_led}")
        print("PWM wrapper class example completed\n")
        
    except Exception as e:
        print(f"PWM wrapper error: {e}")
        print("Pin may not support hardware PWM\n")


def led_breathing_effect():
    """Create a smooth breathing effect with LED"""
    print("=== LED Breathing Effect ===")
    
    try:
        pwm_led = PWMPin(PWM_PIN, 1000)  # 1 kHz for smooth LED control
        
        print("Creating LED breathing effect for 20 seconds...")
        print("(LED will smoothly fade in and out)")
        
        pwm_led.start(0)
        start_time = time.time()
        
        while time.time() - start_time < 20:
            # Breathing pattern: sine wave
            t = (time.time() - start_time) * 2  # 2 Hz breathing rate
            duty_cycle = (math.sin(t) + 1) * 50  # 0-100% duty cycle
            pwm_led.change_duty_cycle(duty_cycle)
            time.sleep(0.05)
        
        pwm_led.stop()
        print("LED breathing effect completed\n")
        
    except Exception as e:
        print(f"Breathing effect error: {e}\n")


def servo_control_example():
    """Example for controlling a servo motor with PWM"""
    print("=== Servo Control Example ===")
    
    try:
        # Servo motors typically use 50 Hz PWM
        servo = PWMPin(PWM_PIN, 50)
        
        print("Servo control example (assuming standard servo)")
        print("Connect servo signal wire to pin", PWM_PIN)
        print("Duty cycles: ~2.5% = 0°, ~7.5% = 90°, ~12.5% = 180°")
        
        servo.start(7.5)  # Start at center position (90°)
        time.sleep(1)
        
        positions = [
            (2.5, "0° (left)"),
            (7.5, "90° (center)"),
            (12.5, "180° (right)"),
            (7.5, "90° (center)")
        ]
        
        for duty_cycle, position in positions:
            print(f"Moving to {position} (duty cycle: {duty_cycle}%)")
            servo.change_duty_cycle(duty_cycle)
            time.sleep(2)
        
        servo.stop()
        print("Servo control example completed\n")
        
    except Exception as e:
        print(f"Servo control error: {e}\n")


def frequency_sweep_example():
    """Sweep through different frequencies"""
    print("=== Frequency Sweep Example ===")
    
    try:
        pwm_pin = PWMPin(PWM_PIN, 100)  # Start at 100 Hz
        
        print("Frequency sweep from 100 Hz to 5000 Hz")
        print("(If connected to a speaker, you should hear the tone change)")
        
        pwm_pin.start(50)  # 50% duty cycle
        
        frequencies = [100, 200, 500, 1000, 2000, 5000, 1000, 500, 200, 100]
        
        for freq in frequencies:
            print(f"  Frequency: {freq} Hz")
            pwm_pin.change_frequency(freq)
            time.sleep(1)
        
        pwm_pin.stop()
        print("Frequency sweep completed\n")
        
    except Exception as e:
        print(f"Frequency sweep error: {e}\n")


def multiple_pwm_example():
    """Control multiple PWM pins simultaneously"""
    print("=== Multiple PWM Example ===")
    
    # PWM-capable pins for Orin Nano
    pwm_pins = [33, 15]  # Adjust based on available pins
    pwm_objects = []
    
    print("Setting up multiple PWM pins...")
    
    for pin in pwm_pins:
        try:
            pwm = PWMPin(pin, 1000)
            pwm_objects.append(pwm)
            print(f"  Setup PWM on pin {pin}")
        except Exception as e:
            print(f"  Could not setup PWM on pin {pin}: {e}")
    
    if not pwm_objects:
        print("No PWM pins available for multiple PWM example")
        return
    
    # Start all PWM pins
    for i, pwm in enumerate(pwm_objects):
        duty = 20 + (i * 20)  # Different duty cycles
        pwm.start(duty)
        print(f"  Started PWM {i+1} at {duty}% duty cycle")
    
    time.sleep(3)
    
    # Phase shift effect
    print("Creating phase shift effect...")
    for phase in range(0, 360, 10):
        for i, pwm in enumerate(pwm_objects):
            # Create different phases for each PWM
            duty = 50 + 40 * math.sin(math.radians(phase + i * 90))
            pwm.change_duty_cycle(max(0, min(100, duty)))
        time.sleep(0.1)
    
    # Stop all PWM
    for pwm in pwm_objects:
        pwm.stop()
    
    print("Multiple PWM example completed\n")


def pwm_measurement_example():
    """Demonstrate PWM timing measurements"""
    print("=== PWM Measurement Example ===")
    
    try:
        import Jetson.GPIO as GPIO
    except ImportError:
        import RPi.GPIO as GPIO
    
    try:
        pwm_pin = PWMPin(PWM_PIN, 1000)
        
        print("PWM timing demonstration")
        print("Frequency: 1000 Hz (1 ms period)")
        print("Testing different duty cycles...")
        
        duty_cycles = [10, 25, 50, 75, 90]
        
        for duty in duty_cycles:
            print(f"\nDuty cycle: {duty}%")
            print(f"  On time: {duty * 0.01:.2f} ms")
            print(f"  Off time: {(100-duty) * 0.01:.2f} ms")
            
            pwm_pin.start(duty)
            time.sleep(2)
            pwm_pin.stop()
            time.sleep(0.5)
        
        print("PWM measurement example completed\n")
        
    except Exception as e:
        print(f"PWM measurement error: {e}\n")


def main():
    """Main function to run all examples"""
    print("PWM Control Examples for NVIDIA Orin Nano")
    print("=" * 50)
    print(f"Using pin {PWM_PIN} for PWM examples")
    print("Note: Hardware PWM pins may require pinmux configuration")
    print("Connect an LED or servo to see the effects!\n")
    
    # Import math for some examples
    global math
    import math
    
    # Setup GPIO
    setup_gpio()
    
    try:
        # Run examples
        basic_pwm_example()
        wrapper_class_pwm_example()
        led_breathing_effect()
        servo_control_example()
        frequency_sweep_example()
        multiple_pwm_example()
        pwm_measurement_example()
        
        print("All PWM examples completed successfully!")
        print("\nIf you encountered PWM errors, try:")
        print("1. Using pin 33 or 15 (known PWM pins for Orin Nano)")
        print("2. Checking if pinmux configuration is needed")
        print("3. Running: sudo busybox devmem 0x02440020 32 0x400  # for pin 15")
        print("4. Running: sudo busybox devmem 0x02434040 32 0x401  # for pin 33")
        
    except KeyboardInterrupt:
        print("\nExample interrupted by user")
    except Exception as e:
        print(f"Error running examples: {e}")
    finally:
        # Always cleanup GPIO
        cleanup_gpio()


if __name__ == "__main__":
    main()