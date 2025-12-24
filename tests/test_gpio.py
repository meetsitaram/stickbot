import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestGPIOClasses(unittest.TestCase):
    """Test GPIO wrapper classes"""
    
    def setUp(self):
        """Setup mock GPIO for testing"""
        # Mock the GPIO libraries
        self.mock_jetson_gpio = MagicMock()
        self.mock_rpi_gpio = MagicMock()
        
        # Setup GPIO constants
        self.mock_jetson_gpio.HIGH = 1
        self.mock_jetson_gpio.LOW = 0
        self.mock_jetson_gpio.OUT = 0
        self.mock_jetson_gpio.IN = 1
        self.mock_jetson_gpio.BOARD = 10
        self.mock_jetson_gpio.model = "JETSON_ORIN_NANO"
        
        # Mock getmode to return None initially
        self.mock_jetson_gpio.getmode.return_value = None
        
        # Patch the imports
        self.jetson_patcher = patch.dict('sys.modules', {'Jetson.GPIO': self.mock_jetson_gpio})
        self.rpi_patcher = patch.dict('sys.modules', {'RPi.GPIO': self.mock_rpi_gpio})
        
        self.jetson_patcher.start()
        self.rpi_patcher.start()
    
    def tearDown(self):
        """Cleanup patches"""
        self.jetson_patcher.stop()
        self.rpi_patcher.stop()
    
    def test_digital_pin_output_creation(self):
        """Test creating a DigitalPin for output"""
        from stickbot.gpio import DigitalPin
        
        # Create output pin
        pin = DigitalPin(18, self.mock_jetson_gpio.OUT, self.mock_jetson_gpio.HIGH)
        
        # Verify GPIO setup calls
        self.mock_jetson_gpio.setmode.assert_called_with(self.mock_jetson_gpio.BOARD)
        self.mock_jetson_gpio.setup.assert_called_with(18, self.mock_jetson_gpio.OUT, initial=self.mock_jetson_gpio.HIGH)
        
        # Test pin properties
        self.assertEqual(pin.pin_number, 18)
        self.assertEqual(pin.direction, self.mock_jetson_gpio.OUT)
        self.assertEqual(pin._current_value, self.mock_jetson_gpio.HIGH)
    
    def test_digital_pin_input_creation(self):
        """Test creating a DigitalPin for input"""
        from stickbot.gpio import DigitalPin
        
        # Create input pin
        pin = DigitalPin(16, self.mock_jetson_gpio.IN)
        
        # Verify GPIO setup calls
        self.mock_jetson_gpio.setup.assert_called_with(16, self.mock_jetson_gpio.IN)
        
        # Test pin properties
        self.assertEqual(pin.pin_number, 16)
        self.assertEqual(pin.direction, self.mock_jetson_gpio.IN)
        self.assertIsNone(pin._current_value)
    
    def test_digital_pin_set_high_low(self):
        """Test setting pin high and low"""
        from stickbot.gpio import DigitalPin
        
        pin = DigitalPin(18, self.mock_jetson_gpio.OUT, self.mock_jetson_gpio.LOW)
        
        # Test set_high
        pin.set_high()
        self.mock_jetson_gpio.output.assert_called_with(18, self.mock_jetson_gpio.HIGH)
        self.assertEqual(pin._current_value, self.mock_jetson_gpio.HIGH)
        
        # Test set_low
        pin.set_low()
        self.mock_jetson_gpio.output.assert_called_with(18, self.mock_jetson_gpio.LOW)
        self.assertEqual(pin._current_value, self.mock_jetson_gpio.LOW)
    
    def test_digital_pin_toggle(self):
        """Test pin toggling"""
        from stickbot.gpio import DigitalPin
        
        pin = DigitalPin(18, self.mock_jetson_gpio.OUT, self.mock_jetson_gpio.LOW)
        
        # Toggle from LOW to HIGH
        pin.toggle()
        self.assertEqual(pin._current_value, self.mock_jetson_gpio.HIGH)
        
        # Toggle from HIGH to LOW  
        pin.toggle()
        self.assertEqual(pin._current_value, self.mock_jetson_gpio.LOW)
    
    def test_digital_pin_read(self):
        """Test reading pin value"""
        from stickbot.gpio import DigitalPin
        
        pin = DigitalPin(16, self.mock_jetson_gpio.IN)
        
        # Mock input return value
        self.mock_jetson_gpio.input.return_value = self.mock_jetson_gpio.HIGH
        
        # Test read
        value = pin.read()
        self.mock_jetson_gpio.input.assert_called_with(16)
        self.assertEqual(value, self.mock_jetson_gpio.HIGH)
        self.assertEqual(pin._current_value, self.mock_jetson_gpio.HIGH)
    
    def test_digital_pin_input_only_operations(self):
        """Test that output operations fail on input pins"""
        from stickbot.gpio import DigitalPin
        
        pin = DigitalPin(16, self.mock_jetson_gpio.IN)
        
        # These should raise ValueError
        with self.assertRaises(ValueError):
            pin.set_high()
        
        with self.assertRaises(ValueError):
            pin.set_low()
        
        with self.assertRaises(ValueError):
            pin.toggle()
    
    def test_pwm_pin_creation(self):
        """Test creating a PWMPin"""
        from stickbot.gpio import PWMPin
        
        # Mock PWM object
        mock_pwm = MagicMock()
        self.mock_jetson_gpio.PWM.return_value = mock_pwm
        
        # Create PWM pin
        pwm_pin = PWMPin(33, 1000)
        
        # Verify setup calls
        self.mock_jetson_gpio.setmode.assert_called_with(self.mock_jetson_gpio.BOARD)
        self.mock_jetson_gpio.setup.assert_called_with(33, self.mock_jetson_gpio.OUT, initial=self.mock_jetson_gpio.LOW)
        self.mock_jetson_gpio.PWM.assert_called_with(33, 1000)
        
        # Test properties
        self.assertEqual(pwm_pin.pin_number, 33)
        self.assertEqual(pwm_pin.frequency, 1000)
        self.assertEqual(pwm_pin._duty_cycle, 0)
        self.assertFalse(pwm_pin._started)
    
    def test_pwm_pin_start_stop(self):
        """Test PWM start and stop"""
        from stickbot.gpio import PWMPin
        
        mock_pwm = MagicMock()
        self.mock_jetson_gpio.PWM.return_value = mock_pwm
        
        pwm_pin = PWMPin(33, 1000)
        
        # Test start
        pwm_pin.start(50)
        mock_pwm.start.assert_called_with(50)
        self.assertTrue(pwm_pin._started)
        self.assertEqual(pwm_pin._duty_cycle, 50)
        
        # Test stop
        pwm_pin.stop()
        mock_pwm.stop.assert_called_once()
        self.assertFalse(pwm_pin._started)
    
    def test_pwm_pin_change_frequency(self):
        """Test changing PWM frequency"""
        from stickbot.gpio import PWMPin
        
        mock_pwm = MagicMock()
        self.mock_jetson_gpio.PWM.return_value = mock_pwm
        
        pwm_pin = PWMPin(33, 1000)
        pwm_pin.start(25)
        
        # Change frequency
        pwm_pin.change_frequency(2000)
        mock_pwm.ChangeFrequency.assert_called_with(2000)
        self.assertEqual(pwm_pin.frequency, 2000)
    
    def test_pwm_pin_change_duty_cycle(self):
        """Test changing PWM duty cycle"""
        from stickbot.gpio import PWMPin
        
        mock_pwm = MagicMock()
        self.mock_jetson_gpio.PWM.return_value = mock_pwm
        
        pwm_pin = PWMPin(33, 1000)
        pwm_pin.start(25)
        
        # Change duty cycle
        pwm_pin.change_duty_cycle(75)
        mock_pwm.ChangeDutyCycle.assert_called_with(75)
        self.assertEqual(pwm_pin._duty_cycle, 75)
    
    def test_pwm_pin_invalid_duty_cycle(self):
        """Test PWM with invalid duty cycle values"""
        from stickbot.gpio import PWMPin
        
        mock_pwm = MagicMock()
        self.mock_jetson_gpio.PWM.return_value = mock_pwm
        
        pwm_pin = PWMPin(33, 1000)
        
        # Test invalid duty cycles
        with self.assertRaises(ValueError):
            pwm_pin.start(-10)
        
        with self.assertRaises(ValueError):
            pwm_pin.start(150)
        
        with self.assertRaises(ValueError):
            pwm_pin.change_duty_cycle(-5)
        
        with self.assertRaises(ValueError):
            pwm_pin.change_duty_cycle(105)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions"""
    
    def setUp(self):
        """Setup mock GPIO"""
        self.mock_gpio = MagicMock()
        self.mock_gpio.BOARD = 10
        self.mock_gpio.HIGH = 1
        self.mock_gpio.LOW = 0
        self.mock_gpio.model = "JETSON_ORIN_NANO"
        
        self.patcher = patch.dict('sys.modules', {'Jetson.GPIO': self.mock_gpio})
        self.patcher.start()
    
    def tearDown(self):
        """Cleanup patches"""
        self.patcher.stop()
    
    def test_setup_gpio(self):
        """Test GPIO setup function"""
        from stickbot.utils import setup_gpio
        
        result = setup_gpio()
        
        self.mock_gpio.setmode.assert_called_with(self.mock_gpio.BOARD)
        self.mock_gpio.setwarnings.assert_called_with(True)
        self.assertEqual(result, "JETSON_ORIN_NANO")
    
    def test_cleanup_gpio(self):
        """Test GPIO cleanup function"""
        from stickbot.utils import cleanup_gpio
        
        cleanup_gpio()
        
        self.mock_gpio.cleanup.assert_called_once()
    
    def test_get_available_pins(self):
        """Test getting available pins for known board"""
        from stickbot.utils import get_available_pins
        
        pins_info = get_available_pins()
        
        # Should return pin info for JETSON_ORIN_NANO
        self.assertIn('digital', pins_info)
        self.assertIn('pwm_capable', pins_info)
        self.assertIn(15, pins_info['pwm_capable'])
        self.assertIn(33, pins_info['pwm_capable'])


if __name__ == '__main__':
    unittest.main()