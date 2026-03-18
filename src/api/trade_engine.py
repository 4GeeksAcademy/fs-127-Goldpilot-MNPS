"""
Trade Engine — V4 Ghost signal evaluation + MetaAPI order placement + trade sync
================================================================================
Applies PDH/PDL sweep logic directly on live M15 XAUUSD candles from MetaAPI.
No backtesting.py dependency — pure pandas/numpy matching backtest_engine.py logic.

MetaAPI call budget (2000/day limit):
  evaluate_signal()    = 2 calls (candles + account-info for equity)
  place_order()        = 1 call  (only when SIGNAL_FOUND)
  sync_open_trades()   = 2 calls (positions + history-deals)
  All calls are demand-driven (no background polling).
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone, timedelta

import numpy as np
import pandas as pd
import requests as req

logger = logging.getLogger(__name__)

# Reuse auth headers and base URL from wallet_controller
from api.controllers.wallet_controller import _metaapi_headers, METAAPI_CLIENT_BASE

# Risk params — identical to backtest_engine.py strategy_map
RISK_PARAMS: dict[str, dict] = {
    "low":    {"risk_pct": 0.005, "atr_sl_mult": 1.5, "rr_ratio": 3.0, "lookback": 24},
    "medium": {"risk_pct": 0.01,  "atr_sl_mult": 1.5, "rr_ratio": 3.0, "lookback": 24},
    "high":   {"risk_pct": 0.03,  "atr_sl_mult": 1.5, "rr_ratio": 3.0, "lookback": 24},
}


# ─── Candle fetcher ───────────────────────────────────────────────────────────

def _fetch_m15_candles(account) -> "pd.DataFrame | None":
    """
    Fetch last 50 M15 XAUUSD candles.
    Primary source: yfinance GC=F (Gold Futures, no API call budget cost).
    Fallback: MetaAPI historical-market-data (requires higher-tier MetaAPI plan).
    Returns DataFrame with columns: open, high, low, close (DatetimeIndex, UTC).
    """
    import yfinance as yf

    try:
        df = yf.download("GC=F", period="5d", interval="15m", progress=False)
        if df is not None and not df.empty:
            # yfinance returns multi-level columns like (Close, GC=F) — flatten to lowercase
            df.columns = [col[0].lower() for col in df.columns]
            df.index = pd.to_datetime(df.index, utc=True)
            df = df[["open", "high", "low", "close"]].dropna()
            if not df.empty:
                return df
    except Exception as e:
        logger.warning("yfinance candle fetch failed: %s — falling back to MetaAPI", e)

    # ── MetaAPI fallback (requires historical-market-data subscription) ────────
    base       = METAAPI_CLIENT_BASE.format(region=account.region)
    start_time = datetime.now(timezone.utc).isoformat()
    url        = (
        f"{base}/users/current/accounts/{account.account_id}"
        f"/historical-market-data/symbols/XAUUSD/timeframes/15m/candles"
    )
    try:
        resp = req.get(
            url,
            headers=_metaapi_headers(),
            params={"startTime": start_time, "limit": 50},
            timeout=15,
        )
    except Exception as e:
        logger.error("MetaAPI candles fetch failed: %s", e)
        return None

    if not resp.ok:
        logger.error("MetaAPI candles %s: %s", resp.status_code, resp.text[:200])
        return None

    raw = resp.json()
    if not raw:
        return None

    df = pd.DataFrame(raw)
    df.columns = [c.lower() for c in df.columns]
    if "time" not in df.columns:
        logger.error("MetaAPI candles missing 'time' column. Cols: %s", list(df.columns))
        return None
    df["time"] = pd.to_datetime(df["time"], utc=True, errors="coerce")
    df = df.dropna(subset=["time"]).set_index("time").sort_index()
    for col in ("open", "high", "low", "close"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["open", "high", "low", "close"])
    return df if not df.empty else None


# ─── ATR helper ──────────────────────────────────────────────────────────────

def _atr(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14) -> float:
    h, l, c = pd.Series(high), pd.Series(low), pd.Series(close)
    tr = pd.concat(
        [h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1
    ).max(axis=1)
    return float(tr.ewm(span=period, adjust=False).mean().iloc[-1])


# ─── Signal evaluation ────────────────────────────────────────────────────────

def evaluate_signal(account, risk_level: str, equity: float) -> dict:
    """
    Evaluate V4 Ghost PDH/PDL sweep on current M15 data.

    Returns:
        {"status": "SIGNAL_FOUND", "action": "BUY"|"SELL", "entry", "sl", "tp", "volume"}
        {"status": "WAITING",      "msg": "..."}
        {"status": "ERROR",        "msg": "..."}
    """
    params   = RISK_PARAMS.get(risk_level, RISK_PARAMS["medium"])
    lookback = params["lookback"]  # 24 bars

    df = _fetch_m15_candles(account)
    if df is None:
        return {"status": "ERROR", "msg": "Could not fetch M15 candles from MetaAPI"}

    if len(df) < lookback + 2:
        return {"status": "WAITING", "msg": f"Not enough bars ({len(df)} < {lookback + 2})"}

    # PDH / PDL from the last `lookback` closed bars (exclude the current forming bar)
    pdh = float(df["high"].iloc[-lookback - 1:-1].max())
    pdl = float(df["low"].iloc[-lookback - 1:-1].min())

    curr_high  = float(df["high"].iloc[-1])
    curr_low   = float(df["low"].iloc[-1])
    curr_close = float(df["close"].iloc[-1])

    atr_val = _atr(df["high"].values, df["low"].values, df["close"].values)
    if atr_val <= 0:
        return {"status": "WAITING", "msg": "ATR is zero — no volatility data"}

    sl_dist = atr_val * params["atr_sl_mult"]
    tp_dist = sl_dist * params["rr_ratio"]
    # lot size: risk_pct of equity / (sl_dist in price × 100 oz/lot for gold)
    volume  = round(max(0.01, (equity * params["risk_pct"]) / (sl_dist * 100)), 2)

    # LONG — wick below PDL, close back above PDL (liquidity sweep)
    if curr_low < pdl and curr_close > pdl:
        return {
            "status": "SIGNAL_FOUND",
            "action": "BUY",
            "entry":  round(curr_close, 2),
            "sl":     round(curr_close - sl_dist, 2),
            "tp":     round(curr_close + tp_dist, 2),
            "volume": volume,
        }

    # SHORT — wick above PDH, close back below PDH (liquidity sweep)
    if curr_high > pdh and curr_close < pdh:
        return {
            "status": "SIGNAL_FOUND",
            "action": "SELL",
            "entry":  round(curr_close, 2),
            "sl":     round(curr_close + sl_dist, 2),
            "tp":     round(curr_close - tp_dist, 2),
            "volume": volume,
        }

    return {
        "status": "WAITING",
        "msg":    "No PDH/PDL sweep on current M15 bar",
        "pdh":    round(pdh, 2),
        "pdl":    round(pdl, 2),
        "price":  round(curr_close, 2),
    }


# ─── Order placement ─────────────────────────────────────────────────────────

def place_order(account, signal: dict) -> tuple[dict | None, str | None]:
    """
    Place a market order on MetaAPI.  1 API call.
    Returns (response_dict, None) on success, (None, error_str) on failure.
    """
    base = METAAPI_CLIENT_BASE.format(region=account.region)
    url  = f"{base}/users/current/accounts/{account.account_id}/trade"
    body: dict = {
        "actionType": "ORDER_TYPE_BUY" if signal["action"] == "BUY" else "ORDER_TYPE_SELL",
        "symbol":     "XAUUSD",
        "volume":     signal["volume"],
    }
    # Only include SL/TP if they are explicitly provided and non-zero
    if signal.get("sl"):
        body["stopLoss"]   = signal["sl"]
    if signal.get("tp"):
        body["takeProfit"] = signal["tp"]
    try:
        resp = req.post(url, json=body, headers=_metaapi_headers(), timeout=10)
    except Exception as e:
        logger.error("MetaAPI place_order exception: %s", e)
        return None, str(e)

    if resp.ok:
        return resp.json(), None

    error = f"HTTP {resp.status_code}: {resp.text[:300]}"
    logger.error("MetaAPI place_order %s", error)
    return None, error


# ─── Trade sync ──────────────────────────────────────────────────────────────

def sync_open_trades(account, open_trades: list, db) -> int:
    """
    Poll MetaAPI for open positions and deal history.  2 API calls total.
    Closes any DB Trade records that MetaAPI has already closed.
    Returns the number of trades updated.
    """
    base = METAAPI_CLIENT_BASE.format(region=account.region)

    # 1 call — get current open positions
    try:
        pos_resp = req.get(
            f"{base}/users/current/accounts/{account.account_id}/positions",
            headers=_metaapi_headers(),
            timeout=10,
        )
        open_meta_ids = set()
        if pos_resp.ok:
            open_meta_ids = {str(p.get("id", "")) for p in pos_resp.json()}
    except Exception as e:
        logger.error("MetaAPI positions fetch failed: %s", e)
        return 0

    # Build position profit map for still-open trades
    positions_by_id: dict[str, dict] = {}
    if pos_resp.ok:
        for p in pos_resp.json():
            positions_by_id[str(p.get("id", ""))] = p

    # Update floating P&L for trades still open in MetaAPI
    still_open = [t for t in open_trades if t.meta_trade_id and t.meta_trade_id in open_meta_ids]
    updated = 0
    for trade in still_open:
        pos = positions_by_id.get(trade.meta_trade_id)
        if pos:
            live_profit = pos.get("profit") or pos.get("unrealizedProfit")
            if live_profit is not None:
                trade.profit_loss = float(live_profit)
                updated += 1

    # Find trades that are no longer open on MetaAPI (closed/SL/TP hit)
    to_close = [t for t in open_trades if t.meta_trade_id and t.meta_trade_id not in open_meta_ids]
    if not to_close:
        if updated:
            db.session.commit()
        return updated

    # 1 call — get deal history covering the oldest open trade
    oldest_opened = min(
        (t.opened_at for t in to_close if t.opened_at),
        default=datetime.now(timezone.utc) - timedelta(days=7),
    )
    start = oldest_opened.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    end   = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    deals_by_pos: dict[str, list] = {}
    try:
        hist_resp = req.get(
            f"{base}/users/current/accounts/{account.account_id}/history-deals/time/{start}/{end}",
            headers=_metaapi_headers(),
            timeout=10,
        )
        if hist_resp.ok:
            for deal in hist_resp.json():
                pid = str(deal.get("positionId", ""))
                if pid:
                    deals_by_pos.setdefault(pid, []).append(deal)
    except Exception as e:
        logger.error("MetaAPI history-deals fetch failed: %s", e)

    for trade in to_close:
        pos_deals = deals_by_pos.get(trade.meta_trade_id, [])
        closing = next(
            (d for d in pos_deals if d.get("entryType") == "DEAL_ENTRY_OUT"),
            None,
        )
        trade.close_price = float(closing["price"]) if closing and closing.get("price") else trade.open_price
        trade.profit_loss = float(closing["profit"]) if closing and closing.get("profit") is not None else 0.0
        trade.status      = "closed"
        trade.closed_at   = datetime.now(timezone.utc)
        updated += 1

    if updated:
        db.session.commit()

    return updated


# ─── Prop Firm Guard ──────────────────────────────────────────────────────────

def check_prop_firm_guard(account) -> dict:
    """
    Check whether the prop firm daily loss limit has been hit.
    Returns:
        blocked    : True if trading must stop for today
        daily_pnl  : sum of closed trade P&L today (this wallet)
        limit      : dollar threshold (negative) e.g. -250.0
        target     : profit target in dollars e.g. 500.0
        reason     : human-readable string
    Only call when account.is_prop_firm=True.
    """
    from api.models.trade import Trade
    from api.models.db import db as _db

    today = datetime.now(timezone.utc).date()
    today_trades = Trade.query.filter(
        Trade.wallet_id == account.id,
        Trade.status    == "closed",
        _db.func.date(Trade.closed_at) == today,
    ).all()

    daily_pnl   = sum(t.profit_loss or 0.0 for t in today_trades)
    # Use fixed dollar amounts when set (prop_max_loss_usd / prop_profit_target_usd)
    # Fall back to percentage-based calculation for legacy records
    initial_bal = account.prop_initial_balance or 5_000.0
    if account.prop_max_loss_usd is not None:
        daily_limit = -abs(account.prop_max_loss_usd)
    else:
        daily_limit = -(initial_bal * (account.prop_daily_loss_pct or 5.0) / 100)
    if account.prop_profit_target_usd is not None:
        profit_goal = account.prop_profit_target_usd
    else:
        profit_goal = initial_bal * (account.prop_profit_target_pct or 6.0) / 100

    blocked = daily_pnl <= daily_limit
    return {
        "blocked":   blocked,
        "daily_pnl": round(daily_pnl, 2),
        "limit":     round(daily_limit, 2),
        "target":    round(profit_goal, 2),
        "phase":     getattr(account, "prop_phase", None),
        "reason":    (
            f"Daily loss limit hit ({daily_pnl:.2f} ≤ {daily_limit:.2f})"
            if blocked else "OK"
        ),
    }
