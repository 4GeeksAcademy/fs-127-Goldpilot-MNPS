#!/bin/bash

echo "=============================================="
echo "🚀 AGGRESSOR PULSE - LIVE TRADING BOT"
echo "=============================================="
echo ""
echo "Strategy: H1 → M15 EMA Channel → M5 CHoCH"
echo "Backtest: +9.55% ROI | 57% Win Rate"
echo ""
echo "=============================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 not found"
    exit 1
fi

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "✅ Activating virtual environment..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo "✅ Activating virtual environment..."
    source .venv/bin/activate
fi

# Set environment variables if not already set
if [ -z "$PORT" ]; then
    export PORT=8080
    echo "📌 PORT set to 8080"
fi

if [ -z "$WS_HOST" ]; then
    export WS_HOST="0.0.0.0"
    echo "📌 WS_HOST set to 0.0.0.0"
fi

echo ""
echo "🔗 Starting bot..."
echo "🌐 WebSocket will be available at: ws://localhost:$PORT"
echo "🌍 Frontend URL: http://localhost:5173 (if running)"
echo ""
echo "Press Ctrl+C to stop the bot"
echo ""
echo "=============================================="
echo ""

# Run the bot
python3 aggressor_pulse_live.py
