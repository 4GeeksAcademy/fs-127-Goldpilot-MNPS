from api.controllers.user_controller import user_bp
from api.controllers.auth_controller import auth_bp
from api.controllers.dashboard_controller import dashboard_bp
from api.controllers.wallet_controller import wallet_bp
from api.controllers.bot_controller import bot_bp
from api.controllers.market_controller import market_bp

def register_controllers(api):
       
    api.register_blueprint(user_bp)
    api.register_blueprint(auth_bp)
    api.register_blueprint(dashboard_bp)
    api.register_blueprint(wallet_bp)
    api.register_blueprint(bot_bp)
    api.register_blueprint(market_bp)
