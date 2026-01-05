"""
Configuration File
Stores all constants and configurable settings for the vehicle safety system.
"""

# ============================================================================
# GPIO Pin Configuration (BCM numbering)
# ============================================================================

# LED pins
RED_LED_PIN = 17        # GPIO 17 - Red LED (ignition OFF indicator)
GREEN_LED_PIN = 27      # GPIO 27 - Green LED (ignition ON indicator)

# Relay pin
RELAY_PIN = 22          # GPIO 22 - Relay module (controls DC motor)

# Button pin
BUTTON_PIN = 23         # GPIO 23 - Push button (ignition attempt)


# ============================================================================
# Button Configuration
# ============================================================================

DEBOUNCE_DELAY = 0.05   # Debounce delay in seconds (50ms)


# ============================================================================
# Camera Configuration
# ============================================================================

CAMERA_RESOLUTION = (640, 480)      # Camera capture resolution (width, height)
CAMERA_WARMUP_TIME = 2              # Camera warmup time in seconds

# Image storage paths
LIVE_FACE_IMAGE_PATH = "data/live_captures/"
LICENSE_IMAGE_PATH = "data/licenses/"


# ============================================================================
# Database Configuration
# ============================================================================

DATABASE_PATH = "data/vehicle_safety.db"
DATABASE_TABLE_NAME = "authorized_drivers"


# ============================================================================
# Face Recognition Configuration
# ============================================================================

FACE_MATCH_TOLERANCE = 0.6          # Lower is more strict (0.0 - 1.0)
FACE_DETECTION_MODEL = "hog"        # Options: "hog" (faster) or "cnn" (more accurate)


# ============================================================================
# System Configuration
# ============================================================================

SYSTEM_NAME = "Vehicle Safety Prototype"
VERSION = "1.0.0"