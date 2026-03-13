"""
Optimizer Engine v2.0 — uses backtesting.py bt.optimize()
===========================================================
Replaces the manual grid-search loop with backtesting.py's built-in optimizer.
Runs each strategy's parameter space in the background and saves ranked results.

Usage (from routes.py):
    run_optimization_async(balance=100_000, start_date="2020-01-01")
    get_status()    → {"running": bool, "progress": "X/3", ...}
    get_results()   → saved JSON from last run
"""

import json
import logging
import os
import threading
from datetime import datetime

import numpy as np

logger = logging.getLogger(__name__)

_HERE        = os.path.dirname(os.path.abspath(__file__))
RESULTS_FILE = os.path.join(_HERE, "data", "optimizer_results.json")

# ── Thread-safe state ─────────────────────────────────────────────────────────
_state = {
    "running":    False,
    "progress":   "0/3",
    "last_run":   None,
    "error":      None,
}
_state_lock = threading.Lock()


def get_status() -> dict:
    with _state_lock:
        return dict(_state)


def get_results() -> dict:
    if not os.path.exists(RESULTS_FILE):
        return {"status": "no_results", "message": "Run /api/optimize first"}
    try:
        with open(RESULTS_FILE) as f:
            return json.load(f)
    except Exception as e:
        return {"status": "error", "error": str(e)}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _safe(val, default=0.0):
    try:
        if val is None or (isinstance(val, float) and (np.isnan(val) or np.isinf(val))):
            return default
        return float(val)
    except Exception:
        return default


def _format_opt(stats, strategy_name, level, best_params):
    return {
        "strategy":         strategy_name,
        "risk_level":       level,
        "best_params":      best_params,
        "return_pct":       _safe(stats.get("Return [%]")),
        "win_rate":         _safe(stats.get("Win Rate [%]")),
        "profit_factor":    _safe(stats.get("Profit Factor")),
        "max_drawdown_pct": abs(_safe(stats.get("Max. Drawdown [%]"))),
        "sharpe_ratio":     _safe(stats.get("Sharpe Ratio")),
        "trades_count":     int(_safe(stats.get("# Trades"))),
        "final_equity":     _safe(stats.get("Equity Final [$]")),
    }


