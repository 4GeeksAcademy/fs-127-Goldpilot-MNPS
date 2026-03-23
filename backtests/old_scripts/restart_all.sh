#!/bin/bash

echo "🛑 Stopping everything..."
pkill -f "aggressor_pulse_live.py"
pkill -f "vite"
sleep 3

echo "🧹 Cleaning up..."
rm -f /tmp/bot_pid.txt /tmp/frontend_pid.txt

echo "🚀 Starting backend..."
cd /Users/mariusargint/Projects/Forex_bot
nohup python3 -u aggressor_pulse_live.py > /tmp/aggressor_pulse.log 2>&1 &
echo $! > /tmp/bot_pid.txt
echo "   Backend PID: $(cat /tmp/bot_pid.txt)"
sleep 5

echo "🚀 Starting frontend..."
cd /Users/mariusargint/Projects/Forex_bot/frontend
npm run dev > /tmp/frontend.log 2>&1 &
echo $! > /tmp/frontend_pid.txt
echo "   Frontend PID: $(cat /tmp/frontend_pid.txt)"
sleep 5

echo ""
echo "✅ System Started!"
echo ""
echo "📊 Backend logs: tail -f /tmp/aggressor_pulse.log"
echo "🌐 Frontend: http://localhost:5173"
echo "🔑 Password: aurum2024"
echo ""
echo "⏳ Wait 10 seconds after login for data to appear"
