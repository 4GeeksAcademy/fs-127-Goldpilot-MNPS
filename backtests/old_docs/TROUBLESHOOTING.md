# 🔧 Troubleshooting Guide

## Issue: Frontend Shows "Connecting..." or Equity = $0

### ✅ Quick Fix Steps

1. **Hard Refresh the Browser**
   - Mac: `Cmd + Shift + R`
   - Windows: `Ctrl + Shift + R`
   - Or clear browser cache completely

2. **Login to the Dashboard**
   - Password: `aurum2024`
   - The WebSocket only connects AFTER login

3. **Check Both Services Are Running**
   ```bash
   ps aux | grep "aggressor_pulse_live.py\|vite" | grep -v grep
   ```
   Should show 2 processes

4. **Restart Everything**
   ```bash
   # Stop all
   pkill -f "aggressor_pulse_live.py"
   pkill -f "vite"

   # Start backend
   nohup python3 -u aggressor_pulse_live.py > /tmp/aggressor_pulse.log 2>&1 &

   # Start frontend
   cd frontend && npm run dev
   ```

5. **Test WebSocket Directly**
   Open in browser: `file:///Users/mariusargint/Projects/Forex_bot/test_connection.html`

   If this shows data, the backend is working. The issue is frontend connection.

---

## Common Issues

### Issue 1: "Connecting..." Forever

**Cause**: Frontend can't reach WebSocket server

**Check**:
```bash
# Is backend listening?
lsof -i:8080 | grep LISTEN
```

**Fix**:
- Make sure backend is running
- Check firewall isn't blocking port 8080
- Try restarting backend

### Issue 2: Equity Shows $0

**Cause**: Frontend received data but not displaying correctly

**Check**:
1. Did you login? (password: `aurum2024`)
2. Open browser console (F12) - any errors?
3. Check backend logs:
   ```bash
   tail -f /tmp/aggressor_pulse.log
   ```

**Fix**:
- Hard refresh browser
- Clear all browser data for localhost
- Restart frontend

### Issue 3: MetaMask Error

**Cause**: Harmless browser extension search

**Fix**:
- Ignore it (doesn't affect functionality)
- OR disable MetaMask extension
- OR use Incognito/Private window

### Issue 4: No Positions Showing

**Cause**: MetaAPI reports 0 positions

**Check**:
```bash
tail /tmp/aggressor_pulse.log | grep "positions"
```

**Reality Check**:
- Do you actually have open positions in MT4/MT5?
- Check the correct account
- Give it 30 seconds to sync

---

## Verification Steps

### 1. Backend is Working
```bash
# Should show vault data every 10 seconds
tail -f /tmp/aggressor_pulse.log
```

Expected output:
```
💼 Vaults Updated: 2 accounts, 0 positions
📡 Fetching candles for analysis... (Live Price: $4463.71)
📊 Fetched 173 1h candles
```

### 2. Frontend is Running
```bash
# Check if Vite dev server is running
lsof -i:5173
```

### 3. WebSocket Connection Exists
```bash
# Should show ESTABLISHED connection
netstat -an | grep 8080 | grep ESTABLISHED
```

### 4. Manual WebSocket Test
```bash
python3 << 'EOF'
import asyncio
import websockets

async def test():
    async with websockets.connect("ws://localhost:8080") as ws:
        msg = await ws.recv()
        print(f"✅ Received: {msg[:100]}...")

asyncio.run(test())
EOF
```

---

## Nuclear Option: Full Restart

```bash
#!/bin/bash

echo "🛑 Stopping everything..."
pkill -f "aggressor_pulse_live.py"
pkill -f "vite"
pkill -f "node"
sleep 3

echo "🧹 Cleaning up..."
rm -f /tmp/bot_pid.txt /tmp/frontend_pid.txt
rm -f /tmp/aggressor_pulse.log /tmp/frontend.log

echo "🚀 Starting backend..."
cd /Users/mariusargint/Projects/Forex_bot
nohup python3 -u aggressor_pulse_live.py > /tmp/aggressor_pulse.log 2>&1 &
echo $! > /tmp/bot_pid.txt
sleep 5

echo "🚀 Starting frontend..."
cd frontend
npm run dev > /tmp/frontend.log 2>&1 &
echo $! > /tmp/frontend_pid.txt
sleep 3

echo ""
echo "✅ Done!"
echo ""
echo "📊 Backend logs: tail -f /tmp/aggressor_pulse.log"
echo "🌐 Frontend: http://localhost:5173"
echo "🔑 Password: aurum2024"
```

Save this as `restart_all.sh` and run:
```bash
chmod +x restart_all.sh
./restart_all.sh
```

---

## Expected Behavior

### After Login

1. **Within 2 seconds**: Should see "✅ UPLINK ESTABLISHED" in logs
2. **Within 5 seconds**: Vault cards appear with balances
3. **Within 10 seconds**: Live price updates
4. **Every 10 seconds**: Price and vault data refresh

### If You See

- **Connecting...**: Frontend hasn't established WebSocket yet
  - Wait 5 seconds OR hard refresh

- **$0 Total Equity**: Data hasn't loaded yet
  - Wait 10 seconds OR check backend logs

- **No vault cards**: Not logged in
  - Login with password: `aurum2024`

---

## Still Not Working?

### Check This
1. **Are you logged in?** The WebSocket only connects AFTER login
2. **Is backend running?** `ps aux | grep aggressor_pulse_live.py | grep -v grep`
3. **Is frontend running?** `ps aux | grep vite | grep -v grep`
4. **Any errors?** `tail -30 /tmp/aggressor_pulse.log`

### Try This
1. Open http://localhost:5173
2. Open browser console (F12 → Console tab)
3. Look for errors or "UPLINK ESTABLISHED" message
4. If you see "UPLINK ESTABLISHED", data should appear within 5 seconds

### Contact Info
- Check backend: `tail -f /tmp/aggressor_pulse.log`
- Check frontend console (F12 in browser)
- Both should show active connections

---

## Success Checklist

- ✅ Backend running (check with `ps aux | grep aggressor`)
- ✅ Frontend running (check with `ps aux | grep vite`)
- ✅ Port 8080 listening (check with `lsof -i:8080`)
- ✅ Port 5173 open (check with `lsof -i:5173`)
- ✅ Logged in to frontend (password: aurum2024)
- ✅ Browser console shows "UPLINK ESTABLISHED"
- ✅ Vault cards visible with balances

If all checked, wait 10 seconds for data to populate!
