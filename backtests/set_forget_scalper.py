"""
Strategy: Set & Forget Scalper
================================
Algorithmically implements the scalp variant of the "Set and Forget Strategy 2025".

Multi-timeframe alignment required (4h + 1h both in sync):
  Bullish: 4h = HH+HL, 1h = HH+HL → look for longs only
  Bearish: 4h = LL+LH, 1h = LL+LH → look for shorts only

Entry conditions (ALL must be true):
  1. Price within 1h AOI zone (±tolerance)
  2. 50 EMA filter (price above EMA for longs, below for shorts)
  3. 15m shift of structure in trade direction
  4. Engulfing candle in trade direction
  5. RR ≥ rr_min (default 2.5)

Exit:
  TP at next 4h swing high (long) or swing low (short)
  SL just below/above AOI zone boundary

Rules (from strategy doc):
  - No breakeven moves
  - No partial exits
  - No time-based exits
  Session: 08:00–19:00 UTC (London open → 2h before NY close)

Requires: pre-computed MTF features via data.mtf_builder.build_mtf_features()
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import ta.trend as tat

from strategies.base import BaseScalpStrategy


class SetForgetScalper(BaseScalpStrategy):
    # ── Tunable parameters ──────────────────────────────────────────────────────
    ema_period: int        = 50      # EMA period for trend filter
    aoi_tolerance: float   = 20.0   # extra tolerance beyond AOI zone boundary ($) — optimized
    rr_min: float          = 1.5    # minimum risk-to-reward ratio — optimized (was 2.5)
    session_start: int     = 8      # UTC hour — London open
    session_end: int       = 19     # UTC hour — 2h before NY close

    # Disable the base class ATR-based TP/SL — we use our own computed levels
    atr_sl_mult: float = 1.0
    atr_tp_mult: float = 1.5

    def indicators(self) -> None:
        close = pd.Series(self.data.Close)

        # 50 EMA on the 1m bars
        ema_vals = (
            tat.EMAIndicator(close, window=self.ema_period)
            .ema_indicator()
            .bfill()
            .values
        )
        self._ema50 = self.I(lambda: ema_vals, name="EMA50")

        # MTF columns pre-computed by build_mtf_features() and stored in data
        def _col(name: str) -> np.ndarray:
            """Extract a pre-computed column from the data DataFrame."""
            if hasattr(self.data, name):
                return np.array(getattr(self.data, name), dtype=float)
            # Fallback: return zeros (column not present)
            return np.zeros(len(self.data.Close))

        self._trend_4h  = self.I(lambda: _col("htf_4h_trend"),  name="Trend4h")
        self._trend_1h  = self.I(lambda: _col("htf_1h_trend"),  name="Trend1h")
        self._aoi_low   = self.I(lambda: _col("htf_1h_aoi_low"),  name="AOI_lo")
        self._aoi_high  = self.I(lambda: _col("htf_1h_aoi_high"), name="AOI_hi")
        self._tp_long   = self.I(lambda: _col("htf_4h_tp_long"),  name="TP_long")
        self._tp_short  = self.I(lambda: _col("htf_4h_tp_short"), name="TP_short")
        self._sos       = self.I(lambda: _col("m15_sos"),          name="SoS15m")
        self._eng_bull  = self.I(lambda: _col("engulf_bull"),      name="EngBull")
        self._eng_bear  = self.I(lambda: _col("engulf_bear"),      name="EngBear")

    # ── Session filter override (uses our session_start/end) ──────────────────
    def _in_session(self) -> bool:
        try:
            hour = self.data.index[-1].hour
        except Exception:
            return True
        return self.session_start <= hour < self.session_end

    def signals(self) -> None:
        # ── Session guard ──────────────────────────────────────────────────────
        if not self._in_session():
            return

        price      = self.data.Close[-1]
        ema        = self._ema50[-1]
        trend_4h   = int(self._trend_4h[-1])
        trend_1h   = int(self._trend_1h[-1])
        aoi_lo     = self._aoi_low[-1]
        aoi_hi     = self._aoi_high[-1]
        tp_long    = self._tp_long[-1]
        tp_short   = self._tp_short[-1]
        sos        = int(self._sos[-1])
        eng_bull   = int(self._eng_bull[-1])
        eng_bear   = int(self._eng_bear[-1])

        in_aoi     = not np.isnan(aoi_lo) and not np.isnan(aoi_hi)

        # ── Exit open positions when price leaves AOI ──────────────────────────
        if self.position.is_long and not in_aoi:
            # Price has left the zone — let SL/TP handle exits; no manual close
            pass
        if self.position.is_short and not in_aoi:
            pass

        # ── LONG setup ────────────────────────────────────────────────────────
        if (
            trend_4h == 1           # 4h bullish
            and trend_1h == 1       # 1h bullish
            and in_aoi              # price in AOI zone
            and price > ema         # above 50 EMA
            and sos == 1            # 15m bull shift of structure
            and eng_bull == 1       # bullish engulfing candle
            and not self.position.is_long
        ):
            if not np.isnan(tp_long) and tp_long > price:
                sl = aoi_lo - self.aoi_tolerance
                tp = tp_long
                risk   = price - sl
                reward = tp - price
                if risk > 0 and (reward / risk) >= self.rr_min:
                    if self.position.is_short:
                        self._close_all()
                    self.buy(sl=sl, tp=tp)

        # ── SHORT setup ───────────────────────────────────────────────────────
        elif (
            trend_4h == -1          # 4h bearish
            and trend_1h == -1      # 1h bearish
            and in_aoi              # price in AOI zone
            and price < ema         # below 50 EMA
            and sos == -1           # 15m bear shift of structure
            and eng_bear == 1       # bearish engulfing candle
            and not self.position.is_short
        ):
            if not np.isnan(tp_short) and tp_short < price:
                sl = aoi_hi + self.aoi_tolerance
                tp = tp_short
                risk   = sl - price
                reward = price - tp
                if risk > 0 and (reward / risk) >= self.rr_min:
                    if self.position.is_long:
                        self._close_all()
                    self.sell(sl=sl, tp=tp)
