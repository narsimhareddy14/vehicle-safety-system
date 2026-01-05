#!/usr/bin/env python3
"""
Vehicle Safety Prototype - Main Control System
Raspberry Pi 4 - Linux (Raspberry Pi OS)

This system controls vehicle ignition based on facial recognition authorization.
"""

import time
import sys
from hardware.gpio_control import initialize_gpio, cleanup_gpio
from hardware.led_control import turn_on_red_led, turn_off_red_led, turn_on_green_led, turn_off_green_led
from hardware.relay_control import activate_relay, deactivate_relay
from hardware.button_input import wait_for_button_press, is_button_pressed
from camera.camera_capture import capture_live_face, capture_license_photo
from camera.face_match import compare_face_with_database
from database.db_manager import initialize_database, store_new_registration


def initialize_system():
    """Initialize all system components on startup"""
    print("Initializing Vehicle Safety System...")
    
    # Initialize GPIO pins
    initialize_gpio()
    
    # Initialize camera
    print("Camera initialization handled by camera module")
    
    # Initialize database
    initialize_database()
    
    # Set initial state: ignition OFF
    turn_on_red_led()
    turn_off_green_led()
    deactivate_relay()
    
    print("System initialized. Red LED ON - Ignition OFF")
    print("Waiting for ignition attempt...")


def handle_ignition_attempt():
    """Process driver authorization when button is pressed"""
    print("\nIgnition attempt detected - Button pressed")
    print("Capturing live driver face...")
    
    # Capture live face from camera
    live_face_image = capture_live_face()
    
    if live_face_image is None:
        print("Error: Failed to capture face. Please try again.")
        return
    
    print("Comparing face with authorized drivers...")
    
    # Compare captured face with database
    match_found = compare_face_with_database(live_face_image)
    
    if match_found:
        # Authorization successful
        print("✓ Driver authorized - Match found")
        print("Starting vehicle...")
        
        # Turn OFF red LED
        turn_off_red_led()
        
        # Turn ON green LED
        turn_on_green_led()
        
        # Activate relay to start motor
        activate_relay()
        
        print("Green LED ON - Ignition ON")
        print("Motor running - Vehicle operational")
        
    else:
        # No match found - new registration
        print("✗ Driver not authorized - No match found")
        print("Capturing license photo for registration...")
        
        # Capture driver license photo
        license_photo = capture_license_photo()
        
        if license_photo is not None:
            # Store new registration in database
            store_new_registration(license_photo)
            print("New driver registered successfully")
        else:
            print("Error: Failed to capture license photo")
        
        # Keep ignition OFF
        print("Ignition remains OFF - Red LED ON")


def main():
    """Main control loop"""
    try:
        # Initialize system on startup
        initialize_system()
        
        # Continuous operation loop
        while True:
            # Wait for push button press
            wait_for_button_press()
            
            # Process ignition attempt
            handle_ignition_attempt()
            
            # Small delay to debounce button
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\nShutdown signal received")
        print("Stopping system safely...")
        
    except Exception as e:
        # Handle unexpected errors
        print(f"\nError occurred: {str(e)}")
        print("Shutting down system...")
        
    finally:
        # Cleanup before exit
        print("Turning OFF all components...")
        turn_off_green_led()
        turn_on_red_led()
        deactivate_relay()
        
        print("Cleaning up GPIO...")
        cleanup_gpio()
        
        print("System shutdown complete")
        sys.exit(0)


if __name__ == "__main__":
    main()