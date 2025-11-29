import re
from typing import List, Dict


def validate_email(email):
    """
    Validate email format
    Args:
        email: Email string
    Returns:
        bool: True if valid, False otherwise
    """
    if not email or not isinstance(email, str):
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password(password):
    """
    Validate password (minimum 6 characters)
    Args:
        password: Password string
    Returns:
        bool: True if valid, False otherwise
    """
    if not password or not isinstance(password, str):
        return False
    return len(password) >= 6


def validate_playlist_songs(songs):
    """
    Validate playlist songs (must be exactly 10 songs with song_name and artist_name)
    Args:
        songs: List of song dictionaries
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if not isinstance(songs, list):
        return False, "Songs must be an array"
    
    if len(songs) != 10:
        return False, "Playlist must contain exactly 10 songs"
    
    for i, song in enumerate(songs):
        if not isinstance(song, dict):
            return False, f"Song at index {i} must be an object"
        
        if 'song_name' not in song or 'artist_name' not in song:
            return False, f"Song at index {i} must have 'song_name' and 'artist_name' fields"
        
        if not isinstance(song['song_name'], str) or not song['song_name'].strip():
            return False, f"Song at index {i} must have a non-empty 'song_name'"
        
        if not isinstance(song['artist_name'], str) or not song['artist_name'].strip():
            return False, f"Song at index {i} must have a non-empty 'artist_name'"
    
    return True, None


def validate_arrays(field_name, value, required=False):
    """
    Validate array fields (favorite_songs, favorite_artists, favorite_genres)
    Args:
        field_name: Name of the field
        value: Value to validate
        required: Whether the field is required
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if required and (not value or not isinstance(value, list)):
        return False, f"{field_name} must be an array"
    
    if value is not None and not isinstance(value, list):
        return False, f"{field_name} must be an array"
    
    if value is not None:
        for item in value:
            if not isinstance(item, str) or not item.strip():
                return False, f"All items in {field_name} must be non-empty strings"
    
    return True, None

