import asyncio
import websockets
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
from metaapi_cloud_sdk import MetaApi
import warnings
import os

warnings.filterwarnings("ignore")

# ==========================================
# 🔐 CONFIGURATION
# ==========================================
META_API_TOKEN = os.getenv("META_API_TOKEN", "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiIxNzFjZWQ4Yjg5ODdhMWQyM2JlOGFhMTAxM2YwZjVlZCIsImFjY2Vzc1J1bGVzIjpbeyJpZCI6InRyYWRpbmctYWNjb3VudC1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVzdC1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcnBjLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVhbC10aW1lLXN0cmVhbWluZy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtZXRhc3RhdHMtYXBpIiwibWV0aG9kcyI6WyJtZXRhc3RhdHMtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6InJpc2stbWFuYWdlbWVudC1hcGkiLCJtZXRob2RzIjpbInJpc2stbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoiY29weWZhY3RvcnktYXBpIiwibWV0aG9kcyI6WyJjb3B5ZmFjdG9yeS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibXQtbWFuYWdlci1hcGkiLCJtZXRob2RzIjpbIm10LW1hbmFnZXItYXBpOnJlc3Q6ZGVhbGluZzoqOioiLCJtdC1tYW5hZ2VyLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJiaWxsaW5nLWFwaSIsIm1ldGhvZHMiOlsiYmlsbGluZy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfV0sImlnbm9yZVJhdGVMaW1pdHMiOmZhbHNlLCJ0b2tlbklkIjoiMjAyMTAyMTMiLCJpbXBlcnNvbmF0ZWQiOmZhbHNlLCJyZWFsVXNlcklkIjoiMTcxY2VkOGI4OTg3YTFkMjNiZThhYTEwMTNmMGY1ZWQiLCJpYXQiOjE3NjY3Mjg2MzEsImV4cCI6MTc3NDUwNDYzMX0.TlcBJs-k1nzfPIaNLcYBHkFlAWnnJ9qa43CV7aFDYxWjVxp_ZkAJRbKhy4MYhStwHMdiDP8SLVf_Zd4Wfns5qvV_HNNCiCoDDLSw8xy02gctQsr6su5ZTYCSRLfscQZDk8mfZuVfj3wKNxAYE68TeyMlBc1oEQyaHJ7AuDDGhlLDmwJINX4hhfHBxvPbdYztW92DQ_mmp9PSuLU_sr0O9NywQyiYEFXFjCl1_C_55qShFE0-_PkvnQNAzy-6-kWnqMt6Q3yiZJH_EusHF92VxVhzPcqsSFEXCK1q9VkNHT1bK9gICvGGTMGUy0qr0O0d_8THdZrSbiZKi8t9QHgYy-O4BBMvUCYIHcyDUoigwHQGJoFm_n1ZEzpunmVCqWhjwpUXKeXwQebwdJ0OHyH3bW59Z-NT-Snk70-6oHseEpjd45zBiN8pMClVhXc1DvpMiPFnXmQ4hmSmTnskdAOakXhKbx3VRt4EwRbs8-_Pupp824Q0k852X7VODZ2owKX9gZHjjOKuIG3ZlNztj6StEwb_lDzuEc3r8BNNtntZW8UBkBy9T11lj1mry0SzxsP-NSUGUnfxCtqlXgMBni1uhnyY_JtadDMtXsZ9QDiF3Way8HyBhnE4DBD7-UcsHHQobSRpyyhTYqF8bH4pjmO-Mh1IqVJLLZkZi7NJ0RNCgNk")
WS_HOST = os.getenv("WS_HOST", "0.0.0.0")
WS_PORT = int(os.getenv("PORT", "8080"))

VAULTS = [
    {"id": "77c5fbff-beb8-422a-b085-c135c230a630", "name": "QUANT_DEMO", "is_real": False, "risk_pct": 0.02},
    {"id": "436348e0-be6e-49cc-a991-8895903e5288", "name": "MICRO_REAL", "is_real": True, "risk_pct": 0.01}
]

