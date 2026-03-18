from flask_sqlalchemy import SQLAlchemy

# Inicializamos SQLAlchemy - esto crea la conexion con la base de datos
db = SQLAlchemy()

# Importamos todos los modelos para que esten disponibles desde el paquete
# IMPORTANTE: El orden de imports importa por las dependencias entre modelos
from api.models.db import db
from api.models.user import User
from api.models.strategies import Strategy, UserStrategy
from api.models.wallet import MetaApiAccount
from api.models.trade import Trade
from api.models.notification import Notification
from api.models.activity_log import ActivityLog
