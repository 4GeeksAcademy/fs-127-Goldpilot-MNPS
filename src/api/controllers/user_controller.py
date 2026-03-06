"""
Controlador de usuarios - Endpoints /api/users
"""

from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.services import UserService
from api.models import db, User

user_bp = Blueprint('users', __name__, url_prefix='/users')

# GET /api/users - Obtener todos los usuarios (protegido)
@user_bp.route('', methods=['GET'])
def get_users():
    users = UserService.get_all()
    return jsonify(users), 200

@user_bp.route("/login", methods=['POST'])
def login():
    UserService.login()


@user_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    """Devuelve el perfil completo del usuario autenticado."""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        abort(404, description="Usuario no encontrado")
    return jsonify(user.serialize()), 200


@user_bp.route('/me', methods=['PATCH'])
@jwt_required()
def update_me():
    """
    Actualiza los campos editables del perfil: username y/o phone_number.
    Solo se modifican los campos presentes en el body.
    """
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        abort(404, description="Usuario no encontrado")

    data = request.get_json() or {}

    if "username" in data and data["username"]:
        existing = User.query.filter_by(username=data["username"]).first()
        if existing and existing.id != user_id:
            abort(409, description="Ese nombre de usuario ya está en uso")
        user.username = data["username"]

    if "phone_number" in data and data["phone_number"]:
        user.phone_number = data["phone_number"]

    db.session.commit()
    return jsonify(user.serialize()), 200
