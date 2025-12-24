"""
GPIO utilities and wrapper classes for NVIDIA Orin Nano
"""
import time
import warnings

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
    """Initialize GPIO library and set warnings"""
    GPIO.setwarnings(True)
    print(f"GPIO library initialized for {GPIO.model}")


def cleanup_gpio():
    """Clean up all GPIO resources"""
    GPIO.cleanup()
    print("GPIO cleanup completed")


class DigitalPin:
    """
    Simple wrapper for digital GPIO pins
    
    Args:
        pin_number: GPIO pin number (BOARD numbering)
        direction: GPIO.IN or GPIO.OUT
        initial_value: GPIO.HIGH or GPIO.LOW (for output pins only)
    """
    
    def __init__(self, pin_number, direction, initial_value=None):
        self.pin_number = pin_number
        self.direction = direction
        
        # Set pin numbering mode
        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BOARD)
        elif GPIO.getmode() != GPIO.BOARD:
            raise ValueError("GPIO mode already set to different mode")
        
        # Setup the pin
        if direction == GPIO.OUT:
            GPIO.setup(pin_number, GPIO.OUT, initial=initial_value)
            self._current_value = initial_value if initial_value is not None else GPIO.LOW
        elif direction == GPIO.IN:
            GPIO.setup(pin_number, GPIO.IN)
            self._current_value = None
        else:
            raise ValueError("Direction must be GPIO.IN or GPIO.OUT")
    
    def set_high(self):
        """Set output pin to HIGH"""
        if self.direction != GPIO.OUT:
            raise ValueError("Pin is not configured as output")
        GPIO.output(self.pin_number, GPIO.HIGH)
        self._current_value = GPIO.HIGH
    
    def set_low(self):
        """Set output pin to LOW"""
        if self.direction != GPIO.OUT:
            raise ValueError("Pin is not configured as output")
        GPIO.output(self.pin_number, GPIO.LOW)
        self._current_value = GPIO.LOW
    
    def toggle(self):
        """Toggle output pin state"""
        if self.direction != GPIO.OUT:
            raise ValueError("Pin is not configured as output")
        if self._current_value == GPIO.HIGH:
            self.set_low()
        else:
            self.set_high()
    
    def read(self):
        """Read current pin value"""
        value = GPIO.input(self.pin_number)
        if self.direction == GPIO.IN:
            self._current_value = value
        return value
    
    def get_value(self):
        """Get the last known pin value without reading"""
        return self._current_value
    
    def cleanup(self):
        """Clean up this specific pin"""
        GPIO.cleanup(self.pin_number)
    
    def __str__(self):
        direction_str = "OUTPUT" if self.direction == GPIO.OUT else "INPUT"
        return f"DigitalPin(pin={self.pin_number}, direction={direction_str}, value={self._current_value})"


class PWMPin:
    """
    PWM wrapper for hardware PWM pins
    
    Args:
        pin_number: GPIO pin number (BOARD numbering) - must support hardware PWM
        frequency: PWM frequency in Hz
    """
    
    def __init__(self, pin_number, frequency=1000):
        self.pin_number = pin_number
        self.frequency = frequency
        self._duty_cycle = 0
        self._started = False
        
        # Set pin numbering mode
        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BOARD)
        elif GPIO.getmode() != GPIO.BOARD:
            raise ValueError("GPIO mode already set to different mode")
        
        # Setup pin as output
        GPIO.setup(pin_number, GPIO.OUT, initial=GPIO.LOW)
        
        # Create PWM object
        self._pwm = GPIO.PWM(pin_number, frequency)
    
    def start(self, duty_cycle=0):
        """
        Start PWM output
        
        Args:
            duty_cycle: Duty cycle percentage (0-100)
        """
        if not 0 <= duty_cycle <= 100:
            raise ValueError("Duty cycle must be between 0 and 100")
        
        self._duty_cycle = duty_cycle
        self._pwm.start(duty_cycle)
        self._started = True
    
    def stop(self):
        """Stop PWM output"""
        if self._started:
            self._pwm.stop()
            self._started = False
    
    def change_frequency(self, frequency):
        """Change PWM frequency"""
        self.frequency = frequency
        if self._started:
            self._pwm.ChangeFrequency(frequency)
    
    def change_duty_cycle(self, duty_cycle):
        """Change PWM duty cycle"""
        if not 0 <= duty_cycle <= 100:
            raise ValueError("Duty cycle must be between 0 and 100")
        
        self._duty_cycle = duty_cycle
        if self._started:
            self._pwm.ChangeDutyCycle(duty_cycle)
    
    def is_started(self):
        """Check if PWM is currently running"""
        return self._started
    
    def get_duty_cycle(self):
        """Get current duty cycle"""
        return self._duty_cycle
    
    def get_frequency(self):
        """Get current frequency"""
        return self.frequency
    
    def cleanup(self):
        """Clean up PWM pin"""
        self.stop()
        GPIO.cleanup(self.pin_number)
    
    def __del__(self):
        """Destructor to ensure cleanup"""
        if hasattr(self, '_started') and self._started:
            self.stop()
    
    def __str__(self):
        status = "RUNNING" if self._started else "STOPPED"
        return f"PWMPin(pin={self.pin_number}, freq={self.frequency}Hz, duty={self._duty_cycle}%, status={status})"