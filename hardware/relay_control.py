"""
Relay Control Module
Handles relay module that controls DC motor (vehicle ignition).
"""

import RPi.GPIO as GPIO
from utils.config import RELAY_PIN


def activate_relay():
    """
    Activate the relay to turn ON the DC motor (vehicle ignition ON).
    """
    GPIO.output(RELAY_PIN, GPIO.HIGH)


def deactivate_relay():
    """
    Deactivate the relay to turn OFF the DC motor (vehicle ignition OFF).
    """
    GPIO.output(RELAY_PIN, GPIO.LOW)