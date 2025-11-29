import bcrypt
from app.models.user import User
from app.utils.validators import validate_email, validate_password, validate_arrays
from app.utils.jwt_utils import generate_token


def register_user(data):
    """
    Register a new user
    Args:
        data: dict with email, password, favorite_songs, favorite_artists, favorite_genres, spotify_username
    Returns:
        tuple: (response_dict, status_code)
    """
    # Validate required fields
    email = data.get('email')
    password = data.get('password')
    
    if not email:
        return {'error': 'Email is required', 'status_code': 400}, 400
    
    if not password:
        return {'error': 'Password is required', 'status_code': 400}, 400
    
    # Validate email format
    if not validate_email(email):
        return {'error': 'Invalid email format', 'status_code': 400}, 400
    
    # Validate password
    if not validate_password(password):
        return {'error': 'Password must be at least 6 characters', 'status_code': 400}, 400
    
    # Validate arrays
    favorite_songs = data.get('favorite_songs', [])
    favorite_artists = data.get('favorite_artists', [])
    favorite_genres = data.get('favorite_genres', [])
    
    is_valid, error = validate_arrays('favorite_songs', favorite_songs)
    if not is_valid:
        return {'error': error, 'status_code': 400}, 400
    
    is_valid, error = validate_arrays('favorite_artists', favorite_artists)
    if not is_valid:
        return {'error': error, 'status_code': 400}, 400
    
    is_valid, error = validate_arrays('favorite_genres', favorite_genres)
    if not is_valid:
        return {'error': error, 'status_code': 400}, 400
    
    # Check if user already exists
    existing_user = User.find_by_email(email)
    if existing_user:
        return {'error': 'User with this email already exists', 'status_code': 400}, 400
    
    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
    
    # Create user data
    user_data = {
        'email': email,
        'password': hashed_password.decode('utf-8'),
        'favorite_songs': favorite_songs or [],
        'favorite_artists': favorite_artists or [],
        'favorite_genres': favorite_genres or [],
        'spotify_username': data.get('spotify_username', '')
    }
    
    # Save user to database
    try:
        user = User.create(user_data)
        return {
            'message': 'User registered successfully',
            'user_id': str(user['_id'])
        }, 201
    except Exception as e:
        return {'error': f'Failed to register user: {str(e)}', 'status_code': 500}, 500


def login_user(data):
    """
    Authenticate user and return JWT token
    Args:
        data: dict with email and password
    Returns:
        tuple: (response_dict, status_code)
    """
    email = data.get('email')
    password = data.get('password')
    
    if not email:
        return {'error': 'Email is required', 'status_code': 400}, 400
    
    if not password:
        return {'error': 'Password is required', 'status_code': 400}, 400
    
    # Find user by email
    user = User.find_by_email(email)
    if not user:
        return {'error': 'Invalid email or password', 'status_code': 401}, 401
    
    # Verify password
    stored_password = user.get('password', '').encode('utf-8')
    if not bcrypt.checkpw(password.encode('utf-8'), stored_password):
        return {'error': 'Invalid email or password', 'status_code': 401}, 401
    
    # Generate JWT token
    token = generate_token(str(user['_id']), user['email'])
    
    return {
        'token': token,
        'user_id': str(user['_id']),
        'email': user['email']
    }, 200

