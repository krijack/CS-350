"""
CS 350 Final Project – Smart Thermostat (Simulation Version)
Author: Kristie Jackson
Description:
Simulated embedded thermostat demonstrating heating/cooling logic,
state machine control, and UART/LCD output — all without physical hardware.
"""

import time
import random
import datetime
from enum import Enum

# -------------------------------
# Configuration
# -------------------------------
UART_INTERVAL = 30      # seconds between UART updates (set to 5 for quick demo)
DISPLAY_REFRESH = 5     # seconds between screen updates
DEFAULT_SETPOINT = 72   # Fahrenheit

# -------------------------------
# Simulated Hardware Classes
# -------------------------------

class MockAHT20:
    """Simulated I²C temperature sensor"""
    def read_temperature(self):
        # Simulate realistic ambient temperature variation
        return round(random.uniform(65.0, 80.0), 1)

class MockLED:
    """Simulated GPIO LED"""
    def __init__(self, color):
        self.color = color
        self.state = "off"

    def fade(self):
        self.state = "fading"
        print(f"   [{self.color.upper()} LED] fading in/out...")

    def solid(self):
        self.state = "solid"
        print(f"   [{self.color.upper()} LED] solid on.")

    def off(self):
        self.state = "off"
        print(f"   [{self.color.upper()} LED] off.")

class MockLCD:
    """Simulated LCD Display"""
    def display(self, line1, line2):
        print(f"\n[LCD DISPLAY]")
        print(f"{line1}")
        print(f"{line2}")
        print("-" * 40)

class MockUART:
    """Simulated UART Communication"""
    def send(self, data):
        print(f"[UART OUTPUT] {data}")

# -------------------------------
# State Machine
# -------------------------------
class ThermostatState(Enum):
    OFF = 0
    HEAT = 1
    COOL = 2

class SmartThermostat:
    """Main thermostat logic"""
    def __init__(self):
        self.sensor = MockAHT20()
        self.red_led = MockLED("red")
        self.blue_led = MockLED("blue")
        self.lcd = MockLCD()
        self.uart = MockUART()
        self.state = ThermostatState.OFF
        self.set_point = DEFAULT_SETPOINT
        self.last_uart_time = time.time()

    def toggle_state(self):
        if self.state == ThermostatState.OFF:
            self.state = ThermostatState.HEAT
        elif self.state == ThermostatState.HEAT:
            self.state = ThermostatState.COOL
        else:
            self.state = ThermostatState.OFF
        print(f"\n[STATE CHANGE] → {self.state.name}")

    def increase_setpoint(self):
        self.set_point += 1
        print(f"[INPUT] Set point increased to {self.set_point}°F")

    def decrease_setpoint(self):
        self.set_point -= 1
        print(f"[INPUT] Set point decreased to {self.set_point}°F")

    def control_logic(self, current_temp):
        """Core control logic simulating LEDs and heating/cooling"""
        self.red_led.off()
        self.blue_led.off()

        if self.state == ThermostatState.HEAT:
            if current_temp < self.set_point:
                self.red_led.fade()
            else:
                self.red_led.solid()
        elif self.state == ThermostatState.COOL:
            if current_temp > self.set_point:
                self.blue_led.fade()
            else:
                self.blue_led.solid()
        else:
            # OFF state, both LEDs off
            pass

    def update_display(self, current_temp):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line1 = f"{now}"
        line2 = f"Mode: {self.state.name:<4} | Cur: {current_temp:.1f}°F | Set: {self.set_point}°F"
        self.lcd.display(line1, line2)

    def send_uart_update(self, current_temp):
        """Send UART output every interval"""
        if time.time() - self.last_uart_time >= UART_INTERVAL:
            data = f"{self.state.name},{current_temp:.1f},{self.set_point}"
            self.uart.send(data)
            self.last_uart_time = time.time()

    def run(self):
        """Main simulation loop"""
        print("\n--- SMART THERMOSTAT SIMULATION STARTED ---")
        print("Controls: [1] Toggle mode  [2] Temp +  [3] Temp -  [Enter] Continue  [q] Quit")
        while True:
            current_temp = self.sensor.read_temperature()
            self.update_display(current_temp)
            self.control_logic(current_temp)
            self.send_uart_update(current_temp)

            # Simulate button interrupts with keyboard input
            user_input = input("\nPress a button (1/2/3/q): ").strip().lower()
            if user_input == "1":
                self.toggle_state()
            elif user_input == "2":
                self.increase_setpoint()
            elif user_input == "3":
                self.decrease_setpoint()
            elif user_input == "q":
                print("\nShutting down thermostat simulation...")
                break
            else:
                print("[NO INPUT] Continuing...")

            time.sleep(DISPLAY_REFRESH)

# -------------------------------1
# Main Execution
# -------------------------------
if __name__ == "__main__":
    thermostat = SmartThermostat()
    thermostat.run()
