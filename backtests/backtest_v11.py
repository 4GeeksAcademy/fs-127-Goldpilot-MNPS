import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz, os, json, time
from twelvedata import TDClient
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# 🔐 GHOST CONFIG (v11.0)
# ==========================================
TWELVEDATA_API_KEY = os.getenv('TWELVEDATA_API_KEY')
VAULT_DEMO_START = 5000.0
VAULT_REAL_START = 200.0
RISK_PCT = 0.01 
MIN_RRR = 3.0   
PARTIAL_RR = 1.5   # Bank 60% early to ensure income
PARTIAL_PCT = 0.6

class SniperV11:
    def __init__(self):
        self.demo_balance = VAULT_DEMO_START
        self.real_balance = VAULT_REAL_START
        self.trades = []
        self.cooldowns = {} # Level cooldown logic

    def run(self):
        print("🏛️ AURUM ARCHITECT: GHOST PROTOCOL v11.0")
        td = TDClient(apikey=TWELVEDATA_API_KEY)
        df_15m = td.time_series(symbol="XAU/USD", interval="15min", outputsize=5000).as_pandas()
        df_15m.index = pd.to_datetime(df_15m.index).tz_localize('UTC')
        
        # Calculate 1H EMA 50 for Mean Reversion Filter
        df_1h = df_15m.resample('1H').last().ffill()
        df_1h['ema50'] = df_1h['close'].ewm(span=50).mean()

        for i in range(50, len(df_15m) - 100):
            curr, prev, ts = df_15m.iloc[i], df_15m.iloc[i-1], df_15m.index[i]
            
            # 1. Kill Zones (Entry only)
            if not (7 <= ts.hour <= 10 or 13 <= ts.hour <= 16): continue
            
            # 2. Institutional Levels
            window = df_15m[df_15m.index < ts].tail(96)
            pdh, pdl = window['high'].max(), window['low'].min()
            
            # 3. Mean Reversion Filter (Is price extended?)
            current_ema = df_1h.loc[df_1h.index <= ts].iloc[-1]['ema50']
            dist_from_ema = (curr['close'] - current_ema) / current_ema

            signal = None
            # Only SELL if price is extended ABOVE the EMA
            if prev['high'] > pdh and curr['close'] < pdh and dist_from_ema > 0.002:
                if self.check_cooldown("PDH", ts): signal = "SELL"
            # Only BUY if price is extended BELOW the EMA
            elif prev['low'] < pdl and curr['close'] > pdl and dist_from_ema < -0.002:
                if self.check_cooldown("PDL", ts): signal = "BUY"

            if signal:
                entry = curr['close']
                # --- ATR-BASED STOP (The Fixed $1.50 is banned) ---
                atr = (df_15m.iloc[i-14:i]['high'] - df_15m.iloc[i-14:i]['low']).mean()
                sl_dist = max(atr * 1.5, 4.0) # Minimum $4.00 stop for Gold
                
                sl_price = entry + sl_dist if signal == "SELL" else entry - sl_dist
                
                # --- VOLATILITY GATE ---
                take_real = True
                if sl_dist > 8.0: take_real = False # Skip if risk > $800 on Demo ($8 on Real)

                tp = entry - (sl_dist * MIN_RRR) if signal == "SELL" else entry + (sl_dist * MIN_RRR)
                partial_p = entry - (sl_dist * PARTIAL_RR) if signal == "SELL" else entry + (sl_dist * PARTIAL_RR)
                be_trigger = entry - sl_dist if signal == "SELL" else entry + sl_dist

                # Simulate
                status, exit_p, partial_hit = self.simulate_v11(df_15m.iloc[i+1:i+200], signal, entry, sl_price, tp, be_trigger, partial_p)
                
                # PnL
                demo_sz = (self.demo_balance * RISK_PCT) / (sl_dist * 100)
                real_sz = 0.01 

                demo_pnl = self.calc_pnl(signal, entry, exit_p, demo_sz, partial_hit, sl_dist)
                real_pnl = self.calc_pnl(signal, entry, exit_p, real_sz, partial_hit, sl_dist) if take_real else 0

                self.demo_balance += demo_pnl
                self.real_balance += real_pnl
                self.trades.append({"time": ts, "signal": signal, "status": status, "demo_pnl": demo_pnl, "real_pnl": real_pnl, "real_active": take_real})

        self.export()

    def check_cooldown(self, level, ts):
        key = f"{level}_{ts.date()}"
        if key in self.cooldowns: return False
        self.cooldowns[key] = True
        return True

    def simulate_v11(self, df, side, entry, sl, tp, be_p, partial_p):
        curr_sl, be_hit, partial_hit = sl, False, False
        for _, c in df.iterrows():
            if not be_hit and ((side == "BUY" and c['high'] >= be_p) or (side == "SELL" and c['low'] <= be_p)):
                curr_sl, be_hit = entry, True
            if not partial_hit and ((side == "BUY" and c['high'] >= partial_p) or (side == "SELL" and c['low'] <= partial_p)):
                partial_hit = True
            if (side == "BUY" and c['high'] >= tp) or (side == "SELL" and c['low'] <= tp):
                return "WIN", tp, True
            if (side == "BUY" and c['low'] <= curr_sl) or (side == "SELL" and c['high'] >= curr_sl):
                return ("PARTIAL_BE" if partial_hit else ("BE" if be_hit else "LOSS")), curr_sl, partial_hit
        return "TIMEOUT", df['close'].iloc[-1], partial_hit

    def calc_pnl(self, side, entry, exit_p, size, partial_hit, sl_dist):
        mult = 1 if side == "BUY" else -1
        if not partial_hit: return (exit_p - entry) * mult * size * 100
        else:
            banked = (sl_dist * PARTIAL_RR) * PARTIAL_PCT * size * 100
            rem = (exit_p - entry) * mult * (1 - PARTIAL_PCT) * size * 100
            return banked + rem

    def export(self):
        output = {"demo_start": VAULT_DEMO_START, "demo_final": self.demo_balance, "real_start": VAULT_REAL_START, "real_final": self.real_balance, "trades": []}
        for t in self.trades:
            output["trades"].append({"time": t['time'].strftime('%Y-%m-%d %H:%M'), "status": t['status'], "demo_pnl": t['demo_pnl'], "real_pnl": t['real_pnl'], "real_active": t['real_active'], "signal": t['signal'], "entry": 0})
        with open('STRATEGY_V11_RESULTS.json', 'w') as f: json.dump(output, f, indent=2)
        print(f"✅ v11.0 Complete. Demo: ${self.demo_balance:.2f} | Real: ${self.real_balance:.2f}")

if __name__ == "__main__":
    SniperV11().run()