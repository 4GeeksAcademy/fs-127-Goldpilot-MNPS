"""
Controlador del Dashboard.
Expone el resumen de cuenta, estadísticas de trading y estrategia activa.
Blueprint: /dashboard
"""

from flask import Blueprint, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.models.wallet import MetaApiAccount
from api.models.trade import Trade
from api.models.db import db

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
def get_trade_history():
    """
    Retorna el historial de operaciones cerradas del usuario.
    Datos mock basados en el modelo Trade (tabla: trades).
    Columnas usadas: symbol, trade_type, open_price, close_price, profit_loss, opened_at, closed_at, status

    Returns:
        JSON con lista de trades cerrados.
    """
    mock_trades = [
        {
            "id": 1,
            "symbol": "XAUUSD",
            "trade_type": "BUY",
            "open_price": 2015.50,
            "close_price": 2028.30,
            "profit_loss": 128.00,
            "opened_at": "2026-02-24T09:15:00",
            "closed_at": "2026-02-24T11:42:00",
            "status": "closed",
        },
        {
            "id": 2,
            "symbol": "XAUUSD",
            "trade_type": "SELL",
            "open_price": 2031.20,
            "close_price": 2019.80,
            "profit_loss": 114.00,
            "opened_at": "2026-02-24T13:00:00",
            "closed_at": "2026-02-24T15:30:00",
            "status": "closed",
        },
        {
            "id": 3,
            "symbol": "XAUUSD",
            "trade_type": "BUY",
            "open_price": 2022.00,
            "close_price": 2017.50,
            "profit_loss": -45.00,
            "opened_at": "2026-02-23T10:00:00",
            "closed_at": "2026-02-23T12:15:00",
            "status": "closed",
        },
        {
            "id": 4,
            "symbol": "XAUUSD",
            "trade_type": "SELL",
            "open_price": 2028.75,
            "close_price": 2014.20,
            "profit_loss": 145.50,
            "opened_at": "2026-02-22T08:30:00",
            "closed_at": "2026-02-22T10:45:00",
            "status": "closed",
        },
        {
            "id": 5,
            "symbol": "XAUUSD",
            "trade_type": "BUY",
            "open_price": 2010.00,
            "close_price": 2006.50,
            "profit_loss": -35.00,
            "opened_at": "2026-02-21T14:00:00",
            "closed_at": "2026-02-21T16:20:00",
            "status": "closed",
        },
    ]

    return jsonify({"trades": mock_trades}), 200


@dashboard_bp.route('/trades/open', methods=['GET'])
@jwt_required()
def get_open_trades():
    """
    Retorna las operaciones abiertas (status='open') del usuario autenticado.
    """
    user_id = int(get_jwt_identity())
    trades = Trade.query.filter_by(user_id=user_id, status='open').order_by(Trade.opened_at.desc()).all()
    return jsonify({"trades": [t.serialize() for t in trades]}), 200


@dashboard_bp.route('/trades/<int:trade_id>/cancel', methods=['PATCH'])
@jwt_required()
def cancel_trade(trade_id):
    """
    Cancela una operación abierta del usuario.
    Solo se puede cancelar si pertenece al usuario y está en status='open'.
    """
    user_id = int(get_jwt_identity())
    trade = Trade.query.filter_by(id=trade_id, user_id=user_id).first()

    if not trade:
        abort(404, description="Operación no encontrada")

    if trade.status != 'open':
        abort(400, description="Solo se pueden cancelar operaciones abiertas")

    trade.status = 'cancelled'
    db.session.commit()

    return jsonify({"msg": "Operación cancelada correctamente", "trade": trade.serialize()}), 200
