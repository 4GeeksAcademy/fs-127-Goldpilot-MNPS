"""
=============================================================================
                         CAPA DE SERVICIOS
=============================================================================

Los servicios contienen la logica de negocio de la aplicacion.
Actuan como intermediarios entre los controllers/routes y los models.

Responsabilidades de un servicio:
- Validar datos de entrada
- Ejecutar queries a la base de datos
- Manejar errores con try/except y rollback
- Retornar resultados o lanzar excepciones
"""

from api.services.user_services import UserService
from api.services.auth_services import AuthService