"""
=============================================================================
                              MODELO: USER (Usuario)
=============================================================================

Tabla principal de usuarios.
- Relacion 1 a 1 con ProfileInfo
- Relacion 1 a Muchos con Order
"""

import bcrypt
import uuid  # NUEVO: para generar tokens unicos de verificacion
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from api.models import db


class User(db.Model):
    __tablename__ = 'users'

    # Columnas
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(
        String(80), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean(), default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(  # NUEVO: indica si el usuario verifico su email (NAPOLES)
        Boolean(), default=False, nullable=False)
    verification_token: Mapped[str] = mapped_column(  # NUEVO: token UUID enviado por email para verificar (NAPOLES)
        String(256), unique=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(), default=datetime.utcnow)

    def set_password(self, password):
        """Hashea un password en texto plano y lo almacena."""
        password_bytes = password.encode('utf-8')
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        self.password = hashed.decode('utf-8')

    def check_password(self, password):
        """Verifica un password en texto plano contra el hash almacenado."""
        password_bytes = password.encode('utf-8')
        hashed_bytes = self.password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)

    # NUEVO: metodo para generar token de verificacion (NAPOLES)
    def generate_verification_token(self):
        """Genera un token unico para la verificacion de email."""
        self.verification_token = str(
            uuid.uuid4())  # NUEVO: genera UUID v4 como token (NAPOLES)
        return self.verification_token

    def __repr__(self):
        return f'<User {self.id}: {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "is_active": self.is_active,
            # NUEVO: incluimos is_verified en la respuesta JSON (NAPOLES)
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
