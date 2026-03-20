"""
Abstract base strategy for the XAUUSD scalping system.
All strategies extend backtesting.py's Strategy class.
Uses the 'ta' library (ta-finance) which supports Python 3.9+.
"""
from __future__ import annotations

from abc import abstractmethod

import numpy as np
import pandas as pd
import ta.volatility as tav
from backtesting import Strategy

from config import SESSION_START_HOUR, SESSION_END_HOUR, ATR_PERIOD


class BaseScalpStrategy(Strategy):
    """
    Common helpers shared by all three scalping strategies.

    Subclasses implement:
        - indicators()   → called once from init()
        - signals()      → called every bar from next()
    """

    # ── Session filter ─────────────────────────────────────────────────────────
    session_start: int   = SESSION_START_HOUR   # 13 UTC
    session_end: int     = SESSION_END_HOUR     # 17 UTC
    enforce_session: bool = True

    # ── ATR risk management ────────────────────────────────────────────────────
    atr_period: int    = ATR_PERIOD   # 14
    atr_sl_mult: float = 1.0
    atr_tp_mult: float = 1.5

    def init(self) -> None:
        high  = pd.Series(self.data.High)
        low   = pd.Series(self.data.Low)
        close = pd.Series(self.data.Close)

        atr_vals = (
            tav.AverageTrueRange(high, low, close, window=self.atr_period)
            .average_true_range()
            .fillna(0)
            .values
        )
        self._atr = self.I(lambda: atr_vals, name="ATR")
        self.indicators()

    @abstractmethod
    def indicators(self) -> None:
        """Compute strategy-specific indicators using self.I()."""

    def next(self) -> None:
        if self.enforce_session and not self._in_session():
            return
        self.signals()

    @abstractmethod
    def signals(self) -> None:
        """Generate buy/sell signals each bar."""

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _in_session(self) -> bool:
        """Return True when current bar's hour is within the trading session."""
        try:
            hour = self.data.index[-1].hour
        except Exception:
            return True
        return self.session_start <= hour < self.session_end

    def _open_long(self) -> None:
        if self.position.is_long:
            return
        atr = self._atr[-1]
        if atr <= 0:
            return
        price = self.data.Close[-1]
        self.buy(sl=price - atr * self.atr_sl_mult,
                 tp=price + atr * self.atr_tp_mult)

    def _open_short(self) -> None:
        if self.position.is_short:
            return
        atr = self._atr[-1]
        if atr <= 0:
            return
        price = self.data.Close[-1]
        self.sell(sl=price + atr * self.atr_sl_mult,
                  tp=price - atr * self.atr_tp_mult)

    def _close_all(self) -> None:
        if self.position:
            self.position.close()
