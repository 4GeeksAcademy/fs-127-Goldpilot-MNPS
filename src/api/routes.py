import os
import asyncio
from flask import Flask, request, jsonify, Blueprint
from api.models.db import db
from api.models import User, Strategy
from api.utils import APIException
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import CORS

# SDK de MetaAPI
from metaapi_cloud_sdk import MetaApi

# Motores
from api.backtest_engine import execute_backtest_by_level
from api.live_engine import evaluate_live_market 

api = Blueprint('api', __name__)
CORS(api)

# -----------------------------------------------------------
# RUTAS DE ESTADO Y CONTROL DEL BOT (Sincronizadas con Frontend)
# -----------------------------------------------------------

@api.route('/bot/status', methods=['GET'])
@jwt_required()
def get_bot_status():
    """ Devuelve si el bot está encendido y qué estrategia tiene """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    # Simulamos o consultamos la cuenta vinculada (esto vendrá de tu tabla de Wallets)
    # Por ahora devolvemos un objeto mock para que el front no rompa
    return jsonify({
        "bot_active": getattr(user, "bot_enabled", False), # Asegúrate de tener esta columna en tu modelo User
        "strategy": {
            "name": getattr(user, "active_strategy", "Ninguna")
        },
        "account": {
            "broker_name": "MetaQuotes-Demo",
            "account_type": "demo",
            "status": "connected"
        }
    }), 200

@api.route('/bot/start', methods=['POST'])
@jwt_required()
def start_bot():
    """ Activa el bot con la estrategia recibida """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    body = request.get_json()
    strategy_name = body.get("strategy") # "X-Sniper Scalper", etc.

    if not strategy_name:
        return jsonify({"msg": "Debes seleccionar una estrategia"}), 400

    try:
        # 1. Guardamos el estado en la base de datos (Opcional pero recomendado)
        # user.bot_enabled = True
        # user.active_strategy = strategy_name
        # db.session.commit()

        # 2. Ejecutamos el escaneo inicial del mercado con el motor live
        # Mapeamos el nombre largo a 'low', 'medium', 'high' si es necesario
        level = "medium"
        if "Sniper" in strategy_name: level = "low"
        if "Grid" in strategy_name: level = "high"
        
        live_scan = evaluate_live_market(level)

        return jsonify({
            "msg": f"Bot activado con éxito usando {strategy_name}",
            "strategy": strategy_name,
            "live_scan": live_scan
        }), 200

    except Exception as e:
        return jsonify({"msg": f"Error al arrancar el bot: {str(e)}"}), 500

@api.route('/bot/stop', methods=['POST'])
@jwt_required()
def stop_bot():
    """ Apaga el bot """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # user.bot_enabled = False
    # db.session.commit()

    return jsonify({"msg": "Bot detenido correctamente (Kill Switch activado)"}), 200

# -----------------------------------------------------------
# OTRAS RUTAS (Estrategias, Backtest y Tests)
# -----------------------------------------------------------

@api.route('/strategies', methods=['GET'])
def get_all_strategies():
    try:
        strategies = Strategy.query.all()
        return jsonify([s.serialize() for s in strategies]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/backtest/<string:level>', methods=['GET'])
def run_unified_backtest(level):
    try:
        balance_param = request.args.get('balance', default=10000.0, type=float)
        start_param = request.args.get('start', default='2024-01-01', type=str)
        data = execute_backtest_by_level(level, initial_cash=balance_param, start_date=start_param) 
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Tu ruta de prueba original de MetaAPI por si quieres seguir testeando conexión manual
@api.route('/test-trade', methods=['POST'])
def test_trade():
    token = os.getenv("METAAPI_TOKEN")
    account_id = os.getenv("METAAPI_ACCOUNT_ID")
    
    async def execute_trade():
        meta_api = MetaApi(token)
        account = await meta_api.metatrader_account_api.get_account(account_id)
        connection = account.get_rpc_connection()
        await connection.connect()
        await connection.wait_synchronized()
        result = await connection.create_market_buy_order('XAUUSD', 0.01)
        return result

    try:
        result = asyncio.run(execute_trade())
        return jsonify({"status": "success", "orderId": result['orderId']}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500