"""
Strategy 2: RSI + MACD Momentum
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Timeframe : 5m
Indicators: RSI(14), MACD(12,26,9), EMA(200) trend filter
Long      : RSI crosses up through 30 AND MACD bullish cross, price > EMA200
Short     : RSI crosses down through 70 AND MACD bearish cross, price < EMA200
Exit      : RSI extreme reached, MACD counter-cross, or ATR SL/TP
"""
from __future__ import annotations

import pandas as pd
import ta.momentum as tam
import ta.trend as tat
from backtesting.lib import crossover

from .base import BaseScalpStrategy


class RsiMacdStrategy(BaseScalpStrategy):
    # ── Parameters ─────────────────────────────────────────────────────────────
    rsi_period: int      = 14
    rsi_oversold: int    = 30
    rsi_overbought: int  = 70
    rsi_window: int      = 5   # bars to look back for RSI oversold/overbought
    macd_fast: int       = 12
    macd_slow: int       = 26
    macd_signal: int     = 9
    ema_trend: int       = 200

    def indicators(self) -> None:
        close = pd.Series(self.data.Close)

        rsi_vals = (
            tam.RSIIndicator(close, window=self.rsi_period)
            .rsi().fillna(50).values
        )

        macd_obj = tat.MACD(
            close,
            window_slow=self.macd_slow,
            window_fast=self.macd_fast,
            window_sign=self.macd_signal,
        )
        macd_line_vals   = macd_obj.macd().fillna(0).values
        macd_signal_vals = macd_obj.macd_signal().fillna(0).values

        ema200_raw = tat.EMAIndicator(close, window=self.ema_trend).ema_indicator()
        ema200_vals = ema200_raw.bfill().fillna(close).values

        self._rsi         = self.I(lambda: rsi_vals,         name="RSI")
        self._macd        = self.I(lambda: macd_line_vals,   name="MACD")
        self._macd_signal = self.I(lambda: macd_signal_vals, name="MACD_signal")
        self._ema200      = self.I(lambda: ema200_vals,      name="EMA200")

    def signals(self) -> None:
        price = self.data.Close[-1]
        rsi   = self._rsi[-1]

        above_trend  = price > self._ema200[-1]
        below_trend  = price < self._ema200[-1]
        macd_bullish = crossover(self._macd, self._macd_signal)
        macd_bearish = crossover(self._macd_signal, self._macd)

        # RSI threshold crossovers — check if RSI exited oversold/overbought in last rsi_window bars
        n = min(self.rsi_window, len(self._rsi) - 1)
        rsi_cross_up   = rsi > self.rsi_oversold   and any(self._rsi[-(i+2)] < self.rsi_oversold   for i in range(n))
        rsi_cross_down = rsi < self.rsi_overbought and any(self._rsi[-(i+2)] > self.rsi_overbought for i in range(n))

        # ── Long entry ────────────────────────────────────────────────────────
        if rsi_cross_up and macd_bullish and above_trend:
            if self.position.is_short:
                self._close_all()
            self._open_long()

        # ── Short entry ───────────────────────────────────────────────────────
        elif rsi_cross_down and macd_bearish and below_trend:
            if self.position.is_long:
                self._close_all()
            self._open_short()

        # ── Exit: RSI extreme or MACD flip ────────────────────────────────────
        elif self.position.is_long and (rsi >= self.rsi_overbought or macd_bearish):
            self._close_all()

        elif self.position.is_short and (rsi <= self.rsi_oversold or macd_bullish):
            self._close_all()
