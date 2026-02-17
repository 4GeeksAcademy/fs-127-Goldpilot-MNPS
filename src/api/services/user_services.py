"""
Servicio de usuarios - Logica de negocio para CRUD de User
"""

from flask import abort
from api.models import db, User


class UserService:

    def get_all():
        users = User.query.all()
        return [user.serialize() for user in users]
