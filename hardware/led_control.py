"""
LED Control Module
Handles red and green LED indicators for vehicle ignition status.
"""

import RPi.GPIO as GPIO
from utils.config import RED_LED_PIN, GREEN_LED_PIN


def turn_on_red_led():
    """
    Turn ON the red LED (indicates ignition OFF state).
    """
    GPIO.output(RED_LED_PIN, GPIO.HIGH)


def turn_off_red_led():
    """
    Turn OFF the red LED.
    """
    GPIO.output(RED_LED_PIN, GPIO.LOW)


def turn_on_green_led():
    """
    Turn ON the green LED (indicates ignition ON state).
    """
    GPIO.output(GREEN_LED_PIN, GPIO.HIGH)


def turn_off_green_led():
    """
    Turn OFF the green LED.
    """
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)
    