STATE = {
    "vaults": [],
    "analysis": {"type": "HEARTBEAT", "symbol": "GOLD.pro", "price": 0, "decision": "INIT", "reason": "System Booting..."},
    "chart_data": [],
    "ready": False,
    "trade_notifications": [],  # Store recent trade executions
    "api_requests_today": 0,  # Track API requests for 2000 daily limit
    "last_request_reset": datetime.now(pytz.utc).date(),
    "last_trade_time": None,  # Track last trade to avoid over-trading
    "trades_today": 0  # Track number of trades per day
}

# ==========================================
# 📊 SMART MONEY CONCEPTS (SMC) ANALYZER
# ==========================================
class SMCAnalyzer:
    """Advanced Smart Money Concepts & Fibonacci Analysis"""

    @staticmethod
    def identify_structure(df, timeframe_name=""):
        """Identify market structure: HH, HL, LH, LL"""
        highs = df['high'].values
        lows = df['low'].values

        # Find swing points (local extrema)
        swing_highs = []
        swing_lows = []

        for i in range(2, len(df) - 2):
            # Swing High: higher than 2 candles before and after
            if highs[i] > max(highs[i-2:i]) and highs[i] > max(highs[i+1:i+3]):
                swing_highs.append({"index": i, "price": highs[i]})

            # Swing Low: lower than 2 candles before and after
            if lows[i] < min(lows[i-2:i]) and lows[i] < min(lows[i+1:i+3]):
                swing_lows.append({"index": i, "price": lows[i]})

        # Determine trend
        trend = "NEUTRAL"
        if len(swing_highs) >= 2 and len(swing_lows) >= 2:
            recent_highs = [sh['price'] for sh in swing_highs[-3:]]
            recent_lows = [sl['price'] for sl in swing_lows[-3:]]

            # Uptrend: Higher Highs + Higher Lows
            if all(recent_highs[i] < recent_highs[i+1] for i in range(len(recent_highs)-1)) and \
               all(recent_lows[i] < recent_lows[i+1] for i in range(len(recent_lows)-1)):
                trend = "BULLISH"

            # Downtrend: Lower Highs + Lower Lows
            elif all(recent_highs[i] > recent_highs[i+1] for i in range(len(recent_highs)-1)) and \
                 all(recent_lows[i] > recent_lows[i+1] for i in range(len(recent_lows)-1)):
                trend = "BEARISH"

        print(f"📈 {timeframe_name} Structure: {trend} | Swing Highs: {len(swing_highs)} | Swing Lows: {len(swing_lows)}")
        return trend, swing_highs, swing_lows

    @staticmethod
    def detect_choch_bos(df, swing_highs, swing_lows):
        """Detect Change of Character (CHoCH) and Break of Structure (BOS)"""
        if len(swing_highs) < 2 or len(swing_lows) < 2:
            return None, None

        recent_close = df['close'].iloc[-1]
        last_swing_high = swing_highs[-1]['price']
        last_swing_low = swing_lows[-1]['price']

        # BOS: Price breaks previous structure level with momentum
        bos = None
        if recent_close > last_swing_high:
            momentum = recent_close - last_swing_high
            if momentum >= 0.0020:  # 20 pips minimum (XAUUSD: $2 = 20 pips)
                bos = {"type": "BULLISH_BOS", "level": last_swing_high, "momentum": momentum}
                print(f"🔥 BULLISH BOS Detected | Broke: ${last_swing_high:.2f} | Momentum: {momentum * 100:.1f} pips")

        elif recent_close < last_swing_low:
            momentum = last_swing_low - recent_close
            if momentum >= 0.0020:
                bos = {"type": "BEARISH_BOS", "level": last_swing_low, "momentum": momentum}
                print(f"🔥 BEARISH BOS Detected | Broke: ${last_swing_low:.2f} | Momentum: {momentum * 100:.1f} pips")

        # CHoCH: Change of character (reversal signal)
        choch = None
        if len(df) > 10:
            prev_trend = "BULLISH" if df['close'].iloc[-10] < df['close'].iloc[-5] else "BEARISH"
            curr_trend = "BULLISH" if df['close'].iloc[-5] < recent_close else "BEARISH"

            if prev_trend != curr_trend:
                choch = {"type": f"{curr_trend}_CHOCH", "confirmed": True}
                print(f"⚡ CHoCH Detected: {prev_trend} → {curr_trend}")

        return choch, bos

    @staticmethod
    def calculate_fibonacci(swing_high, swing_low, direction="bullish"):
        """Calculate Fibonacci retracement levels"""
        diff = swing_high - swing_low

        if direction == "bullish":
            # For uptrend: retracement from swing low
            fib_levels = {
                "0.236": swing_low + diff * 0.236,
                "0.382": swing_low + diff * 0.382,
                "0.500": swing_low + diff * 0.500,
                "0.618": swing_low + diff * 0.618,  # Golden Pocket start
                "0.786": swing_low + diff * 0.786,  # Golden Pocket end
            }
        else:
            # For downtrend: retracement from swing high
            fib_levels = {
                "0.236": swing_high - diff * 0.236,
                "0.382": swing_high - diff * 0.382,
                "0.500": swing_high - diff * 0.500,
                "0.618": swing_high - diff * 0.618,
                "0.786": swing_high - diff * 0.786,
            }

        return fib_levels

