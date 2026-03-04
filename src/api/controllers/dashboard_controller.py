"""
Controlador del Dashboard.
Expone el resumen de cuenta, estadísticas de trading y estrategia activa.
Blueprint: /dashboard
"""

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.models.wallet import MetaApiAccount
from api.models.trade import Trade

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_summary():
    """
    Retorna el resumen del dashboard del usuario.
    Devuelve valores vacíos si no hay wallet conectada.
    TODO: Integrar datos reales de MetaApi cuando el servicio esté disponible.
    """
    user_id = int(get_jwt_identity())
    wallet = MetaApiAccount.query.filter_by(user_id=user_id).first()

    data = {
        "account": {
            "balance": None,
            "equity": None,
            "currency": "USD",
            "margin": None,
            "free_margin": None,
            "is_connected": wallet is not None,
        },
        "stats": {
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "win_rate": 0,
            "total_profit": 0,
        },
        "wallet": wallet.serialize() if wallet else None,
    }

    return jsonify(data), 200


@dashboard_bp.route('/trades/history', methods=['GET'])
@jwt_required()
def get_trade_history():
    """
    Retorna el historial de operaciones cerradas del usuario.
    Consulta la tabla trades filtrada por user_id y status='closed'.
    """
    user_id = int(get_jwt_identity())
    trades = Trade.query.filter_by(
        user_id=user_id, status="closed"
    ).order_by(Trade.closed_at.desc()).all()

    return jsonify({"trades": [t.serialize() for t in trades]}), 200
