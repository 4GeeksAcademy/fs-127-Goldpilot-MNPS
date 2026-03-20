"""
XAUUSD Aurum Liquidity Sniper Strategy Backtest - December 2025
Focus: Liquidity Sweeps at Key Levels with ATR-Based Risk Management
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
MAX_TRADES_PER_DAY = 4  # Increased for more opportunities

class LiquiditySniperBacktest:
    def __init__(self):
        self.balance = INITIAL_BALANCE
        self.trades = []
        self.api_requests = 0
        self.trades_today = 0
        self.current_date = None
        self.daily_levels = {}  # Store PDH/PDL/Tokyo levels

    async def fetch_historical_data(self):
        """Fetch December 2025 historical candles"""
        print("🔄 Connecting to MetaAPI...")

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

        print("✅ Connected! Fetching December 2025 data...")

        # December 1-27, 2025
        start_date = datetime(2025, 12, 1, 0, 0, 0, tzinfo=pytz.utc)

        print("📊 Fetching 15-minute candles...")
        candles_15m = await account.get_historical_candles('GOLD.pro', '15m', start_date, 2600)
        self.api_requests += 1

        print("📊 Fetching 1-hour candles...")
        candles_1h = await account.get_historical_candles('GOLD.pro', '1h', start_date, 650)
        self.api_requests += 1

        print("📊 Fetching 4-hour candles...")
        candles_4h = await account.get_historical_candles('GOLD.pro', '4h', start_date, 200)
        self.api_requests += 1

        print("📊 Fetching daily candles...")
        candles_1d = await account.get_historical_candles('GOLD.pro', '1d', start_date, 30)
        self.api_requests += 1

        print("📊 Fetching EURUSD daily candles...")
        eurusd_1d = await account.get_historical_candles('EURUSD', '1d', start_date, 30)
        self.api_requests += 1

        print(f"✅ Data fetched: {len(candles_15m)} 15m, {len(candles_1h)} 1h, {len(candles_4h)} 4h candles")

        await connection.close()

        return {
            '15m': candles_15m,
            '1h': candles_1h,
            '4h': candles_4h,
            '1d': candles_1d,
            'eurusd_1d': eurusd_1d
        }

    def calculate_atr(self, candles_4h, period=14):
        """Calculate Average True Range for stop loss sizing"""
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

    def get_market_structure(self, candles_1h):
        """Determine market structure: BULLISH (Higher Highs) or BEARISH (Lower Lows)"""
        if len(candles_1h) < 20:
            return "NEUTRAL"

        recent = candles_1h[-20:]
        highs = [c['high'] for c in recent]
        lows = [c['low'] for c in recent]

        # Check for Higher Highs (HH)
        recent_high = max(highs[-5:])
        previous_high = max(highs[-15:-5])

        # Check for Lower Lows (LL)
        recent_low = min(lows[-5:])
        previous_low = min(lows[-15:-5])

        if recent_high > previous_high and recent_low >= previous_low:
            return "BULLISH"  # Making Higher Highs
        elif recent_low < previous_low and recent_high <= previous_high:
            return "BEARISH"  # Making Lower Lows
        else:
            return "NEUTRAL"

    def calculate_daily_levels(self, candles_15m, current_index):
        """Calculate PDH/PDL and Tokyo High/Low for liquidity sweep detection"""
        current_candle = candles_15m[current_index]
        current_time = current_candle['time']
        current_date = current_time.date()

        # Check if we need to recalculate levels (new day)
        if self.current_date != current_date:
            self.current_date = current_date
            self.trades_today = 0  # Reset daily trade count

            # Find previous day's candles
            previous_day = current_date - timedelta(days=1)
            prev_day_candles = [c for c in candles_15m[:current_index]
                               if c['time'].date() == previous_day]

            if prev_day_candles:
                pdh = max(c['high'] for c in prev_day_candles)
                pdl = min(c['low'] for c in prev_day_candles)
            else:
                # Use recent highs/lows if previous day not available
                recent = candles_15m[max(0, current_index-96):current_index]  # ~24h of 15m candles
                pdh = max(c['high'] for c in recent) if recent else current_candle['high']
                pdl = min(c['low'] for c in recent) if recent else current_candle['low']

            # Find Tokyo session (23:00-08:00 UTC) candles from today
            tokyo_candles = [c for c in candles_15m[:current_index]
                           if c['time'].date() == current_date and
                           (c['time'].hour >= 23 or c['time'].hour < 8)]

            if tokyo_candles:
                tokyo_high = max(c['high'] for c in tokyo_candles)
                tokyo_low = min(c['low'] for c in tokyo_candles)
            else:
                tokyo_high = pdh
                tokyo_low = pdl

            self.daily_levels = {
                'PDH': pdh,
                'PDL': pdl,
                'TOKYO_HIGH': tokyo_high,
                'TOKYO_LOW': tokyo_low
            }

        return self.daily_levels

    def detect_liquidity_sweep(self, candles_15m, current_index, levels, market_structure):
        """
        Detect liquidity sweep: Price breaks a key level then reverses back inside range
        Returns: ('BUY'/'SELL', level_name, rejection_candle) or None
        """
        if current_index < 3:
            return None

        current = candles_15m[current_index]
        prev = candles_15m[current_index - 1]
        prev2 = candles_15m[current_index - 2]

        # BULLISH SWEEP: Price sweeps below PDL/Tokyo Low then reverses up
        # Allow in BULLISH or NEUTRAL structure
        if market_structure in ["BULLISH", "NEUTRAL"]:
            for level_name in ['PDL', 'TOKYO_LOW']:
                level = levels[level_name]

                # Check if ANY of the last 2 candles broke below level
                # and current candle closed back above
                swept = (prev['low'] < level or prev2['low'] < level)
                reversed = current['close'] > level

                if swept and reversed:
                    # Rejection candle: Bullish Pin Bar or Engulfing (relaxed)
                    if self.is_bullish_rejection(current, prev):
                        return ('BUY', level_name, current)
                    # Also accept simple bullish close
                    elif current['close'] > current['open']:
                        return ('BUY', level_name, current)

        # BEARISH SWEEP: Price sweeps above PDH/Tokyo High then reverses down
        # Allow in BEARISH or NEUTRAL structure
        if market_structure in ["BEARISH", "NEUTRAL"]:
            for level_name in ['PDH', 'TOKYO_HIGH']:
                level = levels[level_name]

                # Check if ANY of the last 2 candles broke above level
                # and current candle closed back below
                swept = (prev['high'] > level or prev2['high'] > level)
                reversed = current['close'] < level

                if swept and reversed:
                    # Rejection candle: Bearish Pin Bar or Engulfing (relaxed)
                    if self.is_bearish_rejection(current, prev):
                        return ('SELL', level_name, current)
                    # Also accept simple bearish close
                    elif current['close'] < current['open']:
                        return ('SELL', level_name, current)

        return None

    def is_bullish_rejection(self, current, prev):
        """Check if current candle is a bullish rejection (Pin Bar or Engulfing)"""
        c_body = abs(current['close'] - current['open'])
        c_range = current['high'] - current['low']
        c_lower_wick = min(current['open'], current['close']) - current['low']

        # Bullish Pin Bar: Long lower wick, small body
        if c_lower_wick > c_range * 0.6 and c_body < c_range * 0.3:
            return True

        # Bullish Engulfing
        if (prev['close'] < prev['open'] and
            current['close'] > current['open'] and
            current['open'] < prev['close'] and
            current['close'] > prev['open']):
            return True

        return False

    def is_bearish_rejection(self, current, prev):
        """Check if current candle is a bearish rejection (Pin Bar or Engulfing)"""
        c_body = abs(current['close'] - current['open'])
        c_range = current['high'] - current['low']
        c_upper_wick = current['high'] - max(current['open'], current['close'])

        # Bearish Pin Bar: Long upper wick, small body
        if c_upper_wick > c_range * 0.6 and c_body < c_range * 0.3:
            return True

        # Bearish Engulfing
        if (prev['close'] > prev['open'] and
            current['close'] < current['open'] and
            current['open'] > prev['close'] and
            current['close'] < prev['open']):
            return True

        return False

    def check_eurusd_confirmation(self, eurusd_candles, trade_direction):
        """Check EURUSD is not moving aggressively against our trade"""
        if len(eurusd_candles) < 2:
            return True

        latest = eurusd_candles[-1]
        prev = eurusd_candles[-2]

        eur_change = ((latest['close'] - prev['close']) / prev['close']) * 100

        # If EURUSD is moving strongly opposite to Gold trade, reject
        if trade_direction == 'BUY' and eur_change < -0.5:  # EUR falling strongly
            return False
        if trade_direction == 'SELL' and eur_change > 0.5:  # EUR rising strongly
            return False

        return True

    def is_trading_window(self, timestamp):
        """Check if within London or NY sessions (expanded for more opportunities)"""
        hour = timestamp.hour

        # London Session: 07:00-16:00 UTC (expanded)
        if 7 <= hour < 16:
            return True, "LONDON"

        # NY Session: 13:00-21:00 UTC (expanded)
        if 13 <= hour < 21:
            return True, "NY"

        return False, "CLOSED"

    def generate_signal(self, candle_data, all_data, timestamp, index):
        """Generate trade signal based on Liquidity Sniper strategy"""

        # Check trading window
        in_window, session = self.is_trading_window(timestamp)
        if not in_window:
            return None

        # Check daily trade limit
        if self.trades_today >= MAX_TRADES_PER_DAY:
            return None

        # Calculate key levels
        levels = self.calculate_daily_levels(all_data['15m'], index)

        # Determine market structure (allow NEUTRAL now)
        market_structure = self.get_market_structure(all_data['1h'])

        # Detect liquidity sweep
        sweep_result = self.detect_liquidity_sweep(all_data['15m'], index, levels, market_structure)
        if not sweep_result:
            return None

        trade_direction, level_name, rejection_candle = sweep_result

        # REMOVED: EURUSD confirmation filter - trade purely on Gold levels

        # Calculate ATR for stop loss
        atr = self.calculate_atr(all_data['4h'])
        if atr is None:
            return None

        current_price = candle_data['close']

        # Calculate position size based on 1% risk
        risk_amount = self.balance * RISK_PER_TRADE

        if trade_direction == 'BUY':
            # Stop Loss: 1.5x ATR OR rejection candle low + $2
            atr_stop = current_price - (atr * ATR_MULTIPLIER)
            candle_stop = rejection_candle['low'] - 2.0
            sl = max(atr_stop, candle_stop)  # Use the tighter stop

            risk = current_price - sl
            tp = current_price + (risk * RISK_REWARD_RATIO)  # 1:3 RR

            # Calculate lot size based on risk
            # For Gold: 0.01 lots = $0.10 per $1 move
            # Formula: lot_size = risk_amount / (risk_in_dollars * 10)
            lot_size = risk_amount / (risk * 10)
            lot_size = max(0.01, round(lot_size, 2))  # Minimum 0.01 lots

            if risk <= 0:
                return None

            return {
                "decision": "BUY",
                "price": current_price,
                "sl": round(sl, 2),
                "tp": round(tp, 2),
                "lot_size": lot_size,
                "risk": round(risk, 2),
                "atr": round(atr, 2),
                "window": session,
                "level": level_name,
                "structure": market_structure,
                "reason": f"{session} | {market_structure} Structure | Sweep {level_name} | ATR: ${atr:.1f}"
            }

        else:  # SELL
            # Stop Loss: 1.5x ATR OR rejection candle high + $2
            atr_stop = current_price + (atr * ATR_MULTIPLIER)
            candle_stop = rejection_candle['high'] + 2.0
            sl = min(atr_stop, candle_stop)  # Use the tighter stop

            risk = sl - current_price
            tp = current_price - (risk * RISK_REWARD_RATIO)  # 1:3 RR

            # Calculate lot size based on risk
            # For Gold: 0.01 lots = $0.10 per $1 move
            lot_size = risk_amount / (risk * 10)
            lot_size = max(0.01, round(lot_size, 2))  # Minimum 0.01 lots

            if risk <= 0:
                return None

            return {
                "decision": "SELL",
                "price": current_price,
                "sl": round(sl, 2),
                "tp": round(tp, 2),
                "lot_size": lot_size,
                "risk": round(risk, 2),
                "atr": round(atr, 2),
                "window": session,
                "level": level_name,
                "structure": market_structure,
                "reason": f"{session} | {market_structure} Structure | Sweep {level_name} | ATR: ${atr:.1f}"
            }

    def execute_trade(self, signal, timestamp):
        """Execute trade and track it"""
        self.trades_today += 1

        trade = {
            "timestamp": timestamp,
            "decision": signal['decision'],
            "entry_price": signal['price'],
            "sl": signal['sl'],
            "tp": signal['tp'],
            "lot_size": signal['lot_size'],
            "risk": signal['risk'],
            "atr": signal['atr'],
            "window": signal['window'],
            "level": signal['level'],
            "structure": signal['structure'],
            "reason": signal['reason'],
            "outcome": None,
            "exit_price": None,
            "exit_time": None,
            "pnl": 0,
            "breakeven_moved": False
        }

        self.trades.append(trade)
        return trade

    def simulate_trade_outcome(self, trade, future_candles):
        """Simulate trade outcome with 1:1 breakeven move"""
        if not future_candles:
            trade['outcome'] = 'OPEN'
            return

        entry = trade['entry_price']
        sl = trade['sl']
        tp = trade['tp']
        lot_size = trade['lot_size']

        for candle in future_candles:
            high = candle['high']
            low = candle['low']

            if trade['decision'] == 'BUY':
                # Check if 1:1 hit (move SL to breakeven)
                if not trade['breakeven_moved']:
                    risk = entry - sl
                    if high >= entry + risk:  # 1:1 hit
                        sl = entry  # Move SL to breakeven
                        trade['breakeven_moved'] = True

                # Check if SL hit
                if low <= sl:
                    trade['outcome'] = 'BREAKEVEN' if trade['breakeven_moved'] else 'LOSS'
                    trade['exit_price'] = sl
                    trade['exit_time'] = candle['time']
                    price_diff = (sl - entry) if not trade['breakeven_moved'] else 0
                    # P&L = price_diff * lot_size * 10 (Gold: 0.01 lot = $0.10 per $1)
                    trade['pnl'] = price_diff * lot_size * 10
                    self.balance += trade['pnl']
                    return

                # Check if TP hit
                if high >= tp:
                    trade['outcome'] = 'WIN'
                    trade['exit_price'] = tp
                    trade['exit_time'] = candle['time']
                    price_diff = tp - entry
                    trade['pnl'] = price_diff * lot_size * 10
                    self.balance += trade['pnl']
                    return

            else:  # SELL
                # Check if 1:1 hit (move SL to breakeven)
                if not trade['breakeven_moved']:
                    risk = sl - entry
                    if low <= entry - risk:  # 1:1 hit
                        sl = entry
                        trade['breakeven_moved'] = True

                # Check if SL hit
                if high >= sl:
                    trade['outcome'] = 'BREAKEVEN' if trade['breakeven_moved'] else 'LOSS'
                    trade['exit_price'] = sl
                    trade['exit_time'] = candle['time']
                    price_diff = (entry - sl) if not trade['breakeven_moved'] else 0
                    trade['pnl'] = price_diff * lot_size * 10 * -1  # Negative for loss
                    self.balance += trade['pnl']
                    return

                # Check if TP hit
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
        """Main backtest simulation"""
        print("\n" + "="*70)
        print("🎯 AURUM LIQUIDITY SNIPER BACKTEST - DECEMBER 2025")
        print("="*70)
        print(f"Initial Balance: ${INITIAL_BALANCE:,.2f}")
        print(f"Risk Per Trade: {RISK_PER_TRADE*100}%")
        print(f"Risk:Reward: 1:{RISK_REWARD_RATIO}")
        print(f"Stop Loss: {ATR_MULTIPLIER}x ATR (Dynamic)")
        print(f"Max Trades/Day: {MAX_TRADES_PER_DAY}")
        print(f"Strategy: Liquidity Sweeps at PDH/PDL/Tokyo Levels")
        print("="*70 + "\n")

        # Fetch data
        data = await self.fetch_historical_data()

        print("\n🔍 Scanning for liquidity sweeps...\n")

        candles_15m = data['15m']

        for i, candle in enumerate(candles_15m):
            timestamp = candle['time'] if isinstance(candle['time'], datetime) else datetime.fromtimestamp(candle['time'], tz=pytz.utc)

            # Get data up to current candle
            current_data = {
                '15m': candles_15m[:i+1],
                '1h': [c for c in data['1h'] if c['time'] <= candle['time']],
                '4h': [c for c in data['4h'] if c['time'] <= candle['time']],
                '1d': [c for c in data['1d'] if c['time'] <= candle['time']],
                'eurusd_1d': [c for c in data['eurusd_1d'] if c['time'] <= candle['time']]
            }

            # Generate signal
            signal = self.generate_signal(candle, current_data, timestamp, i)

            if signal:
                trade = self.execute_trade(signal, timestamp)
                print(f"🎯 TRADE #{len(self.trades)}")
                print(f"   Time: {timestamp.strftime('%Y-%m-%d %H:%M UTC')}")
                print(f"   Signal: {signal['decision']} @ ${signal['price']:.2f}")
                print(f"   SL: ${signal['sl']:.2f} | TP: ${signal['tp']:.2f} | RR: 1:{RISK_REWARD_RATIO}")
                print(f"   Lot Size: {signal['lot_size']} (Risk: ${signal['risk']:.2f} | ATR: ${signal['atr']:.2f})")
                print(f"   Level: {signal['level']} Sweep | Structure: {signal['structure']}")
                print(f"   Window: {signal['window']}\n")

                # Simulate outcome
                future_candles = candles_15m[i+1:]
                self.simulate_trade_outcome(trade, future_candles)

                if trade['outcome'] in ['WIN', 'LOSS', 'BREAKEVEN']:
                    outcome_emoji = {"WIN": "✅", "LOSS": "❌", "BREAKEVEN": "➖"}[trade['outcome']]
                    print(f"   {outcome_emoji} {trade['outcome']}: ${trade['pnl']:+,.2f}")
                    if trade['breakeven_moved']:
                        print(f"   🔒 SL moved to Breakeven after 1:1")
                    exit_time = trade['exit_time'] if isinstance(trade['exit_time'], datetime) else datetime.fromtimestamp(trade['exit_time'], tz=pytz.utc)
                    print(f"   Exit: ${trade['exit_price']:.2f} @ {exit_time.strftime('%Y-%m-%d %H:%M UTC')}")
                    print(f"   New Balance: ${self.balance:,.2f}\n")

        # Generate report
        self.generate_report()

    def generate_report(self):
        """Generate detailed backtest report"""
        print("\n" + "="*70)
        print("📊 LIQUIDITY SNIPER BACKTEST RESULTS")
        print("="*70)

        total_trades = len(self.trades)
        wins = [t for t in self.trades if t['outcome'] == 'WIN']
        losses = [t for t in self.trades if t['outcome'] == 'LOSS']
        breakevens = [t for t in self.trades if t['outcome'] == 'BREAKEVEN']
        open_trades = [t for t in self.trades if t['outcome'] == 'OPEN']

        win_rate = (len(wins) / total_trades * 100) if total_trades > 0 else 0

        total_pnl = sum(t['pnl'] for t in self.trades)
        final_balance = self.balance
        roi = ((final_balance - INITIAL_BALANCE) / INITIAL_BALANCE) * 100

        print(f"\n📈 PERFORMANCE METRICS")
        print(f"   Total Trades: {total_trades}")
        print(f"   Wins: {len(wins)} ({win_rate:.1f}%)")
        print(f"   Losses: {len(losses)} ({(len(losses)/total_trades*100) if total_trades > 0 else 0:.1f}%)")
        print(f"   Breakevens: {len(breakevens)} ({(len(breakevens)/total_trades*100) if total_trades > 0 else 0:.1f}%)")
        print(f"   Open: {len(open_trades)}")

        print(f"\n💰 FINANCIAL RESULTS")
        print(f"   Initial Balance: ${INITIAL_BALANCE:,.2f}")
        print(f"   Final Balance: ${final_balance:,.2f}")
        print(f"   Total P&L: ${total_pnl:+,.2f}")
        print(f"   ROI: {roi:+.2f}%")

        if wins:
            avg_win = sum(t['pnl'] for t in wins) / len(wins)
            print(f"   Average Win: ${avg_win:,.2f}")

        if losses:
            avg_loss = sum(t['pnl'] for t in losses) / len(losses)
            print(f"   Average Loss: ${avg_loss:,.2f}")

        print(f"\n🔧 STRATEGY STATS")
        print(f"   Risk Per Trade: {RISK_PER_TRADE*100}%")
        print(f"   Risk:Reward: 1:{RISK_REWARD_RATIO}")
        print(f"   Stop Loss Method: {ATR_MULTIPLIER}x ATR (Dynamic)")
        print(f"   Max Trades/Day: {MAX_TRADES_PER_DAY}")
        print(f"   Breakeven Protection: Enabled (at 1:1 RR)")

        print("\n" + "="*70)

        # Trade log
        if total_trades > 0:
            print("\n📋 TRADE LOG")
            print("="*70)
            for i, trade in enumerate(self.trades, 1):
                outcome_emoji = {"WIN": "✅", "LOSS": "❌", "BREAKEVEN": "➖", "OPEN": "⏳"}[trade['outcome']]
                be_indicator = " 🔒" if trade['breakeven_moved'] else ""
                print(f"\n{i}. {outcome_emoji}{be_indicator} {trade['decision']} @ ${trade['entry_price']:.2f}")
                print(f"   {trade['timestamp'].strftime('%Y-%m-%d %H:%M UTC')} | {trade['window']}")
                print(f"   SL: ${trade['sl']:.2f} | TP: ${trade['tp']:.2f} | Lot: {trade['lot_size']}")
                print(f"   {trade['reason']}")
                if trade['outcome'] != 'OPEN':
                    print(f"   Exit: ${trade['exit_price']:.2f} | P&L: ${trade['pnl']:+,.2f}")
            print("="*70)

async def main():
    backtest = LiquiditySniperBacktest()
    await backtest.run_backtest()

if __name__ == "__main__":
    asyncio.run(main())
