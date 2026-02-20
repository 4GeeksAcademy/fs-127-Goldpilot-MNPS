"""
=============================================================================
                    MODELOS DE BASE DE DATOS - PAQUETE
=============================================================================

Este paquete contiene todos los modelos (tablas) de nuestra base de datos,
organizados en archivos separados siguiendo el patron MVC.

Desde aqui se exportan todos los modelos y el objeto db para que
el resto de la aplicacion pueda importarlos facilmente:

    from api.models import db, User, Article, Order, Tag
"""

from flask_sqlalchemy import SQLAlchemy

# Inicializamos SQLAlchemy - esto crea la conexion con la base de datos
db = SQLAlchemy()

# Importamos todos los modelos para que esten disponibles desde el paquete
# IMPORTANTE: El orden de imports importa por las dependencias entre modelos
from api.models.user import User
from api.models.db import db
from api.models.user import User
from api.models.strategies import Strategy, UserStrategy