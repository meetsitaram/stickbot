#!/home/stick/solo_venv/bin/python3
"""
NVIDIA Orin Nano GPIO Pin Diagram and Reference

This file provides a visual reference for the 40-pin GPIO header
on the NVIDIA Orin Nano development board.

The pinout follows the Raspberry Pi standard layout.
Pin numbering uses BOARD mode (physical pin numbers 1-40).
"""

def print_gpio_pinout():
    """Print a visual diagram of the 40-pin GPIO header"""
    print("NVIDIA Orin Nano - 40-Pin GPIO Header")
    print("=" * 50)
    print("Pin numbering: BOARD mode (physical pins 1-40)")
    print("Orientation: USB ports facing down")
    print()
    
    print("    3.3V  (1) ● ● (2)  5V")
    print("   GPIO2  (3) ● ● (4)  5V")  
    print("   GPIO3  (5) ● ● (6)  GND")
    print("   GPIO4  (7) ● ● (8)  GPIO14")
    print("     GND  (9) ● ● (10) GPIO15")
    print("  GPIO17 (11) ● ● (12) GPIO18")
    print("  GPIO27 (13) ● ● (14) GND")
    print("  GPIO22 (15) ● ● (16) GPIO23")
    print("    3.3V (17) ● ● (18) GPIO24")
    print("  GPIO10 (19) ● ● (20) GND")
    print("   GPIO9 (21) ● ● (22) GPIO25")
    print("  GPIO11 (23) ● ● (24) GPIO8")
    print("     GND (25) ● ● (26) GPIO7")
    print("   GPIO0 (27) ● ● (28) GPIO1")
    print("   GPIO5 (29) ● ● (30) GND")
    print("   GPIO6 (31) ● ● (32) GPIO12")
    print("  GPIO13 (33) ● ● (34) GND")
    print("  GPIO19 (35) ● ● (36) GPIO16")
    print("  GPIO26 (37) ● ● (38) GPIO20")
    print("     GND (39) ● ● (40) GPIO21")
    print()


def print_pin_functions():
    """Print detailed pin function information"""
    print("Pin Function Reference (BOARD numbering)")
    print("=" * 45)
    print()
    
    print("POWER PINS:")
    print("-----------")
    print("Pin  1: 3.3V Power")
    print("Pin  2: 5V Power") 
    print("Pin  4: 5V Power")
    print("Pin 17: 3.3V Power")
    print()
    
    print("GROUND PINS:")
    print("------------")
    ground_pins = [6, 9, 14, 20, 25, 30, 34, 39]
    for pin in ground_pins:
        print(f"Pin {pin:2d}: Ground (GND)")
    print()
    
    print("GPIO PINS (Digital I/O):")
    print("-------------------------")
    gpio_pins = [7, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 26, 29, 31, 32, 33, 35, 36, 37, 38, 40]
    for pin in gpio_pins:
        print(f"Pin {pin:2d}: Digital I/O")
    print()
    
    print("PWM-CAPABLE PINS:")
    print("-----------------")
    print("Pin 15: PWM capable (may need pinmux config)")
    print("Pin 33: PWM capable (may need pinmux config)")
    print()
    
    print("SPECIAL FUNCTION PINS:")
    print("----------------------")
    print("Pin  3: I2C1 SDA (GPIO2)")
    print("Pin  5: I2C1 SCL (GPIO3)")
    print("Pin  8: UART TX (GPIO14)")
    print("Pin 10: UART RX (GPIO15)")
    print("Pin 19: SPI MOSI (GPIO10)")
    print("Pin 21: SPI MISO (GPIO9)")
    print("Pin 23: SPI SCLK (GPIO11)")
    print("Pin 24: SPI CE0 (GPIO8)")
    print("Pin 26: SPI CE1 (GPIO7)")
    print()


def print_pinmux_commands():
    """Print pinmux configuration commands for PWM"""
    print("PWM Pinmux Configuration Commands")
    print("=" * 35)
    print("Some PWM pins may require hardware configuration:")
    print()
    print("Enable PWM on Pin 15:")
    print("sudo busybox devmem 0x02440020 32 0x400")
    print()
    print("Enable PWM on Pin 33:")
    print("sudo busybox devmem 0x02434040 32 0x401")
    print()
    print("Note: These commands are temporary (until reboot).")
    print("For permanent configuration, modify the device tree.")
    print()


def print_wiring_examples():
    """Print common wiring examples"""
    print("Common Wiring Examples")
    print("=" * 22)
    print()
    
    print("LED CONNECTION:")
    print("---------------")
    print("LED Anode (long leg) → GPIO Pin (e.g., Pin 18)")
    print("LED Cathode (short leg) → 330Ω Resistor → Ground (e.g., Pin 6)")
    print()
    
    print("BUTTON CONNECTION:")
    print("------------------")
    print("Button Terminal 1 → GPIO Pin (e.g., Pin 16)")
    print("Button Terminal 2 → Ground (e.g., Pin 6)")
    print("Note: Use internal pull-up in software")
    print()
    
    print("SERVO CONNECTION:")
    print("-----------------")
    print("Servo Red Wire → 5V (Pin 2 or Pin 4)")
    print("Servo Black/Brown Wire → Ground (e.g., Pin 6)")
    print("Servo Orange/Yellow Wire → PWM Pin (Pin 15 or Pin 33)")
    print()
    
    print("SENSOR CONNECTION (3.3V):")
    print("--------------------------")
    print("Sensor VCC → 3.3V (Pin 1 or Pin 17)")
    print("Sensor GND → Ground (e.g., Pin 6)")
    print("Sensor Signal → GPIO Pin (e.g., Pin 18)")
    print()


