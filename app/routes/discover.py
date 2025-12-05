from flask import Blueprint, request, jsonify
from app.middleware.auth_middleware import require_auth
from app.controllers.discover_controller import get_random_user, swipe_right, get_user_matches

discover_bp = Blueprint('discover', __name__)


@discover_bp.route('/user', methods=['GET'])
@require_auth
def get_random_user_profile():
    """Get random user profile endpoint"""
    try:
        user_id = request.user_id
        response, status_code = get_random_user(user_id)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}', 'status_code': 500}), 500


@discover_bp.route('/swipe-right', methods=['POST'])
@require_auth
def swipe_right_endpoint():
    """Swipe right on a user endpoint"""
    try:
        user_id = request.user_id
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required', 'status_code': 400}), 400
        
        swiped_user_id = data.get('user_id')
        if not swiped_user_id:
            return jsonify({'error': 'user_id is required', 'status_code': 400}), 400
        
        response, status_code = swipe_right(user_id, swiped_user_id)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}', 'status_code': 500}), 500


@discover_bp.route('/matches', methods=['GET'])
@require_auth
def get_matches():
    """Get all user matches endpoint"""
    try:
        user_id = request.user_id
        response, status_code = get_user_matches(user_id)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}', 'status_code': 500}), 500

