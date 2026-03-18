"""
Strategy 3: Bollinger Band Squeeze Breakout
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Timeframe : 15m
Indicators: BB(20, 2.0) outer bands, BB(20, 1.0) inner bands, ATR(14)
Squeeze   : Inner BB width < outer BB width for squeeze_bars consecutive bars
Long      : Price closes above upper inner band after squeeze releases
Short     : Price closes below lower inner band after squeeze releases
Exit      : Price touches opposite outer BB or ATR SL hit
"""
from __future__ import annotations

import pandas as pd
import ta.volatility as tav

from .base import BaseScalpStrategy


class BollingerSqueezeStrategy(BaseScalpStrategy):
    # ── Parameters ─────────────────────────────────────────────────────────────
    bb_period: int       = 20
    bb_std_outer: float  = 2.0
    bb_std_inner: float  = 1.0
    squeeze_bars: int    = 5

    def indicators(self) -> None:
        close = pd.Series(self.data.Close)

        # Outer bands (2.0 std)
        bb_outer = tav.BollingerBands(close, window=self.bb_period,
                                       window_dev=self.bb_std_outer)
        self._bb_upper_outer = self.I(
            lambda: bb_outer.bollinger_hband().fillna(close).values,
            name="BB_upper_outer",
        )
        self._bb_lower_outer = self.I(
            lambda: bb_outer.bollinger_lband().fillna(close).values,
            name="BB_lower_outer",
        )

        # Inner bands (1.0 std)
        bb_inner = tav.BollingerBands(close, window=self.bb_period,
                                       window_dev=self.bb_std_inner)
        inner_upper = bb_inner.bollinger_hband().fillna(close).values
        inner_lower = bb_inner.bollinger_lband().fillna(close).values

        self._bb_upper_inner = self.I(lambda: inner_upper, name="BB_upper_inner")
        self._bb_lower_inner = self.I(lambda: inner_lower, name="BB_lower_inner")

        # Squeeze flag: inner width < outer width → 1, else 0
        outer_w = bb_outer.bollinger_hband() - bb_outer.bollinger_lband()
        inner_w = bb_inner.bollinger_hband() - bb_inner.bollinger_lband()
        squeeze_vals = (inner_w.fillna(0) < outer_w.fillna(0)).astype(float).values
        self._squeeze = self.I(lambda: squeeze_vals, name="Squeeze")

    def _squeeze_was_active(self) -> bool:
        """True if squeeze was active for the preceding squeeze_bars bars."""
        sq = self._squeeze
        n = self.squeeze_bars
        if len(sq) < n + 1:
            return False
        return all(sq[-(n + 1 + i)] == 1.0 for i in range(n))

    def signals(self) -> None:
        if not self._squeeze_was_active():
            return

        price       = self.data.Close[-1]
        upper_inner = self._bb_upper_inner[-1]
        lower_inner = self._bb_lower_inner[-1]
        upper_outer = self._bb_upper_outer[-1]
        lower_outer = self._bb_lower_outer[-1]

        # ── Long breakout above inner upper band ───────────────────────────────
        if price > upper_inner and not self.position.is_long:
            if self.position.is_short:
                self._close_all()
            self._open_long()

        # ── Short breakout below inner lower band ──────────────────────────────
        elif price < lower_inner and not self.position.is_short:
            if self.position.is_long:
                self._close_all()
            self._open_short()

        # ── Exit: price reaches opposite outer band ────────────────────────────
        elif self.position.is_long and price >= upper_outer:
            self._close_all()

        elif self.position.is_short and price <= lower_outer:
            self._close_all()
