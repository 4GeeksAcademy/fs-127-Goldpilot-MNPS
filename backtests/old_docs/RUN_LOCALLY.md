# 🚀 Run Trading Bot Locally

Since your backend is running on your local machine (localhost), you need to also run the frontend locally to connect to it.

## Quick Start (2 Terminals)

### Terminal 1: Backend
```bash
# In project root
python3 aggressor_pulse_live.py
```

### Terminal 2: Frontend
```bash
cd frontend
npm run dev
```

Then open: http://localhost:5173

## What This Fixes

**Problem**:
- Backend: Running on `ws://localhost:8080` (your computer)
- Frontend: Deployed on Vercel at https://frontend-fawn-kappa.vercel.app
- Vercel can't connect to your localhost!

**Solution**:
Run frontend locally so it can connect to your local backend.

## Alternative: Deploy Backend to Cloud

If you want to use the Vercel frontend, you need to deploy the backend to a cloud service:

### Option A: Railway
1. Go to railway.app
2. Deploy `aggressor_pulse_live.py`
3. Set environment variable: `META_API_TOKEN`
4. Get your Railway URL (e.g., `wss://your-app.railway.app`)
5. Update Vercel environment: `VITE_WS_URL=wss://your-app.railway.app`

### Option B: Render
1. Go to render.com
2. Deploy `aggressor_pulse_live.py`
3. Set environment variable: `META_API_TOKEN`
4. Get your Render URL
5. Update Vercel environment variable

## Current Setup (Local)

For now, just run both locally:

```bash
# Terminal 1
python3 aggressor_pulse_live.py

# Terminal 2 (new terminal)
cd frontend
npm run dev
```

Open http://localhost:5173 and you'll see your wallets!
