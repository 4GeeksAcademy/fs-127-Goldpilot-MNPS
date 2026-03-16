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
@jwt_required()
def get_trade_history():
    user_id = int(get_jwt_identity())
    trades = Trade.query.filter_by(
        user_id=user_id, status="closed"
    ).order_by(Trade.closed_at.desc()).all()

    return jsonify({"trades": [t.serialize() for t in trades]}), 200


@dashboard_bp.route('/trades/open', methods=['GET'])
@jwt_required()
def get_open_trades():
    user_id = int(get_jwt_identity())
    trades = Trade.query.filter_by(user_id=user_id, status='open').order_by(Trade.opened_at.desc()).all()
    return jsonify({"trades": [t.serialize() for t in trades]}), 200


@dashboard_bp.route('/trades/<int:trade_id>/cancel', methods=['PATCH'])
@jwt_required()
def cancel_trade(trade_id):
    user_id = int(get_jwt_identity())
    trade = Trade.query.filter_by(id=trade_id, user_id=user_id).first()

    if not trade:
        abort(404, description="Operación no encontrada")

    if trade.status != 'open':
        abort(400, description="Solo se pueden cancelar operaciones abiertas")

    trade.status = 'cancelled'
    db.session.commit()

    return jsonify({"msg": "Operación cancelada correctamente", "trade": trade.serialize()}), 200
