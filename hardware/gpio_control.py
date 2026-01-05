"""
GPIO Control Module
Handles GPIO initialization and cleanup for vehicle safety system.
"""

import RPi.GPIO as GPIO
from utils.config import RED_LED_PIN, GREEN_LED_PIN, RELAY_PIN, BUTTON_PIN


def initialize_gpio():
    """
    Initialize GPIO pins for the vehicle safety system.
    Sets up BCM mode, configures pin directions, and sets initial states.
    """
    # Disable GPIO warnings
    GPIO.setwarnings(False)
    
    # Set GPIO mode to BCM numbering
    GPIO.setmode(GPIO.BCM)
    
    # Configure LED pins as OUTPUT
    GPIO.setup(RED_LED_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(GREEN_LED_PIN, GPIO.OUT, initial=GPIO.LOW)
    
    # Configure relay pin as OUTPUT (initial state OFF)
    GPIO.setup(RELAY_PIN, GPIO.OUT, initial=GPIO.LOW)
    
    # Configure button pin as INPUT with internal pull-up resistor
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def cleanup_gpio():
    """
    Safely release all GPIO resources.
    Should be called before program exit.
    """
    GPIO.cleanup()