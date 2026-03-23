# Railway Deployment Guide - Aurum Architect

This guide will help you deploy your Forex trading bot to Railway.

## Prerequisites

1. A Railway account ([sign up here](https://railway.app))
2. Railway CLI installed (optional): `npm i -g @railway/cli`
3. Git repository pushed to GitHub/GitLab

## Deployment Steps

### 1. Create a New Project on Railway

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your GitHub account and select your repository
5. Railway will automatically detect the project and start building

### 2. Configure Environment Variables

In your Railway project dashboard, go to **Variables** tab and add:

#### Required Variables:

```bash
META_API_TOKEN=your_metaapi_token_here
PORT=8080
WS_HOST=0.0.0.0
```

#### Optional Variables:

```bash
FRONTEND_PORT=3000
```

### 3. Update Frontend WebSocket URL

After deployment, Railway will provide you with a public URL (e.g., `https://your-app.railway.app`).

1. Update `frontend/.env.production`:
   ```
   VITE_WS_URL=wss://your-app.railway.app
   ```

2. Commit and push the change:
   ```bash
   git add frontend/.env.production
   git commit -m "Update production WebSocket URL"
   git push
   ```

3. Railway will automatically redeploy

### 4. Access Your Application

#### Backend WebSocket:
- Your backend will be available at: `wss://your-app.railway.app`

#### Frontend:
Since Railway runs a single service, you have two options:

**Option A: Deploy Frontend Separately (Recommended)**
1. Deploy the frontend to Vercel/Netlify:
   ```bash
   cd frontend
   npm run build
   # Deploy dist folder to Vercel/Netlify
   ```

**Option B: Serve Frontend from Backend**
1. Update `Procfile`:
   ```
   web: python serve_frontend.py & python xauusd_advanced.py
   ```

## Configuration Files Explained

### `railway.json`
- Configures Railway-specific deployment settings
- Sets restart policy for automatic recovery

### `Procfile`
- Tells Railway what command to run
- Current: `web: python xauusd_advanced.py`

### `nixpacks.toml`
- Defines build phases and dependencies
- Installs Python 3.11 and Node.js 20
- Builds frontend during deployment

### `requirements.txt`
- Python dependencies for the backend
- MetaAPI SDK, pandas, websockets, etc.

## Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `META_API_TOKEN` | Your MetaAPI access token | - | Yes |
| `PORT` | WebSocket server port | 8080 | No |
| `WS_HOST` | WebSocket bind address | 0.0.0.0 | No |
| `FRONTEND_PORT` | Frontend server port (if using serve_frontend.py) | 3000 | No |

## Monitoring and Logs

### View Logs:
1. Go to Railway dashboard
2. Click on your deployment
3. Go to "Deployments" tab
4. Click on latest deployment to view logs

### Check WebSocket Connection:
Look for these logs:
```
🚀 WebSocket Server Running on ws://0.0.0.0:8080
⚡ Golden Triad Strategy: ACTIVE
✅ VAULT SYNCED: QUANT_DEMO
✅ VAULT SYNCED: MICRO_REAL
```

## Troubleshooting

### WebSocket Connection Fails:
1. Ensure `PORT` environment variable is set
2. Check Railway logs for errors
3. Verify MetaAPI token is correct

### Frontend Cannot Connect:
1. Update `VITE_WS_URL` in `.env.production`
2. Use `wss://` (not `ws://`) for production
3. Ensure CORS is properly configured

### Deployment Fails:
1. Check Railway build logs
2. Verify all dependencies in `requirements.txt`
3. Ensure frontend builds successfully locally

## Security Considerations

### Important:
1. **Never commit** `META_API_TOKEN` to Git
2. Use Railway environment variables for secrets
3. The token in `xauusd_advanced.py` is a fallback (should be removed in production)
4. Consider adding `.env` files to `.gitignore`

### Update `.gitignore`:
```
.env
.env.local
.env.production
frontend/.env.production
```

## Production Checklist

- [ ] MetaAPI token set in Railway environment variables
- [ ] Frontend `.env.production` updated with Railway URL
- [ ] CORS configured properly
- [ ] WebSocket URL uses `wss://` (not `ws://`)
- [ ] Monitoring/logging enabled
- [ ] Auto-trading reviewed and tested
- [ ] Risk parameters verified (1% real, 2% demo)
- [ ] Session limits configured correctly

## Support

For issues:
1. Check Railway logs
2. Verify environment variables
3. Test locally first: `python xauusd_advanced.py`
4. Check MetaAPI connection status

## Deployment Commands (Alternative)

If using Railway CLI:

```bash
# Login to Railway
railway login

# Link to project
railway link

# Set environment variables
railway variables set META_API_TOKEN=your_token_here

# Deploy
railway up

# View logs
railway logs
```

---

**Note**: This bot executes real trades automatically. Always test thoroughly in demo mode before enabling live trading.
