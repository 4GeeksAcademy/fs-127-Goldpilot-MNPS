#!/bin/bash

echo "🚀 Railway Deployment Setup Script"
echo "===================================="
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
else
    echo "✅ Railway CLI is installed"
fi

echo ""
echo "📋 Pre-deployment checklist:"
echo ""
echo "1. Have you created a Railway account? (https://railway.app)"
echo "2. Have you pushed your code to GitHub/GitLab?"
echo "3. Do you have your MetaAPI token ready?"
echo ""
read -p "Press Enter to continue or Ctrl+C to exit..."

echo ""
echo "🔐 Setting up environment variables..."
echo ""
echo "You'll need to set these in Railway dashboard:"
echo ""
echo "Required:"
echo "  META_API_TOKEN=your_metaapi_token_here"
echo "  PORT=8080"
echo "  WS_HOST=0.0.0.0"
echo ""
echo "Optional:"
echo "  FRONTEND_PORT=3000"
echo ""

read -p "Have you set these variables in Railway? (y/n): " confirm

if [ "$confirm" != "y" ]; then
    echo ""
    echo "⚠️  Please set environment variables in Railway first:"
    echo "   1. Go to https://railway.app/dashboard"
    echo "   2. Select your project"
    echo "   3. Go to 'Variables' tab"
    echo "   4. Add the required variables"
    echo ""
    exit 1
fi

echo ""
echo "📦 Building frontend..."
cd frontend
npm install
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Frontend build failed!"
    exit 1
fi

cd ..
echo "✅ Frontend built successfully"

echo ""
echo "🎯 Deployment steps:"
echo ""
echo "1. Go to https://railway.app/new"
echo "2. Click 'Deploy from GitHub repo'"
echo "3. Select this repository"
echo "4. Railway will auto-deploy"
echo ""
echo "5. After deployment, update frontend/.env.production:"
echo "   VITE_WS_URL=wss://your-railway-url.railway.app"
echo ""
echo "6. Commit and push to trigger redeployment"
echo ""
echo "📖 For detailed instructions, see DEPLOYMENT.md"
echo ""
echo "✨ Ready for deployment!"
