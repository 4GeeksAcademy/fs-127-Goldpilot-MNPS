"""
XAUUSD Golden Triad Strategy Backtest - December 2025
Simulates trading strategy on real historical market data
"""

import asyncio
from datetime import datetime, timedelta
import pytz
from metaapi_cloud_sdk import MetaApi
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
META_API_TOKEN = os.getenv('METAAPI_TOKEN')  # Match .env variable name
ACCOUNT_ID = os.getenv('METAAPI_ACCOUNT_ID', '436348e0-be6e-49cc-a991-8895903e5288')
INITIAL_BALANCE = 10000  # Starting balance for simulation
LOT_SIZE = 0.01  # Same as live trading

# Strategy parameters (matching live bot - OPTIMIZED)
API_LIMIT_PER_DAY = 1500
COOLDOWN_MINUTES = 60  # Updated to 60 minutes (1 hour) for quality over quantity

class DecemberBacktest:
    def __init__(self):
        self.balance = INITIAL_BALANCE
        self.trades = []
        self.api_requests = 0
        self.last_trade_time = None

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

        # Use historical market data API instead of RPC connection
        connection = account.get_streaming_connection()
        await connection.connect()
        await connection.wait_synchronized()

        print("✅ Connected! Fetching December 2025 data...")

        # December 1-27, 2025 (up to today)
        start_date = datetime(2025, 12, 1, 0, 0, 0, tzinfo=pytz.utc)

        # Calculate number of candles needed
        # 27 days * 24 hours * 4 (15m candles per hour) = ~2600 candles
        # 27 days * 6 (4h candles per day) = ~162 candles
        # 27 days = 27 daily candles

        # Fetch different timeframes using historical market data API (use Oanda's symbol "GOLD.pro")
        print("📊 Fetching 15-minute candles...")
        candles_15m = await account.get_historical_candles('GOLD.pro', '15m', start_date, 2600)
        self.api_requests += 1

        print("📊 Fetching 4-hour candles...")
        candles_4h = await account.get_historical_candles('GOLD.pro', '4h', start_date, 200)
        self.api_requests += 1

        print("📊 Fetching daily candles...")
        candles_1d = await account.get_historical_candles('GOLD.pro', '1d', start_date, 30)
        self.api_requests += 1

        # Fetch EURUSD for correlation analysis
        print("📊 Fetching EURUSD daily candles...")
        eurusd_1d = await account.get_historical_candles('EURUSD', '1d', start_date, 30)
        self.api_requests += 1

        print(f"✅ Data fetched: {len(candles_15m)} 15m candles, {len(candles_4h)} 4h candles, {len(candles_1d)} daily candles")

        await connection.close()

        return {
            '15m': candles_15m,
            '4h': candles_4h,
            '1d': candles_1d,
            'eurusd_1d': eurusd_1d
        }

    def calculate_eurusd_correlation(self, eurusd_candles):
        """Analyze EURUSD trend (Layer 1)"""
        if len(eurusd_candles) < 5:
            return "NEUTRAL", "Insufficient data"

        recent = eurusd_candles[-5:]
        closes = [c['close'] for c in recent]

        # Simple trend detection
        if closes[-1] > closes[0]:
            momentum = ((closes[-1] - closes[0]) / closes[0]) * 100
            if momentum > 0.5:
                return "STRONG_BULLISH", f"EUR up {momentum:.2f}% → XAU likely bullish"
            return "BULLISH", f"EUR up {momentum:.2f}% → XAU may rise"
        else:
            momentum = ((closes[0] - closes[-1]) / closes[0]) * 100
            if momentum > 0.5:
                return "STRONG_BEARISH", f"EUR down {momentum:.2f}% → XAU likely bearish"
            return "BEARISH", f"EUR down {momentum:.2f}% → XAU may fall"

    def analyze_daily_structure(self, daily_candles):
        """Analyze daily timeframe (Layer 2)"""
        if len(daily_candles) < 10:
            return None

        recent = daily_candles[-10:]
        closes = [c['close'] for c in recent]
        highs = [c['high'] for c in recent]
        lows = [c['low'] for c in recent]

        current = recent[-1]['close']
        swing_high = max(highs[-5:])
        swing_low = min(lows[-5:])

        # Check for higher highs / lower lows
        if current > swing_high * 0.998:
            return {"trend": "BULLISH", "reason": "Breaking daily swing high"}
        elif current < swing_low * 1.002:
            return {"trend": "BEARISH", "reason": "Breaking daily swing low"}

        return {"trend": "NEUTRAL", "reason": "No clear daily bias"}

    def analyze_4h_structure(self, candles_4h):
        """Analyze 4H breaks of structure (Layer 3)"""
        if len(candles_4h) < 20:
            return None

        recent = candles_4h[-20:]
        highs = [c['high'] for c in recent]
        lows = [c['low'] for c in recent]

        current = recent[-1]['close']
        recent_high = max(highs[-5:])
        recent_low = min(lows[-5:])

        # Break of structure detection
        if current > recent_high * 0.999:
            momentum = ((current - recent_low) / recent_low) * 100
            return {"bos": "BULLISH", "momentum": momentum, "reason": "4H BOS to upside"}
        elif current < recent_low * 1.001:
            momentum = ((recent_high - current) / current) * 100
            return {"bos": "BEARISH", "momentum": momentum, "reason": "4H BOS to downside"}

        return {"bos": "NEUTRAL", "momentum": 0, "reason": "No 4H BOS"}

    def calculate_golden_pocket(self, candles_4h):
        """Calculate Fibonacci golden pocket entry (0.618 - 0.65)"""
        if len(candles_4h) < 10:
            return None

        recent = candles_4h[-10:]
        highs = [c['high'] for c in recent]
        lows = [c['low'] for c in recent]

        swing_high = max(highs)
        swing_low = min(lows)

        range_size = swing_high - swing_low
        fib_618 = swing_high - (range_size * 0.618)
        fib_65 = swing_high - (range_size * 0.65)

        return {
            "high": swing_high,
            "low": swing_low,
            "fib_618": fib_618,
            "fib_65": fib_65,
            "pocket_mid": (fib_618 + fib_65) / 2
        }

    def check_market_timing(self, timestamp):
        """Check if market is actively trading (expanded windows)"""
        hour = timestamp.hour

        # Tokyo Session: 23:00-08:00 UTC
        if 23 <= hour or hour < 8:
            return True, "TOKYO"

        # London Session: 07:00-16:00 UTC
        if 7 <= hour < 16:
            return True, "LONDON"

        # NY Session: 12:00-21:00 UTC
        if 12 <= hour < 21:
            return True, "NY"

        return False, "LOW_LIQUIDITY"

    def check_trade_cooldown(self, current_time):
        """Ensure 30-minute cooldown between trades"""
        if self.last_trade_time is None:
            return True

        time_diff = (current_time - self.last_trade_time).total_seconds()
        return time_diff >= (COOLDOWN_MINUTES * 60)

    def detect_price_action_signal(self, candles_15m):
        """Detect bullish/bearish price action patterns on 15m chart"""
        if len(candles_15m) < 3:
            return None

        # Get last 3 candles
        c2 = candles_15m[-2]  # Previous candle
        c3 = candles_15m[-1]  # Current candle

        # Calculate candle properties
        c3_body = abs(c3['close'] - c3['open'])
        c3_range = c3['high'] - c3['low']
        c3_upper_wick = c3['high'] - max(c3['open'], c3['close'])
        c3_lower_wick = min(c3['open'], c3['close']) - c3['low']

        # Bullish Engulfing
        if (c2['close'] < c2['open'] and
            c3['close'] > c3['open'] and
            c3['open'] < c2['close'] and
            c3['close'] > c2['open']):
            return {"type": "BUY", "pattern": "Bullish Engulfing", "confidence": 0.8}

        # Hammer
        if (c3_lower_wick > c3_body * 2 and
            c3_upper_wick < c3_body * 0.3 and
            c3['close'] > c3['open']):
            return {"type": "BUY", "pattern": "Hammer", "confidence": 0.7}

        # Bullish Pin Bar
        if (c3_lower_wick > c3_range * 0.6 and
            c3_body < c3_range * 0.3):
            return {"type": "BUY", "pattern": "Bullish Pin Bar", "confidence": 0.75}

        # Bearish Engulfing
        if (c2['close'] > c2['open'] and
            c3['close'] < c3['open'] and
            c3['open'] > c2['close'] and
            c3['close'] < c2['open']):
            return {"type": "SELL", "pattern": "Bearish Engulfing", "confidence": 0.8}

        # Shooting Star
        if (c3_upper_wick > c3_body * 2 and
            c3_lower_wick < c3_body * 0.3 and
            c3['close'] < c3['open']):
            return {"type": "SELL", "pattern": "Shooting Star", "confidence": 0.7}

        # Bearish Pin Bar
        if (c3_upper_wick > c3_range * 0.6 and
            c3_body < c3_range * 0.3):
            return {"type": "SELL", "pattern": "Bearish Pin Bar", "confidence": 0.75}

        return None

    def find_support_resistance(self, candles_4h):
        """Find significant support and resistance levels (OPTIMIZED - stricter criteria)"""
        if len(candles_4h) < 30:
            return []

        levels = []
        recent_candles = candles_4h[-30:]  # Look at more candles

        # Find swing highs and lows with stricter criteria
        for i in range(3, len(recent_candles) - 3):  # Require 3 candles on each side
            current = recent_candles[i]

            # Stronger swing high detection
            if (current['high'] > recent_candles[i-1]['high'] and
                current['high'] > recent_candles[i-2]['high'] and
                current['high'] > recent_candles[i-3]['high'] and
                current['high'] > recent_candles[i+1]['high'] and
                current['high'] > recent_candles[i+2]['high'] and
                current['high'] > recent_candles[i+3]['high']):
                levels.append({"price": current['high'], "type": "RESISTANCE", "strength": "STRONG"})

            # Stronger swing low detection
            if (current['low'] < recent_candles[i-1]['low'] and
                current['low'] < recent_candles[i-2]['low'] and
                current['low'] < recent_candles[i-3]['low'] and
                current['low'] < recent_candles[i+1]['low'] and
                current['low'] < recent_candles[i+2]['low'] and
                current['low'] < recent_candles[i+3]['low']):
                levels.append({"price": current['low'], "type": "SUPPORT", "strength": "STRONG"})

        # Remove duplicate/close levels (consolidate within $10 range)
        filtered_levels = []
        for level in levels:
            is_duplicate = False
            for existing in filtered_levels:
                if abs(level['price'] - existing['price']) < 10.0:
                    is_duplicate = True
                    break
            if not is_duplicate:
                filtered_levels.append(level)

        return filtered_levels

    def calculate_atr(self, candles_4h, period=14):
        """Calculate Average True Range for volatility filtering"""
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

    def check_trend_alignment(self, candles_4h):
        """Check if 4H trend is clear using moving averages"""
        if len(candles_4h) < 50:
            return "NEUTRAL"

        # Calculate EMAs
        closes = [c['close'] for c in candles_4h]
        ema_20 = self.calculate_ema(closes, 20)
        ema_50 = self.calculate_ema(closes, 50)

        if ema_20 is None or ema_50 is None:
            return "NEUTRAL"

        # Trend determination
        if ema_20 > ema_50 * 1.002:  # 0.2% above
            return "BULLISH"
        elif ema_20 < ema_50 * 0.998:  # 0.2% below
            return "BEARISH"
        else:
            return "NEUTRAL"

    def calculate_ema(self, data, period):
        """Calculate Exponential Moving Average"""
        if len(data) < period:
            return None

        multiplier = 2 / (period + 1)
        ema = sum(data[:period]) / period  # Start with SMA

        for price in data[period:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))

        return ema

    def is_near_level(self, price, level, tolerance=5.0):
        """Check if price is near support/resistance level"""
        return abs(price - level) <= tolerance

    def generate_signal(self, candle, all_data, timestamp):
        """Generate trade signal based on Price Action strategy"""

        # Check market timing
        in_window, session = self.check_market_timing(timestamp)
        if not in_window:
            return None

        # Check cooldown
        if not self.check_trade_cooldown(timestamp):
            return None

        # Check API limit
        if self.api_requests >= API_LIMIT_PER_DAY:
            return None

        current_price = candle['close']

        # ===== NEW FILTER 1: Volatility Check (ATR) =====
        atr = self.calculate_atr(all_data['4h'])
        if atr is None or atr < 8.0 or atr > 50.0:
            return None  # Skip if volatility is too low or too high

        # ===== NEW FILTER 2: Trend Alignment (4H) =====
        trend_4h = self.check_trend_alignment(all_data['4h'])

        # Detect price action pattern
        price_action = self.detect_price_action_signal(all_data['15m'])
        if not price_action:
            return None

        # Find S/R levels
        sr_levels = self.find_support_resistance(all_data['4h'])

        # Check if near key level
        near_level = False
        level_type = ""
        for level in sr_levels:
            if self.is_near_level(current_price, level['price']):
                near_level = True
                level_type = level['type']
                break

        # Calculate confidence
        confidence = price_action['confidence']

        # EURUSD correlation bonus (optional)
        eurusd_trend, eurusd_reason = self.calculate_eurusd_correlation(all_data['eurusd_1d'])
        correlation_bonus = 0
        if price_action['type'] == 'BUY' and eurusd_trend in ['BULLISH', 'STRONG_BULLISH']:
            correlation_bonus = 0.1
        elif price_action['type'] == 'SELL' and eurusd_trend in ['BEARISH', 'STRONG_BEARISH']:
            correlation_bonus = 0.1

        confidence += correlation_bonus

        # Bonus for key level
        if near_level:
            confidence += 0.15

        # ===== NEW FILTER 3: Increased Confidence Threshold =====
        # Minimum confidence 80% (more selective)
        if confidence < 0.80:
            return None

        # BUY Signal
        if price_action['type'] == 'BUY':
            # ===== NEW FILTER 4: Trend Alignment Check =====
            # Only allow BUY in BULLISH or NEUTRAL trends
            if trend_4h == "BEARISH":
                return None

            supports = [l['price'] for l in sr_levels if l['type'] == 'SUPPORT' and l['price'] < current_price]
            if supports:
                swing_low = max(supports)
            else:
                recent_lows = [c['low'] for c in all_data['4h'][-10:]]
                swing_low = min(recent_lows)

            sl = swing_low - 3.0
            risk = current_price - sl
            tp = current_price + (risk * 2.0)  # 2:1 RRR
            rrr = (tp - current_price) / (current_price - sl)

            if rrr >= 2.0:
                reason_parts = [session, price_action['pattern'], f"{int(confidence*100)}% Conf"]
                if near_level:
                    reason_parts.append(f"@ {level_type}")
                if correlation_bonus > 0:
                    reason_parts.append(eurusd_reason)

                return {
                    "decision": "BUY",
                    "price": current_price,
                    "sl": sl,
                    "tp": tp,
                    "rrr": rrr,
                    "window": session,
                    "reason": " | ".join(reason_parts)
                }

        # SELL Signal
        elif price_action['type'] == 'SELL':
            # ===== NEW FILTER 4: Trend Alignment Check =====
            # Only allow SELL in BEARISH or NEUTRAL trends
            if trend_4h == "BULLISH":
                return None

            resistances = [l['price'] for l in sr_levels if l['type'] == 'RESISTANCE' and l['price'] > current_price]
            if resistances:
                swing_high = min(resistances)
            else:
                recent_highs = [c['high'] for c in all_data['4h'][-10:]]
                swing_high = max(recent_highs)

            sl = swing_high + 3.0
            risk = sl - current_price
            tp = current_price - (risk * 2.0)  # 2:1 RRR
            rrr = (current_price - tp) / (sl - current_price)

            if rrr >= 2.0:
                reason_parts = [session, price_action['pattern'], f"{int(confidence*100)}% Conf"]
                if near_level:
                    reason_parts.append(f"@ {level_type}")
                if correlation_bonus > 0:
                    reason_parts.append(eurusd_reason)

                return {
                    "decision": "SELL",
                    "price": current_price,
                    "sl": sl,
                    "tp": tp,
                    "rrr": rrr,
                    "window": session,
                    "reason": " | ".join(reason_parts)
                }

        return None

    def execute_trade(self, signal, timestamp):
        """Simulate trade execution and outcome"""

        trade = {
            "timestamp": timestamp,
            "decision": signal['decision'],
            "entry_price": signal['price'],
            "sl": signal['sl'],
            "tp": signal['tp'],
            "rrr": signal['rrr'],
            "window": signal['window'],
            "reason": signal['reason'],
            "lot_size": LOT_SIZE,
            "outcome": None,
            "pnl": 0,
            "exit_price": None,
            "exit_time": None
        }

        self.trades.append(trade)
        self.last_trade_time = timestamp
        self.api_requests += 1  # Count trade as API request

        return trade

    def simulate_trade_outcome(self, trade, future_candles):
        """Simulate if SL or TP was hit based on future price action"""

        for candle in future_candles:
            high = candle['high']
            low = candle['low']

            if trade['decision'] == 'BUY':
                # Check if SL hit
                if low <= trade['sl']:
                    trade['outcome'] = 'LOSS'
                    trade['exit_price'] = trade['sl']
                    trade['exit_time'] = candle['time']
                    pips = (trade['sl'] - trade['entry_price'])
                    trade['pnl'] = pips * LOT_SIZE * 100  # Simplified P&L
                    self.balance += trade['pnl']
                    return

                # Check if TP hit
                if high >= trade['tp']:
                    trade['outcome'] = 'WIN'
                    trade['exit_price'] = trade['tp']
                    trade['exit_time'] = candle['time']
                    pips = (trade['tp'] - trade['entry_price'])
                    trade['pnl'] = pips * LOT_SIZE * 100
                    self.balance += trade['pnl']
                    return

            elif trade['decision'] == 'SELL':
                # Check if SL hit
                if high >= trade['sl']:
                    trade['outcome'] = 'LOSS'
                    trade['exit_price'] = trade['sl']
                    trade['exit_time'] = candle['time']
                    pips = (trade['entry_price'] - trade['sl'])
                    trade['pnl'] = -abs(pips * LOT_SIZE * 100)
                    self.balance += trade['pnl']
                    return

                # Check if TP hit
                if low <= trade['tp']:
                    trade['outcome'] = 'WIN'
                    trade['exit_price'] = trade['tp']
                    trade['exit_time'] = candle['time']
                    pips = (trade['entry_price'] - trade['tp'])
                    trade['pnl'] = pips * LOT_SIZE * 100
                    self.balance += trade['pnl']
                    return

        # If neither hit, mark as open
        trade['outcome'] = 'OPEN'
        trade['pnl'] = 0

    async def run_backtest(self):
        """Main backtest simulation"""

        print("\n" + "="*60)
        print("🏛️  GOLDEN TRIAD STRATEGY BACKTEST - DECEMBER 2025")
        print("="*60)
        print(f"Initial Balance: ${INITIAL_BALANCE:,.2f}")
        print(f"Lot Size: {LOT_SIZE}")
        print(f"Strategy: Golden Triad (EURUSD Correlation + Daily + 4H BOS)")
        print("="*60 + "\n")

        # Fetch data
        data = await self.fetch_historical_data()

        print("\n🔍 Scanning for trading opportunities...\n")

        # Iterate through 15m candles
        candles_15m = data['15m']

        for i, candle in enumerate(candles_15m):
            # candle['time'] is already a datetime object from MetaAPI
            timestamp = candle['time'] if isinstance(candle['time'], datetime) else datetime.fromtimestamp(candle['time'], tz=pytz.utc)

            # Get data up to current candle
            current_data = {
                '15m': candles_15m[:i+1],
                '4h': [c for c in data['4h'] if c['time'] <= candle['time']],
                '1d': [c for c in data['1d'] if c['time'] <= candle['time']],
                'eurusd_1d': [c for c in data['eurusd_1d'] if c['time'] <= candle['time']]
            }

            # Generate signal
            signal = self.generate_signal(candle, current_data, timestamp)

            if signal:
                trade = self.execute_trade(signal, timestamp)
                print(f"🎯 TRADE #{len(self.trades)}")
                print(f"   Time: {timestamp.strftime('%Y-%m-%d %H:%M UTC')}")
                print(f"   Signal: {signal['decision']} @ ${signal['price']:.2f}")
                print(f"   SL: ${signal['sl']:.2f} | TP: ${signal['tp']:.2f} | RRR: {signal['rrr']:.1f}:1")
                print(f"   Window: {signal['window']}")
                print(f"   Reason: {signal['reason']}\n")

                # Simulate outcome with future candles
                future_candles = candles_15m[i+1:]
                self.simulate_trade_outcome(trade, future_candles)

                if trade['outcome'] in ['WIN', 'LOSS']:
                    outcome_emoji = "✅" if trade['outcome'] == 'WIN' else "❌"
                    print(f"   {outcome_emoji} {trade['outcome']}: ${trade['pnl']:+,.2f}")
                    exit_time = trade['exit_time'] if isinstance(trade['exit_time'], datetime) else datetime.fromtimestamp(trade['exit_time'], tz=pytz.utc)
                    print(f"   Exit: ${trade['exit_price']:.2f} @ {exit_time.strftime('%Y-%m-%d %H:%M UTC')}")
                    print(f"   New Balance: ${self.balance:,.2f}\n")

        # Generate report
        self.generate_report()

    def generate_report(self):
        """Generate detailed backtest report"""

        print("\n" + "="*60)
        print("📊 BACKTEST RESULTS")
        print("="*60)

        total_trades = len(self.trades)
        wins = [t for t in self.trades if t['outcome'] == 'WIN']
        losses = [t for t in self.trades if t['outcome'] == 'LOSS']
        open_trades = [t for t in self.trades if t['outcome'] == 'OPEN']

        win_rate = (len(wins) / total_trades * 100) if total_trades > 0 else 0

        total_pnl = sum(t['pnl'] for t in self.trades)
        final_balance = self.balance
        roi = ((final_balance - INITIAL_BALANCE) / INITIAL_BALANCE) * 100

        print(f"\n📈 PERFORMANCE METRICS")
        print(f"   Total Trades: {total_trades}")
        print(f"   Wins: {len(wins)} ({win_rate:.1f}%)")
        print(f"   Losses: {len(losses)} ({(len(losses)/total_trades*100) if total_trades > 0 else 0:.1f}%)")
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

        print(f"\n🔧 OPERATIONAL STATS")
        print(f"   API Requests: {self.api_requests}/{API_LIMIT_PER_DAY}")
        print(f"   Lot Size: {LOT_SIZE}")
        print(f"   Cooldown: {COOLDOWN_MINUTES} minutes between trades")

        print("\n" + "="*60)

        # Trade log
        if total_trades > 0:
            print("\n📋 TRADE LOG")
            print("="*60)
            for i, trade in enumerate(self.trades, 1):
                outcome_emoji = {"WIN": "✅", "LOSS": "❌", "OPEN": "⏳"}[trade['outcome']]
                print(f"\n{i}. {outcome_emoji} {trade['decision']} @ ${trade['entry_price']:.2f}")
                print(f"   {trade['timestamp'].strftime('%Y-%m-%d %H:%M UTC')} | {trade['window']}")
                print(f"   SL: ${trade['sl']:.2f} | TP: ${trade['tp']:.2f} | RRR: {trade['rrr']:.1f}:1")
                if trade['outcome'] != 'OPEN':
                    print(f"   Exit: ${trade['exit_price']:.2f} | P&L: ${trade['pnl']:+,.2f}")
                print(f"   {trade['reason']}")
            print("="*60)

async def main():
    backtest = DecemberBacktest()
    await backtest.run_backtest()

if __name__ == "__main__":
    asyncio.run(main())
