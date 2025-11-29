from flask import Blueprint, request, jsonify
from app.middleware.auth_middleware import require_auth
from app.controllers.playlist_controller import create_or_update_playlist, get_user_playlist

playlist_bp = Blueprint('playlist', __name__)


@playlist_bp.route('', methods=['POST'])
@require_auth
def create_playlist():
    """Create or update user's top 10 playlist endpoint"""
    try:
        user_id = request.user_id
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required', 'status_code': 400}), 400
        
        response, status_code = create_or_update_playlist(user_id, data)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}', 'status_code': 500}), 500


@playlist_bp.route('', methods=['GET'])
@require_auth
def get_playlist():
    """Get user's playlist endpoint"""
    try:
        user_id = request.user_id
        response, status_code = get_user_playlist(user_id)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}', 'status_code': 500}), 500

