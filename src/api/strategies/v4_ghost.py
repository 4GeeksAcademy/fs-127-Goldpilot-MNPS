The ONLY proven profitable strategy from the evolution analysis (+44% ROI on demo).

Core rules (from STRATEGY_EVOLUTION_ANALYSIS.md — DO NOT add extra filters):
  1. PDH/PDL sweep detection (rolling high/low over `lookback_bars`)
  2. 1:1 breakeven trigger (ironclad shield — THE edge)
  3. Full 1:3 RR take profit (no partials — they reduce avg win)
  4. ATR × 1.5 stop loss
  5. Full session hours: London 07:00 + NY 13:00 combined → 07:00–21:00 UTC
  6. No displacement filter, no mean reversion filter, no time-based exits

Why it works: 5.9% win rate × 7.9:1 win/loss ratio = positive expectancy.
  Volume (100+ trades) + 40% breakeven rate + large wins = edge.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import ta.volatility as tav
import ta.trend as tat
from backtesting import Strategy


def _ema(arr: np.ndarray, period: int) -> np.ndarray:
    return pd.Series(arr).ewm(span=period, adjust=False).mean().values


def _atr(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14) -> np.ndarray:
    h, l, c = pd.Series(high), pd.Series(low), pd.Series(close)
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(span=period, adjust=False).mean().values


class V4GhostStrategy(Strategy):

    lookback_bars: int   = 24
    atr_period: int      = 14
    atr_sl_mult: float   = 1.5
    rr_ratio: float      = 3.0
    risk_pct: float      = 0.01   # fraction of equity risked per trade (1%)
    session_start: int   = 7
    session_end: int     = 21

    def init(self) -> None:
        self._atr_vals = self.I(
            _atr,
            self.data.High, self.data.Low, self.data.Close,
            self.atr_period,
            name="ATR",
        )

    def next(self) -> None:
        try:
            hour = self.data.index[-1].hour
        except Exception:
            hour = 12
        if not (self.session_start <= hour < self.session_end):
            return

        close = self.data.Close[-1]
        for trade in self.trades:
            entry = trade.entry_price
            if trade.sl == entry:   # already at breakeven — skip
                continue
            sl_dist = abs(entry - trade.sl)
            if sl_dist == 0:
                continue
            if trade.is_long and close >= entry + sl_dist and trade.sl < entry:
                trade.sl = entry
            elif trade.is_short and close <= entry - sl_dist and trade.sl > entry:
                trade.sl = entry

        if self.position:
            return

        if len(self.data) < self.lookback_bars + 2:
            return

        pdh = float(np.max(self.data.High[-self.lookback_bars - 1:-1]))
        pdl = float(np.min(self.data.Low[-self.lookback_bars - 1:-1]))

        curr_high  = self.data.High[-1]
        curr_low   = self.data.Low[-1]
        curr_close = self.data.Close[-1]
        atr        = self._atr_vals[-1]

        if atr <= 0:
            return

        sl_dist = atr * self.atr_sl_mult
        tp_dist = sl_dist * self.rr_ratio

        size = max(int(round((self.equity * self.risk_pct) / sl_dist)), 1)

        if curr_low < pdl and curr_close > pdl:
            sl = curr_close - sl_dist
            tp = curr_close + tp_dist
            self.buy(sl=sl, tp=tp, size=size)

        elif curr_high > pdh and curr_close < pdh:
            sl = curr_close + sl_dist
            tp = curr_close - tp_dist
            self.sell(sl=sl, tp=tp, size=size)


class LowRiskStrategy(V4GhostStrategy):
    pass
