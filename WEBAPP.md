# Web Application Guide

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the web server:**
   ```bash
   python app.py
   ```

3. **Open your browser:**
   Navigate to `http://localhost:5000`

## Features

### 🎨 Modern Web Interface

The web app provides a beautiful, responsive interface with:

- **Dark Theme** - Easy on the eyes
- **Real-time Updates** - Live progress via WebSocket
- **Interactive Tabs** - Easy navigation between features
- **Mobile Responsive** - Works on all devices

### 📊 Four Main Features

#### 1. Password Analyzer
- Enter any password
- Get instant strength analysis
- See character composition
- Identify common patterns

#### 2. Hash Generator
- Generate MD5, SHA1, SHA256, or SHA512 hashes
- Useful for testing dictionary attacks
- Copy hashes easily

#### 3. Brute Force Attack
- Enter a password to crack
- Choose random or sequential method
- Watch real-time progress
- See statistics when complete

#### 4. Dictionary Attack
- Enter a hashed password
- Auto-detects hash algorithm
- Uses default or custom dictionary
- Real-time progress tracking

## Example Workflow

### Test Password Security

1. **Generate a hash:**
   - Go to "Hash Generator" tab
   - Enter password: `sunshine`
   - Select MD5
   - Click "Generate Hash"
   - Copy the hash: `5e8ff9bf55ba3508199d22e984129be6`

2. **Try to crack it:**
   - Go to "Dictionary Attack" tab
   - Paste the hash
   - Leave dictionary field empty (uses default)
   - Click "Start Attack"
   - Watch it crack in seconds!

3. **Analyze the password:**
   - Go to "Password Analyzer" tab
   - Enter `sunshine`
   - See why it's weak

## Tips

- Start with short passwords (3-4 chars) for brute force to see quick results
- Use the default dictionary for dictionary attacks
- The web app shows real-time progress - no need to wait!
- All results are displayed beautifully with color coding
- Green = success, Red = error/failure, Yellow = warning

## Troubleshooting

**Port already in use?**
- Change the port in `app.py`: `socketio.run(app, port=5001)`

**WebSocket not working?**
- Make sure you're accessing via `http://localhost:5000` (not `127.0.0.1`)
- Check browser console for errors

**Attacks not starting?**
- Check browser console for error messages
- Make sure all required fields are filled

## Architecture

- **Backend:** Flask with Flask-SocketIO for real-time updates
- **Frontend:** Vanilla JavaScript with Socket.IO client
- **Styling:** Modern CSS with CSS variables for theming
- **Communication:** REST API + WebSocket for real-time progress

Enjoy exploring password security! 🔐

