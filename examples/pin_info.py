#!/home/stick/solo_venv/bin/python3
"""
GPIO Pin Information and Testing Script for NVIDIA Orin Nano

This script provides:
- Board information and available pins
- Pin testing utilities
- GPIO pin state checking
- Hardware capability detection

Usage:
    python pin_info.py              # Show board info
    python pin_info.py --test-pin 18   # Test specific pin
    python pin_info.py --scan-pins     # Scan all available pins
"""

import sys
import os
import argparse
import time

# Add the src directory to the path to import our library  
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from stickbot import setup_gpio, cleanup_gpio, print_board_info, get_available_pins, check_pin_function


def test_pin_as_output(pin_number):
    """Test a pin as digital output"""
    try:
        import Jetson.GPIO as GPIO
    except ImportError:
        import RPi.GPIO as GPIO
    
    print(f"Testing pin {pin_number} as OUTPUT...")
    
    try:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin_number, GPIO.OUT, initial=GPIO.LOW)
        
        print("  Setting HIGH for 2 seconds...")
        GPIO.output(pin_number, GPIO.HIGH)
        time.sleep(2)
        
        print("  Setting LOW for 2 seconds...")  
        GPIO.output(pin_number, GPIO.LOW)
        time.sleep(2)
        
        print(f"  Pin {pin_number} output test completed successfully")
        return True
        
    except Exception as e:
        print(f"  Error testing pin {pin_number} as output: {e}")
        return False
    finally:
        try:
            GPIO.cleanup(pin_number)
        except:
            pass


def test_pin_as_input(pin_number):
    """Test a pin as digital input"""
    try:
        import Jetson.GPIO as GPIO
    except ImportError:
        import RPi.GPIO as GPIO
    
    print(f"Testing pin {pin_number} as INPUT...")
    
    try:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        print("  Reading pin state for 5 seconds (try connecting to ground)...")
        for i in range(50):  # 5 seconds of readings
            state = GPIO.input(pin_number)
            state_str = "HIGH" if state == GPIO.HIGH else "LOW"
            if i % 10 == 0:  # Print every 10th reading
                print(f"    Reading {i//10 + 1}: {state_str}")
            time.sleep(0.1)
        
        print(f"  Pin {pin_number} input test completed successfully")
        return True
        
    except Exception as e:
        print(f"  Error testing pin {pin_number} as input: {e}")
        return False
    finally:
        try:
            GPIO.cleanup(pin_number)
        except:
            pass


def test_pin_as_pwm(pin_number):
    """Test a pin for PWM capability"""
    try:
        import Jetson.GPIO as GPIO
    except ImportError:
        import RPi.GPIO as GPIO
    
    print(f"Testing pin {pin_number} for PWM capability...")
    
    try:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin_number, GPIO.OUT, initial=GPIO.LOW)
        
        # Try to create PWM object
        pwm = GPIO.PWM(pin_number, 1000)
        pwm.start(50)  # 50% duty cycle
        
        print("  PWM started successfully at 50% duty cycle")
        time.sleep(2)
        
        print("  Testing duty cycle changes...")
        for duty in [25, 75, 50]:
            pwm.ChangeDutyCycle(duty)
            print(f"    Changed to {duty}% duty cycle")
            time.sleep(1)
        
        pwm.stop()
        print(f"  Pin {pin_number} PWM test completed successfully")
        return True
        
    except Exception as e:
        print(f"  Pin {pin_number} does not support PWM: {e}")
        return False
    finally:
        try:
            GPIO.cleanup(pin_number)
        except:
            pass


