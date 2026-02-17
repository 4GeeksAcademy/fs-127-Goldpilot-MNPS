"""
Controlador de autenticacion - Endpoints /api/auth
"""

from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.services import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')