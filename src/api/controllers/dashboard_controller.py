"""
Controlador del Dashboard.
Expone el resumen de cuenta, estadísticas de trading y estrategia activa.
Blueprint: /dashboard
"""

import requests as req
from flask import Blueprint, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.models.wallet import MetaApiAccount
from api.models.trade import Trade
from api.models.db import db
from api.controllers.wallet_controller import (
    _metaapi_headers,
    _check_token,
    METAAPI_CLIENT_BASE,
)

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


def _fetch_wallet_balance(account):
    """
    Consulta balance, equity y margen libre de una wallet conectada vía MetaApi.
    Retorna un dict con los valores o None para cada campo si no están disponibles.
    """
    empty = {"balance": None, "equity": None, "currency": None, "margin": None, "free_margin": None}

    if account.status != "connected" or not account.region:
        return empty

    try:
        base = METAAPI_CLIENT_BASE.format(region=account.region)
        resp = req.get(
            f"{base}/users/current/accounts/{account.account_id}/account-information",
            headers=_metaapi_headers(),
            timeout=10,
        )
        if resp.ok:
            data = resp.json()
            return {
                "balance": data.get("balance"),
                "equity": data.get("equity"),
                "currency": data.get("currency", "USD"),
                "margin": data.get("margin"),
                "free_margin": data.get("freeMargin"),
            }
    except Exception:
        pass

    return empty


@dashboard_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_summary():
    """
    Retorna el resumen del dashboard del usuario.
    Incluye todas las wallets con su balance real consultado a MetaApi.
    """
    user_id = int(get_jwt_identity())
    accounts = MetaApiAccount.query.filter_by(user_id=user_id).all()

    has_token = _check_token()
    wallets_data = []

    for account in accounts:
        wallet_info = account.serialize()
        balance_info = _fetch_wallet_balance(account) if has_token else {
            "balance": None, "equity": None, "currency": None, "margin": None, "free_margin": None
        }
        wallet_info.update(balance_info)
        wallets_data.append(wallet_info)

    data = {
        "wallets": wallets_data,
        "stats": {
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "win_rate": 0,
            "total_profit": 0,
        },
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
