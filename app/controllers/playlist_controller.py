from app.models.playlist import Playlist
from app.models.user import User
from app.utils.validators import validate_playlist_songs


def create_or_update_playlist(user_id, data):
    """
    Create or update user's top 10 playlist
    Args:
        user_id: User ID string
        data: dict with songs array
    Returns:
        tuple: (response_dict, status_code)
    """
    # Verify user exists
    user = User.find_by_id(user_id)
    if not user:
        return {'error': 'User not found', 'status_code': 404}, 404
    
    # Validate songs
    songs = data.get('songs')
    if not songs:
        return {'error': 'Songs array is required', 'status_code': 400}, 400
    
    is_valid, error = validate_playlist_songs(songs)
    if not is_valid:
        return {'error': error, 'status_code': 400}, 400
    
    # Create or update playlist
    try:
        playlist = Playlist.update_or_create(user_id, songs)
        playlist_dict = Playlist.to_dict(playlist)
        return playlist_dict, 200
    except Exception as e:
        return {'error': f'Failed to save playlist: {str(e)}', 'status_code': 500}, 500


def get_user_playlist(user_id):
    """
    Get user's playlist
    Args:
        user_id: User ID string
    Returns:
        tuple: (response_dict, status_code)
    """
    # Verify user exists
    user = User.find_by_id(user_id)
    if not user:
        return {'error': 'User not found', 'status_code': 404}, 404
    
    # Find playlist
    playlist = Playlist.find_by_user_id(user_id)
    if not playlist:
        return {'error': 'Playlist not found', 'status_code': 404}, 404
    
    playlist_dict = Playlist.to_dict(playlist)
    return playlist_dict, 200

