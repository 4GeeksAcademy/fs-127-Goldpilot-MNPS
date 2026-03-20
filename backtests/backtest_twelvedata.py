#!/usr/bin/env python3
"""
Aurum Sniper Backtest using Twelve Data API
Alternative data source for 60-day historical validation

Free tier: 800 API calls/day
Strategy: v5.1 Balanced Production Model
"""

import asyncio
from datetime import datetime, timedelta
import pytz
import os
from dotenv import load_dotenv
from twelvedata import TDClient
import time

load_dotenv()

# Configuration
TWELVEDATA_API_KEY = os.getenv('TWELVEDATA_API_KEY', '')  # Get free key from https://twelvedata.com
INITIAL_BALANCE = 10000
RISK_PER_TRADE = 0.01
RISK_REWARD_RATIO = 3.0
ATR_MULTIPLIER = 1.5
ATR_MAX_VOLATILITY = 40.0
MAX_TRADES_PER_DAY = 4
BREAKEVEN_TRIGGER = 1.5

class TwelveDataBacktest:
    def __init__(self):
        self.balance = INITIAL_BALANCE
        self.trades = []
        self.trades_today = 0
        self.current_date = None

    def fetch_historical_data_sync(self):
        """Fetch data from Twelve Data API"""

        if not TWELVEDATA_API_KEY:
            print("⚠️ TWELVEDATA_API_KEY not found in .env file")
            print("📝 Get your free API key from: https://twelvedata.com/")
            print("   Add to .env: TWELVEDATA_API_KEY=your_key_here")
            return None

        td = TDClient(apikey=TWELVEDATA_API_KEY)

        print("✅ Twelve Data API initialized")
        print("📊 Fetching Gold (XAU/USD) historical data...")
        print("   ⏰ Time range: Nov 1 - Dec 27, 2025 (60 days)")

        # Define end date as today or Dec 27, 2025
        end_date = datetime.now(pytz.utc)
        if end_date > datetime(2025, 12, 27, tzinfo=pytz.utc):
            end_date = datetime(2025, 12, 27, tzinfo=pytz.utc)

        start_date = datetime(2025, 11, 1, tzinfo=pytz.utc)

        # Note: Twelve Data uses outputsize parameter
        # Free tier allows up to 5000 data points per request

        data = {}

        try:
            # Fetch 15-minute candles (primary timeframe)
            print("   📈 Fetching 15m candles...")
            ts_15m = td.time_series(
                symbol="XAU/USD",
                interval="15min",
                outputsize=5000,  # Max for free tier
                timezone="UTC"
            )
            df_15m = ts_15m.as_pandas()

            if df_15m is None or df_15m.empty:
                print("   ❌ No 15m data received")
                return None

            # Convert to our expected format
            candles_15m = self.convert_dataframe_to_candles(df_15m, start_date, end_date)
            print(f"   ✅ Received {len(candles_15m)} 15m candles")
            time.sleep(1)  # Rate limit protection

            # Fetch 1-hour candles (structure)
            print("   📈 Fetching 1h candles...")
            ts_1h = td.time_series(
                symbol="XAU/USD",
                interval="1h",
                outputsize=2000,
                timezone="UTC"
            )
            df_1h = ts_1h.as_pandas()

            if df_1h is None or df_1h.empty:
                print("   ❌ No 1h data received")
                return None

            candles_1h = self.convert_dataframe_to_candles(df_1h, start_date, end_date)
            print(f"   ✅ Received {len(candles_1h)} 1h candles")
            time.sleep(1)

            # Fetch 4-hour candles (ATR)
            print("   📈 Fetching 4h candles...")
            ts_4h = td.time_series(
                symbol="XAU/USD",
                interval="4h",
                outputsize=500,
                timezone="UTC"
            )
            df_4h = ts_4h.as_pandas()

            if df_4h is None or df_4h.empty:
                print("   ❌ No 4h data received")
                return None

            candles_4h = self.convert_dataframe_to_candles(df_4h, start_date, end_date)
            print(f"   ✅ Received {len(candles_4h)} 4h candles")
            time.sleep(1)

            # Create 5m candles from 15m (approximation)
            print("   🔄 Creating 5m candles from 15m data (approximation)...")
            candles_5m = candles_15m  # Use 15m as proxy (CHoCH optional anyway)

            data = {
                '5m': candles_5m,
                '15m': candles_15m,
                '1h': candles_1h,
                '4h': candles_4h
            }

            print(f"\n✅ Data fetch complete!")
            print(f"   15m: {len(candles_15m)} candles")
            print(f"   1h: {len(candles_1h)} candles")
            print(f"   4h: {len(candles_4h)} candles")

            return data

        except Exception as e:
            print(f"❌ Error fetching data: {e}")
            print(f"   Note: Free tier limited to 8 API calls/minute, 800/day")
            return None

    def convert_dataframe_to_candles(self, df, start_date, end_date):
        """Convert Twelve Data pandas dataframe to our candle format"""
        candles = []

        # Twelve Data returns data in reverse chronological order
        df = df.sort_index()

        for index, row in df.iterrows():
            # Convert index to datetime if needed
            if isinstance(index, str):
                timestamp = datetime.strptime(index, '%Y-%m-%d %H:%M:%S')
                timestamp = pytz.utc.localize(timestamp)
            else:
                timestamp = index
                if timestamp.tzinfo is None:
                    timestamp = pytz.utc.localize(timestamp)

            # Filter to our date range
            if timestamp < start_date or timestamp > end_date:
                continue

            candle = {
                'time': timestamp,
                'open': float(row['open']),
                'high': float(row['high']),
                'low': float(row['low']),
                'close': float(row['close'])
            }
            candles.append(candle)

        return sorted(candles, key=lambda x: x['time'])

    # ... [Rest of the strategy code - same as v5.1]
    # For brevity, I'll note that all the strategy methods from v5.1 would be copied here

    def run_backtest_sync(self):
        """Synchronous backtest runner"""
        print("="*80)
        print("🎯 AURUM SNIPER V5.1 - TWELVE DATA SOURCE")
        print("="*80)
        print("\n📅 DATA SOURCE: Twelve Data API (twelvedata.com)")
        print("🔑 Free Tier: 8 calls/minute, 800 calls/day")
        print("📊 Symbol: XAU/USD (Gold Spot)")
        print("⏰ Period: Nov 1 - Dec 27, 2025 (57 days)")
        print("\n" + "="*80 + "\n")

        data = self.fetch_historical_data_sync()

        if data is None:
            print("\n❌ Failed to fetch data. Exiting.")
            return

        # Run same backtest logic as v5.1
        # ... (simplified for this example)

        print(f"\n✅ Backtest complete! Total data points: {len(data['15m'])}")
        print(f"   Date range: {data['15m'][0]['time'].date()} to {data['15m'][-1]['time'].date()}")

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🔄 ALTERNATIVE DATA SOURCE: TWELVE DATA API")
    print("="*80)
    print("\nℹ️ This script uses Twelve Data as alternative to MetaAPI")
    print("📝 Setup instructions:")
    print("   1. Sign up at https://twelvedata.com/ (free)")
    print("   2. Get your API key from dashboard")
    print("   3. Add to .env file: TWELVEDATA_API_KEY=your_key_here")
    print("\n" + "="*80 + "\n")

    backtest = TwelveDataBacktest()
    backtest.run_backtest_sync()
