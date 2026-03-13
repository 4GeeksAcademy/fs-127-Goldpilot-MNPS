"""
Fibonacci Retracement Scalper — M1 XAUUSD
==========================================
High-risk, high-frequency scalping strategy.
Trades last < 5 minutes (force-exited via `max_bars_open`).

Concept:
  After a strong impulse move, price often retraces to the 61.8% Fibonacci
  ("golden ratio") level before continuing in the original direction.
  We enter at this retracement zone with a tight ATR stop and let backtesting.py
  manage the 1:3 RR target.

Entry — LONG (all conditions must be true):
  1. Price > EMA(ema_period) → uptrend confirmed
  2. RSI(rsi_period) < rsi_long_max  → slight oversold on the pullback
  3. Current close is within ±(ATR × fib_tolerance) of the 61.8% fib level

Entry — SHORT (mirror of long):
  1. Price < EMA(ema_period)
  2. RSI > rsi_short_min
  3. Close within ±(ATR × fib_tolerance) of the bearish 61.8% fib level

Exit:
  - TP = entry ± ATR × atr_sl_mult × rr_ratio
  - SL = entry ∓ ATR × atr_sl_mult
  - Force close after `max_bars_open` bars regardless (prevents overnight drag)

Risk:
  - risk_pct × equity per trade (default 2%)
  - margin=1/50 must be set in Backtest() constructor
"""
from __future__ import annotations

from datetime import timedelta

import numpy as np
import pandas as pd
from backtesting import Strategy


# ── Pure-numpy helpers (compatible with self.I()) ────────────────────────────

def _ema(close: np.ndarray, period: int) -> np.ndarray:
    return pd.Series(close).ewm(span=period, adjust=False).mean().values


def _rsi(close: np.ndarray, period: int) -> np.ndarray:
    s = pd.Series(close)
    delta = s.diff()
    gain = delta.clip(lower=0).ewm(com=period - 1, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(com=period - 1, adjust=False).mean()
    rs = gain / loss.replace(0, np.nan)
    return (100 - 100 / (1 + rs)).fillna(50).values


def _atr(high: np.ndarray, low: np.ndarray, close: np.ndarray,
         period: int) -> np.ndarray:
    h, l, c = pd.Series(high), pd.Series(low), pd.Series(close)
    tr = pd.concat(
        [h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1
    ).max(axis=1)
    return tr.ewm(span=period, adjust=False).mean().values


# ── Strategy ─────────────────────────────────────────────────────────────────

class FibonacciScalper(Strategy):
    """
    Fibonacci 61.8% retracement scalper on M1 XAUUSD.

    All parameters are exposed for grid-search via bt.optimize().
    """

    # ── Swing definition ───────────────────────────────────────────────────────
    swing_bars: int      = 60      # bars to measure recent swing H/L

    # ── Fibonacci ──────────────────────────────────────────────────────────────
    fib_entry: float     = 0.618   # enter at 61.8% retracement (golden ratio)
    fib_tolerance: float = 2.0     # ATR multiples to define the fib "zone"
    rng_min: float       = 3.0     # minimum swing range in price units (noise filter)

    # ── Indicators ────────────────────────────────────────────────────────────
    ema_period: int      = 20
    rsi_period: int      = 7
    atr_period: int      = 14

    # ── Signal filters ────────────────────────────────────────────────────────
    rsi_long_max: int    = 55      # long RSI must be below this (slight oversold)
    rsi_short_min: int   = 45      # short RSI must be above this

    # ── Risk / exit ───────────────────────────────────────────────────────────
    atr_sl_mult: float   = 2.5     # 2.5×ATR stop — room for M5 noise
    rr_ratio: float      = 2.0     # 1:2 RR
    risk_pct: float      = 0.005   # 0.5% equity per trade
    max_bars_open: int   = 300     # force-exit after 300 min wall-clock (intraday cap)

    # ── Session ───────────────────────────────────────────────────────────────
    session_start: int   = 7
    session_end: int     = 21

    def init(self) -> None:
        self._ema_vals = self.I(
            _ema, self.data.Close, self.ema_period, name="EMA"
        )
        self._rsi_vals = self.I(
            _rsi, self.data.Close, self.rsi_period, name="RSI"
        )
        self._atr_vals = self.I(
            _atr,
            self.data.High, self.data.Low, self.data.Close,
            self.atr_period,
            name="ATR",
        )

    def next(self) -> None:
        # ── Force-exit stale trades ───────────────────────────────────────────
        current_time = self.data.index[-1]
        for trade in list(self.trades):
            try:
                elapsed = current_time - trade.entry_time
                if elapsed >= timedelta(minutes=self.max_bars_open):
                    trade.close()
            except Exception:
                pass

        # ── Only one position at a time ───────────────────────────────────────
        if self.position:
            return

        # ── Session filter ────────────────────────────────────────────────────
        try:
            hour = current_time.hour
        except Exception:
            hour = 12
        if not (self.session_start <= hour < self.session_end):
            return

        # ── Enough bars for swing detection ───────────────────────────────────
        if len(self.data) < self.swing_bars + 2:
            return

        # ── Swing High / Low from previous `swing_bars` closed bars ──────────
        swing_h = float(np.max(self.data.High[-self.swing_bars - 1:-1]))
        swing_l = float(np.min(self.data.Low[-self.swing_bars - 1:-1]))
        rng = swing_h - swing_l

        # Ignore micro-ranges (noise) — configurable minimum range
        if rng < self.rng_min:
            return

        # ── Indicators ────────────────────────────────────────────────────────
        price = self.data.Close[-1]
        ema   = self._ema_vals[-1]
        rsi   = self._rsi_vals[-1]
        atr   = self._atr_vals[-1]

        if atr <= 0:
            return

        sl_dist = atr * self.atr_sl_mult
        tp_dist = sl_dist * self.rr_ratio
        zone    = atr * self.fib_tolerance

        if sl_dist <= 0:
            return

        # ── LONG — price retraces to 61.8% in uptrend ────────────────────────
        fib_long = swing_h - rng * self.fib_entry   # support zone center
        if (
            price > ema                              # uptrend
            and rsi < self.rsi_long_max              # pullback (not oversold extreme)
            and abs(price - fib_long) <= zone        # inside the fib zone
        ):
            sl   = price - sl_dist
            tp   = price + tp_dist
            size = max(int(round((self.equity * self.risk_pct) / sl_dist)), 1)
            self.buy(sl=sl, tp=tp, size=size)

        # ── SHORT — price retraces to 61.8% in downtrend ─────────────────────
        elif (
            price < ema                              # downtrend
            and rsi > self.rsi_short_min             # pullback (not overbought extreme)
            and abs(price - (swing_l + rng * self.fib_entry)) <= zone
        ):
            fib_short = swing_l + rng * self.fib_entry   # resistance zone center
            sl   = price + sl_dist
            tp   = price - tp_dist
            size = max(int(round((self.equity * self.risk_pct) / sl_dist)), 1)
            self.sell(sl=sl, tp=tp, size=size)


# Backward-compatible alias
class HighRiskStrategy(FibonacciScalper):
    pass
