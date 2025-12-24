"""
Utility functions for StickBot GPIO operations
"""
import time
import sys

try:
    import Jetson.GPIO as GPIO
except ImportError:
    try:
        import RPi.GPIO as GPIO
    except ImportError:
        raise ImportError(
            "Neither Jetson.GPIO nor RPi.GPIO is available. "
            "Please install the appropriate GPIO library for your platform."
        )


def setup_gpio():
    """Initialize GPIO library and set mode to BOARD"""
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(True)
    print(f"GPIO initialized for {GPIO.model}")
    return GPIO.model


def cleanup_gpio():
    """Clean up all GPIO resources"""
    GPIO.cleanup()
    print("All GPIO resources cleaned up")


def wait_for_signal(pin, edge_type=GPIO.BOTH, timeout=None):
    """
    Wait for a signal edge on a pin
    
    Args:
        pin: GPIO pin number (BOARD numbering)
        edge_type: GPIO.RISING, GPIO.FALLING, or GPIO.BOTH
        timeout: Timeout in seconds (None for no timeout)
        
    Returns:
        The pin number if edge detected, None if timeout
    """
    if GPIO.getmode() != GPIO.BOARD:
        raise ValueError("GPIO mode must be BOARD")
    
    GPIO.setup(pin, GPIO.IN)
    return GPIO.wait_for_edge(pin, edge_type, timeout=timeout)


def blink_led(pin, duration=1.0, times=5):
    """
    Blink an LED connected to a pin
    
    Args:
        pin: GPIO pin number (BOARD numbering)
        duration: How long each blink lasts (seconds)
        times: Number of times to blink
    """
    if GPIO.getmode() is None:
        GPIO.setmode(GPIO.BOARD)
    
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
    
    try:
        for i in range(times):
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(duration / 2)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(duration / 2)
            print(f"Blink {i + 1}/{times}")
    finally:
        GPIO.output(pin, GPIO.LOW)


def read_pin_state(pin):
    """
    Read and return the current state of a pin
    
    Args:
        pin: GPIO pin number (BOARD numbering)
        
    Returns:
        GPIO.HIGH or GPIO.LOW
    """
    if GPIO.getmode() is None:
        GPIO.setmode(GPIO.BOARD)
    
    GPIO.setup(pin, GPIO.IN)
    state = GPIO.input(pin)
    state_str = "HIGH" if state == GPIO.HIGH else "LOW"
    print(f"Pin {pin} state: {state_str}")
    return state


def get_available_pins():
    """
    Return a list of available GPIO pins for the current board
    
    Returns:
        Dictionary with pin information
    """
    board_pins = {
        'JETSON_ORIN_NANO': {
            'digital': [7, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 26, 29, 31, 32, 33, 35, 36, 37, 38, 40],
            'pwm_capable': [15, 33],  # Hardware PWM pins
            'notes': {
                15: 'PWM capable - may need pinmux configuration',
                33: 'PWM capable - may need pinmux configuration',
                36: 'May be input-only depending on base board'
            }
        },
        'JETSON_ORIN_NX': {
            'digital': [7, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 26, 29, 31, 32, 33, 35, 36, 37, 38, 40],
            'pwm_capable': [15, 33],
            'notes': {
                15: 'PWM capable - may need pinmux configuration',
                33: 'PWM capable - may need pinmux configuration'
            }
        },
        'JETSON_ORIN': {
            'digital': [7, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 26, 29, 31, 32, 33, 35, 36, 37, 38, 40],
            'pwm_capable': [15, 18],
            'notes': {
                15: 'PWM capable - may need pinmux configuration',
                18: 'PWM capable - may need pinmux configuration'
            }
        }
    }
    
    model = GPIO.model
    return board_pins.get(model, {
        'digital': [7, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 26, 29, 31, 32, 33, 35, 36, 37, 38, 40],
        'pwm_capable': [],
        'notes': {'unknown': f'Unknown board model: {model}'}
    })


def print_board_info():
    """Print information about the current board"""
    try:
        model = GPIO.model
        pins_info = get_available_pins()
        
        print(f"\n=== Board Information ===")
        print(f"Model: {model}")
        print(f"Available digital pins: {pins_info.get('digital', [])}")
        print(f"PWM-capable pins: {pins_info.get('pwm_capable', [])}")
        
        notes = pins_info.get('notes', {})
        if notes:
            print("\nNotes:")
            for pin, note in notes.items():
                print(f"  Pin {pin}: {note}")
        print()
        
    except Exception as e:
        print(f"Error getting board information: {e}")


def check_pin_function(pin):
    """
    Check the current function/direction of a pin
    
    Args:
        pin: GPIO pin number (BOARD numbering)
        
    Returns:
        String describing the pin function
    """
    try:
        func = GPIO.gpio_function(pin)
        if func == GPIO.IN:
            return "INPUT"
        elif func == GPIO.OUT:
            return "OUTPUT"
        else:
            return "UNKNOWN"
    except Exception as e:
        return f"ERROR: {e}"