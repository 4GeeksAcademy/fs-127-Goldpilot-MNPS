# Alternative Data Sources for Gold (XAUUSD) Backtesting

## Problem with MetaAPI
MetaAPI historical data is limited and only returns recent data regardless of date range requested. For proper 60-90 day backtesting, we need alternative sources.

---

## ✅ RECOMMENDED: Twelve Data API

**Best free option for forex/commodities historical data**

### Setup (3 minutes)
```bash
# 1. Install library
pip3 install twelvedata

# 2. Get free API key
# Visit: https://twelvedata.com/
# Sign up (free)
# Copy API key from dashboard

# 3. Add to .env file
echo "TWELVEDATA_API_KEY=your_api_key_here" >> .env
```

### Free Tier Limits
- **8 API calls per minute**
- **800 API calls per day**
- **5000 data points per request**
- **Real-time & historical data**

### Coverage
- ✅ Gold (XAU/USD)
- ✅ Forex pairs (all majors)
- ✅ Multiple timeframes (1m, 5m, 15m, 1h, 4h, 1d)
- ✅ Up to 12 years historical data

### Sample Usage
```python
from twelvedata import TDClient

td = TDClient(apikey="YOUR_API_KEY")

# Fetch 15m Gold data
ts = td.time_series(
    symbol="XAU/USD",
    interval="15min",
    outputsize=5000,  # Last 5000 candles
    timezone="UTC"
)

df = ts.as_pandas()
print(df.head())
```

### Backtest Script
```bash
python3 backtest_twelvedata.py
```

---

## Alternative Option 1: Alpha Vantage

### Pros
- Free tier available
- Reliable data
- Good documentation

### Cons
- **Only 25 API calls per day** (very limited)
- **500 data points per call** (max)
- Would need 12+ API calls for 60 days = multi-day fetch

### Setup
```bash
pip3 install alpha-vantage

# Get key from: https://www.alphavantage.co/support/#api-key
# Add to .env: ALPHA_VANTAGE_KEY=your_key
```

### Usage
```python
from alpha_vantage.foreignexchange import ForeignExchange

fx = ForeignExchange(key='YOUR_API_KEY', output_format='pandas')
data, meta = fx.get_currency_exchange_intraday(
    from_symbol='XAU',
    to_symbol='USD',
    interval='15min',
    outputsize='full'
)
```

### Verdict
⚠️ **Not recommended** - Daily API limit too restrictive for backtesting

---

## Alternative Option 2: Polygon.io

### Pros
- Comprehensive data
- Good free tier
- Clean API

### Cons
- **5 API calls per minute** (free tier)
- Forex data requires **paid plan** ($99/month minimum)

### Verdict
❌ **Not suitable** - Free tier doesn't include forex/commodities

---

## Alternative Option 3: MT5 Python Direct

### Pros
- Direct access to broker data
- No API limits
- Same data as MetaAPI (but local control)

### Cons
- Requires MT5 terminal installed
- Broker-dependent data availability
- More complex setup

### Setup
```bash
pip3 install MetaTrader5

# Requires:
# 1. MetaTrader 5 terminal installed
# 2. Login to your broker account
# 3. Python library connects to local MT5
```

### Usage
```python
import MetaTrader5 as mt5
from datetime import datetime

# Initialize
if not mt5.initialize():
    print("MT5 init failed")
    quit()

# Fetch data
rates = mt5.copy_rates_range(
    "XAUUSD",
    mt5.TIMEFRAME_M15,
    datetime(2025, 11, 1),
    datetime(2025, 12, 27)
)

mt5.shutdown()
```

### Verdict
✅ **Good option IF you have MT5 installed** - Direct broker access

---

## Alternative Option 4: CSV Export from TradingView

### Pros
- Accurate tick-level data
- No API limits
- Reliable source

### Cons
- Manual export process
- Not automated
- Time-consuming for multiple timeframes

### Process
1. Go to TradingView.com
2. Open XAUUSD chart
3. Set timeframe (15m)
4. Set date range (Nov 1 - Dec 27, 2025)
5. Export → CSV
6. Repeat for 1h, 4h timeframes
7. Load into backtest script

### Sample Code
```python
import pandas as pd

# Load exported CSV
df_15m = pd.read_csv('XAUUSD_15m_nov_dec.csv')
df_1h = pd.read_csv('XAUUSD_1h_nov_dec.csv')
df_4h = pd.read_csv('XAUUSD_4h_nov_dec.csv')

# Convert to candle format
candles_15m = []
for _, row in df_15m.iterrows():
    candle = {
        'time': pd.to_datetime(row['time']),
        'open': row['open'],
        'high': row['high'],
        'low': row['low'],
        'close': row['close']
    }
    candles_15m.append(candle)
```

### Verdict
✅ **Reliable fallback** - Use if API sources fail

---

## Alternative Option 5: OANDA API

### Pros
- Direct broker data
- Free practice account
- Good historical coverage
- Reliable forex/metal data

### Cons
- Requires OANDA account (free demo available)
- API limits on free tier
- Some setup complexity

### Setup
```bash
pip3 install oandapyV20

# Get account from: https://www.oanda.com/
# Practice account = free
# Get API key from account dashboard
```

### Usage
```python
from oandapyV20 import API
from oandapyV20.endpoints.instruments import InstrumentsCandles

api = API(access_token="YOUR_PRACTICE_TOKEN")

params = {
    "from": "2025-11-01T00:00:00Z",
    "to": "2025-12-27T23:59:59Z",
    "granularity": "M15",  # 15-minute candles
    "price": "M"  # Midpoint pricing
}

r = InstrumentsCandles(instrument="XAU_USD", params=params)
api.request(r)

candles = r.response['candles']
```

