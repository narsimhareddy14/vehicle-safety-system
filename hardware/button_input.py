"""
Button Input Module
Handles push button input for vehicle ignition attempts.
"""

import RPi.GPIO as GPIO
import time
from utils.config import BUTTON_PIN, DEBOUNCE_DELAY


def is_button_pressed():
    """
    Check if the button is currently pressed (non-blocking).
    
    Returns:
        bool: True if button is pressed, False otherwise
    """
    # Button is active LOW (pressed = LOW)
    return GPIO.input(BUTTON_PIN) == GPIO.LOW


def wait_for_button_press():
    """
    Block execution until button is pressed and released.
    Includes software debouncing to prevent false triggers.
    """
    # Wait until button is pressed (goes LOW)
    while GPIO.input(BUTTON_PIN) == GPIO.HIGH:
        time.sleep(0.01)
    
    # Debounce delay
    time.sleep(DEBOUNCE_DELAY)
    
    # Wait until button is released (goes HIGH)
    while GPIO.input(BUTTON_PIN) == GPIO.LOW:
        time.sleep(0.01)
    
    # Debounce delay after release
    time.sleep(DEBOUNCE_DELAY)