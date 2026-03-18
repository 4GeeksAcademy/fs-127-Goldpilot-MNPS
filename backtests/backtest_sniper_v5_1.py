#!/usr/bin/env python3
"""
Aurum Sniper v5.1 - BALANCED Production Model

V5.1 Adjustments (more practical than v5.0):
1. Expanded Kill Zones: London (07:00-10:00), NY (13:00-16:00) - 6 hours total
2. Relaxed CHoCH: Optional bonus (not required) - adds confidence if present
3. ATR Volatility Cap: Keep $40 limit (good filter)
4. Breakeven at 1:1.5 RR: Keep (excellent protection)
5. Stricter Stops: Keep 1.5x ATR OR swing extreme

Philosophy: v4 quality with v5 risk management enhancements
"""

import asyncio
from datetime import datetime, timedelta
import pytz
from metaapi_cloud_sdk import MetaApi
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
META_API_TOKEN = os.getenv('METAAPI_TOKEN')
ACCOUNT_ID = os.getenv('METAAPI_ACCOUNT_ID', '436348e0-be6e-49cc-a991-8895903e5288')
INITIAL_BALANCE = 10000
RISK_PER_TRADE = 0.01  # 1% risk per trade
RISK_REWARD_RATIO = 3.0  # 1:3 RR
ATR_MULTIPLIER = 1.5  # Stop loss = 1.5x ATR
ATR_MAX_VOLATILITY = 40.0  # Skip trades if ATR > $40 (v5 enhancement)
MAX_TRADES_PER_DAY = 4  # Increased from v5's 2 for more opportunities
BREAKEVEN_TRIGGER = 1.5  # Move to BE at 1:1.5 RR (v5 enhancement - earlier protection)

