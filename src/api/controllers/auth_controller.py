"""
Controlador de autenticacion - Endpoints /api/auth
"""

from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.services import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')



@auth_bp.route('/signup', methods=['POST'])
def signup():
    body = request.get_json()
    if not body:
        abort(400, description="El body no puede estar vacio")
    result = AuthService.signup(body)
    return jsonify(result), 201



@auth_bp.route('/verify/<token>', methods=['GET'])
def verify_email(token):
    result = AuthService.verify_email(token)
    return jsonify(result), 200


@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    body = request.get_json()
    if not body:
        abort(400, description="El body no puede estar vacio")
    result = AuthService.forgot_password(body)
    return jsonify(result), 200


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    body = request.get_json()
    if not body:
        abort(400, description="El body no puede estar vacio")
    result = AuthService.reset_password(body)
    return jsonify(result), 200


@auth_bp.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    if not body:
        abort(400, description="El body no puede estar vacio")
    result = AuthService.login(body)
    return jsonify(result), 200             
