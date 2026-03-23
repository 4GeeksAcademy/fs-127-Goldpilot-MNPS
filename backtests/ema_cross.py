"""
Strategy 1: EMA Cross Scalper
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Timeframe : 1m (scalping) or 5m (safer)
Indicators: EMA(5), EMA(20), RSI(14), ATR(14)
Long      : EMA5 crosses above EMA20, RSI < 65, in session
Short     : EMA5 crosses below EMA20, RSI > 35, in session
Exit      : ATR-based TP (1.5×) / SL (1.0×) — managed by backtesting.py
"""
from __future__ import annotations

import pandas as pd
import ta.momentum as tam
import ta.trend as tat
from backtesting.lib import crossover

from strategies.base import BaseScalpStrategy


class EmaCrossStrategy(BaseScalpStrategy):
    # ── Tunable parameters ──────────────────────────────────────────────────────
    ema_fast: int   = 5
    ema_slow: int   = 20
    rsi_period: int = 14
    rsi_upper: int  = 65   # long entry: RSI must be below this
    rsi_lower: int  = 35   # short entry: RSI must be above this

    def indicators(self) -> None:
        close = pd.Series(self.data.Close)

        ema_fast_vals = (
            tat.EMAIndicator(close, window=self.ema_fast)
            .ema_indicator().fillna(0).values
        )
        ema_slow_vals = (
            tat.EMAIndicator(close, window=self.ema_slow)
            .ema_indicator().fillna(0).values
        )
        rsi_vals = (
            tam.RSIIndicator(close, window=self.rsi_period)
            .rsi().fillna(50).values
        )

        self._ema_fast = self.I(lambda: ema_fast_vals, name="EMA_fast")
        self._ema_slow = self.I(lambda: ema_slow_vals, name="EMA_slow")
        self._rsi      = self.I(lambda: rsi_vals,      name="RSI")

    def signals(self) -> None:
        rsi = self._rsi[-1]

        # ── Long: EMA fast crosses above EMA slow ──────────────────────────────
        if crossover(self._ema_fast, self._ema_slow) and rsi < self.rsi_upper:
            if self.position.is_short:
                self._close_all()
            self._open_long()

        # ── Short: EMA fast crosses below EMA slow ─────────────────────────────
        elif crossover(self._ema_slow, self._ema_fast) and rsi > self.rsi_lower:
            if self.position.is_long:
                self._close_all()
            self._open_short()
