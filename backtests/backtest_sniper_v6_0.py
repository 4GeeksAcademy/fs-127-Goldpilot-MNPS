#!/usr/bin/env python3
"""
Strategy v6.0: "Resilient Sniper" - Enhanced Liquidity Sweep Strategy
60-Day Backtest with Three Critical Optimizations

Enhancements from v4:
1. PARTIAL PROFIT TAKING: Close 50% at 1:1.5 RR, move SL to entry
2. DISPLACEMENT FILTER: Expansion candle requirement (body > avg of last 5)
3. TIME NARROWING: London 07:00-11:00 + NY 13:00-16:00 UTC only

Test Period: November 1 - December 27, 2025 (57 days)
"""

import asyncio
from datetime import datetime, timedelta
import pytz
import os
from dotenv import load_dotenv
from twelvedata import TDClient
import time
import json

load_dotenv()

TWELVEDATA_API_KEY = os.getenv('TWELVEDATA_API_KEY')
INITIAL_BALANCE = 10000
RISK_PER_TRADE = 0.01  # 1% risk
RISK_REWARD_RATIO = 3.0
ATR_MULTIPLIER = 1.5
ATR_MAX_VOLATILITY = 40.0
MAX_TRADES_PER_DAY = 4
PARTIAL_CLOSE_RR = 1.5  # Close 50% at 1:1.5 RR
PARTIAL_CLOSE_PERCENT = 0.5  # Close 50% of position