def _run_optimize(balance, start_date):
    from backtesting import Backtest
    from api.backtest_engine import load_csv, _best_df, _prep_for_bt
    from api.strategies.v4_ghost import V4GhostStrategy
    from api.strategies.fibonacci_scalper import FibonacciScalper

    results = {}
    errors  = []

    # Low/Medium use M15 or H1; High uses M5
    df_swing, tf_swing = _best_df(start_date)
    if df_swing is None:
        with _state_lock:
            _state["running"] = False
            _state["error"]   = "No CSV data found"
        return

    bt_swing = _prep_for_bt(df_swing)
    logger.info("Optimizer (swing) using %s data: %d bars", tf_swing, len(bt_swing))

    # Load M5 for high risk scalper
    df_m5 = load_csv("M5", start_date)
    if df_m5 is None or len(df_m5) < 500:
        df_m5 = load_csv("M1", start_date)
        tf_high = "M1"
    else:
        tf_high = "M5"
    bt_m5 = _prep_for_bt(df_m5) if df_m5 is not None else None

    # ── 1 / 3  Low Risk — V4 Ghost ───────────────────────────────────────────
    with _state_lock:
        _state["progress"] = "1/3 — V4 Ghost (Low)"
    try:
        bt  = Backtest(bt_swing, V4GhostStrategy, cash=balance, commission=0.0002,
                       exclusive_orders=True, margin=1/50)
        opt = bt.optimize(
            lookback_bars = range(16, 33, 4),
            atr_sl_mult   = [1.0, 1.5, 2.0],
            rr_ratio      = [2.0, 3.0, 4.0],
            risk_pct      = [0.005],
            maximize      = "Equity Final [$]",
            constraint    = lambda p: p.rr_ratio >= 2,
            max_tries     = 200,
        )
        best_params = {
            "lookback_bars": int(opt._strategy.lookback_bars),
            "atr_sl_mult":   float(opt._strategy.atr_sl_mult),
            "rr_ratio":      float(opt._strategy.rr_ratio),
            "risk_pct":      0.005,
        }
        results["low"] = _format_opt(opt, "V4 Ghost Protocol — Conservative", "low", best_params)
    except Exception as e:
        logger.exception("Low opt failed")
        errors.append("low: " + str(e))

    # ── 2 / 3  Medium Risk — V4 Ghost ────────────────────────────────────────
    with _state_lock:
        _state["progress"] = "2/3 — V4 Ghost (Medium)"
    try:
        bt  = Backtest(bt_swing, V4GhostStrategy, cash=balance, commission=0.0002,
                       exclusive_orders=True, margin=1/50)
        opt = bt.optimize(
            lookback_bars = range(16, 33, 4),
            atr_sl_mult   = [1.0, 1.5, 2.0],
            rr_ratio      = [2.0, 3.0, 4.0],
            risk_pct      = [0.01],
            maximize      = "Equity Final [$]",
            constraint    = lambda p: p.rr_ratio >= 2,
            max_tries     = 200,
        )
        best_params = {
            "lookback_bars": int(opt._strategy.lookback_bars),
            "atr_sl_mult":   float(opt._strategy.atr_sl_mult),
            "rr_ratio":      float(opt._strategy.rr_ratio),
            "risk_pct":      0.01,
        }
        results["medium"] = _format_opt(opt, "V4 Ghost Protocol — Balanced", "medium", best_params)
    except Exception as e:
        logger.exception("Medium opt failed")
        errors.append("medium: " + str(e))

    # ── 3 / 3  High Risk — Fibonacci Scalper (M5) ────────────────────────────
    with _state_lock:
        _state["progress"] = "3/3 — Fibonacci Scalper (High)"
    if bt_m5 is None:
        errors.append("high: No M5/M1 data for Fibonacci scalper")
    else:
        try:
            bt  = Backtest(bt_m5, FibonacciScalper, cash=balance, commission=0.0002,
                           exclusive_orders=True, margin=1/50)
            opt = bt.optimize(
                swing_bars    = [40, 60, 80],
                atr_sl_mult   = [2.0, 2.5, 3.0],
                rr_ratio      = [2.0, 2.5, 3.0],
                max_bars_open = [120, 300, 480],
                rsi_long_max  = [50, 55, 60],
                maximize      = "Equity Final [$]",
                constraint    = lambda p: p.rr_ratio >= 2,
                max_tries     = 200,
            )
            best_params = {
                "swing_bars":    int(opt._strategy.swing_bars),
                "atr_sl_mult":   float(opt._strategy.atr_sl_mult),
                "rr_ratio":      float(opt._strategy.rr_ratio),
                "max_bars_open": int(opt._strategy.max_bars_open),
                "rsi_long_max":  int(opt._strategy.rsi_long_max),
            }
            results["high"] = _format_opt(opt, "Fibonacci Scalper", "high", best_params)
        except Exception as e:
            logger.exception("High opt failed")
            errors.append("high: " + str(e))

    # ── Save results ─────────────────────────────────────────────────────────
    output = {
        "status":     "ok",
        "timestamp":  datetime.utcnow().isoformat(),
        "data_tf":    tf_swing,
        "start_date": start_date,
        "results":    results,
        "errors":     errors,
    }
    os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)
    with open(RESULTS_FILE, "w") as f:
        json.dump(output, f, indent=2)

    with _state_lock:
        _state["running"]  = False
        _state["progress"] = "3/3"
        _state["last_run"] = datetime.utcnow().isoformat()
        _state["error"]    = "; ".join(errors) if errors else None


def run_optimization_async(balance=100_000.0, start_date="2020-01-01"):
    """Start optimization in background thread. Returns False if already running."""
    with _state_lock:
        if _state["running"]:
            return False
        _state["running"]  = True
        _state["progress"] = "0/3"
        _state["error"]    = None

    t = threading.Thread(target=_run_optimize, args=(balance, start_date), daemon=True)
    t.start()
    return True


def run_full_optimization(balance=100_000.0, start_date="2020-01-01"):
    """Synchronous — blocks until complete. Used for CLI testing."""
    _run_optimize(balance, start_date)
    return get_results()
