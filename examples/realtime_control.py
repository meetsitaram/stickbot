#!/usr/bin/env python3
"""
Real-time Keyboard GPIO Toggle Control for NVIDIA Orin Nano

This example demonstrates:
- Controlling 6 digital output pins in real-time
- Reading keyboard input without pressing Enter
- Toggle mode: each key press toggles pin ON/OFF
- Press 0 to exit

Hardware setup:
- Connect LEDs with resistors to the 6 GPIO pins
- Or connect other output devices like relays, motors, etc.

Controls:
- Press keys 1-6: Toggle corresponding pin ON/OFF
- Press 0 or ESC: Exit program

Pin mapping (you can modify these):
- Key 1 → Pin 18
- Key 2 → Pin 16  
- Key 3 → Pin 15
- Key 4 → Pin 13
- Key 5 → Pin 11
- Key 6 → Pin 7
"""

import time
import sys
import os
import select
import termios
import tty

# Add the src directory to the path to import our library
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from stickbot import DigitalPin, setup_gpio, cleanup_gpio

# GPIO pin mapping for keys 1-6
PIN_MAPPING = {
    '1': 18,  # Key 1 → Pin 18
    '2': 16,  # Key 2 → Pin 16
    '3': 15,  # Key 3 → Pin 15
    '4': 13,  # Key 4 → Pin 13
    '5': 11,  # Key 5 → Pin 11
    '6': 7,   # Key 6 → Pin 7
}

class NonBlockingInput:
    """Handle non-blocking keyboard input on Linux/Unix"""
    
    def __init__(self):
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin.fileno())
        
    def __del__(self):
        self.restore()
        
    def restore(self):
        """Restore terminal settings"""
        try:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
        except:
            pass
            
    def get_char(self):
        """Get a character if available, return None if no input"""
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            return sys.stdin.read(1)
        return None


class RealTimeGPIOController:
    """Real-time GPIO controller with keyboard input"""
    
    def __init__(self):
        self.pins = {}
        self.pin_states = {}
        self.running = True
        self.input_handler = None
        
        # Setup GPIO
        setup_gpio()
        
        try:
            import Jetson.GPIO as GPIO
        except ImportError:
            import RPi.GPIO as GPIO
        
        # Initialize all pins as outputs
        for key, pin_num in PIN_MAPPING.items():
            try:
                pin = DigitalPin(pin_num, GPIO.OUT, GPIO.LOW)
                self.pins[key] = pin
                self.pin_states[key] = False
                print(f"Initialized Pin {pin_num} for key '{key}'")
            except Exception as e:
                print(f"Warning: Could not initialize pin {pin_num} for key '{key}': {e}")
    
    def print_instructions(self):
        """Print usage instructions"""
        print("\n" + "="*60)
        print("Real-time GPIO Toggle Control - NVIDIA Orin Nano")
        print("="*60)
        print("Controls:")
        print("  Press keys 1-6: Toggle corresponding pin ON/OFF")
        print("  Press 0 or ESC: Exit program")
        print()
        print("Pin Mapping:")
        for key, pin_num in PIN_MAPPING.items():
            status = "✓" if key in self.pins else "✗"
            print(f"  Key '{key}' → Pin {pin_num:2d} {status}")
        print()
        print("Status: Ready - Start pressing keys!")
        print("="*60)
    

    

    

    

    
    def run(self):
        """Run the GPIO toggle controller"""
        self.print_instructions()
        print("Press keys 1-6 to toggle pins, 0 to exit\n")
        
        try:
            self.input_handler = NonBlockingInput()
            
            while self.running:
                char = self.input_handler.get_char()
                
                if char == '0' or (char and ord(char) == 27):
                    print(f"\nExit key pressed. Shutting down...")
                    self.running = False
                    break
                
                if char and char in PIN_MAPPING and char in self.pins:
                    # Toggle pin state
                    current_state = self.pin_states[char]
                    new_state = not current_state
                    
                    if new_state:
                        self.pins[char].set_high()
                        print(f"Key '{char}' → Pin {PIN_MAPPING[char]} ON ")
                    else:
                        self.pins[char].set_low()
                        print(f"Key '{char}' → Pin {PIN_MAPPING[char]} OFF")
                    
                    self.pin_states[char] = new_state
                
                time.sleep(0.01)
                
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        print("\nCleaning up...")
        
        # Set all pins LOW
        for key, pin in self.pins.items():
            try:
                pin.set_low()
                print(f"Pin {PIN_MAPPING[key]} set to LOW")
            except:
                pass
        
        # Restore terminal
        if self.input_handler:
            self.input_handler.restore()
        
        cleanup_gpio()
        print("GPIO cleanup completed")


def main():
    """Main function"""
    print("Real-time GPIO Toggle Controller for NVIDIA Orin Nano")
    print("=" * 55)
    
    try:
        controller = RealTimeGPIOController()
        controller.run()
            
    except KeyboardInterrupt:
        print("\nProgram interrupted")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Program ended")


if __name__ == "__main__":
    main()