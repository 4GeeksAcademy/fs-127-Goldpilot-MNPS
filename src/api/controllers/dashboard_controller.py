"""
Controlador del Dashboard.
Expone el resumen de cuenta, estadísticas de trading y estrategia activa.
Blueprint: /dashboard
"""

from flask import Blueprint, jsonify

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/summary', methods=['GET'])
def get_summary():
    """
    Retorna el resumen del dashboard del usuario.
    Datos mock mientras MetaApi no está conectado.
    TODO: Reemplazar con datos reales de MetaApi cuando el servicio esté disponible.

    Returns:
        JSON con account (balance/equity), stats (trades/win_rate) y strategy activa.
    """
    mock_data = {
        "account": {
            "balance": 10000.00,
            "equity": 10326.40,
            "currency": "USD",
            "margin": 150.00,
            "free_margin": 10176.40,
            "is_connected": False,
        },
        "stats": {
            "total_trades": 24,
            "winning_trades": 16,
            "losing_trades": 8,
            "win_rate": 66.7,
            "total_profit": 326.40,
        },
        "strategy": {
            "name": "Medio",
            "risk_level": "2",
            "is_active": True,
        },
    }

    return jsonify(mock_data), 200


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
