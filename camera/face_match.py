"""
Face Match Module
Handles face recognition and matching for driver authorization.
"""

import face_recognition
import cv2
import os
import numpy as np
from utils.config import (
    LICENSE_IMAGE_PATH,
    FACE_MATCH_TOLERANCE,
    FACE_DETECTION_MODEL
)


def _load_stored_face_encodings():
    """
    Load and encode all stored license images.
    
    Returns:
        list: List of face encodings from stored license images
    """
    stored_encodings = []
    
    # Check if directory exists
    if not os.path.exists(LICENSE_IMAGE_PATH):
        return stored_encodings
    
    # Get all image files from license directory
    image_files = [f for f in os.listdir(LICENSE_IMAGE_PATH) 
                   if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    # Load and encode each stored license image
    for image_file in image_files:
        image_path = os.path.join(LICENSE_IMAGE_PATH, image_file)
        
        try:
            # Load image
            image = face_recognition.load_image_file(image_path)
            
            # Get face encodings
            encodings = face_recognition.face_encodings(
                image, 
                model=FACE_DETECTION_MODEL
            )
            
            # Add encoding if face detected
            if len(encodings) > 0:
                stored_encodings.append(encodings[0])
                
        except Exception as e:
            continue
    
    return stored_encodings


def _get_face_encoding(image_path):
    """
    Get face encoding from a single image.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        numpy.ndarray: Face encoding or None if no face detected
    """
    try:
        # Load image
        image = face_recognition.load_image_file(image_path)
        
        # Get face encodings
        encodings = face_recognition.face_encodings(
            image,
            model=FACE_DETECTION_MODEL
        )
        
        # Return first encoding if face detected
        if len(encodings) > 0:
            return encodings[0]
        else:
            return None
            
    except Exception as e:
        return None


def compare_face_with_database(live_image_path):
    """
    Compare live face image with stored license images in database.
    
    Args:
        live_image_path (str): Path to the live captured face image
        
    Returns:
        bool: True if authorized driver found, False otherwise
    """
    # Get encoding for live face
    live_encoding = _get_face_encoding(live_image_path)
    
    # No face detected in live image
    if live_encoding is None:
        return False
    
    # Load all stored face encodings
    stored_encodings = _load_stored_face_encodings()
    
    # No stored faces to compare
    if len(stored_encodings) == 0:
        return False
    
    # Compare live face with all stored faces
    matches = face_recognition.compare_faces(
        stored_encodings,
        live_encoding,
        tolerance=FACE_MATCH_TOLERANCE
    )
    
    # Check if any match found
    if True in matches:
        return True
    else:
        return False