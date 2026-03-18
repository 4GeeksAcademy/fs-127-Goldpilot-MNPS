# 🚀 Deploy Backend to Cloud (Railway)

## ✅ Files Ready for Deployment

I've created all necessary deployment files:
- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - Start command
- ✅ `railway.json` - Railway configuration
- ✅ `runtime.txt` - Python version

---

## 🚂 Deploy to Railway (Recommended)

### Step 1: Push to GitHub

```bash
cd /Users/mariusargint/Projects/Forex_bot

# Initialize git (if not already)
git init

# Add all files
git add aggressor_pulse_live.py requirements.txt Procfile railway.json runtime.txt strategies/

# Create .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
.DS_Store
venv/
.venv/
.env
*.log
node_modules/
frontend/node_modules/
frontend/dist/
.vercel/
backtests/
strategy_reports/
*.json
!railway.json
!package.json
!vercel.json
EOF

# Commit
git add .gitignore
git commit -m "Deploy: Aggressor Pulse trading bot to Railway"

# Create GitHub repo and push
# (Follow GitHub instructions to create repo and add remote)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Railway

1. **Go to**: https://railway.app
2. **Sign up** with GitHub
3. **Click**: "New Project"
4. **Select**: "Deploy from GitHub repo"
5. **Choose**: Your Forex_bot repository
6. **Railway will**:
   - Auto-detect Python
   - Install dependencies from `requirements.txt`
   - Run `python3 aggressor_pulse_live.py`

### Step 3: Set Environment Variable

In Railway dashboard:
1. Go to your project
2. Click **"Variables"** tab
3. Add variable:
   - **Key**: `META_API_TOKEN`
   - **Value**: Your MetaAPI token (the long JWT token)
4. Click **"Add"**

### Step 4: Get Your URL

1. Go to **"Settings"** tab
2. Click **"Generate Domain"**
3. Copy your URL (e.g., `https://your-app.up.railway.app`)
4. Note: Use `wss://` for WebSocket (not `https://`)

---

## 🔧 Update Vercel Frontend

### Option A: Via Vercel Dashboard

1. Go to: https://vercel.com/dashboard
2. Select your `frontend` project
3. Go to **Settings** → **Environment Variables**
4. Add new variable:
   - **Key**: `VITE_WS_URL`
   - **Value**: `wss://your-app.up.railway.app` (your Railway URL)
5. Click **"Save"**
6. Go to **Deployments** → Click **"Redeploy"**

### Option B: Via Command Line

```bash
cd frontend
npx vercel env add VITE_WS_URL production
# Enter: wss://your-app.up.railway.app

# Redeploy
npx vercel --prod
```

---

## 🌐 Alternative: Deploy to Render

If you prefer Render (has free tier):

### Step 1: Create Render Account

1. Go to: https://render.com
2. Sign up with GitHub

### Step 2: Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `forex-trading-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python3 aggressor_pulse_live.py`
4. Click **"Create Web Service"**

### Step 3: Add Environment Variable

1. Go to **"Environment"** tab
2. Add:
   - **Key**: `META_API_TOKEN`
   - **Value**: Your MetaAPI token
3. Click **"Save Changes"**

### Step 4: Get URL

- Render provides URL like: `https://forex-trading-bot-xxxx.onrender.com`
- For WebSocket use: `wss://forex-trading-bot-xxxx.onrender.com`

---

## ✅ Verify Deployment

### Check Backend is Running

```bash
# Test health endpoint
curl https://your-app.up.railway.app/health

# Should return: OK
```

### Test WebSocket Connection

```bash
python3 << 'EOF'
import asyncio
import websockets

async def test():
    uri = "wss://your-app.up.railway.app"  # Your Railway URL
    async with websockets.connect(uri) as ws:
        msg = await ws.recv()
        print(f"✅ Connected! Received: {msg[:100]}...")

asyncio.run(test())
EOF
```

### Check Frontend Connection

1. Open: https://frontend-fawn-kappa.vercel.app
2. Login with password: `aurum2024`
3. Should see vault balances and live price

---

## 🔍 Troubleshooting

### Railway Logs

View logs in Railway dashboard:
1. Go to your project
2. Click **"Deployments"**
3. Click on latest deployment
4. View logs in real-time

### Common Issues

**Build Failed**:
- Check `requirements.txt` has correct package versions
- Ensure Python 3.9 is specified in `runtime.txt`

**WebSocket Not Connecting**:
- Verify environment variable `META_API_TOKEN` is set
- Check Railway logs for errors
- Ensure using `wss://` (not `ws://`) for HTTPS

**Frontend Can't Connect**:
- Verify `VITE_WS_URL` in Vercel is correct
- Must use `wss://` protocol
- Redeploy Vercel frontend after updating env variable

---

## 💰 Cost

### Railway
- **Free Tier**: $5 credit/month (good for testing)
- **Hobby Plan**: $5/month (recommended for production)
- **Usage**: Your bot should use ~1-2 GB RAM

### Render
- **Free Tier**: Available (sleeps after 15 min inactivity)
- **Starter Plan**: $7/month (always on)

**Recommendation**: Start with Railway free tier to test, then upgrade if needed.

---

## 📊 Post-Deployment Checklist

- ✅ Backend deployed to Railway/Render
- ✅ Environment variable `META_API_TOKEN` set
- ✅ Backend URL obtained (e.g., `https://xxx.railway.app`)
- ✅ Vercel environment variable `VITE_WS_URL` updated to `wss://xxx.railway.app`
- ✅ Vercel frontend redeployed
- ✅ Tested WebSocket connection
- ✅ Vault balances showing on frontend

---

## 🎉 Success!

Once deployed, your trading bot will run 24/7 in the cloud:
- ✅ No need to keep your computer on
- ✅ Frontend on Vercel connects to backend on Railway
- ✅ Auto-restarts if it crashes
- ✅ Scales automatically

**Your URLs**:
- Frontend: https://frontend-fawn-kappa.vercel.app
- Backend: wss://your-app.up.railway.app (WebSocket)

---

## 📞 Need Help?

- Railway Docs: https://docs.railway.app
- Render Docs: https://render.com/docs
- Check logs in Railway/Render dashboard
- Test WebSocket with the Python script above
