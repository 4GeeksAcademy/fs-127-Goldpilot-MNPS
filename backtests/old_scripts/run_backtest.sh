#!/bin/bash
# Backtest Launcher Script
# Usage: ./run_backtest.sh <backtest_name>
# Example: ./run_backtest.sh internal_flow

if [ -z "$1" ]; then
    echo "Available backtests:"
    ls backtests/ | grep "^backtest_" | sed 's/backtest_//g' | sed 's/\.py//g'
    echo ""
    echo "Usage: ./run_backtest.sh <backtest_name>"
    echo "Example: ./run_backtest.sh internal_flow"
    exit 1
fi

BACKTEST_FILE="backtests/backtest_$1.py"

if [ ! -f "$BACKTEST_FILE" ]; then
    echo "Error: $BACKTEST_FILE not found"
    echo ""
    echo "Available backtests:"
    ls backtests/ | grep "^backtest_" | sed 's/backtest_//g' | sed 's/\.py//g'
    exit 1
fi

echo "🚀 Running backtest: $1"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 "$BACKTEST_FILE"
