from functools import wraps
from flask import request, jsonify
from app.utils.jwt_utils import decode_token


def require_auth(f):
    """
    Decorator to require JWT authentication
    Extracts token from Authorization header and adds user info to request
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(' ')[1]  # Format: "Bearer <token>"
            except IndexError:
                return jsonify({'error': 'Invalid authorization header format', 'status_code': 401}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing', 'status_code': 401}), 401
        
        # Decode and validate token
        payload = decode_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token', 'status_code': 401}), 401
        
        # Add user info to request context
        request.user_id = payload.get('user_id')
        request.user_email = payload.get('email')
        
        return f(*args, **kwargs)
    
    return decorated_function

