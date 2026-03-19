"""
Logic: Fibonacci 61.8% retracement + RSI(7) momentum cross + EMA(50) trend bias.

After a strong impulse, institutional money re-enters at the 61.8% golden ratio.
RSI crossing 50 confirms momentum has turned. 3% risk per trade = high risk/reward.

Differentiator from V4 Ghost:
  V4 Ghost (low/medium) = contrarian — sweeps above PDH / below PDL
  GoldenBreakout (high) = trend-continuation — retracement back into trend

Key edges:
  1. 61.8% fib level = highest-probability Fibonacci retracement (institutional magnet)
  2. RSI(7) cross 50 = momentum confirmation (not just "near the level")
  3. EMA(50) trend bias = only trade WITH the dominant H1 trend
  4. Breakeven at 1:1 — same proven edge as V4 Ghost
  5. 1:3 RR — needs only 25% win rate to break even
  6. 3% risk/trade — genuinely high risk vs 0.5–1% for low/medium
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from backtesting import Strategy


# ── Indicator helpers (same pattern as v4_ghost.py) ──────────────────────────

def _ema(arr: np.ndarray, period: int) -> np.ndarray:
    return pd.Series(arr).ewm(span=period, adjust=False).mean().values


def _atr(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14) -> np.ndarray:
    h, l, c = pd.Series(high), pd.Series(low), pd.Series(close)
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(span=period, adjust=False).mean().values


def _rsi(close: np.ndarray, period: int = 7) -> np.ndarray:
    s = pd.Series(close)
    delta = s.diff()
    gain = delta.clip(lower=0).ewm(com=period - 1, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(com=period - 1, adjust=False).mean()
    rs = gain / loss.replace(0, np.nan)
    rsi = 100 - 100 / (1 + rs)
    return rsi.fillna(50).values


# ── Strategy ──────────────────────────────────────────────────────────────────

class GoldenBreakout(Strategy):

    swing_bars: int      = 20
    fib_level: float     = 0.618
    fib_tolerance: float = 1.5
    ema_period: int      = 50
    rsi_period: int      = 7
    rsi_threshold: int   = 50
    atr_period: int      = 14
    atr_sl_mult: float   = 1.5
    rr_ratio: float      = 3.0
    risk_pct: float      = 0.03
    session_start: int   = 7
    session_end: int     = 21

    def init(self) -> None:
        self._ema_vals = self.I(_ema, self.data.Close, self.ema_period, name="EMA")
        self._atr_vals = self.I(
            _atr, self.data.High, self.data.Low, self.data.Close,
            self.atr_period, name="ATR",
        )
        self._rsi_vals = self.I(_rsi, self.data.Close, self.rsi_period, name="RSI")

    def next(self) -> None:
        close = self.data.Close[-1]
        for trade in self.trades:
            entry   = trade.entry_price
            sl_dist = abs(entry - trade.sl)
            if sl_dist == 0:
                continue
            if trade.is_long and close >= entry + sl_dist and trade.sl < entry:
                trade.sl = entry
            elif trade.is_short and close <= entry - sl_dist and trade.sl > entry:
                trade.sl = entry

        try:
            hour = self.data.index[-1].hour
        except Exception:
            hour = 12

        if hour >= self.session_end:
            for trade in list(self.trades):
                trade.close()
            return
        if hour < self.session_start:
            return

        if self.position:
            return

        min_bars = max(self.swing_bars, self.ema_period, self.atr_period) + 2
        if len(self.data) < min_bars:
            return

        ema      = self._ema_vals[-1]
        atr      = self._atr_vals[-1]
        rsi      = self._rsi_vals[-1]
        rsi_prev = self._rsi_vals[-2]

        if atr <= 0 or np.isnan(ema) or np.isnan(atr):
            return

        swing_h = float(np.max(self.data.High[-self.swing_bars:]))
        swing_l = float(np.min(self.data.Low[-self.swing_bars:]))
        rng     = swing_h - swing_l

        if rng < atr:
            return

        fib_long  = swing_h - rng * self.fib_level   # 61.8% below swing high
        fib_short = swing_l + rng * self.fib_level   # 61.8% above swing low
        zone      = atr * self.fib_tolerance

        sl_dist = atr * self.atr_sl_mult
        tp_dist = sl_dist * self.rr_ratio
        size    = max(int(round((self.equity * self.risk_pct) / sl_dist)), 1)

        if (close > ema
                and abs(close - fib_long) <= zone
                and rsi >= self.rsi_threshold > rsi_prev):
            self.buy(
                sl=close - sl_dist,
                tp=close + tp_dist,
                size=size,
            )

        elif (close < ema
                and abs(close - fib_short) <= zone
                and rsi <= self.rsi_threshold < rsi_prev):
            self.sell(
                sl=close + sl_dist,
                tp=close - tp_dist,
                size=size,
            )
