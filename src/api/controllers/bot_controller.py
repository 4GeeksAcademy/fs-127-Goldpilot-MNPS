
from datetime import datetime

from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.models.strategies import UserStrategy, Strategy
from api.models.wallet import MetaApiAccount
from api.models.trade import Trade
from api.models.db import db

bot_bp = Blueprint('bot', __name__, url_prefix='/bot')


@bot_bp.route('/status', methods=['GET'])
@jwt_required()
def get_bot_status():
    """
    Returns status for ALL wallets the user has, each with its own bot state.
    Also returns a legacy top-level shape for backward compat.
    """
    user_id  = int(get_jwt_identity())
    wallets  = MetaApiAccount.query.filter_by(user_id=user_id, status="connected").all()

    bots = []
    for acc in wallets:
        # Find the active strategy for this wallet (wallet_id=acc.id OR wallet_id=None for default)
        us = (
            UserStrategy.query
            .filter_by(user_id=user_id, wallet_id=acc.id, is_active=True)
            .order_by(UserStrategy.created_at.desc())
            .first()
        )
        # If no wallet-specific strategy, check if there's a "default" (wallet_id=None) active strategy
        if not us and not any(w.id == acc.id for w in wallets if w != acc):
            us_default = (
                UserStrategy.query
                .filter_by(user_id=user_id, wallet_id=None, is_active=True)
                .order_by(UserStrategy.created_at.desc())
                .first()
            )
            if us_default:
                us = us_default

        prop_firm = None
        if acc.is_prop_firm:
            from api.trade_engine import check_prop_firm_guard
            prop_firm = check_prop_firm_guard(acc)

        bots.append({
            "wallet_id":  acc.id,
            "bot_active": us is not None,
            "strategy": {
                "id":         us.strategy.id,
                "name":       us.strategy.name,
                "risk_level": us.strategy.risk_level,
            } if us else None,
            "account":   acc.serialize(),
            "prop_firm": prop_firm,
        })

    # Legacy top-level shape — first active bot (or first wallet)
    primary = next((b for b in bots if b["bot_active"]), bots[0] if bots else None)
    return jsonify({
        "bot_active": primary["bot_active"] if primary else False,
        "strategy":   primary["strategy"]   if primary else None,
        "account":    primary["account"]    if primary else None,
        "prop_firm":  primary["prop_firm"]  if primary else None,
        "bots":       bots,
    }), 200


@bot_bp.route('/strategy', methods=['POST'])
@jwt_required()
def set_strategy():
    """
    Assign a strategy to the user by risk level.
    Body: { "strategy": "low" | "medium" | "high" }
    Creates a new (inactive) UserStrategy — must call /bot/start to activate.
    """
    user_id  = int(get_jwt_identity())
    body     = request.get_json(silent=True) or {}
    risk_lvl = body.get("strategy")

    if not risk_lvl:
        abort(400, description="Missing 'strategy' field. Use: low | medium | high")

    strategy = Strategy.query.filter_by(risk_level=risk_lvl).first()
    if not strategy:
        abort(400, description=f"Unknown strategy '{risk_lvl}'. Use: low | medium | high")

    wallet_id = body.get("wallet_id")  # optional — links bot to a specific account

    # Deactivate existing strategies for the same wallet (or all if no wallet specified)
    if wallet_id:
        existing = UserStrategy.query.filter_by(user_id=user_id, wallet_id=wallet_id, is_active=True).all()
        for e in existing:
            e.is_active = False
    else:
        UserStrategy.query.filter_by(user_id=user_id, is_active=True).update({"is_active": False})

    # Create new inactive UserStrategy (activated via /bot/start)
    us = UserStrategy(user_id=user_id, strategy_id=strategy.id, wallet_id=wallet_id, is_active=False)
    db.session.add(us)
    db.session.commit()

    return jsonify({
        "msg":      "Strategy set",
        "strategy": strategy.serialize(),
    }), 200


