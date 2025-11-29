import jwt
from datetime import datetime, timedelta
from app.config import Config


def generate_token(user_id, email):
    """
    Generate JWT token for user
    Args:
        user_id: User ID (string)
        email: User email
    Returns:
        JWT token string
    """
    payload = {
        'user_id': str(user_id),
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
    # Ensure token is a string (PyJWT 2.x returns string, but older versions return bytes)
    if isinstance(token, bytes):
        return token.decode('utf-8')
    return token


def decode_token(token):
    """
    Decode and validate JWT token
    Args:
        token: JWT token string
    Returns:
        dict with user_id and email, or None if invalid
    """
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

