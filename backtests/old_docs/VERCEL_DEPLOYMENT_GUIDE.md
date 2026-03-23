# Vercel Deployment Guide - Forex Trading Bot

## 🚀 Quick Deploy

The frontend is ready for Vercel deployment with all configuration files in place.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Push your code to GitHub (recommended)
3. **Environment Variables**: Have your API keys ready

## Option 1: Deploy via Vercel Dashboard (Recommended)

### Step 1: Connect GitHub
1. Go to [vercel.com/new](https://vercel.com/new)
2. Click "Import Git Repository"
3. Select your `Forex_bot` repository
4. Vercel will auto-detect it's a Vite app

### Step 2: Configure Project
- **Framework Preset**: Vite
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`

### Step 3: Add Environment Variables
Add these in the Vercel dashboard under "Environment Variables":

```
VITE_API_URL=your_backend_api_url
```

### Step 4: Deploy
- Click "Deploy"
- Vercel will build and deploy your app
- You'll get a URL like `https://forex-bot-xxx.vercel.app`

## Option 2: Deploy via CLI

### Step 1: Login to Vercel
```bash
cd frontend
npx vercel login
```

### Step 2: Deploy (Production)
```bash
npx vercel --prod
```

Follow the prompts:
- **Set up and deploy?** Y
- **Which scope?** Select your account
- **Link to existing project?** N (first time)
- **What's your project's name?** forex-trading-bot
- **In which directory?** ./
- **Want to override settings?** N

### Step 3: Set Environment Variables
```bash
npx vercel env add VITE_API_URL production
```

## Deployment Files Created

### ✅ vercel.json
```json
{
  "version": 2,
  "builds": [{
    "src": "package.json",
    "use": "@vercel/static-build",
    "config": { "distDir": "dist" }
  }],
  "routes": [
    { "src": "/assets/(.*)", "dest": "/assets/$1" },
    { "src": "/(.*)", "dest": "/index.html" }
  ]
}
```

This configuration:
- Builds the Vite app as a static site
- Routes all requests to index.html (SPA routing)
- Serves assets from /assets/

## Project Structure
```
frontend/
├── vercel.json          # Vercel configuration
├── package.json         # Dependencies & build scripts
├── index.html          # Entry HTML
├── src/
│   ├── main.tsx        # React entry point
│   ├── App.tsx         # Main app component
│   └── components/     # React components
└── dist/              # Build output (auto-generated)
```

## Automatic Deployments

Once connected to GitHub:
- **Push to main** → Auto-deploys to production
- **Push to other branches** → Auto-deploys preview
- **Pull requests** → Auto-deploys preview with unique URL

## Custom Domain (Optional)

1. Go to your project in Vercel dashboard
2. Click "Settings" → "Domains"
3. Add your custom domain
4. Update DNS records as instructed

## Backend Integration

Your frontend will need a backend API. Options:

### Option A: Separate Backend (Recommended)
- Deploy Python backend to Railway, Render, or DigitalOcean
- Update `VITE_API_URL` environment variable
- Enable CORS on backend

### Option B: Serverless Functions
- Use Vercel serverless functions for API routes
- Create `api/` folder in frontend
- Limited to Node.js/Edge runtime (not Python)

## Monitoring

- **Analytics**: Vercel provides built-in analytics
- **Logs**: View deployment logs in Vercel dashboard
- **Performance**: Web Vitals tracking included

## Troubleshooting

### Build Fails
```bash
# Test build locally first
npm run build
```

### Environment Variables Not Working
- Ensure they start with `VITE_` prefix
- Restart deployment after adding variables
- Check spelling and case sensitivity

### 404 on Refresh
- Verify `vercel.json` routes configuration
- Ensure SPA routing is enabled

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Connect repository to Vercel
3. ✅ Configure environment variables
4. ✅ Deploy and test
5. ✅ Set up custom domain (optional)

## Support

- Vercel Docs: [vercel.com/docs](https://vercel.com/docs)
- Vite Docs: [vitejs.dev](https://vitejs.dev)
- GitHub Issues: Report bugs in your repository

---

**Ready to deploy!** 🚀
