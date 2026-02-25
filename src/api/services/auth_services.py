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
                           "password", "first_name", "last_name", "phone_number"]
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
                first_name=data["first_name"],
                last_name=data["last_name"],
                phone_number=data["phone_number"],
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
            subject="Bienvenido a Xsniper — Confirma tu acceso",
            recipients=[user.email],
            html=f"""
            <!DOCTYPE html>
            <html lang="es">
            <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
            <body style="margin:0;padding:0;background-color:#1a1208;font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display',sans-serif;">
                <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#1a1208;padding:48px 16px;">
                    <tr><td align="center">
                        <table width="100%" style="max-width:520px;background:rgba(30,22,14,0.95);border-radius:24px;border:1px solid rgba(195,143,55,0.2);overflow:hidden;">

                            <!-- Header dorado -->
                            <tr>
                                <td style="background:linear-gradient(135deg,#2c2117 0%,#1a1208 100%);padding:36px 40px 28px;text-align:center;border-bottom:1px solid rgba(195,143,55,0.15);">
                                    <div style="display:inline-flex;align-items:center;gap:10px;">
                                        <div style="width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#c38f37,#f5e6be);display:inline-flex;align-items:center;justify-content:center;font-size:11px;font-weight:900;color:#1a1208;letter-spacing:-0.5px;">XS</div>
                                        <span style="font-size:20px;font-weight:700;color:#ffffff;letter-spacing:-0.5px;">XSNIPER</span>
                                    </div>
                                </td>
                            </tr>

                            <!-- Cuerpo -->
                            <tr>
                                <td style="padding:40px 40px 32px;">
                                    <p style="margin:0 0 8px;font-size:13px;color:#c38f37;font-weight:600;letter-spacing:2px;text-transform:uppercase;">Bienvenido</p>
                                    <h1 style="margin:0 0 20px;font-size:26px;font-weight:700;color:#ffffff;line-height:1.2;">Hola, {user.first_name} 👋</h1>
                                    <p style="margin:0 0 28px;font-size:15px;color:rgba(255,255,255,0.6);line-height:1.7;">
                                        Nos alegra tenerte aquí. Tu cuenta en <strong style="color:#c38f37;">Xsniper</strong> está casi lista — solo necesitamos confirmar que este email te pertenece.
                                    </p>
                                    <p style="margin:0 0 28px;font-size:15px;color:rgba(255,255,255,0.6);line-height:1.7;">
                                        Haz clic en el botón de abajo y en segundos tendrás acceso completo a la plataforma.
                                    </p>

                                    <!-- Botón -->
                                    <div style="text-align:center;margin:32px 0;">
                                        <a href="{verification_link}" style="display:inline-block;background:linear-gradient(135deg,#c38f37,#d4af37);color:#1a1208;font-size:14px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;text-decoration:none;padding:16px 40px;border-radius:9999px;box-shadow:0 8px 24px rgba(195,143,55,0.35);">
                                            Verificar mi cuenta
                                        </a>
                                    </div>

                                    <p style="margin:28px 0 0;font-size:13px;color:rgba(255,255,255,0.3);line-height:1.6;">
                                        Si no has creado esta cuenta, puedes ignorar este mensaje sin preocupación. El enlace expirará automáticamente.
                                    </p>
                                </td>
                            </tr>

                            <!-- Footer -->
                            <tr>
                                <td style="padding:20px 40px 32px;border-top:1px solid rgba(255,255,255,0.06);text-align:center;">
                                    <p style="margin:0;font-size:12px;color:rgba(255,255,255,0.2);">© 2025 Xsniper — Todos los derechos reservados</p>
                                </td>
                            </tr>

                        </table>
                    </td></tr>
                </table>
            </body>
            </html>
            """
        )
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

        user.is_verified = True
        db.session.commit()

        return {
            "msg": "Email verificado exitosamente",
            "user": user.serialize()
        }

    @staticmethod
    def forgot_password(data):
        """Genera un token de reset y envía el email. No requiere contraseña actual."""
        if "email" not in data or not data["email"]:
            abort(400, description="El campo 'email' es obligatorio")

        user = User.query.filter_by(email=data["email"]).first()
        # Por seguridad no revelamos si el email existe o no
        if not user or not user.is_verified:
            return {"msg": "Si tu email está registrado, recibirás un enlace para restablecer tu contraseña."}

        try:
            user.generate_password_change_token()
            AuthService._send_password_reset_email(user)
            db.session.commit()
            return {"msg": "Si tu email está registrado, recibirás un enlace para restablecer tu contraseña."}
        except Exception as error:
            db.session.rollback()
            abort(500, description=f"Error al procesar la solicitud: {str(error)}")

    @staticmethod
    def reset_password(data):
        """Aplica la nueva contraseña usando el token del email."""
        required_fields = ["token", "new_password"]
        for field in required_fields:
            if field not in data or not data[field]:
                abort(400, description=f"El campo '{field}' es obligatorio")

        user = User.query.filter_by(password_change_token=data["token"]).first()
        if not user:
            abort(404, description="El enlace no es válido o ya ha sido usado")

        if len(data["new_password"]) < 8:
            abort(400, description="La contraseña debe tener al menos 8 caracteres")

        try:
            user.set_password(data["new_password"])
            user.pending_password = None
            user.password_change_token = None
            db.session.commit()
            return {"msg": "Contraseña actualizada correctamente. Ya puedes iniciar sesión."}
        except Exception as error:
            db.session.rollback()
            abort(500, description=f"Error al actualizar la contraseña: {str(error)}")

    @staticmethod
    def _send_password_reset_email(user):
        """Envia el email con el enlace para restablecer la contraseña."""
        from app import mail

        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        confirm_link = f"{frontend_url}/reset-password?token={user.password_change_token}"

        msg = Message(
            subject="Xsniper — Confirma tu cambio de contraseña",
            recipients=[user.email],
            html=f"""
            <!DOCTYPE html>
            <html lang="es">
            <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
            <body style="margin:0;padding:0;background-color:#1a1208;font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display',sans-serif;">
                <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#1a1208;padding:48px 16px;">
                    <tr><td align="center">
                        <table width="100%" style="max-width:520px;background:rgba(30,22,14,0.95);border-radius:24px;border:1px solid rgba(195,143,55,0.2);overflow:hidden;">
                            <tr>
                                <td style="background:linear-gradient(135deg,#2c2117 0%,#1a1208 100%);padding:36px 40px 28px;text-align:center;border-bottom:1px solid rgba(195,143,55,0.15);">
                                    <div style="display:inline-flex;align-items:center;gap:10px;">
                                        <div style="width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#c38f37,#f5e6be);display:inline-flex;align-items:center;justify-content:center;font-size:11px;font-weight:900;color:#1a1208;letter-spacing:-0.5px;">XS</div>
                                        <span style="font-size:20px;font-weight:700;color:#ffffff;letter-spacing:-0.5px;">XSNIPER</span>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td style="padding:40px 40px 32px;">
                                    <p style="margin:0 0 8px;font-size:13px;color:#c38f37;font-weight:600;letter-spacing:2px;text-transform:uppercase;">Seguridad</p>
                                    <h1 style="margin:0 0 20px;font-size:26px;font-weight:700;color:#ffffff;line-height:1.2;">Hola, {user.first_name} 👋</h1>
                                    <p style="margin:0 0 28px;font-size:15px;color:rgba(255,255,255,0.6);line-height:1.7;">
                                        Hemos recibido una solicitud para cambiar la contraseña de tu cuenta en <strong style="color:#c38f37;">Xsniper</strong>.
                                    </p>
                                    <p style="margin:0 0 28px;font-size:15px;color:rgba(255,255,255,0.6);line-height:1.7;">
                                        Haz clic en el botón de abajo para confirmar el cambio. Si no fuiste tú, ignora este mensaje y tu contraseña no cambiará.
                                    </p>
                                    <div style="text-align:center;margin:32px 0;">
                                        <a href="{confirm_link}" style="display:inline-block;background:linear-gradient(135deg,#c38f37,#d4af37);color:#1a1208;font-size:14px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;text-decoration:none;padding:16px 40px;border-radius:9999px;box-shadow:0 8px 24px rgba(195,143,55,0.35);">
                                            Confirmar nueva contraseña
                                        </a>
                                    </div>
                                    <p style="margin:28px 0 0;font-size:13px;color:rgba(255,255,255,0.3);line-height:1.6;">
                                        Si no solicitaste este cambio, no es necesario que hagas nada.
                                    </p>
                                </td>
                            </tr>
                            <tr>
                                <td style="padding:20px 40px 32px;border-top:1px solid rgba(255,255,255,0.06);text-align:center;">
                                    <p style="margin:0;font-size:12px;color:rgba(255,255,255,0.2);">© 2025 Xsniper — Todos los derechos reservados</p>
                                </td>
                            </tr>
                        </table>
                    </td></tr>
                </table>
            </body>
            </html>
            """
        )
        mail.send(msg)


    @staticmethod
    def login(data):
        """Autentica al usuario y devuelve un token JWT."""
        required_fields = ["email", "password"]
        for field in required_fields:
            if field not in data or not data[field]:
                abort(400, description=f"El campo '{field}' es obligatorio")

        user = User.query.filter_by(email=data["email"]).first()
        if not user or not user.check_password(data["password"]):
            abort(401, description="Credenciales invalidas")

        if not user.is_verified:
            abort(
                403, description="Email no verificado. Revisa tu email para verificar tu cuenta.")

        access_token = create_access_token(identity=user.id)
        return {
            "msg": "Login exitoso",
            "access_token": access_token,
            "user": user.serialize()
        }
