"""
Aggressor Pulse — High Risk Strategy
=====================================
Logic: H1 trend bias → M15 EMA10/20 channel (value area) → M15 CHoCH trigger
Hard session exit at 21:00 UTC. 1% risk, 1:3 RR minimum.
"""
import pandas as pd
import numpy as np


DEFAULT_PARAMS = {
    "ema_fast": 10,
    "ema_slow": 20,
    "ema_channel_mult": 1.0,    # expand value area by N× ATR on each side
    "h1_window": 3,             # bars to determine H1 trend (Higher Highs/Lows)
    "choch_body_mult": 1.5,     # body must be N× avg last 5 bodies for CHoCH
    "atr_period": 14,
    "rr": 3.0,
    "risk_pct": 0.01,
    "session_start": 7,         # UTC
    "session_end": 21,          # UTC hard exit
}


class AggressorPulse:
    def __init__(self, params: dict = None):
        self.p = {**DEFAULT_PARAMS, **(params or {})}

    def run(self, df_m15: pd.DataFrame, df_h1: pd.DataFrame,
            initial_balance: float = 100_000.0) -> dict:
        balance = initial_balance
        trades = []
        p = self.p

        # Pre-compute M15 EMAs
        df_m15 = df_m15.copy()
        df_m15["ema_fast"] = df_m15["close"].ewm(span=p["ema_fast"], adjust=False).mean()
        df_m15["ema_slow"] = df_m15["close"].ewm(span=p["ema_slow"], adjust=False).mean()

        # Pre-compute H1 trend column
        df_h1 = df_h1.copy()

        for i in range(max(30, p["atr_period"] + 5), len(df_m15) - 1):
            ts = df_m15.index[i]
            h = ts.hour

            # Session filter
            if not (p["session_start"] <= h < p["session_end"]):
                continue

            curr = df_m15.iloc[i]

            # 1. H1 trend bias
            h1_slice = df_h1[df_h1.index <= ts].tail(p["h1_window"] + 5)
            trend = self._h1_trend(h1_slice, p["h1_window"])
            if trend == "NEUTRAL":
                continue

            # 2. EMA channel — price must be within the value area
            # Expanded by ema_channel_mult × ATR to catch pullbacks near the channel
            ema_f = curr["ema_fast"]
            ema_s = curr["ema_slow"]
            price = curr["close"]
            atr_channel = self._atr(df_m15.iloc[i - p["atr_period"]: i])
            buffer = atr_channel * p["ema_channel_mult"]
            ema_min = min(ema_f, ema_s) - buffer
            ema_max = max(ema_f, ema_s) + buffer

            in_value_area = ema_min <= price <= ema_max
            if not in_value_area:
                continue

            # 3. CHoCH — displacement candle breaking recent structure
            choch = self._choch(df_m15.iloc[i - 10: i + 1], trend, p["choch_body_mult"])
            if not choch:
                continue

            direction, choch_extreme = choch

            # Only trade with H1 trend
            if (direction == "BUY" and trend != "BULLISH") or \
               (direction == "SELL" and trend != "BEARISH"):
                continue

            entry = curr["close"]
            atr = atr_channel  # already computed above

            if direction == "BUY":
                sl = choch_extreme - atr
                risk = entry - sl
                if risk <= 0:
                    continue
                tp = entry + risk * p["rr"]
            else:
                sl = choch_extreme + atr
                risk = sl - entry
                if risk <= 0:
                    continue
                tp = entry - risk * p["rr"]

            lot_size = max(0.01, round((balance * p["risk_pct"]) / (risk * 10), 2))

            future = df_m15.iloc[i + 1: i + 500]
            status, exit_price = self._simulate(future, direction, entry, sl, tp, p["session_end"])

            mult = 1 if direction == "BUY" else -1
            pnl = (exit_price - entry) * mult * lot_size * 10
            balance += pnl

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
                "h1_trend": trend,
                "balance": round(balance, 2),
            })

        return self._build_result(initial_balance, balance, trades)

    # ─────────────────────────────────────────────
    # HELPERS
    # ─────────────────────────────────────────────

    def _h1_trend(self, df: pd.DataFrame, window: int) -> str:
        if len(df) < window + 2:
            return "NEUTRAL"
        recent_highs = df["high"].iloc[-window:].values
        recent_lows  = df["low"].iloc[-window:].values
        hh = all(recent_highs[j] > recent_highs[j - 1] for j in range(1, len(recent_highs)))
        hl = all(recent_lows[j]  > recent_lows[j - 1]  for j in range(1, len(recent_lows)))
        ll = all(recent_lows[j]  < recent_lows[j - 1]  for j in range(1, len(recent_lows)))
        lh = all(recent_highs[j] < recent_highs[j - 1] for j in range(1, len(recent_highs)))
        if hh and hl:
            return "BULLISH"
        if ll and lh:
            return "BEARISH"
        return "NEUTRAL"

    def _choch(self, df: pd.DataFrame, trend: str, body_mult: float):
        """
        Detect Change of Character: displacement candle that breaks recent structure.
        Returns (direction, extreme_price) or None.
        """
        if len(df) < 7:
            return None
        last = df.iloc[-1]
        prev_bars = df.iloc[-6:-1]

        bodies = [abs(r["close"] - r["open"]) for _, r in prev_bars.iterrows()]
        avg_body = np.mean(bodies) if bodies else 0
        curr_body = abs(last["close"] - last["open"])

        if avg_body == 0 or curr_body < avg_body * body_mult:
            return None  # Not a displacement candle

        if trend == "BULLISH":
            recent_low = prev_bars["low"].min()
            # Bullish CHoCH: displacement candle breaks above recent high
            recent_high = prev_bars["high"].max()
            if last["close"] > recent_high and last["close"] > last["open"]:
                return ("BUY", recent_low)
        elif trend == "BEARISH":
            recent_high = prev_bars["high"].max()
            recent_low  = prev_bars["low"].min()
            if last["close"] < recent_low and last["close"] < last["open"]:
                return ("SELL", recent_high)
        return None

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

    def _simulate(self, future, side, entry, sl, tp, session_end_hour):
        for _, c in future.iterrows():
            # Hard session exit
            if c.name.hour >= session_end_hour:
                return "TIME STOP ⏰", c["close"]
            # SL
            if (side == "BUY" and c["low"] <= sl) or \
               (side == "SELL" and c["high"] >= sl):
                return "LOSS ❌", sl
            # TP
            if (side == "BUY" and c["high"] >= tp) or \
               (side == "SELL" and c["low"] <= tp):
                return "WIN ✅", tp
        last = future.iloc[-1]["close"] if not future.empty else entry
        return "TIMEOUT ⏱", last

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
            "strategy": "Aggressor Pulse",
            "risk_level": "high",
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
class HighRiskStrategy(AggressorPulse):
    pass
