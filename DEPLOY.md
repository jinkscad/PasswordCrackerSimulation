# Deployment Guide

## Quick Deploy Options

### Option 1: Render (Recommended - Free Tier Available) ⭐

**Steps:**

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `PasswordCrackerSimulation`

3. **Configure Service**
   - **Name:** `password-cracker-sim` (or any name)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
   - **Environment Variables:**
     - `FLASK_ENV` = `production`
     - `PORT` = `10000` (Render uses port 10000)

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Your app will be live at `https://your-app-name.onrender.com`

**Pros:**
- Free tier available
- Easy GitHub integration
- Automatic deployments
- HTTPS included

**Cons:**
- Free tier spins down after inactivity (takes ~30s to wake up)

---

### Option 2: Railway (Modern & Fast)

**Steps:**

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure**
   - Railway auto-detects Python
   - Add environment variables:
     - `PORT` = `${{PORT}}` (Railway provides this automatically)
     - `FLASK_ENV` = `production`

4. **Deploy**
   - Railway automatically deploys
   - Your app will be live at `https://your-app-name.up.railway.app`

**Pros:**
- Very fast deployments
- Free tier with $5 credit
- Great developer experience
- Auto HTTPS

---

### Option 3: PythonAnywhere (Free Tier)

**Steps:**

1. **Create Account**
   - Go to [pythonanywhere.com](https://www.pythonanywhere.com)
   - Sign up for free account

2. **Upload Files**
   - Go to "Files" tab
   - Upload your project files
   - Or clone from GitHub

3. **Configure Web App**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose Flask
   - Set source code directory
   - Set WSGI file to point to `app.py`

4. **Set Working Directory**
   - Set to your project root

5. **Reload**
   - Click "Reload" button
   - Your app will be at `yourusername.pythonanywhere.com`

**Pros:**
- Free tier available
- Good for Python apps
- Simple setup

**Cons:**
- Free tier has limitations
- Custom domain requires paid plan

---

### Option 4: Heroku (Classic Choice)

**Steps:**

1. **Install Heroku CLI**
   ```bash
   brew install heroku/brew/heroku  # macOS
   ```

2. **Login**
   ```bash
   heroku login
   ```

3. **Create App**
   ```bash
   heroku create your-app-name
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set FLASK_ENV=production
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

**Note:** Heroku no longer has a free tier, but has a low-cost hobby tier.

---

## Environment Variables

For production, set these:

- `FLASK_ENV=production`
- `PORT` (usually provided by platform)
- `SECRET_KEY` (generate a secure random key)

## Important Notes

1. **Socket.IO**: Make sure your platform supports WebSockets (Render, Railway, and Heroku do)

2. **Port**: Most platforms provide PORT via environment variable. The app now reads this automatically.

3. **HTTPS**: All platforms provide HTTPS automatically.

4. **Database**: Not needed for this app (no database used).

## Testing Deployment Locally

Test production mode locally:

```bash
export FLASK_ENV=production
export PORT=5001
python app.py
```

## Troubleshooting

**Issue: App won't start**
- Check logs in your platform's dashboard
- Verify all dependencies in `requirements.txt`
- Ensure PORT environment variable is set

**Issue: WebSocket not working**
- Verify platform supports WebSockets
- Check firewall/network settings
- Ensure using HTTPS (required for WebSockets in production)

**Issue: API calls failing**
- Check CORS settings
- Verify external API access (HIBP API)
- Check network restrictions

---

## Recommended: Render

For easiest deployment, I recommend **Render**:
- Free tier available
- Easy GitHub integration
- Automatic HTTPS
- Good documentation

Just connect your GitHub repo and deploy!

