"""
Servicio de autenticacion - Login, Signup y validacion de tokens
"""

import os  # NUEVO: para leer variables de entorno (FRONTEND_URL)
from flask import abort
# NUEVO: clase para construir el email de verificacion
from flask_mail import Message
from flask_jwt_extended import create_access_token
from api.models import db, User


class AuthService:
    @staticmethod
    def signup(data):
        """Registrar un nuevo usuario con password hasheado."""
        required_fields = ["email", "username",
                           "password", "first_name", "last_name","phone_number"]
        for field in required_fields:
            if field not in data or not data[field]:
                abort(400, description=f"El campo '{field}' es obligatorio")

        if User.query.filter_by(email=data["email"]).first():
            abort(409, description="Ya existe un usuario con ese email")

        if User.query.filter_by(username=data["username"]).first():
            abort(409, description="Ya existe un usuario con ese username")

        try:
            new_user = User(
                email=data["email"],
                username=data["username"],
                is_active=True
            )
            new_user.set_password(data["password"])
            # NUEVO: genera token UUID para verificar email
            new_user.generate_verification_token()
            AuthService._send_verification_email(new_user)
            db.session.add(new_user)
            db.session.commit()

            # NUEVO: envia email con link de verificacion

            return {
                # MODIFICADO: mensaje actualizado
                "msg": "Usuario registrado exitosamente. Revisa tu email para verificar tu cuenta.",
                "user": new_user.serialize()
            }
        except Exception as error:
            db.session.rollback()
            abort(500, description=f"Error al registrar usuario: {str(error)}")

    @staticmethod
    # NUEVO: metodo privado para enviar email de verificacion
    def _send_verification_email(user):
        """Envia un email con el link de verificacion."""
        from app import mail  # NUEVO: importamos la instancia de Mail configurada en app.py

        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        verification_link = f"{frontend_url}/verify?token={user.verification_token}"

        msg = Message(
            subject="Verifica tu cuenta",
            recipients=[user.email],
            html=f"""
                <h2>¡Bienvenido, {user.username}!</h2>
                <p>Gracias por registrarte. Haz clic en el siguiente enlace para verificar tu cuenta:</p>
                <a href="{verification_link}" style="
                    background-color: #4CAF50;
                    color: white;
                    padding: 14px 25px;
                    text-decoration: none;
                    display: inline-block;
                    border-radius: 4px;
                ">Verificar mi cuenta</a>
                <p>Si no creaste esta cuenta, ignora este email.</p>
            """
        )
        print(mail)
        mail.send(msg)

    @staticmethod
    def verify_email(token):  # NUEVO: metodo para verificar email con el token recibido (NAPOLES)
        """Verifica el email del usuario usando el token."""
        if not token:
            abort(400, description="Token de verificacion requerido")

        user = User.query.filter_by(verification_token=token).first()
        if not user:
            abort(404, description="Token de verificacion invalido")

        if user.is_verified:
            return {"msg": "El email ya fue verificado anteriormente"}

        # NUEVO: marcamos el email como verificado(NAPOLES)
        user.is_verified = True
        # NUEVO: invalidamos el token para que no se reutilice (NAPOLES)
        user.verification_token = None
        db.session.commit()

        return {
            "msg": "Email verificado exitosamente",
            "user": user.serialize()
        }

    