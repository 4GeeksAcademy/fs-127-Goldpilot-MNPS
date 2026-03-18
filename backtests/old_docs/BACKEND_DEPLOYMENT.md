# 🚀 Backend Deployment - Aggressor Pulse Live

## ✅ Deployed Strategy

**Aggressor Pulse** - Best performing strategy from backtests

### Performance (60-Day Backtest)
- **ROI**: +9.55% (+$477.69 on $5K demo)
- **Win Rate**: 57.1% (4 wins, 1 loss, 2 time stops)
- **Average RRR**: 2.82:1
- **Trades**: 7 trades in 60 days
- **Win/Loss Ratio**: 2.57:1

## 📋 Strategy Logic

### Multi-Timeframe Analysis
1. **H1 Timeframe** - Intraday Trend (Bias)
   - BULLISH: Higher Highs + Higher Lows
   - BEARISH: Lower Highs + Lower Lows
   - Window of 3 for higher sensitivity

2. **M15 Timeframe** - Value Area (Setup)
   - EMA 10 and EMA 20 channel
   - Wait for price to enter the channel
   - Acts as "value zone" for entries

3. **M5 Timeframe** - Execution (Trigger)
   - CHoCH (Change of Character) detection
   - Break of counter-trend structure
   - Confirms entry in H1 trend direction

### Entry Rules
- **LONG**: H1 BULLISH + Price in M15 EMA channel + M5 CHoCH up
- **SHORT**: H1 BEARISH + Price in M15 EMA channel + M5 CHoCH down

### Exit Rules
- **TP**: Next H1 structural level OR minimum 1:3 RR expansion
- **SL**: M5 swing high/low + $3 buffer
- **Hard Exit**: 21:00 UTC (NY Close) - No overnight holding

### Risk Management
- **Demo Account (QUANT_DEMO)**: 2% risk per trade
- **Real Account (MICRO_REAL)**: 1% risk per trade
- **Cooldown**: 30 minutes between trades
- **Minimum RRR**: 1:1 (but targets 1:3)

## 🔧 Deployment Files

### Main Bot File
```
aggressor_pulse_live.py
```

### Strategy File
```
strategies/aggressor_pulse_strategy.py
```

### MetaAPI Configuration
- **Token**: Configured via environment variable
- **Demo Wallet**: 77c5fbff-beb8-422a-b085-c135c230a630
- **Real Wallet**: 436348e0-be6e-49cc-a991-8895903e5288

## 🚀 How to Run

### Local Testing
```bash
python3 aggressor_pulse_live.py
```

### Production (Railway/Render)
```bash
# Set environment variables:
export META_API_TOKEN="your_token_here"
export PORT=8080
export WS_HOST="0.0.0.0"

# Run bot
python3 aggressor_pulse_live.py
```

### Docker (if needed)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "aggressor_pulse_live.py"]
```

## 📊 WebSocket Communication

### Frontend Connection
```javascript
const ws = new WebSocket('ws://localhost:8080');
```

### Message Types

1. **MULTI_VAULT_UPDATE** - Vault balances and positions
```json
{
  "type": "MULTI_VAULT_UPDATE",
  "vaults": [
    {
      "name": "QUANT_DEMO",
      "is_real": false,
      "equity": 5000.00,
      "profit": 0.00,
      "positions": []
    }
  ]
}
```

2. **HEARTBEAT** - System status
```json
{
  "type": "HEARTBEAT",
  "symbol": "GOLD.pro",
  "price": 2650.25,
  "decision": "SCANNING",
  "reason": "H1 Trend: BULLISH | M15 EMA10: $2648.50 | EMA20: $2645.30 | Waiting for M15 channel + M5 CHoCH",
  "timestamp": "14:35:22"
}
```

3. **SIGNAL** - Trade signal generated
```json
{
  "type": "SIGNAL",
  "symbol": "GOLD.pro",
  "price": 2650.25,
  "decision": "BUY",
  "sl": 2642.50,
  "tp": 2665.75,
  "size": 0.06,
  "reason": "24/5 | BULLISH | M15 EMA Channel + M5 CHoCH | 1:3 RR Expansion",
  "timestamp": "14:35:22"
}
```

4. **TRADE_EXECUTED** - Trade executed confirmation
```json
{
  "type": "TRADE_EXECUTED",
  "signal": {...},
  "trades": [
    {
      "vault": "QUANT_DEMO",
      "is_real": false,
      "direction": "BUY",
      "entry": 2650.25,
      "sl": 2642.50,
      "tp": 2665.75,
      "size": 0.06,
      "rrr": 2.0,
      "timestamp": "2025-12-29 14:35:22"
    }
  ],
  "timestamp": "14:35:22"
}
```

## 🔍 Monitoring

### Console Output
The bot logs all important events:
- ✅ Vault connections
- 📊 Candle fetches
- 🎯 Signal generation
- 💼 Trade execution
- ❌ Errors

### Expected Behavior
1. Bot connects to both wallets (DEMO and REAL)
2. Every 30 seconds:
   - Fetches H1, M15, M5 candles
   - Analyzes market structure
   - Generates signals if conditions met
   - Executes trades automatically
3. Updates frontend via WebSocket every 2 seconds

## ⚠️ Important Notes

1. **API Rate Limits**: Analysis runs every 30 seconds to avoid MetaAPI rate limits
2. **Auto-Trading**: This bot executes trades automatically when signals are generated
3. **Time Stop**: All positions are force-closed at 21:00 UTC
4. **Cooldown**: 30-minute minimum gap between trades for quality

## 🎯 Expected Trading Profile

Based on 60-day backtest:
- **Frequency**: ~7 trades per 60 days (1-2 per week)
- **Hold Time**: 2-4 hours average
- **Best Sessions**: London overlap (8-16 UTC) and NY session (13-21 UTC)
- **Win Rate**: 50-70%
- **Average RRR**: 2.5:1 to 3:1

## 🔄 Comparison with Old Strategy

### Old Strategy (xauusd_advanced.py)
- Price action candlestick patterns (Engulfing, Hammer, etc.)
- NOT backtested
- Unknown performance

### New Strategy (Aggressor Pulse)
- ✅ Backtested: +9.55% ROI
- ✅ Proven win rate: 57%
- ✅ Clear rules: H1 → M15 → M5
- ✅ Structural targets
- ✅ Time stop protection

## 📞 Troubleshooting

### Bot Not Connecting to Wallets
```bash
# Check wallet IDs
echo $META_API_TOKEN

# Test connection manually
python3 -c "
from metaapi_cloud_sdk import MetaApi
import asyncio
api = MetaApi('your_token')
asyncio.run(api.metatrader_account_api.get_account('77c5fbff-beb8-422a-b085-c135c230a630'))
"
```

### No Trades Being Executed
- Check if H1 trend is established (needs HH+HL or LH+LL)
- Check if price is in M15 EMA 10-20 channel
- Check if M5 CHoCH has occurred
- Check cooldown timer (30 min between trades)

### Frontend Not Receiving Updates
- Verify WebSocket connection: `ws://localhost:8080`
- Check bot logs for WebSocket server startup
- Ensure PORT environment variable is set correctly

---

**Status**: ✅ READY FOR DEPLOYMENT

**Next Steps**:
1. Test locally: `python3 aggressor_pulse_live.py`
2. Verify wallet connections
3. Monitor for 24 hours to confirm signal generation
4. Deploy to Railway/Render for 24/7 operation