def scan_all_pins():
    """Scan and test all available pins"""
    print("=== Scanning All Available Pins ===")
    
    pins_info = get_available_pins()
    digital_pins = pins_info.get('digital', [])
    pwm_pins = pins_info.get('pwm_capable', [])
    
    print(f"Found {len(digital_pins)} digital pins to test")
    
    results = {
        'output_working': [],
        'input_working': [],
        'pwm_working': [],
        'failed': []
    }
    
    for pin in digital_pins:
        print(f"\n--- Testing Pin {pin} ---")
        
        # Test as output
        if test_pin_as_output(pin):
            results['output_working'].append(pin)
        else:
            results['failed'].append(pin)
            continue
        
        time.sleep(0.5)
        
        # Test as input
        if test_pin_as_input(pin):
            results['input_working'].append(pin)
        
        time.sleep(0.5)
        
        # Test PWM if this pin is supposed to support it
        if pin in pwm_pins:
            if test_pin_as_pwm(pin):
                results['pwm_working'].append(pin)
        
        time.sleep(1)  # Brief pause between pins
    
    # Print results summary
    print("\n=== Scan Results Summary ===")
    print(f"Output working pins: {results['output_working']}")
    print(f"Input working pins: {results['input_working']}")  
    print(f"PWM working pins: {results['pwm_working']}")
    print(f"Failed pins: {results['failed']}")
    
    return results


def show_pinout():
    """Show detailed pinout information"""
    print("=== NVIDIA Orin Nano 40-Pin GPIO Header ===")
    print("""
    3.3V  (1) (2)  5V
   GPIO2  (3) (4)  5V
   GPIO3  (5) (6)  GND
   GPIO4  (7) (8)  GPIO14
     GND  (9) (10) GPIO15
  GPIO17 (11) (12) GPIO18
  GPIO27 (13) (14) GND
  GPIO22 (15) (16) GPIO23
    3.3V (17) (18) GPIO24
  GPIO10 (19) (20) GND
   GPIO9 (21) (22) GPIO25
  GPIO11 (23) (24) GPIO8
     GND (25) (26) GPIO7
   GPIO0 (27) (28) GPIO1
   GPIO5 (29) (30) GND
   GPIO6 (31) (32) GPIO12
  GPIO13 (33) (34) GND
  GPIO19 (35) (36) GPIO16
  GPIO26 (37) (38) GPIO20
     GND (39) (40) GPIO21
    """)
    
    print("Pin Function Reference (BOARD numbering):")
    print("- Pin 7, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 26: Digital I/O")
    print("- Pin 29, 31, 32, 33, 35, 36, 37, 38, 40: Digital I/O")
    print("- Pin 15, 33: PWM capable (may need pinmux config)")
    print("- Pin 1, 17: 3.3V power")
    print("- Pin 2, 4: 5V power") 
    print("- Pin 6, 9, 14, 20, 25, 30, 34, 39: Ground")


def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(description="GPIO Pin Information and Testing for NVIDIA Orin Nano")
    parser.add_argument('--test-pin', type=int, help='Test a specific pin number (BOARD numbering)')
    parser.add_argument('--scan-pins', action='store_true', help='Scan and test all available pins')
    parser.add_argument('--pinout', action='store_true', help='Show detailed pinout diagram')
    parser.add_argument('--output-only', action='store_true', help='Test pin as output only (with --test-pin)')
    parser.add_argument('--input-only', action='store_true', help='Test pin as input only (with --test-pin)')
    parser.add_argument('--pwm-only', action='store_true', help='Test pin for PWM only (with --test-pin)')
    
    args = parser.parse_args()
    
    print("GPIO Pin Information and Testing Tool")
    print("=" * 40)
    
    # Setup GPIO
    setup_gpio()
    
    try:
        if args.pinout:
            show_pinout()
        elif args.test_pin:
            pin = args.test_pin
            print(f"Testing pin {pin}...")
            
            if args.output_only:
                test_pin_as_output(pin)
            elif args.input_only:
                test_pin_as_input(pin)
            elif args.pwm_only:
                test_pin_as_pwm(pin)
            else:
                # Test all functions
                test_pin_as_output(pin)
                time.sleep(1)
                test_pin_as_input(pin)
                time.sleep(1)
                test_pin_as_pwm(pin)
        elif args.scan_pins:
            scan_all_pins()
        else:
            # Default: show board info
            print_board_info()
            print("\nUse --help to see additional options")
            print("Examples:")
            print("  python pin_info.py --test-pin 18")
            print("  python pin_info.py --scan-pins")
            print("  python pin_info.py --pinout")
            
    except KeyboardInterrupt:
        print("\nOperation interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cleanup_gpio()


if __name__ == "__main__":
    main()