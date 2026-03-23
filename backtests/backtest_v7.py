import asyncio
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
import os
import json
import time
from twelvedata import TDClient
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# 🔐 CONFIGURATION
# ==========================================
TWELVEDATA_API_KEY = os.getenv('TWELVEDATA_API_KEY')
VAULT_DEMO_START = 5000.0
VAULT_REAL_START = 100.0
RISK_PCT = 0.01  # 1% Risk
MIN_RRR = 3.0    # 1:3 RR
BE_TRIGGER_RR = 1.0 # Breakeven at 1:1

class SniperV7:
    def __init__(self):
        self.demo_balance = VAULT_DEMO_START
        self.real_balance = VAULT_REAL_START
        self.trades = []

    def calculate_lot_size(self, balance, sl_dist, is_real=False):
        risk_dollars = balance * RISK_PCT
        size = risk_dollars / (sl_dist * 100)
        return max(0.01, round(size, 2))

    def get_atr(self, df_4h, current_time):
        relevant = df_4h[df_4h.index <= current_time].tail(14)
        if len(relevant) < 14: return 5.0
        return (relevant['high'] - relevant['low']).mean()

    def get_daily_levels(self, df_15m, current_time):
        prev_day = current_time - timedelta(days=1)
        prev_data = df_15m[df_15m.index.date == prev_day.date()]
        if prev_data.empty: return None
        
        tokyo_data = df_15m[(df_15m.index.date == current_time.date()) & (df_15m.index.hour < 7)]
        return {
            'PDH': prev_data['high'].max(),
            'PDL': prev_data['low'].min(),
            'TOKYO_H': tokyo_data['high'].max() if not tokyo_data.empty else prev_data['high'].max(),
            'TOKYO_L': tokyo_data['low'].min() if not tokyo_data.empty else prev_data['low'].min()
        }

    def simulate_trade(self, future_candles, side, entry, sl, tp, be_price):
        current_sl = sl
        be_hit = False
        for _, c in future_candles.iterrows():
            if not be_hit:
                if (side == "BUY" and c['high'] >= be_price) or (side == "SELL" and c['low'] <= be_price):
                    current_sl = entry
                    be_hit = True
            if (side == "BUY" and c['high'] >= tp) or (side == "SELL" and c['low'] <= tp):
                return "WIN", tp
            if (side == "BUY" and c['low'] <= current_sl) or (side == "SELL" and c['high'] >= current_sl):
                return "BE" if be_hit else "LOSS", current_sl
        return "OPEN", future_candles['close'].iloc[-1]

    def run(self):
        print("🏛️ AURUM ARCHITECT: INITIALIZING TWIN-VAULT v7.0")
        if not TWELVEDATA_API_KEY:
            print("❌ ERROR: TWELVEDATA_API_KEY missing from .env")
            return

        td = TDClient(apikey=TWELVEDATA_API_KEY)
        # Fetch Data
        df_15m = td.time_series(symbol="XAU/USD", interval="15min", outputsize=5000).as_pandas()
        time.sleep(10) # Protect API limits
        df_4h = td.time_series(symbol="XAU/USD", interval="4h", outputsize=500).as_pandas()

        df_15m.index = pd.to_datetime(df_15m.index).tz_localize('UTC')
        df_4h.index = pd.to_datetime(df_4h.index).tz_localize('UTC')

        for i in range(50, len(df_15m) - 50):
            curr, prev, ts = df_15m.iloc[i], df_15m.iloc[i-1], df_15m.index[i]
            if not (7 <= ts.hour <= 16): continue # London/NY Open only
            
            levels = self.get_daily_levels(df_15m, ts)
            if not levels: continue

            signal = None
            if prev['high'] > levels['PDH'] and curr['close'] < levels['PDH']: signal = "SELL"
            elif prev['low'] < levels['PDL'] and curr['close'] > levels['PDL']: signal = "BUY"

            if signal:
                atr = self.get_atr(df_4h, ts)
                sl_dist = atr * 1.5
                entry = curr['close']
                sl = entry - sl_dist if signal == "BUY" else entry + sl_dist
                tp = entry + (sl_dist * MIN_RRR) if signal == "BUY" else entry - (sl_dist * MIN_RRR)
                be_p = entry + sl_dist if signal == "BUY" else entry - sl_dist

                demo_sz = self.calculate_lot_size(self.demo_balance, sl_dist)
                real_sz = self.calculate_lot_size(self.real_balance, sl_dist, True)

                status, exit_p = self.simulate_trade(df_15m.iloc[i+1:i+100], signal, entry, sl, tp, be_p)
                mult = 1 if signal == "BUY" else -1
                demo_pnl = (exit_p - entry) * mult * demo_sz * 100
                real_pnl = (exit_p - entry) * mult * real_sz * 100
                
                self.demo_balance += demo_pnl
                self.real_balance += real_pnl

                self.trades.append({
                    "time": ts.strftime('%Y-%m-%d %H:%M'), "signal": signal, "entry": entry,
                    "status": status, "demo_pnl": demo_pnl, "real_pnl": real_pnl,
                    "sl": sl, "tp": tp, "demo_size": demo_sz, "real_size": real_sz
                })

        # --- SAVE RESULTS TO JSON ---
        output = {
            "demo_start_balance": VAULT_DEMO_START,
            "demo_final_balance": self.demo_balance,
            "demo_roi": ((self.demo_balance - VAULT_DEMO_START) / VAULT_DEMO_START) * 100,
            "real_start_balance": VAULT_REAL_START,
            "real_final_balance": self.real_balance,
            "real_roi": ((self.real_balance - VAULT_REAL_START) / VAULT_REAL_START) * 100,
            "trades": self.trades
        }
        with open('STRATEGY_V7_RESULTS.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"✅ Backtest Complete. ROI: {output['real_roi']:.2f}%")
        print(f"💾 Results saved to STRATEGY_V7_RESULTS.json")

if __name__ == "__main__":
    SniperV7().run()