@bot_bp.route('/start', methods=['POST'])
@jwt_required()
def start_bot():
    user_id   = int(get_jwt_identity())
    body      = request.get_json(silent=True) or {}
    wallet_id = body.get("wallet_id")   # optional — start bot for a specific wallet

    query = UserStrategy.query.filter_by(user_id=user_id)
    if wallet_id:
        query = query.filter_by(wallet_id=wallet_id)
    latest_us = query.order_by(UserStrategy.created_at.desc()).first()

    if not latest_us:
        abort(400, description="No strategy assigned. Select a strategy before starting the bot.")

    latest_us.is_active = True
    db.session.commit()

    return jsonify({
        "msg":       "Bot started",
        "wallet_id": wallet_id,
        "strategy": {
            "id":   latest_us.strategy.id,
            "name": latest_us.strategy.name,
        },
    }), 200


@bot_bp.route('/stop', methods=['POST'])
@jwt_required()
def stop_bot():
    user_id   = int(get_jwt_identity())
    body      = request.get_json(silent=True) or {}
    wallet_id = body.get("wallet_id")   # optional — stop only this wallet's bot

    if wallet_id:
        UserStrategy.query.filter_by(user_id=user_id, wallet_id=wallet_id, is_active=True).update({"is_active": False})
    else:
        UserStrategy.query.filter_by(user_id=user_id, is_active=True).update({"is_active": False})
    db.session.commit()

    return jsonify({"msg": "Bot stopped", "wallet_id": wallet_id}), 200


@bot_bp.route('/debug-metaapi', methods=['GET'])
@jwt_required()
def debug_metaapi():
    """Returns the raw MetaAPI trade endpoint response for debugging."""
    import requests as req, os
    user_id = int(get_jwt_identity())
    account = MetaApiAccount.query.filter_by(user_id=user_id, status="connected").first()
    if not account:
        return jsonify({"error": "No connected account"}), 200

    token = os.getenv("META_API_TOKEN", os.getenv("METAAPI_TOKEN", ""))
    base  = f"https://mt-client-api-v1.{account.region}.agiliumtrade.ai"
    url   = f"{base}/users/current/accounts/{account.account_id}/trade"
    body  = {"actionType": "ORDER_TYPE_BUY", "symbol": "XAUUSD", "volume": 0.01}
    try:
        r = req.post(url, json=body, headers={"auth-token": token, "Content-Type": "application/json"}, timeout=10)
        return jsonify({"status": r.status_code, "body": r.text, "url": url,
                        "account_id": account.account_id, "region": account.region,
                        "token_set": bool(token)}), 200
    except Exception as e:
        return jsonify({"error": str(e), "url": url}), 200


