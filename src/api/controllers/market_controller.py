import os
from datetime import datetime, timezone

import requests as req
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.models.wallet import MetaApiAccount

market_bp = Blueprint("market", __name__, url_prefix="/market")

METAAPI_CLIENT_BASE = "https://mt-client-api-v1.{region}.agiliumtrade.ai"

VALID_TIMEFRAMES = {"1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1mn"}


def _metaapi_headers():
    token = os.getenv("METAAPI_TOKEN", "")
    return {"auth-token": token, "Content-Type": "application/json"}


def _find_connected_account(user_id):
    return MetaApiAccount.query.filter_by(
        user_id=user_id, status="connected"
    ).filter(MetaApiAccount.region.isnot(None)).first()


@market_bp.route("/candles", methods=["GET"])
@jwt_required()
def get_candles():
    """
    Retorna candles históricas OHLCV para un símbolo dado vía MetaApi.

    Query params:
      - symbol   (str)  : símbolo del instrumento, default 'XAUUSD'
      - timeframe (str) : '1m','5m','15m','30m','1h','4h','1d','1w','1mn' — default '1h'
      - limit    (int)  : número de velas, default 100, max 1000
      - startTime (str) : ISO-8601 datetime, default = now (carga hacia atrás)
    """
    user_id = int(get_jwt_identity())

    symbol = request.args.get("symbol", "XAUUSD").strip().upper()
    timeframe = request.args.get("timeframe", "1h").strip().lower()
    limit = min(int(request.args.get("limit", 100)), 1000)
    start_time = request.args.get("startTime", datetime.now(timezone.utc).isoformat())

    if timeframe not in VALID_TIMEFRAMES:
        return jsonify({"description": f"timeframe inválido. Permitidos: {', '.join(sorted(VALID_TIMEFRAMES))}"}), 400

    token = os.getenv("METAAPI_TOKEN", "")
    if not token or token == "your_metaapi_token_here":
        return jsonify({"description": "METAAPI_TOKEN no configurado"}), 503

    account = _find_connected_account(user_id)
    if not account:
        return jsonify({
            "description": "No hay wallets conectadas. Conecta una wallet MT para ver datos de mercado en tiempo real.",
            "candles": [],
        }), 200

    try:
        base = METAAPI_CLIENT_BASE.format(region=account.region)
        url = (
            f"{base}/users/current/accounts/{account.account_id}"
            f"/historical-market-data/symbols/{symbol}"
            f"/timeframes/{timeframe}/candles"
        )
        resp = req.get(
            url,
            params={"startTime": start_time, "limit": limit},
            headers=_metaapi_headers(),
            timeout=15,
        )

        if not resp.ok:
            error_msg = "Error de MetaApi"
            try:
                error_msg = resp.json().get("message", resp.text[:200])
            except Exception:
                error_msg = resp.text[:200]
            return jsonify({"description": error_msg, "candles": []}), 200

        raw_candles = resp.json()

        candles = [
            {
                "time": c.get("time"),
                "open": c.get("open"),
                "high": c.get("high"),
                "low": c.get("low"),
                "close": c.get("close"),
                "volume": c.get("tickVolume", 0),
            }
            for c in raw_candles
            if c.get("open") is not None
        ]

        # MetaApi devuelve en orden cronológico inverso → lo invertimos
        candles.sort(key=lambda c: c["time"])

        return jsonify({"candles": candles, "symbol": symbol, "timeframe": timeframe}), 200

    except req.exceptions.Timeout:
        return jsonify({"description": "Timeout al conectar con MetaApi", "candles": []}), 200
    except req.exceptions.RequestException as exc:
        return jsonify({"description": f"Error de red: {str(exc)}", "candles": []}), 200


@market_bp.route("/price", methods=["GET"])
@jwt_required()
def get_price():
    """
    Returns current XAUUSD bid/ask from MetaAPI.  1 API call.
    Query param: symbol (default XAUUSD)
    """
    user_id = int(get_jwt_identity())
    symbol  = request.args.get("symbol", "XAUUSD").strip().upper()

    token = os.getenv("METAAPI_TOKEN", "")
    if not token or token == "your_metaapi_token_here":
        return jsonify({"error": "METAAPI_TOKEN not set"}), 503

    account = _find_connected_account(user_id)
    if not account:
        return jsonify({"error": "No connected wallet"}), 200

    try:
        base = METAAPI_CLIENT_BASE.format(region=account.region)
        url  = f"{base}/users/current/accounts/{account.account_id}/symbols/{symbol}/current-price"
        resp = req.get(url, headers=_metaapi_headers(), timeout=10)
        if resp.ok:
            data = resp.json()
            return jsonify({
                "symbol": symbol,
                "bid":    data.get("bid"),
                "ask":    data.get("ask"),
                "time":   data.get("time"),
            }), 200
        # Fallback: get price from latest candle
        candle_url = (
            f"{base}/users/current/accounts/{account.account_id}"
            f"/historical-market-data/symbols/{symbol}/timeframes/1m/candles"
        )
        cr = req.get(candle_url, headers=_metaapi_headers(),
                     params={"startTime": datetime.now(timezone.utc).isoformat(), "limit": 1},
                     timeout=10)
        if cr.ok:
            candles = cr.json()
            if candles:
                price = candles[0].get("close") or candles[0].get("open")
                return jsonify({"symbol": symbol, "bid": price, "ask": price, "time": candles[0].get("time")}), 200
        return jsonify({"error": resp.text[:200]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 200
