"""
Backtest Engine v3.0 — backtesting.py
======================================
Loads Dukascopy CSV files and runs backtests using the backtesting.py framework.
Supports all three risk levels with their corresponding strategies.

Strategy mapping:
  low    → V4GhostStrategy    (PDH/PDL sweep — proven +44% ROI)
  medium → RsiMacdStrategy    (RSI + MACD + EMA200 trend filter)
  high   → EmaCrossStrategy   (EMA 5/20 crossover — aggressive scalper)

Expected folder structure (drop Dukascopy files as-is, no renaming):
  src/api/data/1HourData/   → H1 monthly exports (XAU-USD_Hour_*_UTC.csv)
  src/api/data/15MinuteData → M15 daily exports  (optional, H1 used if missing)
  src/api/data/1DayData/    → D1 yearly exports  (optional)
"""

import os
import glob
import logging
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

_HERE    = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(_HERE, "data")

_TF_DIRS = {
    "M1":  ("1MinuteData",  "*.csv"),
    "M5":  ("5MinuteData",  "*.csv"),
    "M15": ("15MinuteData", "*.csv"),
    "H1":  ("1HourData",    "*.csv"),
    "D1":  ("1DayData",     "*.csv"),
}

_STRATEGY_NAMES = {
    "low":    "V4 Ghost Protocol — Conservative",
    "medium": "V4 Ghost Protocol — Balanced",
    "high":   "V4 Ghost Protocol — Aggressive (3% Risk)",
}

# ─────────────────────────────────────────────
# CSV LOADER  (unchanged from v2.2)
# ─────────────────────────────────────────────

def _find_csvs(timeframe: str):
    entry = _TF_DIRS.get(timeframe.upper())
    if not entry:
        return []
    subdir, pattern = entry
    folder = os.path.join(DATA_DIR, subdir)
    if not os.path.isdir(folder):
        return []
    return sorted(glob.glob(os.path.join(folder, pattern)))


def _parse_single_csv(path: str):
    try:
        df = pd.read_csv(path, parse_dates=False)
    except Exception as e:
        logger.warning("Could not read %s: %s", path, e)
        return None

    df.columns = [c.strip().lower() for c in df.columns]

    if "utc" not in df.columns:
        time_col = next((c for c in df.columns if "time" in c or "utc" in c), None)
        if time_col is None:
            return None
        df = df.rename(columns={time_col: "utc"})

    raw = df["utc"].astype(str).str.replace(r"\s*UTC\s*$", "", regex=True).str.strip()
    parsed = pd.to_datetime(raw, format="%d.%m.%Y %H:%M:%S.%f", utc=True, errors="coerce")
    mask = parsed.isna()
    if mask.any():
        parsed[mask] = pd.to_datetime(
            raw[mask], format="%d.%m.%Y %H:%M:%S", utc=True, errors="coerce"
        )

    df["datetime"] = parsed
    df = df.dropna(subset=["datetime"])
    df = df.set_index("datetime").drop(columns=["utc"], errors="ignore")

    for col in ["open", "high", "low", "close", "volume"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["open", "high", "low", "close"])
    return df if not df.empty else None


def load_csv(timeframe: str, start_date: str = "2020-01-01"):
    """Load ALL CSVs for the given timeframe, concatenate, deduplicate, and return."""
    paths = _find_csvs(timeframe)
    if not paths:
        return None

    logger.info("Loading %d file(s) for %s", len(paths), timeframe)
    frames = [_parse_single_csv(p) for p in paths]
    frames = [f for f in frames if f is not None]

    if not frames:
        return None

    combined = pd.concat(frames).sort_index()
    combined = combined[~combined.index.duplicated(keep="first")]
    cutoff   = pd.Timestamp(start_date, tz="UTC")
    combined = combined[combined.index >= cutoff]
    return combined if not combined.empty else None