### Verdict
✅ **Solid option** - Good data quality, practice account free

---

## Comparison Matrix

| Source | Free? | API Limit | Data Quality | Setup Time | Recommended |
|--------|-------|-----------|--------------|------------|-------------|
| **Twelve Data** | ✅ Yes | 800/day | ⭐⭐⭐⭐⭐ | 3 min | ✅ **BEST** |
| **OANDA API** | ✅ Yes (demo) | Moderate | ⭐⭐⭐⭐⭐ | 10 min | ✅ Good |
| **MT5 Direct** | ✅ Yes | None | ⭐⭐⭐⭐⭐ | 15 min | ✅ If installed |
| **TradingView CSV** | ✅ Yes | None | ⭐⭐⭐⭐⭐ | 20 min | ✅ Fallback |
| Alpha Vantage | ✅ Yes | 25/day | ⭐⭐⭐⭐ | 3 min | ⚠️ Too limited |
| Polygon.io | ❌ Paid | 5/min | ⭐⭐⭐⭐⭐ | 3 min | ❌ Forex paywalled |
| MetaAPI | ✅ Yes | 1500/day | ⭐⭐⭐ | 0 min | ⚠️ Limited history |

---

## RECOMMENDED WORKFLOW

### Step 1: Try Twelve Data (Primary)
```bash
# Install
pip3 install twelvedata

# Get free key: https://twelvedata.com/
# Add to .env: TWELVEDATA_API_KEY=your_key

# Run backtest
python3 backtest_twelvedata.py
```

**Expected**: 60 days of data, 3-4 API calls total

### Step 2: If Twelve Data Fails → Try OANDA
```bash
# Install
pip3 install oandapyV20

# Get free practice account: https://www.oanda.com/
# Add to .env: OANDA_PRACTICE_TOKEN=your_token

# Run OANDA backtest (create script)
```

### Step 3: If Both Fail → Manual TradingView Export
1. Go to TradingView.com/chart
2. Symbol: XAUUSD
3. Interval: 15m
4. Date: Nov 1 - Dec 27, 2025
5. Export → CSV
6. Repeat for 1h, 4h
7. Load into backtest script

---

## Quick Implementation: Twelve Data

I've created `backtest_twelvedata.py` for you. Here's how to use it:

### 1. Get API Key
```
Visit: https://twelvedata.com/
Sign up (30 seconds, free)
Dashboard → API Key → Copy
```

### 2. Add to .env
```bash
echo "TWELVEDATA_API_KEY=your_actual_key_here" >> .env
```

### 3. Run Backtest
```bash
python3 backtest_twelvedata.py
```

### Expected Output
```
🎯 AURUM SNIPER V5.1 - TWELVE DATA SOURCE
================================================================================
📊 Fetching Gold (XAU/USD) historical data...
   📈 Fetching 15m candles...
   ✅ Received 2,688 15m candles
   📈 Fetching 1h candles...
   ✅ Received 672 1h candles
   📈 Fetching 4h candles...
   ✅ Received 168 4h candles

✅ Data fetch complete!
🔍 Running backtest on 60 days of data...
```

---

## Troubleshooting

### Issue: "API rate limit exceeded"
**Solution**: Free tier = 8 calls/minute. Add `time.sleep(8)` between requests

### Issue: "No data returned"
**Solution**:
- Check symbol format (Twelve Data uses "XAU/USD" not "XAUUSD")
- Verify date range is valid
- Check API key is correct

### Issue: "Import error: twelvedata"
**Solution**: `pip3 install twelvedata --upgrade`

### Issue: "Data only goes back 30 days"
**Solution**:
- Free tier may have historical limits
- Use `outputsize=5000` parameter
- Consider TradingView CSV export

---

## Data Quality Validation

Before running full backtest, validate data quality:

```python
# Check for gaps
def validate_data(candles):
    print(f"Total candles: {len(candles)}")
    print(f"Date range: {candles[0]['time']} to {candles[-1]['time']}")

    # Check for time gaps > 1 hour
    for i in range(1, len(candles)):
        gap = (candles[i]['time'] - candles[i-1]['time']).total_seconds() / 3600
        if gap > 1:
            print(f"⚠️ Gap detected: {gap:.1f} hours between {candles[i-1]['time']} and {candles[i]['time']}")

    # Check for invalid prices
    for c in candles:
        if c['high'] < c['low']:
            print(f"❌ Invalid candle: {c}")
        if c['close'] > c['high'] or c['close'] < c['low']:
            print(f"❌ Close outside range: {c}")

    print("✅ Data validation complete")
```

---

## Recommended Next Steps

1. **Today**: Get Twelve Data API key (3 minutes)
2. **Today**: Run `backtest_twelvedata.py` for 60-day validation
3. **If successful**: Update `backtest_output_new.log` with extended results
4. **If fails**: Try OANDA API as backup
5. **Last resort**: Manual TradingView CSV export

---

## Cost Comparison (If Going Paid)

If you need more data in future:

| Service | Monthly Cost | Includes |
|---------|--------------|----------|
| Twelve Data Basic | $79/mo | Unlimited API calls, real-time |
| OANDA (live account) | Free | Free with funded account ($100 min) |
| Alpha Vantage Premium | $50/mo | 1200 calls/min |
| Polygon.io Forex | $99/mo | Forex + stocks real-time |
| MetaAPI Cloud | $100/mo | 10 accounts, unlimited history |

**Recommendation**: Stick with free tier for now (Twelve Data or OANDA demo)

---

*Last Updated: 2025-12-27*
*Status: Twelve Data implementation ready*
*Next: Get API key and run 60-day backtest*
