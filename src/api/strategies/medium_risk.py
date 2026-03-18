"""
Aurum Liquidity Sniper — Medium Risk Strategy
==============================================
Logic: PDH/PDL + Tokyo H/L liquidity sweeps with rejection candle confirmation
       ATR-based SL, 1:3 RR, breakeven at 1:1, market structure filter
Kill Zones: London 07:00-16:00 UTC, NY 13:00-21:00 UTC
Risk: 1% per trade, max 4 trades/day
"""
import pandas as pd
import numpy as np
from datetime import timedelta


DEFAULT_PARAMS = {
    "atr_period": 14,
    "atr_sl_mult": 1.5,
    "rr": 3.0,
    "risk_pct": 0.01,
    "max_trades_per_day": 4,
    "use_tokyo_levels": True,
    "require_rejection_candle": False,  # False = accept any reversal close
    "candle_buffer": 15.0,              # extra buffer $ on rejection candle SL (updated for gold ~4500+)
    "kill_zones": [(7, 16), (13, 21)],  # (start, end) UTC — overlapping is fine
}


class LiquiditySniper:
    def __init__(self, params: dict = None):
        self.p = {**DEFAULT_PARAMS, **(params or {})}

    def run(self, df_m15: pd.DataFrame, df_h1: pd.DataFrame, df_h4: pd.DataFrame,
            initial_balance: float = 100_000.0) -> dict:
        balance = initial_balance
        trades = []
        trades_today = {}   # date → count

        p = self.p

        for i in range(100, len(df_m15) - 1):
            ts = df_m15.index[i]

            # Kill zone
            if not self._in_kill_zone(ts):
                continue

            date_str = str(ts.date())
            if trades_today.get(date_str, 0) >= p["max_trades_per_day"]:
                continue

            curr  = df_m15.iloc[i]
            prev  = df_m15.iloc[i - 1]
            prev2 = df_m15.iloc[i - 2]

            # Daily levels (PDH/PDL)
            prev_date = ts.date() - timedelta(days=1)
            prev_day = df_m15[df_m15.index.date == prev_date]
            if prev_day.empty:
                recent = df_m15.iloc[max(0, i - 96): i]
                pdh = recent["high"].max()
                pdl = recent["low"].min()
            else:
                pdh = prev_day["high"].max()
                pdl = prev_day["low"].min()

            # Tokyo levels (23:00–08:00 UTC)
            if p["use_tokyo_levels"]:
                tokyo_candles = df_m15[
                    (df_m15.index.date == ts.date()) &
                    ((df_m15.index.hour >= 23) | (df_m15.index.hour < 8)) &
                    (df_m15.index < ts)
                ]
                if not tokyo_candles.empty:
                    tokyo_high = tokyo_candles["high"].max()
                    tokyo_low  = tokyo_candles["low"].min()
                else:
                    tokyo_high = pdh
                    tokyo_low  = pdl
            else:
                tokyo_high = pdh
                tokyo_low  = pdl

            # Market structure (H1) — need at least 40 bars for the 25-bar lookback
            h1_slice = df_h1[df_h1.index <= ts].tail(40)
            structure = self._market_structure(h1_slice)

            # ATR from H1 (H4 ATR is too wide for entry-level SL sizing)
            h1_slice = df_h1[df_h1.index <= ts].tail(p["atr_period"] + 1)
            atr = self._atr(h1_slice)

            signal = self._detect_sweep(
                curr, prev, prev2, pdh, pdl, tokyo_high, tokyo_low,
                structure, p["require_rejection_candle"]
            )

            if not signal:
                continue

            direction, level_name, level_val = signal
            entry = curr["close"]

            if direction == "BUY":
                atr_sl   = entry - atr * p["atr_sl_mult"]
                candle_sl = curr["low"] - p["candle_buffer"]
                sl = max(atr_sl, candle_sl)
                risk = entry - sl
                if risk <= 0:
                    continue
                tp = entry + risk * p["rr"]
                be_trigger = entry + risk  # 1:1
            else:
                atr_sl    = entry + atr * p["atr_sl_mult"]
                candle_sl = curr["high"] + p["candle_buffer"]
                sl = min(atr_sl, candle_sl)
                risk = sl - entry
                if risk <= 0:
                    continue
                tp = entry - risk * p["rr"]
                be_trigger = entry - risk

            lot_size = max(0.01, round((balance * p["risk_pct"]) / (risk * 10), 2))

            future = df_m15.iloc[i + 1: i + 400]
            status, exit_price, be_hit = self._simulate(
                future, direction, entry, sl, tp, be_trigger)

            mult = 1 if direction == "BUY" else -1
            pnl = (exit_price - entry) * mult * lot_size * 10
            balance += pnl
            trades_today[date_str] = trades_today.get(date_str, 0) + 1

            trades.append({
                "date": ts.strftime("%Y-%m-%d %H:%M"),
                "type": direction,
                "entry_price": round(entry, 2),
                "exit_price": round(exit_price, 2),
                "lot_size": lot_size,
                "sl": round(sl, 2),
                "tp": round(tp, 2),
                "profit": round(pnl, 2),
                "result": status,
                "level": level_name,
                "structure": structure,
                "breakeven": be_hit,
                "balance": round(balance, 2),
            })

        return self._build_result(initial_balance, balance, trades)

    # ─────────────────────────────────────────────
    # HELPERS
    # ─────────────────────────────────────────────

    def _in_kill_zone(self, ts) -> bool:
        h = ts.hour
        for start, end in self.p["kill_zones"]:
            if start <= h <= end:
                return True
        return False

    def _market_structure(self, df: pd.DataFrame) -> str:
        """
        H1 market structure using EMA20 slope + HH/HL or LH/LL over 20-bar lookback.
        Returns BULLISH, BEARISH, or NEUTRAL.
        """
        if len(df) < 25:
            return "NEUTRAL"
        # EMA20 slope as primary trend filter
        ema = df["close"].ewm(span=20, adjust=False).mean()
        slope = ema.iloc[-1] - ema.iloc[-5]  # 5-bar slope
        # Recent vs previous swing highs/lows
        recent_high   = df["high"].iloc[-10:].max()
        previous_high = df["high"].iloc[-25:-10].max()
        recent_low    = df["low"].iloc[-10:].min()
        previous_low  = df["low"].iloc[-25:-10].min()
        bullish = (recent_high > previous_high and recent_low >= previous_low and slope > 0)
        bearish = (recent_low < previous_low and recent_high <= previous_high and slope < 0)
        if bullish:
            return "BULLISH"
        if bearish:
            return "BEARISH"
        return "NEUTRAL"

    def _atr(self, df: pd.DataFrame) -> float:
        if len(df) < 2:
            return 5.0
        highs  = df["high"].values
        lows   = df["low"].values
        closes = df["close"].values
        trs = [max(highs[j] - lows[j],
                   abs(highs[j] - closes[j - 1]),
                   abs(lows[j]  - closes[j - 1]))
               for j in range(1, len(df))]
        return float(np.mean(trs)) if trs else 5.0

    def _detect_sweep(self, curr, prev, prev2, pdh, pdl,
                      tokyo_high, tokyo_low, structure, require_rejection):
        # Only trade with confirmed directional structure (skip NEUTRAL)
        if structure == "NEUTRAL":
            return None

        levels_bull = [("PDL", pdl), ("TOKYO_LOW", tokyo_low)]
        levels_bear = [("PDH", pdh), ("TOKYO_HIGH", tokyo_high)]

        if structure in ("BULLISH",):
            for name, level in levels_bull:
                swept    = prev["low"] < level or prev2["low"] < level
                reversed_ = curr["close"] > level
                if swept and reversed_:
                    if not require_rejection or self._is_bullish_rejection(curr, prev):
                        return ("BUY", name, level)
                    elif curr["close"] > curr["open"]:
                        return ("BUY", name, level)

        if structure in ("BEARISH",):
            for name, level in levels_bear:
                swept    = prev["high"] > level or prev2["high"] > level
                reversed_ = curr["close"] < level
                if swept and reversed_:
                    if not require_rejection or self._is_bearish_rejection(curr, prev):
                        return ("SELL", name, level)
                    elif curr["close"] < curr["open"]:
                        return ("SELL", name, level)
        return None

    def _is_bullish_rejection(self, curr, prev) -> bool:
        body  = abs(curr["close"] - curr["open"])
        rng   = curr["high"] - curr["low"]
        if rng == 0:
            return False
        lower_wick = min(curr["open"], curr["close"]) - curr["low"]
        if lower_wick > rng * 0.6 and body < rng * 0.3:
            return True
        if (prev["close"] < prev["open"] and curr["close"] > curr["open"] and
                curr["open"] < prev["close"] and curr["close"] > prev["open"]):
            return True
        return False

    def _is_bearish_rejection(self, curr, prev) -> bool:
        body  = abs(curr["close"] - curr["open"])
        rng   = curr["high"] - curr["low"]
        if rng == 0:
            return False
        upper_wick = curr["high"] - max(curr["open"], curr["close"])
        if upper_wick > rng * 0.6 and body < rng * 0.3:
            return True
        if (prev["close"] > prev["open"] and curr["close"] < curr["open"] and
                curr["open"] > prev["close"] and curr["close"] < prev["open"]):
            return True
        return False

    def _simulate(self, future, side, entry, sl, tp, be_trigger):
        curr_sl = sl
        be_hit = False
        for _, c in future.iterrows():
            if not be_hit:
                if (side == "BUY" and c["high"] >= be_trigger) or \
                   (side == "SELL" and c["low"] <= be_trigger):
                    curr_sl = entry
                    be_hit = True
            if (side == "BUY" and c["low"] <= curr_sl) or \
               (side == "SELL" and c["high"] >= curr_sl):
                label = "BE ➖" if be_hit else "LOSS ❌"
                return label, curr_sl, be_hit
            if (side == "BUY" and c["high"] >= tp) or \
               (side == "SELL" and c["low"] <= tp):
                return "WIN ✅", tp, be_hit
        last = future.iloc[-1]["close"] if not future.empty else entry
        return "TIMEOUT ⏱", last, be_hit

    def _build_result(self, initial_balance, final_balance, trades):
        wins = [t for t in trades if "WIN" in t["result"]]
        win_rate = (len(wins) / len(trades) * 100) if trades else 0.0
        all_pnl = [t["profit"] for t in trades]
        gross_wins   = sum(p for p in all_pnl if p > 0)
        gross_losses = abs(sum(p for p in all_pnl if p < 0))
        profit_factor = (gross_wins / gross_losses) if gross_losses > 0 else 999.0
        peak = initial_balance
        max_dd = 0.0
        running = initial_balance
        for t in trades:
            running += t["profit"]
            if running > peak:
                peak = running
            dd = (peak - running) / peak * 100
            if dd > max_dd:
                max_dd = dd
        return {
            "status": "success",
            "strategy": "Aurum Liquidity Sniper",
            "risk_level": "medium",
            "initial_balance": initial_balance,
            "final_balance": round(final_balance, 2),
            "profit_loss": round(final_balance - initial_balance, 2),
            "profit_percent": round((final_balance - initial_balance) / initial_balance * 100, 2),
            "trades_count": len(trades),
            "win_rate": round(win_rate, 1),
            "profit_factor": round(profit_factor, 2),
            "max_drawdown_pct": round(max_dd, 2),
            "history": trades,
        }


# Backward-compatible alias
class MediumRiskStrategy(LiquiditySniper):
    pass
