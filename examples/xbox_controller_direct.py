#!/home/stick/solo_venv/bin/python3
"""
Xbox Controller Input Example for NVIDIA Orin Nano (Direct Device Reading)

This script directly reads from /dev/input/js0 and prints all button presses,
joystick movements, and trigger actions in real-time.

This alternative approach works when the 'inputs' library has detection issues.

Requirements:
    source ~/solo_venv/bin/activate
    # No additional packages required - uses built-in modules

Usage:
    python examples/xbox_controller_direct.py

Supported Inputs:
    - Buttons: A, B, X, Y, Start, Back, Guide, Left/Right Bumpers
    - D-Pad: Up, Down, Left, Right
    - Joysticks: Left and Right analog sticks
    - Triggers: Left (LT) and Right (RT) triggers
"""

import struct
import sys
import os
import time


# Xbox controller button mappings
BUTTON_NAMES = {
    0: 'A',
    1: 'B', 
    2: 'X',
    3: 'Y',
    4: 'Left Bumper (LB)',
    5: 'Right Bumper (RB)',
    6: 'Back/View',
    7: 'Start/Menu',
    8: 'Xbox Guide',
    9: 'Left Stick Click',
    10: 'Right Stick Click',
}

# Xbox controller axis mappings
AXIS_NAMES = {
    0: 'Left Stick X',
    1: 'Left Stick Y',
    2: 'Left Trigger (LT)',
    3: 'Right Stick X',
    4: 'Right Stick Y',
    5: 'Right Trigger (RT)',
    6: 'D-Pad X',
    7: 'D-Pad Y',
}


def read_joystick_events(device_path='/dev/input/js0'):
    """
    Read and parse joystick events directly from the device.
    
    Args:
        device_path: Path to the joystick device (default: /dev/input/js0)
    
    Yields:
        Tuples of (event_type, number, value, timestamp)
    """
    try:
        with open(device_path, 'rb') as device:
            while True:
                # Read 8 bytes for each event
                # Format: unsigned int time, short value, unsigned char type, unsigned char number
                event = device.read(8)
                if not event:
                    break
                    
                # Unpack the binary data
                timestamp, value, event_type, number = struct.unpack('IhBB', event)
                yield (event_type, number, value, timestamp)
                
    except IOError as e:
        print(f"Error reading from {device_path}: {e}")
        return


def format_axis_value(axis_num, value):
    """
    Format axis values for better readability.
    
    Args:
        axis_num: Axis number
        value: Raw axis value
    
    Returns:
        Formatted string or None if value should be ignored
    """
    # D-Pad handling
    if axis_num == 6:  # D-Pad X
        if value == -32767:
            return "D-PAD LEFT"
        elif value == 32767:
            return "D-PAD RIGHT"
        elif value == 0:
            return None  # Neutral
    elif axis_num == 7:  # D-Pad Y
        if value == -32767:
            return "D-PAD UP"
        elif value == 32767:
            return "D-PAD DOWN"
        elif value == 0:
            return None  # Neutral
    
    # Trigger handling (LT/RT)
    elif axis_num in [2, 5]:  # Triggers
        if value > -30000:  # Ignore small values near minimum
            trigger_value = (value + 32767) / 65534 * 100  # Convert to percentage
            return f"{AXIS_NAMES[axis_num]}: {trigger_value:.1f}%"
    
    # Joystick handling
    elif axis_num in [0, 1, 3, 4]:  # Joysticks
        if abs(value) > 3000:  # Deadzone filtering
            return f"{AXIS_NAMES[axis_num]}: {value}"
    
    return None


def main():
    """Main function to continuously read and print controller inputs."""
    device_path = '/dev/input/js0'
    
    print("=" * 60)
    print("Xbox Controller Input Monitor (Direct Device Reading)")
    print("=" * 60)
    print(f"\nAttempting to read from: {device_path}")
    
    # Check if device exists
    if not os.path.exists(device_path):
        print(f"Error: Device {device_path} not found!")
        print("\nTroubleshooting:")
        print("1. Check connected devices: ls /dev/input/js*")
        print("2. Connect your Xbox controller via USB or Bluetooth")
        print("3. If using a different device, modify device_path in the script")
        sys.exit(1)
    
    # Check if device is readable
    if not os.access(device_path, os.R_OK):
        print(f"Error: Cannot read from {device_path}")
        print("\nTroubleshooting:")
        print("1. Check permissions: ls -la /dev/input/js*")
        print("2. Add user to input group: sudo usermod -a -G input $USER")
        print("3. Apply group changes: newgrp input")
        print("4. Alternative: sudo chmod 666 /dev/input/js0")
        sys.exit(1)
    
    print("Controller device found and accessible!")
    print("Press Ctrl+C to exit.\n")
    print("-" * 60)
    
    try:
        for event_type, number, value, timestamp in read_joystick_events(device_path):
            # Filter initialization events (type & 0x80)
            if event_type & 0x80:
                continue
                
            # Button events (type 1)
            if event_type == 1:
                button_name = BUTTON_NAMES.get(number, f"Button {number}")
                action = "PRESSED" if value else "RELEASED"
                print(f"[BUTTON] {button_name}: {action}")
            
            # Axis events (type 2) - joysticks, triggers, d-pad
            elif event_type == 2:
                formatted_value = format_axis_value(number, value)
                if formatted_value:
                    if "D-PAD" in formatted_value:
                        print(f"[D-PAD] {formatted_value}")
                    elif "Trigger" in formatted_value:
                        print(f"[TRIGGER] {formatted_value}")
                    else:
                        print(f"[JOYSTICK] {formatted_value}")
                        
    except KeyboardInterrupt:
        print("\n" + "-" * 60)
        print("Exiting...")
        sys.exit(0)
        
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print("\nTroubleshooting:")
        print("1. Try reconnecting the controller")
        print("2. Check if another process is using the device: sudo lsof /dev/input/js0")
        print("3. Restart the controller or system")
        sys.exit(1)


if __name__ == "__main__":
    main()