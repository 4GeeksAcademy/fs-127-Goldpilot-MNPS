# 🚀 Quick Start Guide - Forex Trading Bot

## ✅ What's Deployed

### Frontend (Vercel)
- **URL**: https://frontend-fawn-kappa.vercel.app
- **Status**: ✅ Live and working
- **Features**: Live price display, vault monitoring, trade notifications

### Backend Strategy
- **File**: `aggressor_pulse_live.py`
- **Strategy**: Aggressor Pulse (+9.55% ROI backtested)
- **Status**: ✅ Ready to run

## 🎯 Run Your Trading Bot (3 Steps)

### Step 1: Start Backend
```bash
./run_live_bot.sh
```

Or manually:
```bash
python3 aggressor_pulse_live.py
```

### Step 2: Open Frontend
Visit: https://frontend-fawn-kappa.vercel.app

OR run locally:
```bash
cd frontend
npm run dev
```

### Step 3: Monitor Trades
Watch the console output for:
- ✅ Wallet connections
- 📊 Market analysis
- 🎯 Trade signals
- 💼 Trade executions

## 📊 Strategy Overview

**Aggressor Pulse** uses a 3-timeframe approach:

1. **H1** - Determines intraday trend (BULLISH/BEARISH)
2. **M15** - EMA 10-20 channel defines value area
3. **M5** - CHoCH (Change of Character) triggers entry

**Performance (60-day backtest)**:
- ROI: +9.55% (+$477.69)
- Win Rate: 57.1%
- Avg RRR: 2.82:1
- Trades: 7 in 60 days

## 🔧 Configuration

### Wallets (MetaAPI)
- **Demo**: QUANT_DEMO (2% risk per trade)
- **Real**: MICRO_REAL (1% risk per trade)

### Risk Settings
- Cooldown: 30 minutes between trades
- Time stop: 21:00 UTC (forces close all positions)
- Min RRR: 1:1 (targets 1:3)

## 📁 Project Structure

```
Forex_bot/
├── aggressor_pulse_live.py      # Main bot (CURRENT)
├── xauusd_advanced.py            # Old bot (NOT USED)
├── strategies/
│   ├── aggressor_pulse_strategy.py  # Strategy logic
│   ├── internal_flow_strategy.py    # Alternative (+7.23% ROI)
│   └── golden_ratio_strategy.py     # Alternative (+5.58% ROI)
├── backtests/                    # All backtest scripts
├── frontend/                     # React frontend (deployed)
└── run_live_bot.sh              # Quick start script
```

## ⚠️ Important Notes

1. **Auto-Trading Enabled**: Bot executes trades automatically when signals are generated
2. **Analysis Frequency**: Every 30 seconds (to avoid API limits)
3. **Expected Trading**: ~7 trades per 60 days (1-2 per week)
4. **WebSocket**: Bot communicates with frontend via ws://localhost:8080

## 🔍 What Changed

### Before (xauusd_advanced.py)
- ❌ Price action candlestick patterns
- ❌ Not backtested
- ❌ Unknown performance

### Now (aggressor_pulse_live.py)
- ✅ Aggressor Pulse strategy
- ✅ Backtested: +9.55% ROI
- ✅ Proven: 57% win rate
- ✅ Clear structure-based rules
- ✅ Time stop protection

## 📞 Troubleshooting

### Bot won't connect to wallets
**Check**: MetaAPI token is set correctly
```bash
echo $META_API_TOKEN
```

### No trades executing
**Reasons**:
- H1 trend not established (needs HH+HL or LH+LL)
- Price not in M15 EMA channel
- No M5 CHoCH detected
- Cooldown active (30 min between trades)

### Frontend shows "Connecting..."
**Check**:
1. Backend is running: `python3 aggressor_pulse_live.py`
2. WebSocket port is 8080
3. No firewall blocking port 8080

## 🎯 Expected Behavior

### First 5 Minutes
1. Bot connects to QUANT_DEMO wallet
2. Bot connects to MICRO_REAL wallet
3. Fetches H1, M15, M5 candles
4. Analyzes market structure
5. Displays: "H1 Trend: BULLISH/BEARISH/NEUTRAL"

### During Trading Hours (7:00-21:00 UTC)
- Scans every 30 seconds
- Shows current H1 trend
- Shows M15 EMA levels
- Generates signal when all conditions align

### When Signal Generated
- Console: "🎯 SIGNAL: BUY/SELL @ $XXXX.XX"
- Auto-executes on both wallets
- Frontend receives notification
- Cooldown timer starts (30 min)

## 📈 Monitoring Performance

### View Trade History
Trade history is stored in the strategy instances:
```python
# Access from bot console or add logging
demo_strategy.trades  # List of all trades
demo_strategy.get_stats()  # Performance stats
```

### Key Metrics to Watch
- Win Rate (target: 50-70%)
- Average RRR (target: 2.5:1+)
- Total ROI (target: +5% monthly)

## 🚀 Next Steps

1. **Run locally**: `./run_live_bot.sh`
2. **Monitor for 24 hours** to see signal generation
3. **Deploy to cloud** (Railway/Render) for 24/7 operation
4. **Track performance** vs backtest results

---

## 🎉 You're Ready!

Your bot is configured with the best-performing strategy from 60 days of backtesting.

**Run it**: `./run_live_bot.sh`

**Monitor**: https://frontend-fawn-kappa.vercel.app

**Enjoy automated trading!** 🚀
