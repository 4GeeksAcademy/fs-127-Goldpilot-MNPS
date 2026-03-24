import requests as req
from concurrent.futures import ThreadPoolExecutor, as_completed
from flask import Blueprint, jsonify, abort, request
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
    empty_balance = {"balance": None, "equity": None, "currency": None, "margin": None, "free_margin": None}

    if has_token and accounts:
        with ThreadPoolExecutor(max_workers=min(len(accounts), 5)) as executor:
            futures = {executor.submit(_fetch_wallet_balance, acc): acc for acc in accounts}
            balances = {acc.id: empty_balance for acc in accounts}
            for future in as_completed(futures):
                acc = futures[future]
                try:
                    balances[acc.id] = future.result()
                except Exception:
                    pass
    else:
        balances = {acc.id: empty_balance for acc in accounts}

    wallets_data = []
    for account in accounts:
        wallet_info = account.serialize()
        wallet_info.update(balances[account.id])
        wallets_data.append(wallet_info)

    closed_trades = Trade.query.filter_by(user_id=user_id, status="closed").all()
    open_trades   = Trade.query.filter_by(user_id=user_id, status="open").all()
    wins          = [t for t in closed_trades if (t.profit_loss or 0) > 0]
    realized_pnl  = sum(t.profit_loss or 0 for t in closed_trades)
    floating_pnl  = sum(t.profit_loss or 0 for t in open_trades if t.profit_loss is not None)
    total_profit  = realized_pnl + floating_pnl

    data = {
        "wallets": wallets_data,
        "stats": {
            "total_trades":   len(closed_trades),
            "winning_trades": len(wins),
            "losing_trades":  len(closed_trades) - len(wins),
            "win_rate":       round(len(wins) / len(closed_trades) * 100, 1) if closed_trades else 0,
            "total_profit":   round(total_profit, 2),
            "realized_pnl":   round(realized_pnl, 2),
            "floating_pnl":   round(floating_pnl, 2),
            "open_trades":    len(open_trades),
        },
    }

    return jsonify(data), 200


@dashboard_bp.route('/trades/history', methods=['GET'])
@jwt_required()
def get_trade_history():
    user_id = int(get_jwt_identity())
    page  = request.args.get("page",  1,   type=int)
    limit = request.args.get("limit", 50,  type=int)
    limit = min(limit, 200)

    query = Trade.query.filter_by(user_id=user_id, status="closed").order_by(Trade.closed_at.desc())
    total  = query.count()
    trades = query.offset((page - 1) * limit).limit(limit).all()

    return jsonify({
        "trades": [t.serialize() for t in trades],
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
    }), 200


@dashboard_bp.route('/trades/open', methods=['GET'])
@jwt_required()
def get_open_trades():
    user_id = int(get_jwt_identity())
    trades = Trade.query.filter_by(user_id=user_id, status='open').order_by(Trade.opened_at.desc()).all()
    return jsonify({"trades": [t.serialize() for t in trades]}), 200


@dashboard_bp.route('/sync', methods=['POST'])
@jwt_required()
def sync_trades():
    """
    Poll MetaAPI for open positions and deal history.
    Closes any DB Trade records that MetaAPI has already closed.
    MetaAPI calls: 2 (positions + history-deals).
    """
    user_id = int(get_jwt_identity())

    accounts = MetaApiAccount.query.filter_by(user_id=user_id, status="connected").all()
    if not accounts:
        return jsonify({"msg": "No connected wallets — nothing to sync"}), 200

    from api.trade_engine import sync_open_trades
    total_updated = 0
    for account in accounts:
        wallet_trades = Trade.query.filter_by(user_id=user_id, wallet_id=account.id, status="open").all()
        if wallet_trades:
            total_updated += sync_open_trades(account, wallet_trades, db)

    return jsonify({"msg": f"Synced all wallets", "updated": total_updated}), 200


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