# ==========================================
# 🌍 GOLDEN TRIAD ENGINE
# ==========================================
class GoldenTriadEngine:
    def __init__(self):
        self.api = MetaApi(META_API_TOKEN)
        self.connections = {}
        self.smc = SMCAnalyzer()

    async def connect(self):
        """Connect to MetaTrader accounts"""
        for vault in VAULTS:
            try:
                acc = await self.api.metatrader_account_api.get_account(vault['id'])
                if acc.state == 'UNDEPLOYED':
                    await acc.deploy()
                await acc.wait_connected()
                conn = acc.get_streaming_connection()
                await conn.connect()
                await conn.wait_synchronized()

                # Subscribe to market data
                await conn.subscribe_to_market_data("GOLD.pro")
                await conn.subscribe_to_market_data("EURUSD")

                self.connections[vault['id']] = {"conn": conn, "meta": vault, "acc_api": acc}
                print(f"✅ VAULT SYNCED: {vault['name']}")
            except Exception as e:
                print(f"❌ VAULT ERROR {vault['name']}: {e}")

    def get_market_session(self):
        """Determine current trading session"""
        utc_now = datetime.now(pytz.utc)
        hour = utc_now.hour

        # Tokyo: 00:00-09:00 UTC
        if 0 <= hour < 9:
            return "tokyo"
        # London: 08:00-17:00 UTC
        elif 8 <= hour < 17:
            return "london"
        # New York: 13:00-22:00 UTC
        elif 13 <= hour < 22:
            return "ny"
        else:
            return "none"

    def check_api_limit(self):
        """Check Oanda 2000 daily API request limit"""
        now = datetime.now(pytz.utc)

        # Reset counter at midnight UTC
        if now.date() != STATE["last_request_reset"]:
            STATE["api_requests_today"] = 0
            STATE["last_request_reset"] = now.date()
            STATE["trades_today"] = 0
            print("📅 Daily API counter reset")

        # Conservative limit: 1500 requests (leaving buffer for other operations)
        if STATE["api_requests_today"] >= 1500:
            print(f"⚠️ API limit reached: {STATE['api_requests_today']}/1500 requests today")
            return False

        return True

    def is_active_trading_hours(self):
        """Check if market is actively trading (expanded windows for more trades)"""
        now = datetime.now(pytz.utc)
        hour = now.hour

        # Tokyo Session: 23:00-08:00 UTC
        if 23 <= hour or hour < 8:
            return True, "TOKYO"

        # London Session: 07:00-16:00 UTC (overlaps with Tokyo and NY)
        if 7 <= hour < 16:
            return True, "LONDON"

        # NY Session: 12:00-21:00 UTC
        if 12 <= hour < 21:
            return True, "NY"

        # Avoid low liquidity periods (21:00-23:00 UTC)
        return False, "LOW_LIQUIDITY"

    def check_trade_cooldown(self):
        """Prevent over-trading - minimum 1 hour between trades for quality"""
        if STATE["last_trade_time"] is None:
            return True

        time_since_last_trade = datetime.now(pytz.utc) - STATE["last_trade_time"]
        cooldown_minutes = 60  # 1 hour for better quality trades

        if time_since_last_trade.total_seconds() < (cooldown_minutes * 60):
            remaining = cooldown_minutes * 60 - time_since_last_trade.total_seconds()
            print(f"⏱️ Trade cooldown: {remaining/60:.0f}min remaining")
            return False

        return True

    def calculate_atr(self, df_4h, period=14):
        """Calculate Average True Range for volatility filtering"""
        if len(df_4h) < period + 1:
            return None

        recent = df_4h.tail(period + 1)
        tr_list = []

        for i in range(1, len(recent)):
            high = recent.iloc[i]['high']
            low = recent.iloc[i]['low']
            prev_close = recent.iloc[i-1]['close']

            tr = max(
                high - low,
                abs(high - prev_close),
                abs(low - prev_close)
            )
            tr_list.append(tr)

        atr = sum(tr_list) / len(tr_list)
        return atr

    def check_trend_alignment(self, df_4h):
        """Check if 4H trend is clear using moving averages"""
        if len(df_4h) < 50:
            return "NEUTRAL"

        # Calculate EMAs
        closes = df_4h['close'].values
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

    def detect_price_action_signal(self, df_15m):
        """Detect bullish/bearish price action patterns on 15m chart"""
        if len(df_15m) < 3:
            return None

        # Get last 3 candles
        c1 = df_15m.iloc[-3]  # 2 candles ago
        c2 = df_15m.iloc[-2]  # 1 candle ago
        c3 = df_15m.iloc[-1]  # Current candle

        # Calculate candle properties
        c3_body = abs(c3['close'] - c3['open'])
        c3_range = c3['high'] - c3['low']
        c3_upper_wick = c3['high'] - max(c3['open'], c3['close'])
        c3_lower_wick = min(c3['open'], c3['close']) - c3['low']

        # Bullish Patterns
        # 1. Bullish Engulfing
        if (c2['close'] < c2['open'] and  # Previous candle bearish
            c3['close'] > c3['open'] and  # Current candle bullish
            c3['open'] < c2['close'] and  # Opens below previous close
            c3['close'] > c2['open']):    # Closes above previous open
            return {"type": "BUY", "pattern": "Bullish Engulfing", "confidence": 0.8}

        # 2. Hammer (bullish reversal at support)
        if (c3_lower_wick > c3_body * 2 and  # Long lower wick
            c3_upper_wick < c3_body * 0.3 and  # Small upper wick
            c3['close'] > c3['open']):  # Bullish close
            return {"type": "BUY", "pattern": "Hammer", "confidence": 0.7}

        # 3. Bullish Pin Bar
        if (c3_lower_wick > c3_range * 0.6 and  # Dominant lower wick
            c3_body < c3_range * 0.3):  # Small body
            return {"type": "BUY", "pattern": "Bullish Pin Bar", "confidence": 0.75}

        # Bearish Patterns
        # 1. Bearish Engulfing
        if (c2['close'] > c2['open'] and  # Previous candle bullish
            c3['close'] < c3['open'] and  # Current candle bearish
            c3['open'] > c2['close'] and  # Opens above previous close
            c3['close'] < c2['open']):    # Closes below previous open
            return {"type": "SELL", "pattern": "Bearish Engulfing", "confidence": 0.8}

        # 2. Shooting Star (bearish reversal at resistance)
        if (c3_upper_wick > c3_body * 2 and  # Long upper wick
            c3_lower_wick < c3_body * 0.3 and  # Small lower wick
            c3['close'] < c3['open']):  # Bearish close
            return {"type": "SELL", "pattern": "Shooting Star", "confidence": 0.7}

        # 3. Bearish Pin Bar
        if (c3_upper_wick > c3_range * 0.6 and  # Dominant upper wick
            c3_body < c3_range * 0.3):  # Small body
            return {"type": "SELL", "pattern": "Bearish Pin Bar", "confidence": 0.75}

        return None

    def find_support_resistance(self, df_4h):
        """Find significant support and resistance levels (optimized)"""
        if len(df_4h) < 30:
            return []

        levels = []
        recent_candles = df_4h.tail(30)  # Look at more candles

        # Find swing highs and lows with stricter criteria
        for i in range(3, len(recent_candles) - 3):  # Require 3 candles on each side
            current = recent_candles.iloc[i]

            # Stronger swing high detection
            if (current['high'] > recent_candles.iloc[i-1]['high'] and
                current['high'] > recent_candles.iloc[i-2]['high'] and
                current['high'] > recent_candles.iloc[i-3]['high'] and
                current['high'] > recent_candles.iloc[i+1]['high'] and
                current['high'] > recent_candles.iloc[i+2]['high'] and
                current['high'] > recent_candles.iloc[i+3]['high']):
                levels.append({"price": current['high'], "type": "RESISTANCE", "strength": "STRONG"})

            # Stronger swing low detection
            if (current['low'] < recent_candles.iloc[i-1]['low'] and
                current['low'] < recent_candles.iloc[i-2]['low'] and
                current['low'] < recent_candles.iloc[i-3]['low'] and
                current['low'] < recent_candles.iloc[i+1]['low'] and
                current['low'] < recent_candles.iloc[i+2]['low'] and
                current['low'] < recent_candles.iloc[i+3]['low']):
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

    def is_near_level(self, price, level, tolerance=5.0):
        """Check if price is near support/resistance level"""
        return abs(price - level) <= tolerance

    async def analyze_correlation(self, demo_api):
        """Step 2: EURUSD Correlation Analysis (Optional Filter)"""
        try:
            # Get EURUSD 4H data (last 7 days)
            start = datetime.now(pytz.utc) - timedelta(days=7)
            eurusd_candles = await demo_api.get_historical_candles("EURUSD", '4h', start, 42)

            if not eurusd_candles or len(eurusd_candles) < 10:
                return "NEUTRAL", "Insufficient EURUSD data", 0

            df_eur = pd.DataFrame(eurusd_candles)

            # Simple trend: compare recent close vs 7-day average
            recent_close = df_eur['close'].iloc[-1]
            avg_price = df_eur['close'].mean()

            # Momentum check
            price_change = df_eur['close'].iloc[-1] - df_eur['close'].iloc[-10]
            change_pct = (price_change / df_eur['close'].iloc[-10]) * 100

            if recent_close > avg_price and change_pct > 0.3:
                bias = "GOLD_LONG"
                reason = f"EUR +{change_pct:.2f}% (USD Weak)"
                bonus = 0.1  # 10% bonus confidence
            elif recent_close < avg_price and change_pct < -0.3:
                bias = "GOLD_SHORT"
                reason = f"EUR {change_pct:.2f}% (USD Strong)"
                bonus = 0.1
            else:
                bias = "NEUTRAL"
                reason = f"EUR Flat ({change_pct:.2f}%)"
                bonus = 0

            print(f"🌍 Correlation: {reason}")
            return bias, reason, bonus

        except Exception as e:
            print(f"❌ Correlation Error: {e}")
            return "NEUTRAL", "Correlation analysis failed", 0

    async def golden_triad_analysis(self, demo_api, demo_conn):
        """The Complete Golden Triad Strategy"""

        # Track API requests
        STATE["api_requests_today"] += 1

        # Get live price
        symbol_price = demo_conn.terminal_state.price("GOLD.pro")
        live_price = symbol_price.get('bid', 0) if symbol_price else 0

        if live_price == 0:
            return None

        # ====================
        # STEP 1: Macro Filter - Not implemented (would need DXY data)
        # For now, we proceed to correlation
        # ====================

        # ====================
        # STEP 2: Correlation Check (EURUSD) - OPTIONAL BONUS
        # ====================
        correlation_bias, correlation_reason, correlation_bonus = await self.analyze_correlation(demo_api)

        # ====================
        # STEP 3: Price Action + Support/Resistance
        # ====================

        # Get 15m candles for price action patterns
        start_15m = datetime.now(pytz.utc) - timedelta(hours=12)
        candles_15m = await demo_api.get_historical_candles("GOLD.pro", '15m', start_15m, 48)

        if not candles_15m or len(candles_15m) < 3:
            return None

        df_15m = pd.DataFrame(candles_15m)

        # Get 4H candles for support/resistance
        start_4h = datetime.now(pytz.utc) - timedelta(days=7)
        h4_candles = await demo_api.get_historical_candles("GOLD.pro", '4h', start_4h, 42)

        if not h4_candles:
            return None

        df_4h = pd.DataFrame(h4_candles)

        # ====================
        # SIGNAL GENERATION (Price Action Strategy - OPTIMIZED)
        # ====================
        signal = None

        # Check trading hours
        in_window, session_name = self.is_active_trading_hours()
        if not in_window:
            STATE["analysis"] = {
                "type": "HEARTBEAT",
                "symbol": "GOLD.pro",
                "price": round(live_price, 2),
                "decision": "SCANNING",
                "reason": f"Low liquidity period | {correlation_reason}",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
            return None

        # ===== NEW FILTER 1: Volatility Check (ATR) =====
        atr = self.calculate_atr(df_4h)
        if atr is None or atr < 8.0:  # Minimum volatility required
            STATE["analysis"] = {
                "type": "HEARTBEAT",
                "symbol": "GOLD.pro",
                "price": round(live_price, 2),
                "decision": "SCANNING",
                "reason": f"ATR too low ({atr:.1f} < 8.0) - Low volatility | {session_name}",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
            return None

        if atr > 50.0:  # Extreme volatility - too risky
            STATE["analysis"] = {
                "type": "HEARTBEAT",
                "symbol": "GOLD.pro",
                "price": round(live_price, 2),
                "decision": "SCANNING",
                "reason": f"ATR too high ({atr:.1f} > 50.0) - Extreme volatility | {session_name}",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
            return None

        # ===== NEW FILTER 2: Trend Alignment (4H) =====
        trend_4h = self.check_trend_alignment(df_4h)

        # Detect price action pattern
        price_action = self.detect_price_action_signal(df_15m)

        if not price_action:
            STATE["analysis"] = {
                "type": "HEARTBEAT",
                "symbol": "GOLD.pro",
                "price": round(live_price, 2),
                "decision": "SCANNING",
                "reason": f"No price action setup | {session_name} Session | {correlation_reason}",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
            return None

        # Find support/resistance levels
        sr_levels = self.find_support_resistance(df_4h)

        # Check if price is near a key level (adds confidence)
        near_level = False
        level_type = ""
        for level in sr_levels:
            if self.is_near_level(live_price, level['price']):
                near_level = True
                level_type = level['type']
                break

        # Calculate confidence score
        confidence = price_action['confidence']

        # Bonus for correlation alignment
        if price_action['type'] == 'BUY' and correlation_bias == 'GOLD_LONG':
            confidence += correlation_bonus
        elif price_action['type'] == 'SELL' and correlation_bias == 'GOLD_SHORT':
            confidence += correlation_bonus

        # Bonus for key level
        if near_level:
            confidence += 0.15

        # ===== NEW FILTER 3: Increased Confidence Threshold =====
        # Minimum confidence required: 0.80 (80%) - more selective
        if confidence < 0.80:
            STATE["analysis"] = {
                "type": "HEARTBEAT",
                "symbol": "GOLD.pro",
                "price": round(live_price, 2),
                "decision": "SCANNING",
                "reason": f"{price_action['pattern']} ({confidence*100:.0f}% conf) - Below 80% | {session_name}",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
            return None

        # BUY Signal
        if price_action['type'] == 'BUY':
            # ===== NEW FILTER 4: Trend Alignment Check =====
            # Only allow BUY signals in BULLISH or NEUTRAL trends
            if trend_4h == "BEARISH":
                STATE["analysis"] = {
                    "type": "HEARTBEAT",
                    "symbol": "GOLD.pro",
                    "price": round(live_price, 2),
                    "decision": "SCANNING",
                    "reason": f"BUY rejected - 4H trend is BEARISH | {price_action['pattern']}",
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                }
                return None
            # Find nearest support for SL
            supports = [l['price'] for l in sr_levels if l['type'] == 'SUPPORT' and l['price'] < live_price]
            if supports:
                swing_low = max(supports)  # Nearest support below price
            else:
                swing_low = df_4h['low'].tail(10).min()  # Recent low

            sl = swing_low - 3.0  # $3 buffer
            risk = live_price - sl
            tp = live_price + (risk * 2.0)  # 2:1 RRR

            rrr = (tp - live_price) / (live_price - sl)

            # Check trading conditions
            if rrr >= 2.0 and self.check_api_limit() and self.check_trade_cooldown():
                reason_parts = [
                    f"{session_name} Session",
                    price_action['pattern'],
                    f"{confidence*100:.0f}% Confidence",
                    f"RRR {rrr:.1f}:1"
                ]
                if near_level:
                    reason_parts.append(f"@ {level_type}")
                if correlation_bonus > 0:
                    reason_parts.append(correlation_reason)

                signal = {
                    "decision": "BUY",
                    "price": live_price,
                    "sl": round(sl, 2),
                    "tp": round(tp, 2),
                    "rrr": round(rrr, 2),
                    "reason": " | ".join(reason_parts)
                }

        # SELL Signal
        elif price_action['type'] == 'SELL':
            # ===== NEW FILTER 4: Trend Alignment Check =====
            # Only allow SELL signals in BEARISH or NEUTRAL trends
            if trend_4h == "BULLISH":
                STATE["analysis"] = {
                    "type": "HEARTBEAT",
                    "symbol": "GOLD.pro",
                    "price": round(live_price, 2),
                    "decision": "SCANNING",
                    "reason": f"SELL rejected - 4H trend is BULLISH | {price_action['pattern']}",
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                }
                return None

            # Find nearest resistance for SL
            resistances = [l['price'] for l in sr_levels if l['type'] == 'RESISTANCE' and l['price'] > live_price]
            if resistances:
                swing_high = min(resistances)  # Nearest resistance above price
            else:
                swing_high = df_4h['high'].tail(10).max()  # Recent high

            sl = swing_high + 3.0  # $3 buffer
            risk = sl - live_price
            tp = live_price - (risk * 2.0)  # 2:1 RRR

            rrr = (live_price - tp) / (sl - live_price)

            # Check trading conditions
            if rrr >= 2.0 and self.check_api_limit() and self.check_trade_cooldown():
                reason_parts = [
                    f"{session_name} Session",
                    price_action['pattern'],
                    f"{confidence*100:.0f}% Confidence",
                    f"RRR {rrr:.1f}:1"
                ]
                if near_level:
                    reason_parts.append(f"@ {level_type}")
                if correlation_bonus > 0:
                    reason_parts.append(correlation_reason)

                signal = {
                    "decision": "SELL",
                    "price": live_price,
                    "sl": round(sl, 2),
                    "tp": round(tp, 2),
                    "rrr": round(rrr, 2),
                    "reason": " | ".join(reason_parts)
                }

        # Update state
        if signal:
            # Track last trade time and increment daily counter
            STATE["last_trade_time"] = datetime.now(pytz.utc)
            STATE["trades_today"] += 1

            STATE["analysis"] = {
                "type": "SIGNAL",
                "symbol": "GOLD.pro",
                "price": signal['price'],
                "decision": signal['decision'],
                "sl": signal['sl'],
                "tp": signal['tp'],
                "size": 0.01,  # Will be calculated dynamically
                "reason": signal['reason'],
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
            print(f"🎯 SIGNAL GENERATED: {signal['decision']} @ ${signal['price']:.2f} | SL: ${signal['sl']:.2f} | TP: ${signal['tp']:.2f}")
        else:
            STATE["analysis"] = {
                "type": "HEARTBEAT",
                "symbol": "GOLD.pro",
                "price": round(live_price, 2),
                "decision": "SCANNING",
                "reason": f"Waiting for Golden Pocket Entry | Daily: {daily_trend} | 4H: {h4_trend}",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }

        return signal

    async def execute_trade(self, signal):
        """Execute trade with dynamic position sizing"""
        executed_trades = []

        for v_id, data in self.connections.items():
            try:
                conn = data['conn']
                ts = conn.terminal_state.account_information

                if ts:
                    equity = ts.get('equity', 100)
                    risk_amt = equity * data['meta']['risk_pct']
                    sl_dist = abs(signal['price'] - signal['sl'])

                    # Position size = Risk Amount / (SL Distance × Point Value)
                    # For XAUUSD: 1 lot = $100/point, so point_value = 100
                    size = max(0.01, round(risk_amt / (sl_dist * 100), 2))

                    print(f"💼 {data['meta']['name']}: Equity ${equity:.2f} | Risk ${risk_amt:.2f} | Size: {size} lots")

                    if signal['decision'] == "BUY":
                        result = await conn.create_market_buy_order("GOLD.pro", size, signal['sl'], signal['tp'])
                    else:
                        result = await conn.create_market_sell_order("GOLD.pro", size, signal['sl'], signal['tp'])

                    print(f"✅ Order Executed: {signal['decision']} {size} lots")

                    # Record successful execution
                    executed_trades.append({
                        "vault": data['meta']['name'],
                        "is_real": data['meta']['is_real'],
                        "direction": signal['decision'],
                        "entry": signal['price'],
                        "sl": signal['sl'],
                        "tp": signal['tp'],
                        "size": size,
                        "rrr": signal['rrr'],
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })

            except Exception as e:
                print(f"❌ Execution Error: {e}")

        # Add notification to state
        if executed_trades:
            notification = {
                "type": "TRADE_EXECUTED",
                "signal": signal,
                "trades": executed_trades,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
            STATE["trade_notifications"].append(notification)
            # Keep only last 10 notifications
            STATE["trade_notifications"] = STATE["trade_notifications"][-10:]

    async def run_hunt(self):
        """Main trading loop"""
        while True:
            try:
                # Update vault information
                v_list = []
                for v_id, data in self.connections.items():
                    ts = data['conn'].terminal_state
                    info = ts.account_information
                    if info and 'equity' in info:
                        v_list.append({
                            "name": data['meta']['name'],
                            "is_real": data['meta']['is_real'],
                            "equity": info['equity'],
                            "profit": info['equity'] - info.get('balance', info['equity']),
                            "positions": [{
                                "id": p['id'],
                                "symbol": p['symbol'],
                                "profit": p.get('profit', 0),
                                "type": str(p['type']),
                                "volume": p['volume'],
                                "openPrice": p.get('openPrice', 0)
                            } for p in ts.positions]
                        })

                if v_list:
                    STATE["vaults"] = v_list

                # Run Golden Triad Analysis
                if "77c5fbff-beb8-422a-b085-c135c230a630" in self.connections:
                    demo_conn = self.connections["77c5fbff-beb8-422a-b085-c135c230a630"]["conn"]
                    demo_api = self.connections["77c5fbff-beb8-422a-b085-c135c230a630"]["acc_api"]

                    signal = await self.golden_triad_analysis(demo_api, demo_conn)

                    # AUTO-TRADING ENABLED
                    if signal:
                        print(f"🚨 AUTO-EXECUTING TRADE: {signal['decision']} @ ${signal['price']:.2f}")
                        await self.execute_trade(signal)

                    STATE["ready"] = True

            except Exception as e:
                print(f"❌ Hunt Loop Error: {e}")

            await asyncio.sleep(10)  # Analyze every 10 seconds

# ==========================================
# 🌐 WEBSOCKET SERVER
# ==========================================
async def health_check(path, _request_headers):
    """Handle HTTP health checks from Railway"""
    if path == "/health":
        return (200, [], b"OK\n")
    # Accept all other paths as WebSocket connections
    return None

async def socket_handler(websocket):
    print("🟢 COMMANDER JOINED")
    try:
        while True:
            if STATE["ready"]:
                await websocket.send(json.dumps({"type": "MULTI_VAULT_UPDATE", "vaults": STATE["vaults"]}))
                await websocket.send(json.dumps(STATE["analysis"]))
                if STATE["chart_data"]:
                    await websocket.send(json.dumps({"type": "CHART_UPDATE", "data": STATE["chart_data"]}))

                # Send trade notifications
                if STATE["trade_notifications"]:
                    for notification in STATE["trade_notifications"]:
                        await websocket.send(json.dumps(notification))
                    # Clear notifications after sending
                    STATE["trade_notifications"] = []

            await asyncio.sleep(2)
    except websockets.exceptions.ConnectionClosed:
        print("🔴 COMMANDER LEFT")

async def main():
    engine = GoldenTriadEngine()
    await engine.connect()
    asyncio.create_task(engine.run_hunt())

    async with websockets.serve(
        socket_handler,
        WS_HOST,
        WS_PORT,
        ping_interval=20,
        ping_timeout=10,
        process_request=health_check
    ):
        print(f"🚀 WebSocket Server Running on ws://{WS_HOST}:{WS_PORT}")
        print("⚡ Golden Triad Strategy: ACTIVE")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
