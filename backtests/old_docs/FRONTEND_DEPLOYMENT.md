# Frontend Deployment Guide

Your backend is now live on Railway! Now let's deploy the frontend.

## Your Railway Backend URL

First, find your Railway URL from the dashboard. It should look like:
`https://forex-bot-production-xxxx.up.railway.app`

## Deploy Frontend to Vercel

### Method 1: Using Vercel Dashboard (Easiest)

1. **Go to Vercel**: https://vercel.com/new

2. **Import your GitHub repository:**
   - Click "Import Project"
   - Select "Import Git Repository"
   - Choose `mariusargint/Forex_bot`

3. **Configure the project:**
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

4. **Add Environment Variable:**
   - Click "Environment Variables"
   - Add:
     - Name: `VITE_WS_URL`
     - Value: `wss://your-railway-url.railway.app` (replace with your actual URL)
   - **Important**: Use `wss://` (not `ws://`) for production!

5. **Deploy:**
   - Click "Deploy"
   - Wait for build to complete
   - Vercel will give you a URL like `forex-bot.vercel.app`

### Method 2: Using Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend directory
cd frontend

# Login to Vercel
vercel login

# Set environment variable
vercel env add VITE_WS_URL production

# When prompted, enter: wss://your-railway-url.railway.app

# Deploy
vercel --prod
```

## Alternative: Deploy to Netlify

1. **Go to Netlify**: https://app.netlify.com/start

2. **Import repository:**
   - Select GitHub
   - Choose `mariusargint/Forex_bot`

3. **Build settings:**
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/dist`

4. **Environment variables:**
   - Go to Site Settings → Build & Deploy → Environment
   - Add: `VITE_WS_URL` = `wss://your-railway-url.railway.app`

5. **Deploy site**

## Update Local Environment File

For your own reference, update the local production env file:

```bash
# Update frontend/.env.production
echo "VITE_WS_URL=wss://your-railway-url.railway.app" > frontend/.env.production

# Commit (optional)
git add frontend/.env.production
git commit -m "Update production WebSocket URL"
git push origin main
```

## Testing the Deployment

Once both backend and frontend are deployed:

1. **Visit your frontend URL** (Vercel/Netlify provided)
2. **Check console for connection:** Should see "✅ UPLINK ESTABLISHED"
3. **Verify data flowing:**
   - Live price updates
   - Chart rendering
   - Vault information displaying

## Troubleshooting

### WebSocket won't connect:
- Ensure you're using `wss://` (not `ws://`)
- Check Railway logs for WebSocket server running
- Verify environment variable is set correctly in Vercel/Netlify

### CORS issues:
- The WebSocket server doesn't need CORS for WebSocket connections
- If you see CORS errors, they're from HTTP requests (which we're not making)

### Railway backend not responding:
- Check Railway environment variables are set
- Verify `META_API_TOKEN` is configured
- Look for logs: "🚀 WebSocket Server Running"

## Production URLs

After deployment, you'll have:
- **Backend**: `https://your-app.railway.app` (WebSocket at `wss://your-app.railway.app`)
- **Frontend**: `https://your-app.vercel.app` or `https://your-app.netlify.app`

Both should now be communicating and your trading bot is fully live!

## Important Security Notes

- ✅ Backend is on Railway (secure, paid infrastructure)
- ✅ Frontend is on Vercel/Netlify (CDN, fast)
- ✅ WebSocket uses WSS (encrypted)
- ⚠️ Auto-trading is ACTIVE - monitor your accounts
- ⚠️ Start with DEMO account to test

---

**Your bot is now production-ready!** 🚀
