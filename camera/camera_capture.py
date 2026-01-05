"""
Camera Capture Module
Handles camera operations for capturing driver face and license images.
"""

import cv2
import os
import time
from datetime import datetime
from utils.config import (
    CAMERA_RESOLUTION,
    CAMERA_WARMUP_TIME,
    LIVE_FACE_IMAGE_PATH,
    LICENSE_IMAGE_PATH
)


def _initialize_camera():
    """
    Initialize and configure the camera.
    
    Returns:
        cv2.VideoCapture: Configured camera object or None if initialization fails
    """
    camera = cv2.VideoCapture(0)
    
    if not camera.isOpened():
        return None
    
    # Set camera resolution
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_RESOLUTION[0])
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_RESOLUTION[1])
    
    # Allow camera to warm up
    time.sleep(CAMERA_WARMUP_TIME)
    
    return camera


def _ensure_directory_exists(directory_path):
    """
    Create directory if it does not exist.
    
    Args:
        directory_path (str): Path to the directory
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def _generate_filename(prefix):
    """
    Generate a unique filename with timestamp.
    
    Args:
        prefix (str): Filename prefix
        
    Returns:
        str: Generated filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.jpg"


def capture_live_face():
    """
    Capture live driver face image.
    
    Returns:
        str: Path to the saved image file, or None if capture fails
    """
    # Ensure storage directory exists
    _ensure_directory_exists(LIVE_FACE_IMAGE_PATH)
    
    # Initialize camera
    camera = _initialize_camera()
    
    if camera is None:
        return None
    
    try:
        # Capture frame
        ret, frame = camera.read()
        
        if not ret or frame is None:
            return None
        
        # Generate filename and full path
        filename = _generate_filename("live_face")
        filepath = os.path.join(LIVE_FACE_IMAGE_PATH, filename)
        
        # Save image
        cv2.imwrite(filepath, frame)
        
        return filepath
        
    except Exception as e:
        return None
        
    finally:
        # Release camera resource
        camera.release()


def capture_license_photo():
    """
    Capture driver license photo for new registration.
    
    Returns:
        str: Path to the saved image file, or None if capture fails
    """
    # Ensure storage directory exists
    _ensure_directory_exists(LICENSE_IMAGE_PATH)
    
    # Initialize camera
    camera = _initialize_camera()
    
    if camera is None:
        return None
    
    try:
        # Capture frame
        ret, frame = camera.read()
        
        if not ret or frame is None:
            return None
        
        # Generate filename and full path
        filename = _generate_filename("license")
        filepath = os.path.join(LICENSE_IMAGE_PATH, filename)
        
        # Save image
        cv2.imwrite(filepath, frame)
        
        return filepath
        
    except Exception as e:
        return None
        
    finally:
        # Release camera resource
        camera.release()