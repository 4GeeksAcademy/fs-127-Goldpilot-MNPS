from flask import Flask, request, jsonify, url_for, Blueprint
from api.models.db import db
from api.models import User, Strategy # <-- Importamos Strategy
from api.utils import generate_sitemap, APIException
from api.controllers import register_controllers
# Importamos los motores (Backtest y Optimizer)
from api.backtest_engine import execute_backtest_by_level
from api.live_engine import evaluate_live_market
from api.optimizer_engine import run_optimization_async, get_status, get_results

api = Blueprint('api', __name__)

register_controllers(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }
    return jsonify(response_body), 200

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
        start_param = request.args.get('start', default='2026-01-01', type=str)
        
        data = execute_backtest_by_level(level, initial_cash=balance_param, start_date=start_param) 
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route('/optimize', methods=['POST', 'GET'])
def start_optimization():
    """Launch full grid-search optimization in background."""
    balance   = request.args.get('balance', default=100_000.0, type=float)
    start     = request.args.get('start',   default='2024-01-01', type=str)
    result    = run_optimization_async(balance=balance, start_date=start)
    return jsonify(result), 202


@api.route('/optimize/status', methods=['GET'])
def optimization_status():
    """Check if optimization is running and how far it has progressed."""
    return jsonify(get_status()), 200


@api.route('/optimize/results', methods=['GET'])
def optimization_results():
    """Return the ranked results from the last completed optimization run."""
    return jsonify(get_results()), 200


@api.route('/activate-live-bot', methods=['POST'])
def activate_live_bot():
    body = request.get_json()
    
    if not body or "strategy_id" not in body:
        return jsonify({"error": "Falta strategy_id"}), 400

    strategy_id = body.get("strategy_id") # "low", "medium", "high"
    
    try:
        live_scan = evaluate_live_market(strategy_id)

        return jsonify({
            "status": "success",
            "msg": f"¡Bot armado y vigilando con protocolo {strategy_id.upper()}!",
            "live_scan": live_scan
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
