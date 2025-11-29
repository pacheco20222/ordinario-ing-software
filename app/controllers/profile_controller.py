from app.models.user import User
from app.utils.validators import validate_email, validate_arrays


def get_user_profile(user_id):
    """
    Get user profile by ID
    Args:
        user_id: User ID string
    Returns:
        tuple: (response_dict, status_code)
    """
    user = User.find_by_id(user_id)
    if not user:
        return {'error': 'User not found', 'status_code': 404}, 404
    
    user_dict = User.to_dict(user)
    return user_dict, 200


def update_user_profile(user_id, data):
    """
    Update user profile
    Args:
        user_id: User ID string
        data: dict with fields to update (all optional)
    Returns:
        tuple: (response_dict, status_code)
    """
    user = User.find_by_id(user_id)
    if not user:
        return {'error': 'User not found', 'status_code': 404}, 404
    
    # Build update data
    update_data = {}
    
    # Validate and add favorite_songs if provided
    if 'favorite_songs' in data:
        is_valid, error = validate_arrays('favorite_songs', data['favorite_songs'])
        if not is_valid:
            return {'error': error, 'status_code': 400}, 400
        update_data['favorite_songs'] = data['favorite_songs']
    
    # Validate and add favorite_artists if provided
    if 'favorite_artists' in data:
        is_valid, error = validate_arrays('favorite_artists', data['favorite_artists'])
        if not is_valid:
            return {'error': error, 'status_code': 400}, 400
        update_data['favorite_artists'] = data['favorite_artists']
    
    # Validate and add favorite_genres if provided
    if 'favorite_genres' in data:
        is_valid, error = validate_arrays('favorite_genres', data['favorite_genres'])
        if not is_valid:
            return {'error': error, 'status_code': 400}, 400
        update_data['favorite_genres'] = data['favorite_genres']
    
    # Add spotify_username if provided
    if 'spotify_username' in data:
        update_data['spotify_username'] = data.get('spotify_username', '')
    
    # Update user if there's data to update
    if update_data:
        try:
            updated_user = User.update(user_id, update_data)
            user_dict = User.to_dict(updated_user)
            return user_dict, 200
        except Exception as e:
            return {'error': f'Failed to update profile: {str(e)}', 'status_code': 500}, 500
    
    # No data to update, return current profile
    user_dict = User.to_dict(user)
    return user_dict, 200

