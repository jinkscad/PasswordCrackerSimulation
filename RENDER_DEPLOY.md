# Render Deployment Guide for PassCheck Pro

## Configuration Settings

### Basic Settings
- **Name:** `PassCheck Pro` (or `passcheck-pro`)
- **Language:** `Python 3`
- **Branch:** `main`
- **Region:** Choose closest to you (Oregon is fine)

### Build & Start Commands

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
python app.py
```

⚠️ **IMPORTANT:** Do NOT use `gunicorn` - our app uses Flask-SocketIO which needs to run directly with Python.

### Environment Variables

Add these environment variables in the Render dashboard:

1. **FLASK_ENV**
   - Value: `production`

2. **PORT**
   - Value: `10000`
   - Note: Render automatically provides PORT, but we set it to 10000 to match our config

3. **HOST**
   - Value: `0.0.0.0`
   - Note: This allows external connections

### Root Directory
- Leave empty (use repository root)

### Instance Type
- **Free tier** is fine for testing
- If you need better performance, upgrade to Starter ($7/month)

## Deployment Steps

1. ✅ Name: `PassCheck Pro`
2. ✅ Language: `Python 3`
3. ✅ Branch: `main`
4. ✅ Build Command: `pip install -r requirements.txt`
5. ✅ Start Command: `python app.py`
6. ✅ Add Environment Variables (see above)
7. Click "Deploy Web Service"

## After Deployment

Your app will be available at:
```
https://passcheck-pro.onrender.com
```

(Or whatever name you chose)

## Troubleshooting

**If deployment fails:**
- Check the logs in Render dashboard
- Verify all dependencies are in `requirements.txt`
- Make sure PORT is set to 10000

**If WebSocket doesn't work:**
- Render supports WebSockets on paid plans
- Free tier may have limitations
- Check Render documentation for WebSocket support

## Notes

- Free tier spins down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds
- Consider upgrading for production use