def get_pin_info(pin_number):
    """Get information about a specific pin"""
    pin_data = {
        1: {"function": "3.3V Power", "type": "power"},
        2: {"function": "5V Power", "type": "power"},
        3: {"function": "GPIO2 (I2C1 SDA)", "type": "gpio"},
        4: {"function": "5V Power", "type": "power"},
        5: {"function": "GPIO3 (I2C1 SCL)", "type": "gpio"},
        6: {"function": "Ground", "type": "ground"},
        7: {"function": "GPIO4", "type": "gpio"},
        8: {"function": "GPIO14 (UART TX)", "type": "gpio"},
        9: {"function": "Ground", "type": "ground"},
        10: {"function": "GPIO15 (UART RX)", "type": "gpio"},
        11: {"function": "GPIO17", "type": "gpio"},
        12: {"function": "GPIO18", "type": "gpio"},
        13: {"function": "GPIO27", "type": "gpio"},
        14: {"function": "Ground", "type": "ground"},
        15: {"function": "GPIO22 (PWM capable)", "type": "gpio_pwm"},
        16: {"function": "GPIO23", "type": "gpio"},
        17: {"function": "3.3V Power", "type": "power"},
        18: {"function": "GPIO24", "type": "gpio"},
        19: {"function": "GPIO10 (SPI MOSI)", "type": "gpio"},
        20: {"function": "Ground", "type": "ground"},
        21: {"function": "GPIO9 (SPI MISO)", "type": "gpio"},
        22: {"function": "GPIO25", "type": "gpio"},
        23: {"function": "GPIO11 (SPI SCLK)", "type": "gpio"},
        24: {"function": "GPIO8 (SPI CE0)", "type": "gpio"},
        25: {"function": "Ground", "type": "ground"},
        26: {"function": "GPIO7 (SPI CE1)", "type": "gpio"},
        27: {"function": "GPIO0 (I2C0 SDA)", "type": "gpio"},
        28: {"function": "GPIO1 (I2C0 SCL)", "type": "gpio"},
        29: {"function": "GPIO5", "type": "gpio"},
        30: {"function": "Ground", "type": "ground"},
        31: {"function": "GPIO6", "type": "gpio"},
        32: {"function": "GPIO12", "type": "gpio"},
        33: {"function": "GPIO13 (PWM capable)", "type": "gpio_pwm"},
        34: {"function": "Ground", "type": "ground"},
        35: {"function": "GPIO19", "type": "gpio"},
        36: {"function": "GPIO16", "type": "gpio"},
        37: {"function": "GPIO26", "type": "gpio"},
        38: {"function": "GPIO20", "type": "gpio"},
        39: {"function": "Ground", "type": "ground"},
        40: {"function": "GPIO21", "type": "gpio"}
    }
    
    if pin_number in pin_data:
        return pin_data[pin_number]
    else:
        return {"function": "Invalid pin", "type": "invalid"}


def interactive_pin_lookup():
    """Interactive pin information lookup"""
    print("Interactive Pin Lookup")
    print("=" * 22)
    print("Enter pin numbers (1-40) to get information, or 'q' to quit")
    print()
    
    while True:
        try:
            user_input = input("Enter pin number: ").strip()
            
            if user_input.lower() in ['q', 'quit', 'exit']:
                break
                
            pin_number = int(user_input)
            
            if not 1 <= pin_number <= 40:
                print("Error: Pin number must be between 1 and 40")
                continue
                
            pin_info = get_pin_info(pin_number)
            
            print(f"Pin {pin_number:2d}: {pin_info['function']}")
            
            if pin_info['type'] == 'gpio':
                print("        → Digital I/O capable")
            elif pin_info['type'] == 'gpio_pwm':
                print("        → Digital I/O + PWM capable")
            elif pin_info['type'] == 'power':
                print("        → Power supply pin")
            elif pin_info['type'] == 'ground':
                print("        → Ground connection")
            print()
            
        except ValueError:
            print("Error: Please enter a valid number or 'q' to quit")
        except KeyboardInterrupt:
            print("\nExiting...")
            break


def main():
    """Main function with menu system"""
    while True:
        print("\n" + "="*60)
        print("NVIDIA Orin Nano GPIO Pin Reference Tool")
        print("="*60)
        print("1. Show GPIO Pinout Diagram")
        print("2. Show Pin Functions")
        print("3. Show PWM Configuration Commands") 
        print("4. Show Wiring Examples")
        print("5. Interactive Pin Lookup")
        print("6. Show All Information")
        print("0. Exit")
        print()
        
        try:
            choice = input("Select option (0-6): ").strip()
            
            if choice == '0':
                print("Goodbye!")
                break
            elif choice == '1':
                print()
                print_gpio_pinout()
            elif choice == '2':
                print()
                print_pin_functions()
            elif choice == '3':
                print()
                print_pinmux_commands()
            elif choice == '4':
                print()
                print_wiring_examples()
            elif choice == '5':
                print()
                interactive_pin_lookup()
            elif choice == '6':
                print()
                print_gpio_pinout()
                print()
                print_pin_functions()
                print()
                print_pinmux_commands()
                print()
                print_wiring_examples()
            else:
                print("Invalid choice. Please select 0-6.")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
            
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()