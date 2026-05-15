"""
Helper utilities for the Route Explorer app
"""

from typing import Dict, Tuple

def format_distance(meters: float) -> str:
    """
    Format distance in meters to readable format
    
    Args:
        meters: Distance in meters
        
    Returns:
        Formatted distance string (km or m)
    """
    if meters >= 1000:
        return f"{meters / 1000:.1f} km"
    return f"{meters:.0f} m"

def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to readable format
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string (hours:minutes)
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"

def validate_coordinates(lat: float, lon: float) -> bool:
    """
    Validate latitude and longitude values
    
    Args:
        lat: Latitude
        lon: Longitude
        
    Returns:
        True if valid, False otherwise
    """
    return -90 <= lat <= 90 and -180 <= lon <= 180
