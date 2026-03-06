"""
Bot Controller
Endpoints: GET /bot/status, POST /bot/start, POST /bot/stop

Bot state is derived from UserStrategy.is_active:
- bot_active = True  → user has a UserStrategy with is_active=True
- start  → sets the user's latest UserStrategy to is_active=True
- stop   → sets all user's UserStrategies to is_active=False
"""

from flask import Blueprint, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.models.strategies import UserStrategy
from api.models.wallet import MetaApiAccount
from api.models.db import db

bot_bp = Blueprint('bot', __name__, url_prefix='/bot')


@bot_bp.route('/status', methods=['GET'])
@jwt_required()
def get_bot_status():
    user_id = int(get_jwt_identity())

    active_us = (
        UserStrategy.query
        .filter_by(user_id=user_id, is_active=True)
        .order_by(UserStrategy.created_at.desc())
        .first()
    )

    account = (
        MetaApiAccount.query
        .filter_by(user_id=user_id)
        .order_by(MetaApiAccount.created_at.desc())
        .first()
    )

    return jsonify({
        "bot_active": active_us is not None,
        "strategy": {
            "id": active_us.strategy.id,
            "name": active_us.strategy.name,
            "risk_level": active_us.strategy.risk_level,
        } if active_us else None,
        "account": account.serialize() if account else None,
    }), 200


@bot_bp.route('/start', methods=['POST'])
@jwt_required()
def start_bot():
    user_id = int(get_jwt_identity())

    latest_us = (
        UserStrategy.query
        .filter_by(user_id=user_id)
        .order_by(UserStrategy.created_at.desc())
        .first()
    )

    if not latest_us:
        abort(400, description="No strategy assigned. Select a strategy before starting the bot.")

    latest_us.is_active = True
    db.session.commit()

    return jsonify({
        "msg": "Bot started",
        "strategy": {
            "id": latest_us.strategy.id,
            "name": latest_us.strategy.name,
        },
    }), 200


@bot_bp.route('/stop', methods=['POST'])
@jwt_required()
def stop_bot():
    user_id = int(get_jwt_identity())

    UserStrategy.query.filter_by(user_id=user_id, is_active=True).update({"is_active": False})
    db.session.commit()

    return jsonify({"msg": "Bot stopped"}), 200
