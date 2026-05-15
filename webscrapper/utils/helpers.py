"""
Helper utilities for the School Digital Gap Scanner
"""

import logging
from typing import Optional, Dict, List
from urllib.parse import urlparse
import re

logger = logging.getLogger(__name__)


def format_url(url: Optional[str]) -> Optional[str]:
    """
    Normalize and format URL
    
    Args:
        url: URL string or None
        
    Returns:
        Formatted URL or None
    """
    if not url:
        return None
    
    url = url.strip()
    
    # Add https:// if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    return url


def extract_domain(url: Optional[str]) -> Optional[str]:
    """
    Extract domain from URL
    
    Args:
        url: Full URL
        
    Returns:
        Domain name or None
    """
    if not url:
        return None
    
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        # Remove www. prefix if present
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain
    except Exception as e:
        logger.error("Error extracting domain from %s: %s", url, str(e))
        return None


def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email string
        
    Returns:
        True if valid email format
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format
    
    Args:
        phone: Phone number string
        
    Returns:
        True if valid phone format
    """
    # Remove common separators
    clean = re.sub(r'[\s\-\(\)\.]+', '', phone)
    # Check if remaining is numeric and 7-15 digits
    return clean.isdigit() and 7 <= len(clean) <= 15


def get_score_status_emoji(score: float) -> str:
    """
    Get emoji indicator for score
    
    Args:
        score: Digital quality score (0-100)
        
    Returns:
        Emoji indicator
    """
    if score >= 85:
        return '🟢'  # Green - Excellent
    elif score >= 65:
        return '🟡'  # Yellow - Good
    elif score >= 50:
        return '🟠'  # Orange - Fair
    else:
        return '🔴'  # Red - Poor


def get_gap_type_icon(gap_type: str) -> str:
    """
    Get icon for gap type
    
    Args:
        gap_type: Type of digital gap
        
    Returns:
        Icon emoji
    """
    icons = {
        'No Digital Presence': '❌',
        'Broken Website': '🔗',
        'Security Gap': '🔒',
        'Mobile Gap': '📱',
        'Outdated Design': '📅',
        'Opportunity for Enhancement': '💡',
    }
    return icons.get(gap_type, '❓')


def format_file_size(size_bytes: int) -> str:
    """
    Format file size to human-readable format
    
    Args:
        size_bytes: File size in bytes
        
    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f}TB"


def truncate_text(text: str, max_length: int = 50) -> str:
    """
    Truncate text to max length with ellipsis
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + '...'


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file storage
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove/replace invalid characters
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '_', filename)
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip('. ')
    # Limit length
    if len(sanitized) > 200:
        name, ext = sanitized.rsplit('.', 1) if '.' in sanitized else (sanitized, '')
        sanitized = name[:197] + ('.' + ext if ext else '')
    return sanitized


def chunk_list(items: List, chunk_size: int) -> List[List]:
    """
    Split list into chunks
    
    Args:
        items: List to chunk
        chunk_size: Size of each chunk
        
    Returns:
        List of chunks
    """
    chunks = []
    for i in range(0, len(items), chunk_size):
        chunks.append(items[i:i + chunk_size])
    return chunks
