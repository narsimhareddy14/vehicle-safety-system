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
            driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
            license_image_path TEXT NOT NULL,
            registered_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create login_history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver_id INTEGER,
            status TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (driver_id) REFERENCES drivers(driver_id)
        )
    """)
    
    # Create gps_logs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gps_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create alcohol_logs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alcohol_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alcohol_level REAL NOT NULL,
            status TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()


def add_driver(license_image_path):
    """
    Add a new driver to the database.
    
    Args:
        license_image_path (str): Path to the driver's license image
        
    Returns:
        int: The driver_id of the newly added driver
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO drivers (license_image_path, registered_at)
        VALUES (?, ?)
    """, (license_image_path, datetime.now()))
    
    driver_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return driver_id


def log_login_attempt(driver_id, status):
    """
    Log a login/ignition attempt.
    
    Args:
        driver_id (int or None): Driver ID if recognized, None otherwise
        status (str): 'authorized' or 'denied'
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO login_history (driver_id, status, timestamp)
        VALUES (?, ?, ?)
    """, (driver_id, status, datetime.now()))
    
    conn.commit()
    conn.close()


def log_gps_data(latitude, longitude):
    """
    Log GPS location data.
    
    Args:
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO gps_logs (latitude, longitude, timestamp)
        VALUES (?, ?, ?)
    """, (latitude, longitude, datetime.now()))
    
    conn.commit()
    conn.close()


def log_alcohol_data(alcohol_level, status):
    """
    Log alcohol sensor reading.
    
    Args:
        alcohol_level (float): Alcohol level reading
        status (str): 'safe' or 'unsafe'
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO alcohol_logs (alcohol_level, status, timestamp)
        VALUES (?, ?, ?)
    """, (alcohol_level, status, datetime.now()))
    
    conn.commit()
    conn.close()


def get_all_drivers():
    """
    Retrieve all registered drivers.
    
    Returns:
        list: List of driver records as dictionaries
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT driver_id, license_image_path, registered_at
        FROM drivers
        ORDER BY registered_at DESC
    """)
    
    drivers = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return drivers


def get_login_history(limit=100):
    """
    Retrieve login/ignition attempt history.
    
    Args:
        limit (int): Maximum number of records to retrieve
        
    Returns:
        list: List of login attempt records as dictionaries
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, driver_id, status, timestamp
        FROM login_history
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))
    
    history = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return history


def get_latest_gps(limit=100):
    """
    Retrieve latest GPS logs.
    
    Args:
        limit (int): Maximum number of records to retrieve
        
    Returns:
        list: List of GPS log records as dictionaries
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, latitude, longitude, timestamp
        FROM gps_logs
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))
    
    gps_logs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return gps_logs


def get_alcohol_logs(limit=100):
    """
    Retrieve alcohol sensor logs.
    
    Args:
        limit (int): Maximum number of records to retrieve
        
    Returns:
        list: List of alcohol log records as dictionaries
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, alcohol_level, status, timestamp
        FROM alcohol_logs
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))
    
    alcohol_logs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return alcohol_logs


def store_new_registration(license_image_path):
    """
    Store a new driver registration (convenience wrapper).
    
    Args:
        license_image_path (str): Path to the driver's license image
        
    Returns:
        int: The driver_id of the newly registered driver
    """
    return add_driver(license_image_path)