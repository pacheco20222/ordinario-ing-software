from flask import Blueprint, request, jsonify
from app.middleware.auth_middleware import require_auth
from app.controllers.profile_controller import get_user_profile, update_user_profile

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('', methods=['GET'])
@require_auth
def get_profile():
    """Get user profile endpoint"""
    try:
        user_id = request.user_id
        response, status_code = get_user_profile(user_id)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}', 'status_code': 500}), 500


@profile_bp.route('', methods=['PUT'])
@require_auth
def update_profile():
    """Update user profile endpoint"""
    try:
        user_id = request.user_id
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required', 'status_code': 400}), 400
        
        response, status_code = update_user_profile(user_id, data)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}', 'status_code': 500}), 500