class AurumSniperV5_1:
    def __init__(self):
        self.balance = INITIAL_BALANCE
        self.trades = []
        self.api_requests = 0
        self.trades_today = 0
        self.current_date = None

    async def fetch_historical_data(self):
        """Fetch multi-timeframe data for December 2025"""
        api = MetaApi(META_API_TOKEN)
        account = await api.metatrader_account_api.get_account(ACCOUNT_ID)

        if account.state != 'DEPLOYED':
            print(f"⚠️ Deploying account {ACCOUNT_ID}...")
            await account.deploy()

        print("⏳ Waiting for broker connection...")
        await account.wait_connected()

        connection = account.get_streaming_connection()
        await connection.connect()
        await connection.wait_synchronized()

        print("✅ Connected! Fetching historical data...")

        # Extended 60-day backtest: Nov 1 - Dec 27, 2025
        start_date = datetime(2025, 11, 1, 0, 0, 0, tzinfo=pytz.utc)

        # Calculate candles needed for 60 days
        # 60 days * 24 hours * 12 (5m candles per hour) = 17,280 candles
        # 60 days * 24 hours * 4 (15m candles per hour) = 5,760 candles
        # 60 days * 24 hours = 1,440 1h candles
        # 60 days * 6 (4h candles per day) = 360 candles

        # Fetch multiple timeframes
        print("📊 Fetching 5-minute candles (CHoCH bonus) - 60 days...")
        candles_5m = await account.get_historical_candles('GOLD.pro', '5m', start_date, 17500)
        self.api_requests += 1

        print("📊 Fetching 15-minute candles (entry timeframe) - 60 days...")
        candles_15m = await account.get_historical_candles('GOLD.pro', '15m', start_date, 6000)
        self.api_requests += 1

        print("📊 Fetching 1-hour candles (structure) - 60 days...")
        candles_1h = await account.get_historical_candles('GOLD.pro', '1h', start_date, 1500)
        self.api_requests += 1

        print("📊 Fetching 4-hour candles (ATR calculation) - 60 days...")
        candles_4h = await account.get_historical_candles('GOLD.pro', '4h', start_date, 400)
        self.api_requests += 1

        print(f"✅ Data fetched: {len(candles_5m)} 5m, {len(candles_15m)} 15m, {len(candles_1h)} 1h, {len(candles_4h)} 4h candles")

        await connection.close()

        return {
            '5m': candles_5m,
            '15m': candles_15m,
            '1h': candles_1h,
            '4h': candles_4h
        }

    def calculate_daily_levels(self, candles_15m, current_index):
        """Calculate PDH/PDL and Tokyo Session levels (recalculated daily)"""
        current_candle = candles_15m[current_index]
        current_time = current_candle['time'] if isinstance(current_candle['time'], datetime) else datetime.fromtimestamp(current_candle['time'], tz=pytz.utc)
        current_date = current_time.date()

        # Reset daily counter on new day
        if self.current_date != current_date:
            self.current_date = current_date
            self.trades_today = 0

        # Get previous day's candles
        prev_day_start = datetime.combine(current_date - timedelta(days=1), datetime.min.time()).replace(tzinfo=pytz.utc)
        prev_day_end = datetime.combine(current_date, datetime.min.time()).replace(tzinfo=pytz.utc)

        prev_day_candles = [
            c for c in candles_15m[:current_index]
            if prev_day_start <= (c['time'] if isinstance(c['time'], datetime) else datetime.fromtimestamp(c['time'], tz=pytz.utc)) < prev_day_end
        ]

        if not prev_day_candles:
            return None

        # PDH/PDL from previous full day
        pdh = max(c['high'] for c in prev_day_candles)
        pdl = min(c['low'] for c in prev_day_candles)

        # Tokyo Session High/Low
        tokyo_start = datetime.combine(current_date - timedelta(days=1), datetime.min.time()).replace(hour=23, tzinfo=pytz.utc)
        tokyo_end = datetime.combine(current_date, datetime.min.time()).replace(hour=8, tzinfo=pytz.utc)

        tokyo_candles = [
            c for c in candles_15m[:current_index]
            if tokyo_start <= (c['time'] if isinstance(c['time'], datetime) else datetime.fromtimestamp(c['time'], tz=pytz.utc)) < tokyo_end
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
        """Determine market structure: BULLISH, BEARISH, or NEUTRAL"""
        if len(candles_1h) < 15:
            return "NEUTRAL"

        recent = candles_1h[-15:]
        highs = [c['high'] for c in recent]
        lows = [c['low'] for c in recent]

        recent_high = max(highs[-5:])
        previous_high = max(highs[-15:-5]) if len(highs) >= 15 else recent_high
        recent_low = min(lows[-5:])
        previous_low = min(lows[-15:-5]) if len(lows) >= 15 else recent_low

        if recent_high > previous_high and recent_low >= previous_low:
            return "BULLISH"
        elif recent_low < previous_low and recent_high <= previous_high:
            return "BEARISH"
        else:
            return "NEUTRAL"

    def calculate_atr(self, candles_4h, period=14):
        """Calculate ATR for volatility measurement and stop loss sizing"""
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

        atr = sum(tr_list) / len(tr_list)
        return atr

    def detect_choch_bonus(self, candles_5m, direction):
        """
        V5.1: CHoCH is now OPTIONAL bonus (not required)
        Returns confidence boost if CHoCH detected
        """
        if len(candles_5m) < 10:
            return 0

        recent_5m = candles_5m[-10:]
        last_candle = recent_5m[-1]

        candle_range = last_candle['high'] - last_candle['low']
        candle_body = abs(last_candle['close'] - last_candle['open'])
        body_to_range = candle_body / candle_range if candle_range > 0 else 0

        is_strong_candle = body_to_range > 0.6

        if direction == 'BUY':
            is_bullish = last_candle['close'] > last_candle['open']
            recent_highs = [c['high'] for c in recent_5m[-6:-1]]
            breaks_structure = last_candle['high'] > max(recent_highs) if recent_highs else False

            if is_bullish and is_strong_candle and breaks_structure:
                return 0.10  # 10% confidence bonus

        elif direction == 'SELL':
            is_bearish = last_candle['close'] < last_candle['open']
            recent_lows = [c['low'] for c in recent_5m[-6:-1]]
            breaks_structure = last_candle['low'] < min(recent_lows) if recent_lows else False

            if is_bearish and is_strong_candle and breaks_structure:
                return 0.10  # 10% confidence bonus

        return 0

    def detect_liquidity_sweep(self, candles_15m, candles_5m, current_index, levels, market_structure):
        """
        V5.1: Liquidity sweep detection WITHOUT mandatory CHoCH
        CHoCH adds confidence bonus but is not required
        """
        if current_index < 3:
            return None

        current = candles_15m[current_index]
        prev = candles_15m[current_index - 1]
        prev2 = candles_15m[current_index - 2]

        # Get corresponding 5m candles
        current_time = current['time'] if isinstance(current['time'], datetime) else datetime.fromtimestamp(current['time'], tz=pytz.utc)
        recent_5m = [c for c in candles_5m if (c['time'] if isinstance(c['time'], datetime) else datetime.fromtimestamp(c['time'], tz=pytz.utc)) <= current_time][-10:]

        # BULLISH SWEEP
        if market_structure in ["BULLISH", "NEUTRAL"]:
            for level_name in ['PDL', 'TOKYO_LOW']:
                level = levels[level_name]

                swept = (prev['low'] < level or prev2['low'] < level)
                reversed = current['close'] > level

                if swept and reversed:
                    # Base confidence for sweep + reversal
                    confidence = 0.70

                    # V5.1: CHoCH is optional bonus
                    choch_bonus = self.detect_choch_bonus(recent_5m, 'BUY')
                    confidence += choch_bonus

                    return ('BUY', level_name, current, confidence, choch_bonus > 0)

        # BEARISH SWEEP
        if market_structure in ["BEARISH", "NEUTRAL"]:
            for level_name in ['PDH', 'TOKYO_HIGH']:
                level = levels[level_name]

                swept = (prev['high'] > level or prev2['high'] > level)
                reversed = current['close'] < level

                if swept and reversed:
                    # Base confidence for sweep + reversal
                    confidence = 0.70

                    # V5.1: CHoCH is optional bonus
                    choch_bonus = self.detect_choch_bonus(recent_5m, 'SELL')
                    confidence += choch_bonus

                    return ('SELL', level_name, current, confidence, choch_bonus > 0)

        return None

    def is_priority_window(self, timestamp):
        """
        V5.1: Expanded windows from v5.0 kill zones

        Priority Windows (6 hours total):
        - London: 07:00-10:00 GMT (3 hours)
        - NY: 13:00-16:00 GMT (3 hours)

        Note: 13:00-15:00 (NY Open) is HIGHEST PRIORITY for London Low Sweep
        """
        hour = timestamp.hour

        # London Priority Window: 07:00-10:00 UTC
        if 7 <= hour < 10:
            return True, "LONDON"

        # NY Priority Window: 13:00-16:00 UTC
        if 13 <= hour < 16:
            # Mark 13:00-15:00 as highest priority
            if hour < 15:
                return True, "NY_PRIME"  # Highest probability
            return True, "NY"

        return False, "OUTSIDE"

    def generate_signal(self, candle_data, all_data, timestamp, index):
        """Generate trade signal based on Aurum Sniper v5.1 strategy"""

        # Check priority window
        in_window, session = self.is_priority_window(timestamp)
        if not in_window:
            return None

        # Check daily trade limit
        if self.trades_today >= MAX_TRADES_PER_DAY:
            return None

        # Calculate key levels
        levels = self.calculate_daily_levels(all_data['15m'], index)
        if not levels:
            return None

        # Calculate ATR
        atr = self.calculate_atr(all_data['4h'])
        if atr is None:
            return None

        # V5 ENHANCEMENT: Skip if volatility too high (ATR > $40)
        if atr > ATR_MAX_VOLATILITY:
            return None

        # Determine market structure
        market_structure = self.get_market_structure(all_data['1h'])

        # Detect liquidity sweep (CHoCH is optional bonus)
        sweep_result = self.detect_liquidity_sweep(
            all_data['15m'],
            all_data['5m'],
            index,
            levels,
            market_structure
        )
        if not sweep_result:
            return None

        trade_direction, level_name, rejection_candle, confidence, has_choch = sweep_result

        current_price = candle_data['close']
        risk_amount = self.balance * RISK_PER_TRADE

        # Calculate entry, SL, TP based on direction
        if trade_direction == 'BUY':
            # V5 ENHANCEMENT: SL = 1.5x ATR OR swing low (whichever FURTHER)
            atr_stop = current_price - (atr * ATR_MULTIPLIER)
            swing_stop = rejection_candle['low'] - 2.0

            sl = min(atr_stop, swing_stop)  # Use the FURTHER stop

            risk = current_price - sl
            tp = current_price + (risk * RISK_REWARD_RATIO)

            lot_size = risk_amount / (risk * 10)
            lot_size = max(0.01, round(lot_size, 2))

            if risk <= 0:
                return None

            reason_parts = [session, f"{level_name} Sweep", f"{int(confidence*100)}% Conf", market_structure]
            if has_choch:
                reason_parts.append("CHoCH✓")

            return {
                "decision": "BUY",
                "price": current_price,
                "sl": round(sl, 2),
                "tp": round(tp, 2),
                "lot_size": lot_size,
                "window": session,
                "reason": " | ".join(reason_parts),
                "level": level_name,
                "structure": market_structure,
                "atr": round(atr, 2),
                "has_choch": has_choch,
                "confidence": confidence
            }

        elif trade_direction == 'SELL':
            # V5 ENHANCEMENT: SL = 1.5x ATR OR swing high (whichever FURTHER)
            atr_stop = current_price + (atr * ATR_MULTIPLIER)
            swing_stop = rejection_candle['high'] + 2.0

            sl = max(atr_stop, swing_stop)  # Use the FURTHER stop

            risk = sl - current_price
            tp = current_price - (risk * RISK_REWARD_RATIO)

            lot_size = risk_amount / (risk * 10)
            lot_size = max(0.01, round(lot_size, 2))

            if risk <= 0:
                return None

            reason_parts = [session, f"{level_name} Sweep", f"{int(confidence*100)}% Conf", market_structure]
            if has_choch:
                reason_parts.append("CHoCH✓")

            return {
                "decision": "SELL",
                "price": current_price,
                "sl": round(sl, 2),
                "tp": round(tp, 2),
                "lot_size": lot_size,
                "window": session,
                "reason": " | ".join(reason_parts),
                "level": level_name,
                "structure": market_structure,
                "atr": round(atr, 2),
                "has_choch": has_choch,
                "confidence": confidence
            }

        return None

    def execute_trade(self, signal, timestamp):
        """Execute trade and track it"""
        trade = {
            "timestamp": timestamp,
            "decision": signal['decision'],
            "entry_price": signal['price'],
            "sl": signal['sl'],
            "tp": signal['tp'],
            "lot_size": signal['lot_size'],
            "window": signal['window'],
            "reason": signal['reason'],
            "level": signal['level'],
            "structure": signal['structure'],
            "atr": signal['atr'],
            "has_choch": signal['has_choch'],
            "confidence": signal['confidence'],
            "outcome": "OPEN",
            "exit_price": None,
            "exit_time": None,
            "pnl": 0,
            "breakeven_moved": False
        }

        self.trades.append(trade)
        self.trades_today += 1

        return trade

    def simulate_trade_outcome(self, trade, future_candles):
        """
        Simulate trade outcome with V5 enhancement: Breakeven at 1:1.5 RR
        """
        entry = trade['entry_price']
        sl = trade['sl']
        tp = trade['tp']
        lot_size = trade['lot_size']

        for candle in future_candles:
            high = candle['high']
            low = candle['low']

            if trade['decision'] == 'BUY':
                # V5 ENHANCEMENT: Move to breakeven at 1:1.5 RR
                if not trade['breakeven_moved']:
                    risk = entry - sl
                    if high >= entry + (risk * BREAKEVEN_TRIGGER):
                        sl = entry
                        trade['breakeven_moved'] = True

                # Check SL
                if low <= sl:
                    trade['outcome'] = 'BREAKEVEN' if trade['breakeven_moved'] else 'LOSS'
                    trade['exit_price'] = sl
                    trade['exit_time'] = candle['time']
                    price_diff = (sl - entry) if not trade['breakeven_moved'] else 0
                    trade['pnl'] = price_diff * lot_size * 10
                    self.balance += trade['pnl']
                    return

                # Check TP
                if high >= tp:
                    trade['outcome'] = 'WIN'
                    trade['exit_price'] = tp
                    trade['exit_time'] = candle['time']
                    price_diff = tp - entry
                    trade['pnl'] = price_diff * lot_size * 10
                    self.balance += trade['pnl']
                    return

            else:  # SELL
                # V5 ENHANCEMENT: Move to breakeven at 1:1.5 RR
                if not trade['breakeven_moved']:
                    risk = sl - entry
                    if low <= entry - (risk * BREAKEVEN_TRIGGER):
                        sl = entry
                        trade['breakeven_moved'] = True

                # Check SL
                if high >= sl:
                    trade['outcome'] = 'BREAKEVEN' if trade['breakeven_moved'] else 'LOSS'
                    trade['exit_price'] = sl
                    trade['exit_time'] = candle['time']
                    price_diff = (entry - sl) if not trade['breakeven_moved'] else 0
                    trade['pnl'] = price_diff * lot_size * 10 * -1
                    self.balance += trade['pnl']
                    return

                # Check TP
                if low <= tp:
                    trade['outcome'] = 'WIN'
                    trade['exit_price'] = tp
                    trade['exit_time'] = candle['time']
                    price_diff = entry - tp
                    trade['pnl'] = price_diff * lot_size * 10
                    self.balance += trade['pnl']
                    return

        # If neither hit
        trade['outcome'] = 'OPEN'

    async def run_backtest(self):
        """Main backtest simulation for Aurum Sniper v5.1"""
        print("="*80)
        print("🎯 AURUM SNIPER V5.1 - 60-DAY STATISTICAL VALIDATION")
        print("="*80)
        print("\n📅 TEST PERIOD: November 1 - December 27, 2025 (57 days)")
        print("\n📋 V5.1 ENHANCEMENTS (Balanced approach):")
        print("   ✓ Expanded Windows: London (07:00-10:00), NY (13:00-16:00) = 6h total")
        print("   ✓ CHoCH as Bonus: Optional confidence boost (not mandatory)")
        print("   ✓ ATR Volatility Cap: $40 max (v5 enhancement kept)")
        print("   ✓ Breakeven at 1:1.5 RR: Earlier protection (v5 enhancement kept)")
        print("   ✓ Stricter Stops: 1.5x ATR OR swing extreme (v5 enhancement kept)")
        print("   ✓ Max 4 trades/day: Quality focus with reasonable volume")
        print("\n🎯 TARGET: 30+ trades minimum for statistical significance")
        print("="*80 + "\n")

        data = await self.fetch_historical_data()

        print("🔍 Scanning for institutional setups...\n")

        candles_15m = data['15m']

        for i, candle in enumerate(candles_15m):
            timestamp = candle['time'] if isinstance(candle['time'], datetime) else datetime.fromtimestamp(candle['time'], tz=pytz.utc)

            current_data = {
                '5m': [c for c in data['5m'] if c['time'] <= candle['time']],
                '15m': candles_15m[:i+1],
                '1h': [c for c in data['1h'] if c['time'] <= candle['time']],
                '4h': [c for c in data['4h'] if c['time'] <= candle['time']]
            }

            if len(current_data['15m']) < 100:
                continue

            signal = self.generate_signal(candle, current_data, timestamp, i)

            if signal:
                trade = self.execute_trade(signal, timestamp)

                print(f"🎯 TRADE #{len(self.trades)}")
                print(f"   Time: {timestamp.strftime('%Y-%m-%d %H:%M UTC')}")
                print(f"   Direction: {signal['decision']}")
                print(f"   Entry: ${signal['price']:.2f} | SL: ${signal['sl']:.2f} | TP: ${signal['tp']:.2f}")
                print(f"   Lot Size: {signal['lot_size']} (1% risk = ${self.balance * RISK_PER_TRADE:.2f})")
                print(f"   Reason: {signal['reason']}")
                print(f"   ATR: ${signal['atr']:.2f}")

                # Simulate outcome
                future_candles = candles_15m[i+1:]
                self.simulate_trade_outcome(trade, future_candles)

                if trade['outcome'] in ['WIN', 'LOSS', 'BREAKEVEN']:
                    outcome_emoji = "✅" if trade['outcome'] == 'WIN' else ("🟰" if trade['outcome'] == 'BREAKEVEN' else "❌")
                    print(f"   {outcome_emoji} {trade['outcome']}: ${trade['pnl']:+,.2f}")
                    exit_time = trade['exit_time'] if isinstance(trade['exit_time'], datetime) else datetime.fromtimestamp(trade['exit_time'], tz=pytz.utc)
                    print(f"   Exit: ${trade['exit_price']:.2f} @ {exit_time.strftime('%Y-%m-%d %H:%M UTC')}")
                    if trade['breakeven_moved']:
                        print(f"   🛡️ Breakeven Protection Activated (1:1.5 RR)")
                    print(f"   New Balance: ${self.balance:,.2f}\n")

        # Generate report
        self.generate_report()

    def generate_report(self):
        """Generate detailed backtest report"""
        print("\n" + "="*80)
        print("📊 AURUM SNIPER V5.1 - BACKTEST RESULTS")
        print("="*80)

        total_trades = len(self.trades)
        if total_trades == 0:
            print("\n⚠️ No trades generated. Strategy too conservative.")
            return

        wins = [t for t in self.trades if t['outcome'] == 'WIN']
        losses = [t for t in self.trades if t['outcome'] == 'LOSS']
        breakevens = [t for t in self.trades if t['outcome'] == 'BREAKEVEN']
        open_trades = [t for t in self.trades if t['outcome'] == 'OPEN']

        win_rate = (len(wins) / total_trades * 100) if total_trades > 0 else 0
        total_pnl = sum(t['pnl'] for t in self.trades)
        roi = (total_pnl / INITIAL_BALANCE) * 100

        print(f"\n💰 FINANCIAL PERFORMANCE")
        print(f"   Starting Balance: ${INITIAL_BALANCE:,.2f}")
        print(f"   Ending Balance: ${self.balance:,.2f}")
        print(f"   Total P&L: ${total_pnl:+,.2f}")
        print(f"   ROI: {roi:+.2f}%")

        print(f"\n📈 TRADE STATISTICS")
        print(f"   Total Trades: {total_trades}")
        print(f"   Wins: {len(wins)} ({len(wins)/total_trades*100:.1f}%)")
        print(f"   Losses: {len(losses)} ({len(losses)/total_trades*100:.1f}%)")
        print(f"   Breakevens: {len(breakevens)} ({len(breakevens)/total_trades*100:.1f}%)")
        print(f"   Open: {len(open_trades)} ({len(open_trades)/total_trades*100:.1f}%)")
        print(f"   Win Rate: {win_rate:.1f}%")

        if wins:
            avg_win = sum(t['pnl'] for t in wins) / len(wins)
            print(f"   Average Win: ${avg_win:,.2f}")

        if losses:
            avg_loss = sum(t['pnl'] for t in losses) / len(losses)
            print(f"   Average Loss: ${avg_loss:,.2f}")

        # CHoCH analysis
        trades_with_choch = [t for t in self.trades if t['has_choch']]
        trades_without_choch = [t for t in self.trades if not t['has_choch']]

        print(f"\n🔍 CHoCH CONFIRMATION ANALYSIS")
        if trades_with_choch:
            choch_wins = len([t for t in trades_with_choch if t['outcome'] == 'WIN'])
            print(f"   With CHoCH: {len(trades_with_choch)} trades, {choch_wins} wins ({choch_wins/len(trades_with_choch)*100:.1f}% WR)")

        if trades_without_choch:
            no_choch_wins = len([t for t in trades_without_choch if t['outcome'] == 'WIN'])
            print(f"   Without CHoCH: {len(trades_without_choch)} trades, {no_choch_wins} wins ({no_choch_wins/len(trades_without_choch)*100:.1f}% WR)")

        # Breakeven protection stats
        be_saves = len([t for t in self.trades if t['breakeven_moved']])
        print(f"\n🛡️ BREAKEVEN PROTECTION (V5 Enhancement)")
        print(f"   Trades Protected: {be_saves} ({be_saves/total_trades*100:.1f}% of total)")
        print(f"   Protection Trigger: 1:1.5 RR")

        # Window performance
        print(f"\n⏰ TRADING WINDOW PERFORMANCE")
        for window in ['LONDON', 'NY_PRIME', 'NY']:
            window_trades = [t for t in self.trades if window in t['window']]
            if window_trades:
                window_wins = len([t for t in window_trades if t['outcome'] == 'WIN'])
                print(f"   {window}: {len(window_trades)} trades, {window_wins} wins ({window_wins/len(window_trades)*100:.1f}% WR)")

        # Level performance
        print(f"\n📍 LIQUIDITY LEVEL PERFORMANCE")
        for level_name in ['PDH', 'PDL', 'TOKYO_HIGH', 'TOKYO_LOW']:
            level_trades = [t for t in self.trades if t['level'] == level_name]
            if level_trades:
                level_wins = len([t for t in level_trades if t['outcome'] == 'WIN'])
                print(f"   {level_name}: {len(level_trades)} trades, {level_wins} wins ({level_wins/len(level_trades)*100:.1f}% WR)")

        # Structure performance
        print(f"\n📊 MARKET STRUCTURE PERFORMANCE")
        for structure in ['BULLISH', 'BEARISH', 'NEUTRAL']:
            struct_trades = [t for t in self.trades if t['structure'] == structure]
            if struct_trades:
                struct_wins = len([t for t in struct_trades if t['outcome'] == 'WIN'])
                print(f"   {structure}: {len(struct_trades)} trades, {struct_wins} wins ({struct_wins/len(struct_trades)*100:.1f}% WR)")

        print(f"\n🔧 OPERATIONAL STATS")
        print(f"   API Requests: {self.api_requests}")
        print(f"   Max Trades/Day: {MAX_TRADES_PER_DAY}")
        print(f"   ATR Volatility Cap: ${ATR_MAX_VOLATILITY}")
        print(f"   Breakeven Trigger: {BREAKEVEN_TRIGGER}:1 RR")

        print("\n" + "="*80)

        # Expected Value calculation
        if wins and losses:
            print(f"\n📐 MATHEMATICAL VALIDATION")
            print(f"   Break-even Win Rate (1:3 RR): 25%")
            print(f"   Actual Win Rate: {win_rate:.1f}%")
            print(f"   Surplus: {win_rate - 25:.1f}%")

            avg_win = sum(t['pnl'] for t in wins) / len(wins)
            avg_loss = sum(t['pnl'] for t in losses) / len(losses)
            ev = (len(wins)/total_trades * avg_win) - (len(losses)/total_trades * abs(avg_loss))
            print(f"   Expected Value per Trade: ${ev:+,.2f}")

            if ev > 0:
                monthly_projection = ev * 60  # Assume 2 trades/day * 30 days
                print(f"   Projected Monthly (60 trades): ${monthly_projection:+,.2f} ({monthly_projection/INITIAL_BALANCE*100:+.1f}% ROI)")

        print("\n" + "="*80 + "\n")

async def main():
    backtest = AurumSniperV5_1()
    await backtest.run_backtest()

if __name__ == "__main__":
    asyncio.run(main())