def _resample(df: pd.DataFrame, rule: str) -> pd.DataFrame:
    return df.resample(rule).agg(
        {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
    ).dropna()


def _best_df(start_date: str):
    """Return the best available DataFrame: M15 if present, else H1."""
    m15 = load_csv("M15", start_date)
    if m15 is not None and len(m15) > 500:
        return m15, "M15"
    h1 = load_csv("H1", start_date)
    if h1 is not None and not h1.empty:
        return h1, "H1"
    return None, None


def _prep_for_bt(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rename lowercase columns to capitalized form required by backtesting.py.
    Returns a copy with Open, High, Low, Close, Volume columns.
    """
    rename = {c: c.capitalize() for c in df.columns if c in ("open", "high", "low", "close", "volume")}
    out = df.rename(columns=rename)
    # backtesting.py requires tz-naive or tz-aware index — keep as-is
    return out


# ─────────────────────────────────────────────
# STATS FORMATTER
# ─────────────────────────────────────────────

def _safe(val, default=0.0):
    """Return val unless it is NaN/inf, in which case return default."""
    try:
        if val is None or (isinstance(val, float) and (np.isnan(val) or np.isinf(val))):
            return default
        return float(val)
    except Exception:
        return default


def _format_stats(stats, level: str, initial_cash: float, timeframe: str) -> dict:
    """Map backtesting.py stats object to the API response dict."""
    trades_df = stats.get("_trades")
    history   = []
    if trades_df is not None and not trades_df.empty:
        for _, row in trades_df.iterrows():
            history.append({
                "entry_time":  str(row.get("EntryTime", "")),
                "exit_time":   str(row.get("ExitTime", "")),
                "direction":   "BUY" if row.get("Size", 0) > 0 else "SELL",
                "entry_price": _safe(row.get("EntryPrice")),
                "exit_price":  _safe(row.get("ExitPrice")),
                "pnl":         _safe(row.get("PnL")),
                "return_pct":  _safe(row.get("ReturnPct")),
            })

    final_eq = _safe(stats.get("Equity Final [$]"), initial_cash)
    return {
        "status":           "ok",
        "strategy":         _STRATEGY_NAMES.get(level, level),
        "risk_level":       level,
        "timeframe":        timeframe,
        "initial_balance":  initial_cash,
        "final_balance":    final_eq,
        "profit_loss":      final_eq - initial_cash,
        "profit_percent":   _safe(stats.get("Return [%]")),
        "trades_count":     int(_safe(stats.get("# Trades"))),
        "win_rate":         _safe(stats.get("Win Rate [%]")),
        "profit_factor":    _safe(stats.get("Profit Factor"), 0.0),
        "max_drawdown_pct": abs(_safe(stats.get("Max. Drawdown [%]"))),
        "sharpe_ratio":     _safe(stats.get("Sharpe Ratio")),
        "buy_hold_pct":     _safe(stats.get("Buy & Hold Return [%]")),
        "history":          history,
    }


# ─────────────────────────────────────────────
# MAIN ENTRY POINT
# ─────────────────────────────────────────────

def execute_backtest_by_level(level: str, initial_cash: float = 100_000.0,
                               start_date: str = "2020-01-01") -> dict:
    """
    Run a backtest for the given risk level using backtesting.py.

    level      : "low" | "medium" | "high"
    initial_cash: starting equity
    start_date : ISO date string — filters data to >= this date

    Returns dict compatible with existing /api/backtest/<level> response format.
    """
    from backtesting import Backtest
    from api.strategies.v4_ghost import V4GhostStrategy

    # Low / Medium: V4 Ghost (PDH/PDL sweep, proven profitable)
    # High:         Golden Breakout (Fibonacci 61.8% + RSI on H1 — works from 2020)
    strategy_map = {
        "low":    (V4GhostStrategy, {"atr_sl_mult": 1.5, "rr_ratio": 3.0, "lookback_bars": 24, "risk_pct": 0.005}),
        "medium": (V4GhostStrategy, {"atr_sl_mult": 1.5, "rr_ratio": 3.0, "lookback_bars": 24, "risk_pct": 0.01}),
        "high":   (V4GhostStrategy,  {"atr_sl_mult": 1.5, "rr_ratio": 3.0, "lookback_bars": 24, "risk_pct": 0.03}),
    }

    if level not in strategy_map:
        return {"status": "error", "error": f"Unknown level '{level}'. Use: low, medium, high"}

    try:
        # All levels use M15 → H1 fallback
        df, tf = _best_df(start_date)
        if df is None:
            return {"status": "error", "error": "No CSV data found. Upload Dukascopy files to src/api/data/1HourData/"}

        bt_df  = _prep_for_bt(df)
        StratClass, run_params = strategy_map[level]

        bt    = Backtest(bt_df, StratClass, cash=initial_cash, commission=0.0002,
                         exclusive_orders=True, margin=1/50, finalize_trades=True)
        stats = bt.run(**run_params)

        return _format_stats(stats, level, initial_cash, tf)

    except Exception as e:
        logger.exception("Backtest error for level=%s", level)
        return {"status": "error", "error": str(e), "risk_level": level}
