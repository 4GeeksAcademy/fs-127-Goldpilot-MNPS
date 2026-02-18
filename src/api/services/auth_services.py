"""
Servicio de autenticacion - Login, Signup y validacion de tokens
"""

from flask import abort
from flask_jwt_extended import create_access_token
from api.models import db, User


class AuthService:
    pass