"""
Ghost Protocol v11 — Low Risk Strategy
=======================================
Logic: PDH/PDL sweep on M15 + EMA50 (H1) mean reversion filter + ATR sizing
Kill Zones: London 07:00-10:00 UTC, NY 13:00-16:00 UTC
Risk: 1% per trade, 1:3 RR, partial profit at 1.5x, breakeven move
"""
import pandas as pd
import numpy as np


DEFAULT_PARAMS = {
    "pdh_window": 96,
    "ema_period": 50,
    "ema_extension_pct": 0.002,
    "atr_period": 14,
    "atr_sl_mult": 1.5,
    "atr_sl_min": 8.0,    # minimum SL distance in $ (updated for gold ~4500+)
    "atr_sl_max": 40.0,   # maximum SL distance in $ (updated for gold ~4500+)
    "rr": 3.0,
    "partial_rr": 1.5,
    "partial_pct": 0.60,
    "risk_pct": 0.01,
    "kill_zones": [(7, 10), (13, 16)],
}


class GhostProtocol:
    def __init__(self, params: dict = None):
        self.p = {**DEFAULT_PARAMS, **(params or {})}

    def run(self, df_m15: pd.DataFrame, df_h1: pd.DataFrame,
            initial_balance: float = 100_000.0) -> dict:
        balance = initial_balance
        trades = []
        cooldowns = set()

        df_h1 = df_h1.copy()
        df_h1["ema"] = df_h1["close"].ewm(span=self.p["ema_period"], adjust=False).mean()
        p = self.p

        for i in range(p["pdh_window"] + p["atr_period"] + 1, len(df_m15) - 1):
            ts = df_m15.index[i]
            if not self._in_kill_zone(ts):
                continue

            curr = df_m15.iloc[i]
            prev = df_m15.iloc[i - 1]

            # Window excludes prev (i-1) so that prev["high"] > pdh is possible
            window = df_m15.iloc[i - p["pdh_window"]: i - 1]
            pdh = window["high"].max()
            pdl = window["low"].min()

            h1_slice = df_h1[df_h1.index <= ts]
            if h1_slice.empty:
                continue
            ema_val = h1_slice.iloc[-1]["ema"]
            dist_from_ema = (curr["close"] - ema_val) / ema_val

            atr = self._atr(df_m15.iloc[i - p["atr_period"]: i])
            signal = None
            level_key = None

            if prev["high"] > pdh and curr["close"] < pdh and dist_from_ema > p["ema_extension_pct"]:
                level_key = f"PDH_{ts.date()}"
                if level_key not in cooldowns:
                    signal = "SELL"
            elif prev["low"] < pdl and curr["close"] > pdl and dist_from_ema < -p["ema_extension_pct"]:
                level_key = f"PDL_{ts.date()}"
                if level_key not in cooldowns:
                    signal = "BUY"

            if not signal:
                continue

            sl_dist = max(atr * p["atr_sl_mult"], p["atr_sl_min"])
            if sl_dist > p["atr_sl_max"]:
                continue

            entry = curr["close"]
            lot_size = max(0.01, round((balance * p["risk_pct"]) / (sl_dist * 100), 2))

            if signal == "BUY":
                sl = entry - sl_dist
                tp = entry + sl_dist * p["rr"]
                partial_p = entry + sl_dist * p["partial_rr"]
            else:
                sl = entry + sl_dist
                tp = entry - sl_dist * p["rr"]
                partial_p = entry - sl_dist * p["partial_rr"]

            future = df_m15.iloc[i + 1: i + 300]
            status, exit_price, partial_hit, be_hit = self._simulate(
                future, signal, entry, sl, tp, partial_p)

            pnl = self._calc_pnl(signal, entry, exit_price, lot_size, partial_hit, sl_dist)
            balance += pnl
            cooldowns.add(level_key)

            trades.append({
                "date": ts.strftime("%Y-%m-%d %H:%M"),
                "type": signal,
                "entry_price": round(entry, 2),
                "exit_price": round(exit_price, 2),
                "lot_size": lot_size,
                "sl": round(sl, 2),
                "tp": round(tp, 2),
                "profit": round(pnl, 2),
                "result": status,
                "balance": round(balance, 2),
            })

        return self._build_result(initial_balance, balance, trades)

    def _in_kill_zone(self, ts) -> bool:
        h = ts.hour
        for start, end in self.p["kill_zones"]:
            if start <= h <= end:
                return True
        return False

    def _atr(self, df: pd.DataFrame) -> float:
        if len(df) < 2:
            return self.p["atr_sl_min"]
        highs  = df["high"].values
        lows   = df["low"].values
        closes = df["close"].values
        trs = [max(highs[j] - lows[j],
                   abs(highs[j] - closes[j - 1]),
                   abs(lows[j]  - closes[j - 1]))
               for j in range(1, len(df))]
        return float(np.mean(trs)) if trs else self.p["atr_sl_min"]

    def _simulate(self, future, side, entry, sl, tp, partial_p):
        be_sl = sl
        be_hit = False
        partial_hit = False
        for _, c in future.iterrows():
            if not be_hit:
                if (side == "BUY" and c["high"] >= partial_p) or \
                   (side == "SELL" and c["low"] <= partial_p):
                    be_sl = entry
                    be_hit = True
                    partial_hit = True
            if (side == "BUY" and c["low"] <= be_sl) or \
               (side == "SELL" and c["high"] >= be_sl):
                label = "PARTIAL ✅" if partial_hit else ("BE ➖" if be_hit else "LOSS ❌")
                return label, be_sl, partial_hit, be_hit
            if (side == "BUY" and c["high"] >= tp) or \
               (side == "SELL" and c["low"] <= tp):
                return "WIN ✅", tp, partial_hit, be_hit
        last = future.iloc[-1]["close"] if not future.empty else entry
        return "TIMEOUT ⏱", last, partial_hit, be_hit

    def _calc_pnl(self, side, entry, exit_p, lot_size, partial_hit, sl_dist):
        mult = 1 if side == "BUY" else -1
        p = self.p
        if not partial_hit:
            return (exit_p - entry) * mult * lot_size * 100
        banked = sl_dist * p["partial_rr"] * p["partial_pct"] * lot_size * 100
        rem    = (exit_p - entry) * mult * (1 - p["partial_pct"]) * lot_size * 100
        return banked + rem

    def _build_result(self, initial_balance, final_balance, trades):
        wins = [t for t in trades if "WIN" in t["result"] or "PARTIAL" in t["result"]]
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
            "strategy": "Ghost Protocol v11",
            "risk_level": "low",
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
class LowRiskStrategy(GhostProtocol):
    pass