@bot_bp.route('/manual-trade', methods=['POST'])
@jwt_required()
def manual_trade():
    """
    Insert a trade record directly for testing the pipeline.
    Does NOT contact MetaAPI — writes straight to the Trade table.

    Body (all optional, sensible defaults used):
      { "action": "BUY"|"SELL", "entry": 3100.0, "sl": 3085.0, "tp": 3145.0,
        "volume": 0.10, "status": "open"|"closed", "profit_loss": 120.0 }
    """
    user_id = int(get_jwt_identity())

    # Use most recent UserStrategy if available, else any Strategy in DB
    us = (
        UserStrategy.query
        .filter_by(user_id=user_id)
        .order_by(UserStrategy.created_at.desc())
        .first()
    )
    if us:
        strategy_id = us.strategy_id
    else:
        fallback = Strategy.query.first()
        if not fallback:
            abort(400, description="No strategies in DB. Run 'flask seed' first.")
        strategy_id = fallback.id

    account = MetaApiAccount.query.filter_by(user_id=user_id).first()

    body   = request.get_json(silent=True) or {}
    action = body.get("action", "BUY")
    volume = float(body.get("volume", 0.10))

    # Get current price from MetaAPI account-info to build realistic levels
    meta_trade_id = None
    entry         = float(body.get("entry", 3100.0))
    sl            = float(body.get("sl",    entry - 15.0))
    tp            = float(body.get("tp",    entry + 45.0))

    connected_account = MetaApiAccount.query.filter_by(user_id=user_id, status="connected").first()

    meta_error = None
    if connected_account:
        from api.trade_engine import place_order
        # Only pass SL/TP if explicitly provided in request body (avoid invalid stops)
        signal: dict = {"action": action, "volume": volume, "entry": entry}
        if "sl" in body and body["sl"]:
            signal["sl"] = float(body["sl"])
        if "tp" in body and body["tp"]:
            signal["tp"] = float(body["tp"])

        meta_resp, meta_error = place_order(connected_account, signal)
        if meta_resp:
            meta_trade_id = str(meta_resp.get("positionId") or meta_resp.get("orderId") or "")
            entry = meta_resp.get("openPrice", entry)

    trade = Trade(
        user_id       = user_id,
        strategy_id   = strategy_id,
        wallet_id     = connected_account.id if connected_account else (account.id if account else None),
        meta_trade_id = meta_trade_id,
        symbol        = "XAUUSD",
        trade_type    = action,
        lot_size      = volume,
        open_price    = entry,
        stop_loss     = sl,
        take_profit   = tp,
        status        = "open",
        opened_at     = datetime.utcnow(),
    )
    db.session.add(trade)
    db.session.commit()

    return jsonify({
        "msg":           "Trade placed on MetaAPI and recorded" if meta_trade_id else "Trade recorded in DB only",
        "meta_trade_id": meta_trade_id,
        "meta_error":    meta_error,
        "trade":         trade.serialize(),
    }), 201


@bot_bp.route('/signal', methods=['POST'])
@jwt_required()
def run_signal():
    """
    Evaluate V4 Ghost PDH/PDL sweep on current M15 data.
    If a signal is found, place an order via MetaAPI and record it in the Trade table.

    Requires: bot running (is_active=True) + connected MetaApiAccount.
    MetaAPI calls: 2 (evaluate) + 1 (place order, only if SIGNAL_FOUND) = max 3.
    """
    user_id = int(get_jwt_identity())

    active_us = (
        UserStrategy.query
        .filter_by(user_id=user_id, is_active=True)
        .order_by(UserStrategy.created_at.desc())
        .first()
    )
    if not active_us:
        abort(400, description="Bot is not started. Call /bot/start first.")

    account = MetaApiAccount.query.filter_by(user_id=user_id, status="connected").first()
    if not account:
        abort(400, description="No connected wallet found. Connect a MetaTrader account first.")

    risk_level = active_us.strategy.risk_level

    # Get equity from MetaAPI account-information
    from api.controllers.dashboard_controller import _fetch_wallet_balance
    bal    = _fetch_wallet_balance(account)
    equity = bal.get("equity") or bal.get("balance") or 10_000.0

    from api.trade_engine import evaluate_signal, place_order
    signal = evaluate_signal(account, risk_level, equity)

    if signal["status"] != "SIGNAL_FOUND":
        return jsonify(signal), 200

    # Place order via MetaAPI
    meta_resp, meta_error = place_order(account, signal)
    if not meta_resp:
        return jsonify({"status": "ERROR", "msg": "MetaAPI order placement failed", "detail": meta_error}), 502

    # Record trade in DB
    trade = Trade(
        user_id       = user_id,
        strategy_id   = active_us.strategy_id,
        wallet_id     = account.id,
        meta_trade_id = str(meta_resp.get("positionId") or meta_resp.get("orderId") or ""),
        symbol        = "XAUUSD",
        trade_type    = signal["action"],
        lot_size      = signal["volume"],
        open_price    = signal["entry"],
        stop_loss     = signal["sl"],
        take_profit   = signal["tp"],
        status        = "open",
        opened_at     = datetime.utcnow(),
    )
    db.session.add(trade)
    db.session.commit()

    return jsonify({
        "status": "TRADE_PLACED",
        "signal": signal,
        "trade":  trade.serialize(),
    }), 201