class SniperV6:
    def __init__(self):
        self.balance = INITIAL_BALANCE
        self.trades = []
        self.daily_trades = {}

    def convert_df_to_candles(self, df):
        """Convert pandas DataFrame to candle list"""
        candles = []
        for index, row in df.iterrows():
            # Ensure timezone-aware datetime
            timestamp = index
            if timestamp.tzinfo is None:
                timestamp = pytz.utc.localize(timestamp)

            candles.append({
                'time': timestamp,
                'open': float(row['open']),
                'high': float(row['high']),
                'low': float(row['low']),
                'close': float(row['close']),
                'volume': float(row['volume']) if 'volume' in row else 0
            })
        return sorted(candles, key=lambda x: x['time'])

    def fetch_data_twelvedata(self):
        """Fetch 60 days of Gold data from Twelve Data"""
        print("="*80)
        print("📊 STRATEGY v6.0: RESILIENT SNIPER")
        print("="*80)
        print(f"\n🔑 Using Twelve Data API")
        print(f"📅 Target period: Nov 1 - Dec 27, 2025 (57 days)")
        print(f"\n✨ ENHANCEMENTS:")
        print(f"   1. Partial Profit: 50% close at 1:1.5 RR")
        print(f"   2. Displacement Filter: Expansion candle required")
        print(f"   3. Time Windows: London 07:00-11:00 + NY 13:00-16:00 UTC")

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

            print(f"\n✅ DATA SUMMARY:")
            print(f"   15m candles: {len(candles_15m_filtered)}")
            print(f"   1h candles:  {len(candles_1h_filtered)}")
            print(f"   4h candles:  {len(candles_4h_filtered)}")

            return {
                '15m': candles_15m_filtered,
                '1h': candles_1h_filtered,
                '4h': candles_4h_filtered
            }

        except Exception as e:
            print(f"\n❌ Error fetching data: {e}")
            return None

    def get_session(self, timestamp):
        """Determine trading session"""
        hour = timestamp.hour
        if 0 <= hour < 7:
            return "TOKYO"
        elif 7 <= hour < 16:
            return "LONDON"
        else:
            return "NY"

    def is_in_kill_zone(self, timestamp):
        """
        v6.0 ENHANCEMENT #3: Narrowed time windows
        London: 07:00-11:00 UTC
        NY: 13:00-16:00 UTC
        """
        hour = timestamp.hour
        # London morning only (07:00-11:00)
        if 7 <= hour < 11:
            return True, "LONDON"
        # NY open only (13:00-16:00)
        elif 13 <= hour < 16:
            return True, "NY"
        return False, None

    def calculate_atr(self, candles_4h, current_time):
        """Calculate ATR from 4h candles"""
        relevant_candles = [c for c in candles_4h if c['time'] <= current_time]
        if len(relevant_candles) < 14:
            return None

        recent_candles = relevant_candles[-14:]
        tr_values = []

        for i in range(1, len(recent_candles)):
            high = recent_candles[i]['high']
            low = recent_candles[i]['low']
            prev_close = recent_candles[i-1]['close']

            tr = max(
                high - low,
                abs(high - prev_close),
                abs(low - prev_close)
            )
            tr_values.append(tr)

        atr = sum(tr_values) / len(tr_values)
        return min(atr, ATR_MAX_VOLATILITY)

    def get_market_structure(self, candles_1h, current_time):
        """Determine market structure from 1h candles"""
        relevant_candles = [c for c in candles_1h if c['time'] <= current_time]
        if len(relevant_candles) < 20:
            return "NEUTRAL"

        recent = relevant_candles[-20:]
        highs = [c['high'] for c in recent]
        lows = [c['low'] for c in recent]

        higher_highs = sum(1 for i in range(1, len(highs)) if highs[i] > highs[i-1])
        higher_lows = sum(1 for i in range(1, len(lows)) if lows[i] > lows[i-1])
        lower_highs = sum(1 for i in range(1, len(highs)) if highs[i] < highs[i-1])
        lower_lows = sum(1 for i in range(1, len(lows)) if lows[i] < lows[i-1])

        if higher_highs > 12 and higher_lows > 12:
            return "BULLISH"
        elif lower_highs > 12 and lower_lows > 12:
            return "BEARISH"
        return "NEUTRAL"

    def get_daily_levels(self, candles_15m, current_time):
        """Get previous day high/low and Tokyo session levels"""
        prev_day = current_time - timedelta(days=1)
        prev_day_start = prev_day.replace(hour=0, minute=0, second=0)
        prev_day_end = prev_day.replace(hour=23, minute=59, second=59)

        prev_day_candles = [c for c in candles_15m if prev_day_start <= c['time'] <= prev_day_end]
        if not prev_day_candles:
            return None

        pdh = max(c['high'] for c in prev_day_candles)
        pdl = min(c['low'] for c in prev_day_candles)

        # Tokyo session (00:00 - 07:00 UTC)
        tokyo_start = current_time.replace(hour=0, minute=0, second=0)
        tokyo_end = current_time.replace(hour=7, minute=0, second=0)
        tokyo_candles = [c for c in candles_15m if tokyo_start <= c['time'] <= tokyo_end]

        tokyo_high = max(c['high'] for c in tokyo_candles) if tokyo_candles else pdh
        tokyo_low = min(c['low'] for c in tokyo_candles) if tokyo_candles else pdl

        return {
            'PDH': pdh,
            'PDL': pdl,
            'TOKYO_HIGH': tokyo_high,
            'TOKYO_LOW': tokyo_low
        }

    def check_displacement(self, candles_15m, current_index):
        """
        v6.0 ENHANCEMENT #2: Displacement Filter
        Require expansion candle (body > average of last 5 candles)
        """
        if current_index < 6:
            return False

        # Get current candle body
        current = candles_15m[current_index]
        current_body = abs(current['close'] - current['open'])

        # Calculate average body of last 5 candles
        last_5 = candles_15m[current_index-5:current_index]
        avg_body = sum(abs(c['close'] - c['open']) for c in last_5) / 5

        # Current candle must be expansion (larger than average)
        return current_body > avg_body

    def detect_liquidity_sweep(self, candles_15m, current_index, levels, structure):
        """
        Detect liquidity sweep at key levels
        v6.0: Now requires displacement validation
        """
        if current_index < 3:
            return None

        current = candles_15m[current_index]
        prev = candles_15m[current_index - 1]

        # v6.0 ENHANCEMENT #2: Check displacement first
        if not self.check_displacement(candles_15m, current_index):
            return None

        # Check for PDH sweep (SELL setup)
        if prev['high'] > levels['PDH'] and current['close'] < levels['PDH']:
            return {
                'type': 'SELL',
                'level': 'PDH',
                'level_price': levels['PDH'],
                'rejection_candle': current
            }

        # Check for PDL sweep (BUY setup)
        if prev['low'] < levels['PDL'] and current['close'] > levels['PDL']:
            return {
                'type': 'BUY',
                'level': 'PDL',
                'level_price': levels['PDL'],
                'rejection_candle': current
            }

        # Check for Tokyo High sweep (SELL setup)
        if prev['high'] > levels['TOKYO_HIGH'] and current['close'] < levels['TOKYO_HIGH']:
            return {
                'type': 'SELL',
                'level': 'TOKYO_HIGH',
                'level_price': levels['TOKYO_HIGH'],
                'rejection_candle': current
            }

        # Check for Tokyo Low sweep (BUY setup)
        if prev['low'] < levels['TOKYO_LOW'] and current['close'] > levels['TOKYO_LOW']:
            return {
                'type': 'BUY',
                'level': 'TOKYO_LOW',
                'level_price': levels['TOKYO_LOW'],
                'rejection_candle': current
            }

        return None

    def build_signal(self, sweep, current_candle, atr, balance, structure, session):
        """Build trading signal with ATR-based stops"""
        direction = sweep['type']
        price = current_candle['close']

        # ATR-based stop loss
        stop_distance = atr * ATR_MULTIPLIER

        if direction == 'BUY':
            sl = price - stop_distance
            tp = price + (stop_distance * RISK_REWARD_RATIO)
        else:  # SELL
            sl = price + stop_distance
            tp = price - (stop_distance * RISK_REWARD_RATIO)

        # Calculate lot size for 1% risk
        risk_dollars = balance * RISK_PER_TRADE
        lot_size = round(risk_dollars / (stop_distance * 10), 2)

        return {
            'decision': direction,
            'price': price,
            'sl': sl,
            'tp': tp,
            'lot_size': lot_size,
            'risk': stop_distance,
            'atr': atr,
            'level_swept': sweep['level'],
            'level_price': sweep['level_price'],
            'structure': structure,
            'session': session
        }

    def simulate_trade_outcome_v6(self, trade, future_candles):
        """
        v6.0 ENHANCEMENT #1: Partial Profit Taking
        Close 50% at 1:1.5 RR, move SL to entry
        Track both partial and full exits
        """
        if not future_candles:
            trade['outcome'] = 'OPEN'
            return

        entry = trade['entry_price']
        sl = trade['sl']
        tp = trade['tp']
        direction = trade['decision']

        candles_until_exit = 0
        partial_closed = False
        partial_profit = 0
        sl_moved_to_entry = False

        for candle in future_candles[:200]:  # Max 200 candles (50 hours)
            candles_until_exit += 1

            # Calculate risk distance
            if direction == 'BUY':
                risk = entry - sl
                reward_1_5 = entry + (risk * PARTIAL_CLOSE_RR)

                # Check for partial profit at 1:1.5 RR
                if not partial_closed and candle['high'] >= reward_1_5:
                    partial_closed = True
                    partial_profit = (reward_1_5 - entry) * trade['lot_size'] * 10 * PARTIAL_CLOSE_PERCENT
                    sl = entry  # Move SL to breakeven
                    sl_moved_to_entry = True
                    trade['partial_close_price'] = reward_1_5
                    trade['partial_close_candle'] = candles_until_exit

                # Check TP (now only 50% of position if partial closed)
                if candle['high'] >= tp:
                    if partial_closed:
                        # Only 50% left to close at TP
                        remaining_profit = (tp - entry) * trade['lot_size'] * 10 * (1 - PARTIAL_CLOSE_PERCENT)
                        total_profit = partial_profit + remaining_profit
                    else:
                        # Full position closes at TP (no partial triggered)
                        total_profit = (tp - entry) * trade['lot_size'] * 10

                    self.balance += total_profit
                    trade['outcome'] = 'WIN'
                    trade['exit_price'] = tp
                    trade['exit_time'] = candle['time']
                    trade['pnl'] = round(total_profit, 2)
                    trade['candles_in_trade'] = candles_until_exit
                    trade['partial_activated'] = partial_closed
                    return

                # Check SL
                if candle['low'] <= sl:
                    if partial_closed:
                        # Partial already banked, remaining 50% exits at breakeven (entry)
                        total_profit = partial_profit  # Only keep partial profit
                    else:
                        # Full stop loss hit
                        total_profit = (sl - entry) * trade['lot_size'] * 10

                    self.balance += total_profit
                    trade['outcome'] = 'LOSS' if total_profit < 0 else 'BREAKEVEN'
                    trade['exit_price'] = sl
                    trade['exit_time'] = candle['time']
                    trade['pnl'] = round(total_profit, 2)
                    trade['candles_in_trade'] = candles_until_exit
                    trade['partial_activated'] = partial_closed
                    return

            else:  # SELL
                risk = sl - entry
                reward_1_5 = entry - (risk * PARTIAL_CLOSE_RR)

                # Check for partial profit at 1:1.5 RR
                if not partial_closed and candle['low'] <= reward_1_5:
                    partial_closed = True
                    partial_profit = (entry - reward_1_5) * trade['lot_size'] * 10 * PARTIAL_CLOSE_PERCENT
                    sl = entry  # Move SL to breakeven
                    sl_moved_to_entry = True
                    trade['partial_close_price'] = reward_1_5
                    trade['partial_close_candle'] = candles_until_exit

                # Check TP
                if candle['low'] <= tp:
                    if partial_closed:
                        remaining_profit = (entry - tp) * trade['lot_size'] * 10 * (1 - PARTIAL_CLOSE_PERCENT)
                        total_profit = partial_profit + remaining_profit
                    else:
                        total_profit = (entry - tp) * trade['lot_size'] * 10

                    self.balance += total_profit
                    trade['outcome'] = 'WIN'
                    trade['exit_price'] = tp
                    trade['exit_time'] = candle['time']
                    trade['pnl'] = round(total_profit, 2)
                    trade['candles_in_trade'] = candles_until_exit
                    trade['partial_activated'] = partial_closed
                    return

                # Check SL
                if candle['high'] >= sl:
                    if partial_closed:
                        total_profit = partial_profit
                    else:
                        total_profit = (entry - sl) * trade['lot_size'] * 10

                    self.balance += total_profit
                    trade['outcome'] = 'LOSS' if total_profit < 0 else 'BREAKEVEN'
                    trade['exit_price'] = sl
                    trade['exit_time'] = candle['time']
                    trade['pnl'] = round(total_profit, 2)
                    trade['candles_in_trade'] = candles_until_exit
                    trade['partial_activated'] = partial_closed
                    return

        # Trade still open after max candles
        trade['outcome'] = 'OPEN'
        trade['partial_activated'] = partial_closed

    def can_trade_today(self, timestamp):
        """Check if we can take another trade today"""
        date_key = timestamp.strftime('%Y-%m-%d')
        if date_key not in self.daily_trades:
            self.daily_trades[date_key] = 0
        return self.daily_trades[date_key] < MAX_TRADES_PER_DAY

    def increment_daily_trades(self, timestamp):
        """Increment daily trade counter"""
        date_key = timestamp.strftime('%Y-%m-%d')
        if date_key not in self.daily_trades:
            self.daily_trades[date_key] = 0
        self.daily_trades[date_key] += 1

    def run_backtest(self):
        """Run v6.0 backtest with all enhancements"""
        data = self.fetch_data_twelvedata()
        if not data:
            return

        candles_15m = data['15m']
        candles_1h = data['1h']
        candles_4h = data['4h']

        print("\n" + "="*80)
        print("🚀 STARTING v6.0 BACKTEST")
        print("="*80)

        for i in range(100, len(candles_15m) - 1):
            current_candle = candles_15m[i]
            timestamp = current_candle['time']

            # v6.0 ENHANCEMENT #3: Check kill zone
            in_kill_zone, session = self.is_in_kill_zone(timestamp)
            if not in_kill_zone:
                continue

            # Check daily trade limit
            if not self.can_trade_today(timestamp):
                continue

            # Get ATR and structure
            atr = self.calculate_atr(candles_4h, timestamp)
            if not atr:
                continue

            structure = self.get_market_structure(candles_1h, timestamp)

            # Get daily levels
            levels = self.get_daily_levels(candles_15m, timestamp)
            if not levels:
                continue

            # Detect liquidity sweep (now with displacement filter)
            sweep = self.detect_liquidity_sweep(candles_15m, i, levels, structure)
            if not sweep:
                continue

            # Build signal
            signal = self.build_signal(sweep, current_candle, atr, self.balance, structure, session)

            # Create trade
            trade = {
                "trade_number": len(self.trades) + 1,
                "timestamp": timestamp.strftime('%Y-%m-%d %H:%M UTC'),
                "decision": signal['decision'],
                "entry_price": round(signal['price'], 2),
                "sl": round(signal['sl'], 2),
                "tp": round(signal['tp'], 2),
                "lot_size": signal['lot_size'],
                "atr": round(signal['atr'], 2),
                "market_structure": signal['structure'],
                "session": signal['session'],
                "level_swept": signal['level_swept'],
                "level_price": round(signal['level_price'], 2),
                "balance_before": round(self.balance, 2),
                "partial_activated": False,
                "partial_close_price": None,
                "partial_close_candle": None
            }

            # Simulate outcome with v6.0 partial profit logic
            self.simulate_trade_outcome_v6(trade, candles_15m[i+1:])

            if trade.get('outcome') in ['WIN', 'LOSS', 'BREAKEVEN']:
                trade['balance_after'] = round(self.balance, 2)

            # Convert exit_time to string for JSON serialization
            if 'exit_time' in trade and trade['exit_time']:
                trade['exit_time'] = trade['exit_time'].strftime('%Y-%m-%d %H:%M UTC')

            self.trades.append(trade)
            self.increment_daily_trades(timestamp)

            if len(self.trades) % 10 == 0:
                print(f"   📊 Processed {len(self.trades)} trades...")

        self.print_results()
        self.save_results()

    def print_results(self):
        """Print comprehensive results"""
        wins = [t for t in self.trades if t.get('outcome') == 'WIN']
        losses = [t for t in self.trades if t.get('outcome') == 'LOSS']
        breakevens = [t for t in self.trades if t.get('outcome') == 'BREAKEVEN']
        open_trades = [t for t in self.trades if t.get('outcome') == 'OPEN']
        partial_activated = [t for t in self.trades if t.get('partial_activated')]

        total_pnl = self.balance - INITIAL_BALANCE
        roi = (total_pnl / INITIAL_BALANCE) * 100

        print("\n" + "="*80)
        print("📊 STRATEGY v6.0: RESILIENT SNIPER - RESULTS")
        print("="*80)
        print(f"\n💰 PERFORMANCE:")
        print(f"   Initial Balance:  ${INITIAL_BALANCE:,.2f}")
        print(f"   Final Balance:    ${self.balance:,.2f}")
        print(f"   Total P&L:        ${total_pnl:,.2f}")
        print(f"   ROI:              {roi:+.2f}%")

        print(f"\n📈 TRADE STATISTICS:")
        print(f"   Total Trades:     {len(self.trades)}")
        print(f"   Wins:             {len(wins)} ({len(wins)/len(self.trades)*100:.1f}%)")
        print(f"   Losses:           {len(losses)} ({len(losses)/len(self.trades)*100:.1f}%)")
        print(f"   Breakevens:       {len(breakevens)} ({len(breakevens)/len(self.trades)*100:.1f}%)")
        print(f"   Open:             {len(open_trades)} ({len(open_trades)/len(self.trades)*100:.1f}%)")

        print(f"\n✨ v6.0 ENHANCEMENTS:")
        print(f"   Partial Activations: {len(partial_activated)} ({len(partial_activated)/len(self.trades)*100:.1f}%)")

        if wins:
            avg_win = sum(t['pnl'] for t in wins) / len(wins)
            print(f"   Average Win:      ${avg_win:.2f}")

        if losses:
            avg_loss = sum(t['pnl'] for t in losses) / len(losses)
            print(f"   Average Loss:     ${avg_loss:.2f}")

        print("\n" + "="*80)

    def save_results(self):
        """Save results to JSON"""
        output = {
            "strategy": "v6.0 Resilient Sniper",
            "test_period": "November 1 - December 27, 2025",
            "initial_balance": INITIAL_BALANCE,
            "final_balance": round(self.balance, 2),
            "total_pnl": round(self.balance - INITIAL_BALANCE, 2),
            "roi": round(((self.balance - INITIAL_BALANCE) / INITIAL_BALANCE) * 100, 2),
            "enhancements": {
                "partial_profit_at": f"{PARTIAL_CLOSE_RR}:1 RR",
                "partial_close_percent": f"{PARTIAL_CLOSE_PERCENT*100}%",
                "displacement_filter": "Expansion candle required",
                "time_windows": "London 07:00-11:00 + NY 13:00-16:00 UTC"
            },
            "total_trades": len(self.trades),
            "wins": len([t for t in self.trades if t.get('outcome') == 'WIN']),
            "losses": len([t for t in self.trades if t.get('outcome') == 'LOSS']),
            "breakevens": len([t for t in self.trades if t.get('outcome') == 'BREAKEVEN']),
            "partial_activations": len([t for t in self.trades if t.get('partial_activated')]),
            "trades": self.trades
        }

        with open('STRATEGY_V6_0_RESULTS.json', 'w') as f:
            json.dump(output, f, indent=2)

        print(f"\n💾 Results saved to STRATEGY_V6_0_RESULTS.json")

if __name__ == "__main__":
    sniper = SniperV6()
    sniper.run_backtest()
