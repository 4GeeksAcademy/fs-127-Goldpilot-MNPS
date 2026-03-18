# ⚡ Quick Deploy to Railway (5 Minutes)

## 📦 Step 1: Commit to GitHub

```bash
git add aggressor_pulse_live.py requirements.txt Procfile railway.json .gitignore strategies/
git commit -m "Add: Aggressor Pulse trading bot for Railway deployment"
git push origin main
```

## 🚂 Step 2: Deploy to Railway

1. **Go to**: https://railway.app/new
2. **Login** with GitHub
3. **Click**: "Deploy from GitHub repo"
4. **Select**: `Forex_bot` repository
5. **Wait**: Railway auto-detects and deploys (~2 min)

## 🔑 Step 3: Add Environment Variable

1. In Railway dashboard, click your project
2. Go to **Variables** tab
3. Click **"New Variable"**
4. Add:
   ```
   META_API_TOKEN=eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiIxNzFjZWQ4Yjg5ODdhMWQyM2JlOGFhMTAxM2YwZjVlZCIsImFjY2Vzc1J1bGVzIjpbeyJpZCI6InRyYWRpbmctYWNjb3VudC1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVzdC1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcnBjLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVhbC10aW1lLXN0cmVhbWluZy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtZXRhc3RhdHMtYXBpIiwibWV0aG9kcyI6WyJtZXRhc3RhdHMtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6InJpc2stbWFuYWdlbWVudC1hcGkiLCJtZXRob2RzIjpbInJpc2stbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoiY29weWZhY3RvcnktYXBpIiwibWV0aG9kcyI6WyJjb3B5ZmFjdG9yeS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibXQtbWFuYWdlci1hcGkiLCJtZXRob2RzIjpbIm10LW1hbmFnZXItYXBpOnJlc3Q6ZGVhbGluZzoqOioiLCJtdC1tYW5hZ2VyLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJiaWxsaW5nLWFwaSIsIm1ldGhvZHMiOlsiYmlsbGluZy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfV0sImlnbm9yZVJhdGVMaW1pdHMiOmZhbHNlLCJ0b2tlbklkIjoiMjAyMTAyMTMiLCJpbXBlcnNvbmF0ZWQiOmZhbHNlLCJyZWFsVXNlcklkIjoiMTcxY2VkOGI4OTg3YTFkMjNiZThhYTEwMTNmMGY1ZWQiLCJpYXQiOjE3NjY3Mjg2MzEsImV4cCI6MTc3NDUwNDYzMX0.TlcBJs-k1nzfPIaNLcYBHkFlAWnnJ9qa43CV7aFDYxWjVxp_ZkAJRbKhy4MYhStwHMdiDP8SLVf_Zd4Wfns5qvV_HNNCiCoDDLSw8xy02gctQsr6su5ZTYCSRLfscQZDk8mfZuVfj3wKNxAYE68TeyMlBc1oEQyaHJ7AuDDGhlLDmwJINX4hhfHBxvPbdYztW92DQ_mmp9PSuLU_sr0O9NywQyiYEFXFjCl1_C_55qShFE0-_PkvnQNAzy-6-kWnqMt6Q3yiZJH_EusHF92VxVhzPcqsSFEXCK1q9VkNHT1bK9gICvGGTMGUy0qr0O0d_8THdZrSbiZKi8t9QHgYy-O4BBMvUCYIHcyDUoigwHQGJoFm_n1ZEzpunmVCqWhjwpUXKeXwQebwdJ0OHyH3bW59Z-NT-Snk70-6oHseEpjd45zBiN8pMClVhXc1DvpMiPFnXmQ4hmSmTnskdAOakXhKbx3VRt4EwRbs8-_Pupp824Q0k852X7VODZ2owKX9gZHjjOKuIG3ZlNztj6StEwb_lDzuEc3r8BNNtntZW8UBkBy9T11lj1mry0SzxsP-NSUGUnfxCtqlXgMBni1uhnyY_JtadDMtXsZ9QDiF3Way8HyBhnE4DBD7-UcsHHQobSRpyyhTYqF8bH4pjmO-Mh1IqVJLLZkZi7NJ0RNCgNk
   ```
5. Railway will auto-redeploy

## 🌐 Step 4: Get Your Backend URL

1. In Railway, go to **Settings** tab
2. Click **"Generate Domain"**
3. Copy URL (e.g., `forex-bot-production.up.railway.app`)
4. Your WebSocket URL: `wss://forex-bot-production.up.railway.app`

## ✨ Step 5: Update Vercel Frontend

```bash
cd frontend
npx vercel env add VITE_WS_URL production
# Paste: wss://your-railway-url.up.railway.app

# Redeploy
npx vercel --prod
```

## ✅ Step 6: Test

1. Open: https://frontend-fawn-kappa.vercel.app
2. Login: `aurum2024`
3. Should see vault balances within 10 seconds

---

## 🎉 Done!

Your bot is now running 24/7 in the cloud:
- ✅ Backend on Railway (auto-restart, auto-scale)
- ✅ Frontend on Vercel (global CDN)
- ✅ No local computer needed

---

## 📊 Monitor Your Bot

**Railway Dashboard**: https://railway.app/dashboard
- View logs in real-time
- Check CPU/Memory usage
- See deployment history

**Vercel Dashboard**: https://vercel.com/dashboard
- View frontend analytics
- Check deployment status
- Monitor traffic

---

## 💰 Cost

**Railway**: $5/month (Hobby plan) - includes:
- 500 hours/month execution
- $5 credit
- More than enough for this bot

**Vercel**: FREE
- Unlimited bandwidth
- Global CDN
- Automatic HTTPS

**Total**: ~$5/month to run 24/7

---

## 🔄 Future Updates

When you update the bot:

```bash
# Make changes to aggressor_pulse_live.py
git add aggressor_pulse_live.py
git commit -m "Update: [your change]"
git push origin main

# Railway auto-deploys! No other steps needed.
```

---

## 📞 Troubleshooting

**Railway build fails?**
- Check logs in Railway dashboard
- Verify `requirements.txt` is correct
- Ensure `META_API_TOKEN` is set

**Frontend can't connect?**
- Verify `VITE_WS_URL` in Vercel settings
- Must be `wss://` (not `ws://`)
- Check Railway logs - is backend running?

**Need help?**
- Railway Discord: https://discord.gg/railway
- Check [DEPLOY_TO_CLOUD.md](DEPLOY_TO_CLOUD.md) for detailed guide
