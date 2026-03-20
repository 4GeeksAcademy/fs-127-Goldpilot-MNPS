#!/usr/bin/env python3
"""
60-Day Master Backtest - All Strategies Comparison
Using Twelve Data API for complete historical data

Strategies tested:
1. Strategy #2: Price Action Initial (baseline)
2. Strategy #3: Price Action Optimized (filtered)
3. Strategy #4: Aurum Liquidity Sniper (breakthrough)
4. Strategy v5.1: Balanced Production (enhanced)

Test Period: November 1 - December 27, 2025 (57 days)
"""

import asyncio
from datetime import datetime, timedelta
import pytz
import os
from dotenv import load_dotenv
from twelvedata import TDClient
import time

load_dotenv()

TWELVEDATA_API_KEY = os.getenv('TWELVEDATA_API_KEY')
INITIAL_BALANCE = 10000
LOT_SIZE_FIXED = 0.01  # For strategies #2 and #3
RISK_PER_TRADE = 0.01  # For strategies #4 and v5.1
RISK_REWARD_RATIO = 3.0
ATR_MULTIPLIER = 1.5
ATR_MAX_VOLATILITY = 40.0
MAX_TRADES_PER_DAY = 4
BREAKEVEN_TRIGGER = 1.5

class MasterBacktest:
    def __init__(self):
        self.all_results = {}

    def fetch_data_twelvedata(self):
        """Fetch 60 days of Gold data from Twelve Data"""
        print("="*80)
        print("📊 FETCHING 60-DAY HISTORICAL DATA")
        print("="*80)
        print(f"\n🔑 Using Twelve Data API")
        print(f"📅 Target period: Nov 1 - Dec 27, 2025 (57 days)")

        if not TWELVEDATA_API_KEY:
            print("\n❌ ERROR: TWELVEDATA_API_KEY not found in .env")
            return None

        td = TDClient(apikey=TWELVEDATA_API_KEY)

        try:
            # Fetch 15m candles
            print("\n📈 Fetching 15-minute candles...")
            ts_15m = td.time_series(
                symbol="XAU/USD",
                interval="15min",
                outputsize=5000,
                timezone="UTC"
            )
            df_15m = ts_15m.as_pandas()
            if df_15m is None or df_15m.empty:
                print("❌ No 15m data received")
                return None

            candles_15m = self.convert_df_to_candles(df_15m)
            print(f"   ✅ Received {len(candles_15m)} candles")
            time.sleep(8)  # Rate limit

            # Fetch 1h candles
            print("📈 Fetching 1-hour candles...")
            ts_1h = td.time_series(
                symbol="XAU/USD",
                interval="1h",
                outputsize=2000,
                timezone="UTC"
            )
            df_1h = ts_1h.as_pandas()
            candles_1h = self.convert_df_to_candles(df_1h)
            print(f"   ✅ Received {len(candles_1h)} candles")
            time.sleep(8)

            # Fetch 4h candles
            print("📈 Fetching 4-hour candles...")
            ts_4h = td.time_series(
                symbol="XAU/USD",
                interval="4h",
                outputsize=500,
                timezone="UTC"
            )
            df_4h = ts_4h.as_pandas()
            candles_4h = self.convert_df_to_candles(df_4h)
            print(f"   ✅ Received {len(candles_4h)} candles")

            # Filter to Nov 1 - Dec 27, 2025
            start_date = datetime(2025, 11, 1, tzinfo=pytz.utc)
            end_date = datetime(2025, 12, 27, 23, 59, 59, tzinfo=pytz.utc)

            candles_15m_filtered = [c for c in candles_15m if start_date <= c['time'] <= end_date]
            candles_1h_filtered = [c for c in candles_1h if start_date <= c['time'] <= end_date]
            candles_4h_filtered = [c for c in candles_4h if start_date <= c['time'] <= end_date]

            print(f"\n✅ DATA SUMMARY (Nov 1 - Dec 27):")
            print(f"   15m: {len(candles_15m_filtered)} candles ({candles_15m_filtered[0]['time'].date()} to {candles_15m_filtered[-1]['time'].date()})")
            print(f"   1h:  {len(candles_1h_filtered)} candles")
            print(f"   4h:  {len(candles_4h_filtered)} candles")
            print("="*80 + "\n")

            return {
                '15m': candles_15m_filtered,
                '1h': candles_1h_filtered,
                '4h': candles_4h_filtered,
                '5m': candles_15m_filtered  # Use 15m as proxy for 5m
            }

        except Exception as e:
            print(f"❌ Error fetching data: {e}")
            return None

    def convert_df_to_candles(self, df):
        """Convert Twelve Data pandas dataframe to candle format"""
        candles = []
        df_sorted = df.sort_index()

        for index, row in df_sorted.iterrows():
            # Parse timestamp
            if isinstance(index, str):
                timestamp = datetime.strptime(index, '%Y-%m-%d %H:%M:%S')
                timestamp = pytz.utc.localize(timestamp)
            else:
                timestamp = index.to_pydatetime()
                if timestamp.tzinfo is None:
                    timestamp = pytz.utc.localize(timestamp)

            candle = {
                'time': timestamp,
                'open': float(row['open']),
                'high': float(row['high']),
                'low': float(row['low']),
                'close': float(row['close'])
            }
            candles.append(candle)

        return candles

    # ==================== STRATEGY #2: PRICE ACTION INITIAL ====================
    def run_strategy_2(self, data):
        """Run Strategy #2: Price Action Initial (baseline)"""
        print("\n" + "="*80)
        print("📊 STRATEGY #2: PRICE ACTION INITIAL")
        print("="*80)
        print("Configuration: Pin bars, Engulfing, S/R levels, 2:1 RR, 0.01 lots")

        trades = []
        balance = INITIAL_BALANCE

        # Simple price action patterns at support/resistance
        candles_15m = data['15m']
        candles_4h = data['4h']

        for i in range(30, len(candles_15m)):
            current = candles_15m[i]

            # Find S/R levels
            sr_levels = self.find_support_resistance(candles_4h[:i])

            # Detect price action
            signal = self.detect_price_action_signal_basic(candles_15m[i-2:i+1], sr_levels, current['close'])

            if signal and len(trades) < 100:  # Cap at 100 trades
                trade = self.execute_fixed_trade(signal, current['time'], LOT_SIZE_FIXED)
                trades.append(trade)

                # Simulate outcome
                self.simulate_fixed_outcome(trade, candles_15m[i+1:])
                balance += trade['pnl']

        results = self.calculate_results("Strategy #2: Price Action Initial", trades, balance)
        return results

    def find_support_resistance(self, candles_4h):
        """Find swing highs/lows for S/R"""
        if len(candles_4h) < 20:
            return []

        levels = []
        recent = candles_4h[-20:]

        for i in range(3, len(recent) - 3):
            current = recent[i]

            # Swing high
            if (current['high'] > recent[i-1]['high'] and
                current['high'] > recent[i+1]['high'] and
                current['high'] > recent[i-2]['high'] and
                current['high'] > recent[i+2]['high']):
                levels.append({"price": current['high'], "type": "RESISTANCE"})

            # Swing low
            if (current['low'] < recent[i-1]['low'] and
                current['low'] < recent[i+1]['low'] and
                current['low'] < recent[i-2]['low'] and
                current['low'] < recent[i+2]['low']):
                levels.append({"price": current['low'], "type": "SUPPORT"})

        return levels

    def detect_price_action_signal_basic(self, candles, sr_levels, current_price):
        """Detect basic price action patterns"""
        if len(candles) < 3:
            return None

        prev = candles[-2]
        current = candles[-1]

        # Check if near S/R
        near_level = False
        for level in sr_levels:
            if abs(current_price - level['price']) <= 5.0:
                near_level = True
                break

        if not near_level:
            return None

        # Bullish pin bar
        c_range = current['high'] - current['low']
        c_lower_wick = min(current['open'], current['close']) - current['low']
        c_body = abs(current['close'] - current['open'])

        if c_lower_wick > c_range * 0.6 and c_body < c_range * 0.3:
            swing_low = min([c['low'] for c in candles])
            sl = swing_low - 3.0
            risk = current_price - sl
            tp = current_price + (risk * 2.0)

            if risk > 0:
                return {"decision": "BUY", "price": current_price, "sl": sl, "tp": tp}

        # Bearish pin bar
        c_upper_wick = current['high'] - max(current['open'], current['close'])

        if c_upper_wick > c_range * 0.6 and c_body < c_range * 0.3:
            swing_high = max([c['high'] for c in candles])
            sl = swing_high + 3.0
            risk = sl - current_price
            tp = current_price - (risk * 2.0)

            if risk > 0:
                return {"decision": "SELL", "price": current_price, "sl": sl, "tp": tp}

        return None

    def execute_fixed_trade(self, signal, timestamp, lot_size):
        """Execute trade with fixed lot size"""
        return {
            "timestamp": timestamp,
            "decision": signal['decision'],
            "entry_price": signal['price'],
            "sl": signal['sl'],
            "tp": signal['tp'],
            "lot_size": lot_size,
            "outcome": None,
            "pnl": 0
        }

    def simulate_fixed_outcome(self, trade, future_candles):
        """Simulate outcome for fixed lot size trades"""
        for candle in future_candles[:200]:  # Max 200 candles (~2 days)
            if trade['decision'] == 'BUY':
                if candle['low'] <= trade['sl']:
                    trade['outcome'] = 'LOSS'
                    pips = trade['sl'] - trade['entry_price']
                    trade['pnl'] = pips * trade['lot_size'] * 100
                    return
                if candle['high'] >= trade['tp']:
                    trade['outcome'] = 'WIN'
                    pips = trade['tp'] - trade['entry_price']
                    trade['pnl'] = pips * trade['lot_size'] * 100
                    return
            else:  # SELL
                if candle['high'] >= trade['sl']:
                    trade['outcome'] = 'LOSS'
                    pips = trade['entry_price'] - trade['sl']
                    trade['pnl'] = -abs(pips * trade['lot_size'] * 100)
                    return
                if candle['low'] <= trade['tp']:
                    trade['outcome'] = 'WIN'
                    pips = trade['entry_price'] - trade['tp']
                    trade['pnl'] = pips * trade['lot_size'] * 100
                    return

        trade['outcome'] = 'OPEN'

    # ==================== STRATEGY #3: PRICE ACTION OPTIMIZED ====================
    def run_strategy_3(self, data):
        """Run Strategy #3: Price Action Optimized (with filters)"""
        print("\n" + "="*80)
        print("📊 STRATEGY #3: PRICE ACTION OPTIMIZED")
        print("="*80)
        print("Configuration: ATR filter, Trend alignment, Stricter S/R, 80% confidence")

        trades = []
        balance = INITIAL_BALANCE

        candles_15m = data['15m']
        candles_4h = data['4h']

        for i in range(50, len(candles_15m)):
            current = candles_15m[i]

            # Calculate ATR
            atr = self.calculate_atr(candles_4h[:i//16+1])
            if atr is None or atr < 8.0 or atr > 50.0:
                continue

            # Check trend
            trend = self.check_trend_alignment(candles_4h[:i//16+1])

            # Find S/R levels (stricter)
            sr_levels = self.find_support_resistance(candles_4h[:i//16+1])

            # Detect pattern
            signal = self.detect_price_action_optimized(candles_15m[i-2:i+1], sr_levels, current['close'], trend)

            if signal and len(trades) < 100:
                trade = self.execute_fixed_trade(signal, current['time'], LOT_SIZE_FIXED)
                trades.append(trade)

                self.simulate_fixed_outcome(trade, candles_15m[i+1:])
                balance += trade['pnl']

        results = self.calculate_results("Strategy #3: Price Action Optimized", trades, balance)
        return results

    def calculate_atr(self, candles_4h, period=14):
        """Calculate Average True Range"""
        if len(candles_4h) < period + 1:
            return None

        recent = candles_4h[-(period + 1):]
        tr_list = []

        for i in range(1, len(recent)):
            high = recent[i]['high']
            low = recent[i]['low']
            prev_close = recent[i-1]['close']

            tr = max(
                high - low,
                abs(high - prev_close),
                abs(low - prev_close)
            )
            tr_list.append(tr)

        return sum(tr_list) / len(tr_list)

    def check_trend_alignment(self, candles_4h):
        """Check 4H trend using EMAs"""
        if len(candles_4h) < 50:
            return "NEUTRAL"

        closes = [c['close'] for c in candles_4h]
        ema_20 = self.calculate_ema(closes, 20)
        ema_50 = self.calculate_ema(closes, 50)

        if ema_20 and ema_50:
            if ema_20 > ema_50 * 1.002:
                return "BULLISH"
            elif ema_20 < ema_50 * 0.998:
                return "BEARISH"

        return "NEUTRAL"

    def calculate_ema(self, data, period):
        """Calculate EMA"""
        if len(data) < period:
            return None

        multiplier = 2 / (period + 1)
        ema = sum(data[:period]) / period

        for price in data[period:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))

        return ema

    def detect_price_action_optimized(self, candles, sr_levels, current_price, trend):
        """Detect price action with filters"""
        if len(candles) < 3:
            return None

        current = candles[-1]

        # Must be near S/R
        near_level = False
        level_type = None
        for level in sr_levels:
            if abs(current_price - level['price']) <= 5.0:
                near_level = True
                level_type = level['type']
                break

        if not near_level:
            return None

        # Pattern detection
        c_range = current['high'] - current['low']
        c_lower_wick = min(current['open'], current['close']) - current['low']
        c_upper_wick = current['high'] - max(current['open'], current['close'])
        c_body = abs(current['close'] - current['open'])

        # Bullish pin + trend alignment
        if c_lower_wick > c_range * 0.6 and c_body < c_range * 0.3 and trend != "BEARISH":
            swing_low = min([c['low'] for c in candles])
            sl = swing_low - 3.0
            risk = current_price - sl
            tp = current_price + (risk * 2.0)

            if risk > 0:
                return {"decision": "BUY", "price": current_price, "sl": sl, "tp": tp}

        # Bearish pin + trend alignment
        if c_upper_wick > c_range * 0.6 and c_body < c_range * 0.3 and trend != "BULLISH":
            swing_high = max([c['high'] for c in candles])
            sl = swing_high + 3.0
            risk = sl - current_price
            tp = current_price - (risk * 2.0)

            if risk > 0:
                return {"decision": "SELL", "price": current_price, "sl": sl, "tp": tp}

        return None

    # ==================== STRATEGY #4: AURUM LIQUIDITY SNIPER ====================
    def run_strategy_4(self, data):
        """Run Strategy #4: Aurum Liquidity Sniper (proven profitable)"""
        print("\n" + "="*80)
        print("🎯 STRATEGY #4: AURUM LIQUIDITY SNIPER")
        print("="*80)
        print("Configuration: PDH/PDL sweeps, 1H structure, 1:3 RR, ATR stops, Breakeven @ 1:1")

        trades = []
        balance = INITIAL_BALANCE
        trades_today = 0
        current_date = None

        candles_15m = data['15m']
        candles_1h = data['1h']
        candles_4h = data['4h']

        for i in range(100, len(candles_15m)):
            timestamp = candles_15m[i]['time']

            # Reset daily counter
            if current_date != timestamp.date():
                current_date = timestamp.date()
                trades_today = 0

            if trades_today >= MAX_TRADES_PER_DAY:
                continue

            # Check trading window
            in_window, session = self.is_trading_window(timestamp)
            if not in_window:
                continue

            # Calculate levels
            levels = self.calculate_daily_levels_v4(candles_15m, i)
            if not levels:
                continue

            # Market structure
            structure = self.get_market_structure(candles_1h[:i//4+1])

            # ATR
            atr = self.calculate_atr(candles_4h[:i//16+1])
            if not atr:
                continue

            # Detect sweep
            sweep = self.detect_liquidity_sweep(candles_15m, i, levels, structure)
            if not sweep:
                continue

            direction, level_name, rejection_candle = sweep

            # Build signal
            signal = self.build_liquidity_signal(direction, candles_15m[i], rejection_candle, atr, balance)
            if not signal:
                continue

            # Execute
            trade = {
                "timestamp": timestamp,
                "decision": signal['decision'],
                "entry_price": signal['price'],
                "sl": signal['sl'],
                "tp": signal['tp'],
                "lot_size": signal['lot_size'],
                "outcome": None,
                "pnl": 0,
                "breakeven_moved": False
            }
            trades.append(trade)
            trades_today += 1

            # Simulate
            self.simulate_liquidity_outcome(trade, candles_15m[i+1:])
            balance += trade['pnl']

        results = self.calculate_results("Strategy #4: Aurum Liquidity Sniper", trades, balance)
        return results

    def is_trading_window(self, timestamp):
        """Check London/NY sessions"""
        hour = timestamp.hour

        if 7 <= hour < 16:
            return True, "LONDON"
        if 13 <= hour < 21:
            return True, "NY"

        return False, "CLOSED"

    def calculate_daily_levels_v4(self, candles_15m, current_index):
        """Calculate PDH/PDL and Tokyo levels"""
        if current_index < 100:
            return None

        current_time = candles_15m[current_index]['time']
        current_date = current_time.date()

        # Previous day
        prev_day_start = datetime.combine(current_date - timedelta(days=1), datetime.min.time()).replace(tzinfo=pytz.utc)
        prev_day_end = datetime.combine(current_date, datetime.min.time()).replace(tzinfo=pytz.utc)

        prev_day_candles = [
            c for c in candles_15m[:current_index]
            if prev_day_start <= c['time'] < prev_day_end
        ]

        if not prev_day_candles:
            return None

        pdh = max(c['high'] for c in prev_day_candles)
        pdl = min(c['low'] for c in prev_day_candles)

        # Tokyo session
        tokyo_start = datetime.combine(current_date - timedelta(days=1), datetime.min.time()).replace(hour=23, tzinfo=pytz.utc)
        tokyo_end = datetime.combine(current_date, datetime.min.time()).replace(hour=8, tzinfo=pytz.utc)

        tokyo_candles = [
            c for c in candles_15m[:current_index]
            if tokyo_start <= c['time'] < tokyo_end
        ]

        if tokyo_candles:
            tokyo_high = max(c['high'] for c in tokyo_candles)
            tokyo_low = min(c['low'] for c in tokyo_candles)
        else:
            tokyo_high = pdh
            tokyo_low = pdl

        return {
            'PDH': pdh,
            'PDL': pdl,
            'TOKYO_HIGH': tokyo_high,
            'TOKYO_LOW': tokyo_low
        }

    def get_market_structure(self, candles_1h):
        """Get 1H market structure"""
        if len(candles_1h) < 15:
            return "NEUTRAL"

        recent = candles_1h[-15:]
        highs = [c['high'] for c in recent]
        lows = [c['low'] for c in recent]

        recent_high = max(highs[-5:])
        previous_high = max(highs[-15:-5])
        recent_low = min(lows[-5:])
        previous_low = min(lows[-15:-5])

        if recent_high > previous_high and recent_low >= previous_low:
            return "BULLISH"
        elif recent_low < previous_low and recent_high <= previous_high:
            return "BEARISH"

        return "NEUTRAL"

    def detect_liquidity_sweep(self, candles_15m, current_index, levels, structure):
        """Detect liquidity sweep at key levels"""
        if current_index < 3:
            return None

        current = candles_15m[current_index]
        prev = candles_15m[current_index - 1]
        prev2 = candles_15m[current_index - 2]

        # Bullish sweep
        if structure in ["BULLISH", "NEUTRAL"]:
            for level_name in ['PDL', 'TOKYO_LOW']:
                level = levels[level_name]

                swept = (prev['low'] < level or prev2['low'] < level)
                reversed = current['close'] > level

                if swept and reversed:
                    return ('BUY', level_name, current)

        # Bearish sweep
        if structure in ["BEARISH", "NEUTRAL"]:
            for level_name in ['PDH', 'TOKYO_HIGH']:
                level = levels[level_name]

                swept = (prev['high'] > level or prev2['high'] > level)
                reversed = current['close'] < level

                if swept and reversed:
                    return ('SELL', level_name, current)

        return None

    def build_liquidity_signal(self, direction, current_candle, rejection_candle, atr, balance):
        """Build liquidity sweep signal"""
        current_price = current_candle['close']
        risk_amount = balance * RISK_PER_TRADE

        if direction == 'BUY':
            atr_stop = current_price - (atr * ATR_MULTIPLIER)
            candle_stop = rejection_candle['low'] - 2.0
            sl = max(atr_stop, candle_stop)

            risk = current_price - sl
            tp = current_price + (risk * RISK_REWARD_RATIO)

            lot_size = risk_amount / (risk * 10)
            lot_size = max(0.01, round(lot_size, 2))

            if risk <= 0:
                return None

            return {
                "decision": "BUY",
                "price": current_price,
                "sl": round(sl, 2),
                "tp": round(tp, 2),
                "lot_size": lot_size
            }

        else:  # SELL
            atr_stop = current_price + (atr * ATR_MULTIPLIER)
            candle_stop = rejection_candle['high'] + 2.0
            sl = min(atr_stop, candle_stop)

            risk = sl - current_price
            tp = current_price - (risk * RISK_REWARD_RATIO)

            lot_size = risk_amount / (risk * 10)
            lot_size = max(0.01, round(lot_size, 2))

            if risk <= 0:
                return None

            return {
                "decision": "SELL",
                "price": current_price,
                "sl": round(sl, 2),
                "tp": round(tp, 2),
                "lot_size": lot_size
            }

    def simulate_liquidity_outcome(self, trade, future_candles):
        """Simulate with breakeven protection at 1:1"""
        entry = trade['entry_price']
        sl = trade['sl']
        tp = trade['tp']
        lot_size = trade['lot_size']

        for candle in future_candles[:200]:
            if trade['decision'] == 'BUY':
                # Breakeven at 1:1
                if not trade['breakeven_moved']:
                    risk = entry - sl
                    if candle['high'] >= entry + risk:
                        sl = entry
                        trade['breakeven_moved'] = True

                # Check SL
                if candle['low'] <= sl:
                    trade['outcome'] = 'BREAKEVEN' if trade['breakeven_moved'] else 'LOSS'
                    price_diff = (sl - entry) if not trade['breakeven_moved'] else 0
                    trade['pnl'] = price_diff * lot_size * 10
                    return

                # Check TP
                if candle['high'] >= tp:
                    trade['outcome'] = 'WIN'
                    price_diff = tp - entry
                    trade['pnl'] = price_diff * lot_size * 10
                    return

            else:  # SELL
                # Breakeven at 1:1
                if not trade['breakeven_moved']:
                    risk = sl - entry
                    if candle['low'] <= entry - risk:
                        sl = entry
                        trade['breakeven_moved'] = True

                # Check SL
                if candle['high'] >= sl:
                    trade['outcome'] = 'BREAKEVEN' if trade['breakeven_moved'] else 'LOSS'
                    price_diff = (entry - sl) if not trade['breakeven_moved'] else 0
                    trade['pnl'] = price_diff * lot_size * 10 * -1
                    return

                # Check TP
                if candle['low'] <= tp:
                    trade['outcome'] = 'WIN'
                    price_diff = entry - tp
                    trade['pnl'] = price_diff * lot_size * 10
                    return

        trade['outcome'] = 'OPEN'

    # ==================== STRATEGY V5.1: BALANCED PRODUCTION ====================
    def run_strategy_v5_1(self, data):
        """Run Strategy v5.1: Balanced Production Model"""
        print("\n" + "="*80)
        print("🚀 STRATEGY V5.1: BALANCED PRODUCTION")
        print("="*80)
        print("Configuration: Expanded windows, CHoCH bonus, ATR cap, BE @ 1:1.5")

        trades = []
        balance = INITIAL_BALANCE
        trades_today = 0
        current_date = None

        candles_15m = data['15m']
        candles_5m = data['5m']  # Using 15m as proxy
        candles_1h = data['1h']
        candles_4h = data['4h']

        for i in range(100, len(candles_15m)):
            timestamp = candles_15m[i]['time']

            # Reset daily counter
            if current_date != timestamp.date():
                current_date = timestamp.date()
                trades_today = 0

            if trades_today >= MAX_TRADES_PER_DAY:
                continue

            # Check priority window (expanded)
            in_window, session = self.is_priority_window(timestamp)
            if not in_window:
                continue

            # Calculate levels
            levels = self.calculate_daily_levels_v4(candles_15m, i)
            if not levels:
                continue

            # ATR
            atr = self.calculate_atr(candles_4h[:i//16+1])
            if not atr or atr > ATR_MAX_VOLATILITY:
                continue

            # Market structure
            structure = self.get_market_structure(candles_1h[:i//4+1])

            # Detect sweep with CHoCH bonus
            sweep = self.detect_sweep_with_choch(candles_15m, candles_5m, i, levels, structure)
            if not sweep:
                continue

            direction, level_name, rejection_candle, confidence, has_choch = sweep

            # Build signal (same as v4 but with stricter SL)
            signal = self.build_v5_signal(direction, candles_15m[i], rejection_candle, atr, balance)
            if not signal:
                continue

            # Execute
            trade = {
                "timestamp": timestamp,
                "decision": signal['decision'],
                "entry_price": signal['price'],
                "sl": signal['sl'],
                "tp": signal['tp'],
                "lot_size": signal['lot_size'],
                "outcome": None,
                "pnl": 0,
                "breakeven_moved": False,
                "has_choch": has_choch
            }
            trades.append(trade)
            trades_today += 1

            # Simulate with 1:1.5 breakeven
            self.simulate_v5_outcome(trade, candles_15m[i+1:])
            balance += trade['pnl']

        results = self.calculate_results("Strategy v5.1: Balanced Production", trades, balance)
        return results

    def is_priority_window(self, timestamp):
        """Expanded windows for v5.1"""
        hour = timestamp.hour

        # London: 07:00-10:00
        if 7 <= hour < 10:
            return True, "LONDON"

        # NY: 13:00-16:00
        if 13 <= hour < 16:
            return True, "NY_PRIME" if hour < 15 else "NY"

        return False, "OUTSIDE"

    def detect_sweep_with_choch(self, candles_15m, candles_5m, current_index, levels, structure):
        """Detect sweep with optional CHoCH bonus"""
        if current_index < 3:
            return None

        current = candles_15m[current_index]
        prev = candles_15m[current_index - 1]
        prev2 = candles_15m[current_index - 2]

        # Bullish sweep
        if structure in ["BULLISH", "NEUTRAL"]:
            for level_name in ['PDL', 'TOKYO_LOW']:
                level = levels[level_name]

                swept = (prev['low'] < level or prev2['low'] < level)
                reversed = current['close'] > level

                if swept and reversed:
                    confidence = 0.70

                    # Check for CHoCH bonus (optional)
                    has_choch = self.has_choch_confirmation(candles_5m[:current_index], 'BUY')
                    if has_choch:
                        confidence += 0.10

                    return ('BUY', level_name, current, confidence, has_choch)

        # Bearish sweep
        if structure in ["BEARISH", "NEUTRAL"]:
            for level_name in ['PDH', 'TOKYO_HIGH']:
                level = levels[level_name]

                swept = (prev['high'] > level or prev2['high'] > level)
                reversed = current['close'] < level

                if swept and reversed:
                    confidence = 0.70

                    # Check for CHoCH bonus (optional)
                    has_choch = self.has_choch_confirmation(candles_5m[:current_index], 'SELL')
                    if has_choch:
                        confidence += 0.10

                    return ('SELL', level_name, current, confidence, has_choch)

        return None

    def has_choch_confirmation(self, candles_5m, direction):
        """Check for CHoCH (simple version)"""
        if len(candles_5m) < 10:
            return False

        recent = candles_5m[-10:]
        last = recent[-1]

        candle_range = last['high'] - last['low']
        candle_body = abs(last['close'] - last['open'])

        if candle_range == 0:
            return False

        body_to_range = candle_body / candle_range

        if direction == 'BUY':
            is_bullish = last['close'] > last['open']
            is_strong = body_to_range > 0.6
            recent_highs = [c['high'] for c in recent[-6:-1]]
            breaks_structure = last['high'] > max(recent_highs) if recent_highs else False

            return is_bullish and is_strong and breaks_structure

        else:  # SELL
            is_bearish = last['close'] < last['open']
            is_strong = body_to_range > 0.6
            recent_lows = [c['low'] for c in recent[-6:-1]]
            breaks_structure = last['low'] < min(recent_lows) if recent_lows else False

            return is_bearish and is_strong and breaks_structure

    def build_v5_signal(self, direction, current_candle, rejection_candle, atr, balance):
        """Build v5.1 signal with stricter stops"""
        current_price = current_candle['close']
        risk_amount = balance * RISK_PER_TRADE

        if direction == 'BUY':
            # V5: Use FURTHER stop (more conservative)
            atr_stop = current_price - (atr * ATR_MULTIPLIER)
            swing_stop = rejection_candle['low'] - 2.0
            sl = min(atr_stop, swing_stop)  # FURTHER = minimum

            risk = current_price - sl
            tp = current_price + (risk * RISK_REWARD_RATIO)

            lot_size = risk_amount / (risk * 10)
            lot_size = max(0.01, round(lot_size, 2))

            if risk <= 0:
                return None

            return {
                "decision": "BUY",
                "price": current_price,
                "sl": round(sl, 2),
                "tp": round(tp, 2),
                "lot_size": lot_size
            }

        else:  # SELL
            # V5: Use FURTHER stop (more conservative)
            atr_stop = current_price + (atr * ATR_MULTIPLIER)
            swing_stop = rejection_candle['high'] + 2.0
            sl = max(atr_stop, swing_stop)  # FURTHER = maximum

            risk = sl - current_price
            tp = current_price - (risk * RISK_REWARD_RATIO)

            lot_size = risk_amount / (risk * 10)
            lot_size = max(0.01, round(lot_size, 2))

            if risk <= 0:
                return None

            return {
                "decision": "SELL",
                "price": current_price,
                "sl": round(sl, 2),
                "tp": round(tp, 2),
                "lot_size": lot_size
            }

    def simulate_v5_outcome(self, trade, future_candles):
        """Simulate with breakeven at 1:1.5 (v5 enhancement)"""
        entry = trade['entry_price']
        sl = trade['sl']
        tp = trade['tp']
        lot_size = trade['lot_size']

        for candle in future_candles[:200]:
            if trade['decision'] == 'BUY':
                # Breakeven at 1:1.5
                if not trade['breakeven_moved']:
                    risk = entry - sl
                    if candle['high'] >= entry + (risk * BREAKEVEN_TRIGGER):
                        sl = entry
                        trade['breakeven_moved'] = True

                # Check SL
                if candle['low'] <= sl:
                    trade['outcome'] = 'BREAKEVEN' if trade['breakeven_moved'] else 'LOSS'
                    price_diff = (sl - entry) if not trade['breakeven_moved'] else 0
                    trade['pnl'] = price_diff * lot_size * 10
                    return

                # Check TP
                if candle['high'] >= tp:
                    trade['outcome'] = 'WIN'
                    price_diff = tp - entry
                    trade['pnl'] = price_diff * lot_size * 10
                    return

            else:  # SELL
                # Breakeven at 1:1.5
                if not trade['breakeven_moved']:
                    risk = sl - entry
                    if candle['low'] <= entry - (risk * BREAKEVEN_TRIGGER):
                        sl = entry
                        trade['breakeven_moved'] = True

                # Check SL
                if candle['high'] >= sl:
                    trade['outcome'] = 'BREAKEVEN' if trade['breakeven_moved'] else 'LOSS'
                    price_diff = (entry - sl) if not trade['breakeven_moved'] else 0
                    trade['pnl'] = price_diff * lot_size * 10 * -1
                    return

                # Check TP
                if candle['low'] <= tp:
                    trade['outcome'] = 'WIN'
                    price_diff = entry - tp
                    trade['pnl'] = price_diff * lot_size * 10
                    return

        trade['outcome'] = 'OPEN'

    # ==================== RESULTS CALCULATION ====================
    def calculate_results(self, name, trades, balance):
        """Calculate strategy results"""
        total_trades = len(trades)

        if total_trades == 0:
            return {
                'name': name,
                'trades': 0,
                'wins': 0,
                'losses': 0,
                'breakevens': 0,
                'roi': 0,
                'win_rate': 0,
                'avg_win': 0,
                'avg_loss': 0
            }

        wins = [t for t in trades if t.get('outcome') == 'WIN']
        losses = [t for t in trades if t.get('outcome') == 'LOSS']
        breakevens = [t for t in trades if t.get('outcome') == 'BREAKEVEN']

        win_rate = (len(wins) / total_trades * 100) if total_trades > 0 else 0
        total_pnl = sum(t['pnl'] for t in trades)
        roi = (total_pnl / INITIAL_BALANCE) * 100

        avg_win = sum(t['pnl'] for t in wins) / len(wins) if wins else 0
        avg_loss = sum(t['pnl'] for t in losses) / len(losses) if losses else 0

        return {
            'name': name,
            'trades': total_trades,
            'wins': len(wins),
            'losses': len(losses),
            'breakevens': len(breakevens),
            'roi': roi,
            'win_rate': win_rate,
            'avg_win': avg_win,
            'avg_loss': avg_loss
        }

    def generate_comparison_report(self):
        """Generate master comparison report"""
        print("\n" + "="*80)
        print("📊 60-DAY MASTER BACKTEST - ALL STRATEGIES COMPARISON")
        print("="*80)
        print(f"\nTest Period: November 1 - December 27, 2025 (57 days)")
        print(f"Initial Balance: ${INITIAL_BALANCE:,.2f}")
        print(f"Data Source: Twelve Data API\n")

        # Print comparison table
        print("="*80)
        print(f"{'Strategy':<40} {'Trades':<8} {'Win%':<8} {'ROI%':<10}")
        print("="*80)

        for name, results in self.all_results.items():
            print(f"{results['name']:<40} {results['trades']:<8} {results['win_rate']:<8.1f} {results['roi']:<10.2f}")

        print("="*80)

        # Detailed breakdown
        print("\n" + "="*80)
        print("📈 DETAILED BREAKDOWN")
        print("="*80)

        for name, results in self.all_results.items():
            print(f"\n{results['name']}")
            print(f"   Total Trades: {results['trades']}")
            print(f"   Wins: {results['wins']} ({results['win_rate']:.1f}%)")
            print(f"   Losses: {results['losses']}")
            print(f"   Breakevens: {results['breakevens']}")
            print(f"   ROI: {results['roi']:+.2f}%")
            if results['wins'] > 0:
                print(f"   Average Win: ${results['avg_win']:,.2f}")
            if results['losses'] > 0:
                print(f"   Average Loss: ${results['avg_loss']:,.2f}")

        print("\n" + "="*80)

def main():
    print("\n" + "="*80)
    print("🚀 60-DAY MASTER BACKTEST - ALL STRATEGIES")
    print("="*80)
    print("\nThis script will run ALL 4 strategies on 60 days of Gold data")
    print("and provide a comprehensive comparison report.\n")

    backtest = MasterBacktest()

    # Fetch data
    data = backtest.fetch_data_twelvedata()

    if data is None:
        print("❌ Failed to fetch data. Exiting.")
        return

    print(f"\n✅ Data loaded successfully!")
    print(f"   Ready to backtest {len(data['15m'])} candles across 4 strategies\n")

    # Run all strategies
    print("📊 RUNNING ALL STRATEGIES...")
    print("   This will take a few minutes...\n")

    # Strategy #2
    results_2 = backtest.run_strategy_2(data)
    backtest.all_results['strategy_2'] = results_2

    # Strategy #3
    results_3 = backtest.run_strategy_3(data)
    backtest.all_results['strategy_3'] = results_3

    # Strategy #4
    results_4 = backtest.run_strategy_4(data)
    backtest.all_results['strategy_4'] = results_4

    # Strategy v5.1
    results_v5_1 = backtest.run_strategy_v5_1(data)
    backtest.all_results['strategy_v5_1'] = results_v5_1

    # Generate final report
    backtest.generate_comparison_report()

    print("\n✅ Master backtest complete!")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
