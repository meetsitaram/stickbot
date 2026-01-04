#!/home/stick/solo_venv/bin/python3
"""
Xbox Controller Input Example for NVIDIA Orin Nano

This script connects to an Xbox controller via USB or Bluetooth and prints
all button presses, joystick movements, and trigger actions in real-time.

Requirements:
    source ~/solo_venv/bin/activate
    pip install inputs

Usage:
    python xbox_controller.py

Supported Inputs:
    - Buttons: A, B, X, Y, Start, Back, Guide, Left/Right Bumpers
    - D-Pad: Up, Down, Left, Right
    - Joysticks: Left and Right analog sticks
    - Triggers: Left (LT) and Right (RT) triggers
"""

try:
    from inputs import get_gamepad
except ImportError:
    print("Error: 'inputs' library not found.")
    print("Install it with: pip install inputs")
    exit(1)

import sys


def print_controller_event(event):
    """
    Print controller events in a readable format.
    
    Args:
        event: Input event from the controller
    """
    event_type = event.ev_type
    code = event.code
    state = event.state
    
    # Button events
    if event_type == 'Key':
        button_names = {
            'BTN_SOUTH': 'A',
            'BTN_EAST': 'B',
            'BTN_NORTH': 'X',
            'BTN_WEST': 'Y',
            'BTN_TL': 'Left Bumper (LB)',
            'BTN_TR': 'Right Bumper (RB)',
            'BTN_SELECT': 'Back/View',
            'BTN_START': 'Start/Menu',
            'BTN_MODE': 'Xbox Guide',
            'BTN_THUMBL': 'Left Stick Click',
            'BTN_THUMBR': 'Right Stick Click',
        }
        
        button_name = button_names.get(code, code)
        action = "PRESSED" if state == 1 else "RELEASED"
        print(f"[BUTTON] {button_name}: {action}")
    
    # Analog events (joysticks and triggers)
    elif event_type == 'Absolute':
        analog_names = {
            'ABS_X': 'Left Stick X',
            'ABS_Y': 'Left Stick Y',
            'ABS_RX': 'Right Stick X',
            'ABS_RY': 'Right Stick Y',
            'ABS_Z': 'Left Trigger (LT)',
            'ABS_RZ': 'Right Trigger (RT)',
            'ABS_HAT0X': 'D-Pad X',
            'ABS_HAT0Y': 'D-Pad Y',
        }
        
        analog_name = analog_names.get(code, code)
        
        # Format D-Pad directions
        if code in ['ABS_HAT0X', 'ABS_HAT0Y']:
            if state == 0:
                return  # Neutral position, skip printing
            direction = ""
            if code == 'ABS_HAT0X':
                direction = "RIGHT" if state > 0 else "LEFT"
            else:
                direction = "DOWN" if state > 0 else "UP"
            print(f"[D-PAD] {direction}")
        
        # Format triggers (0-255 range)
        elif code in ['ABS_Z', 'ABS_RZ']:
            if state > 10:  # Ignore noise near zero
                percentage = (state / 255) * 100
                print(f"[TRIGGER] {analog_name}: {state} ({percentage:.1f}%)")
        
        # Format joysticks (typically -32768 to 32767)
        elif code in ['ABS_X', 'ABS_Y', 'ABS_RX', 'ABS_RY']:
            if abs(state) > 3000:  # Ignore small deadzone movements
                print(f"[JOYSTICK] {analog_name}: {state}")
    
    # Sync events (can be ignored)
    elif event_type == 'Sync':
        pass


def main():
    """Main function to continuously read and print controller inputs."""
    print("=" * 60)
    print("Xbox Controller Input Monitor")
    print("=" * 60)
    print("\nSearching for Xbox controller...")
    print("Please ensure your controller is connected via USB or Bluetooth.\n")
    
    try:
        print("Controller found! Reading inputs...")
        print("Press Ctrl+C to exit.\n")
        print("-" * 60)
        
        # Continuously read events from the controller
        while True:
            events = get_gamepad()
            for event in events:
                print_controller_event(event)
                
    except KeyboardInterrupt:
        print("\n" + "-" * 60)
        print("Exiting...")
        sys.exit(0)
        
    except Exception as e:
        print(f"\nError: {e}")
        print("\nTroubleshooting:")
        print("1. Check if controller is connected: ls /dev/input/js*")
        print("2. Check permissions:")
        print("   sudo usermod -a -G input $USER")
        print("   newgrp input  # or logout/login to refresh groups")
        print("3. Alternative permission fix: sudo chmod 666 /dev/input/js0")
        print("4. Try reconnecting the controller")
        print("5. For Bluetooth: sudo bluetoothctl and pair the device")
        print("6. Check if another process is using the controller: sudo lsof /dev/input/js0")
        sys.exit(1)


if __name__ == "__main__":
    main()
