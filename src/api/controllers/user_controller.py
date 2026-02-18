"""
Controlador de usuarios - Endpoints /api/users
"""

from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required
from api.services import UserService

user_bp = Blueprint('users', __name__, url_prefix='/users')

# GET /api/users - Obtener todos los usuarios (protegido)
@user_bp.route('', methods=['GET'])
def get_users():
    users = UserService.get_all()
    return jsonify(users), 200

@user_bp.route("/login", methods=['POST'])
def login():
    UserService.login()
