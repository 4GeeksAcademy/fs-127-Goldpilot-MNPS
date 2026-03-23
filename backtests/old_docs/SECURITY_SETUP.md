# Security Setup Guide

## Login Authentication ✅

Your frontend now has password protection!

### Change the Password

**IMPORTANT:** Change the default password before deploying!

1. Open `frontend/src/App.tsx`
2. Find line 17:
   ```typescript
   const CORRECT_PASSWORD = 'aurum2024';
   ```
3. Change `'aurum2024'` to your own secure password
4. Commit and push:
   ```bash
   git add frontend/src/App.tsx
   git commit -m "Update login password"
   git push origin main
   ```

### How It Works

- **Login Screen**: Users must enter the password to access the dashboard
- **Session Storage**: Authentication persists during the browser session
- **No Backend Required**: Simple client-side authentication
- **Auto-logout**: Closes when browser/tab is closed

### Default Password

```
aurum2024
```

**Change this immediately!**

## Chart Debugging

The chart now has improved logging:

- Check browser console for: `📊 Chart data updated: X candles`
- If you see `⏳ Waiting for chart data...` - the backend hasn't sent chart data yet
- Check Railway logs to ensure the backend is fetching candles

### Common Chart Issues

1. **No data showing**:
   - Backend might not be connected to MetaAPI
   - Check Railway logs for "✅ VAULT SYNCED" messages
   - Verify `META_API_TOKEN` is set in Railway environment variables

2. **Chart renders but empty**:
   - WebSocket connection might be fine but no historical data
   - Check backend logs for "📊 Live Price" messages
   - Historical candles API might be timing out

3. **Connection issues**:
   - Verify `VITE_WS_URL` in Vercel matches your Railway URL
   - Should be `wss://` not `ws://`
   - Check browser console for "✅ UPLINK ESTABLISHED"

## Enhanced Security (Optional)

For production, consider:

### 1. Environment Variable Password

Instead of hardcoding, use an environment variable:

```typescript
// In App.tsx
const CORRECT_PASSWORD = import.meta.env.VITE_APP_PASSWORD || 'aurum2024';
```

Then in Vercel:
- Add environment variable: `VITE_APP_PASSWORD=your_secure_password`

### 2. Multiple Users

Create a user list:

```typescript
const AUTHORIZED_USERS = {
  'admin': 'your_admin_password',
  'trader': 'your_trader_password'
};
```

### 3. JWT Token (Advanced)

For enterprise-level security, implement JWT tokens with a backend authentication service.

## Testing

1. **Clear session**: Open browser console and run:
   ```javascript
   sessionStorage.clear()
   ```
2. **Refresh page**: Should show login screen
3. **Enter password**: Should authenticate and show dashboard
4. **Close tab**: Reopen - should require login again

## Deployment Checklist

- [ ] Change default password in `App.tsx`
- [ ] Verify `VITE_WS_URL` in Vercel environment variables
- [ ] Test login on deployed site
- [ ] Check chart data is loading (browser console)
- [ ] Verify WebSocket connection (✅ UPLINK ESTABLISHED)
- [ ] Monitor Railway backend logs

---

**Security Note**: This is basic client-side authentication. For highly sensitive data, implement server-side authentication with JWT tokens.
