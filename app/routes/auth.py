from flask import Blueprint, request, jsonify
from app.controllers.auth_controller import register_user, login_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required', 'status_code': 400}), 400
        
        response, status_code = register_user(data)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}', 'status_code': 500}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required', 'status_code': 400}), 400
        
        response, status_code = login_user(data)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}', 'status_code': 500}), 500

