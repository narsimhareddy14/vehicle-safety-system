"""
Database Manager Module
Handles all SQLite database operations for the vehicle safety system.
"""

import sqlite3
from datetime import datetime
from utils.config import DATABASE_PATH


def get_connection():
    """
    Create and return a database connection.
    
    Returns:
        sqlite3.Connection: Database connection object
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    """
    Initialize the database and create all required tables if they don't exist.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create drivers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            license_image_path TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create login_history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()


def store_new_registration(license_image_path):
    """
    Store a new driver registration.
    
    Args:
        license_image_path (str): Path to the driver's license image
        
    Returns:
        int: The id of the newly registered driver
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO drivers (license_image_path, created_at)
        VALUES (?, ?)
    """, (license_image_path, datetime.now()))
    
    driver_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return driver_id


def log_login_attempt(status):
    """
    Log an ignition attempt.
    
    Args:
        status (str): 'AUTHORIZED' or 'UNAUTHORIZED'
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO login_history (status, timestamp)
        VALUES (?, ?)
    """, (status, datetime.now()))
    
    conn.commit()
    conn.close()