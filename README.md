# Password Security Lab

<div align="center">

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

**Comprehensive Password Security Analysis & Educational Tool**

[Live Demo](https://passcheck-pro.onrender.com) • [Features](#-features) • [Quick Start](#-quick-start) • [Deployment](#-deployment)

</div>

---

## Overview

A professional web application for analyzing password security, checking breach exposure, and demonstrating password attack methodologies. Built for educational purposes to promote better password security practices.

---

## Features

### Password Breach Checker
- **Real breach data** from Have I Been Pwned API
- **Privacy-focused** k-anonymity model (only first 5 hash chars sent)
- **Visual breach timeline** showing when passwords were leaked
- **Risk assessment** with color-coded indicators
- **Actionable recommendations**

### Password Strength Analyzer
- Comprehensive strength scoring (0-100)
- Character composition analysis
- Entropy calculation
- Common pattern detection
- Real-time feedback

### Hash Generator
- Support for MD5, SHA1, SHA256, SHA512
- Quick hash generation for testing
- Copy-friendly output

### Dictionary Attack Simulator
- **500+ password dictionary** with variations
- **Password variations** (substitutions, case changes, patterns)
- **Pattern matching** (Password123, password@123, etc.)
- **Pause/Resume/Stop** controls
- **Real-time progress** with WebSocket updates
- **Detailed statistics** and tested passwords list

---

## Quick Start

### Prerequisites
- Python 3.7+
- pip

### Installation

```bash
# Clone repository
git clone https://github.com/jinkscad/PasswordCrackerSimulation.git
cd PasswordCrackerSimulation

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Locally

```bash
# Start the web server
python app.py

# Open browser
# http://localhost:5001
```

### CLI Usage

```bash
# Analyze password strength
python main.py analyze --password "MyP@ssw0rd"

# Generate hash
python main.py hash --password "test" --algorithm md5

# Dictionary attack
python main.py dictionary
```

---

## Live Demo

**Live Application:** [https://passcheck-pro.onrender.com](https://passcheck-pro.onrender.com)

Or run locally following the Quick Start guide above.

---

## Tech Stack

- **Backend:** Flask, Flask-SocketIO
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **APIs:** Have I Been Pwned API
- **Python Libraries:** requests, colorama, tqdm

---

## Project Structure

```
PasswordCrackerSimulation/
├── app.py                 # Flask web application
├── main.py                # CLI entry point
├── requirements.txt       # Dependencies
├── src/
│   ├── breach_checker.py  # Breach checking with HIBP API
│   ├── dictionary_attack.py  # Dictionary attack simulator
│   ├── brute_force.py     # Brute force simulator
│   └── utils.py           # Utilities (analyzer, stats)
├── templates/
│   └── index.html         # Web app UI
└── static/
    ├── css/style.css      # Styling
    └── js/app.js          # Frontend logic
```

---

## Deployment

### Render (Recommended)

1. Connect GitHub repository to Render
2. Create new Web Service
3. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
   - **Environment Variables:**
     - `FLASK_ENV=production`
     - `PORT=10000`
     - `HOST=0.0.0.0`

See [DEPLOY.md](DEPLOY.md) for detailed deployment instructions.

---

## Security & Privacy

- **k-Anonymity Model:** Only first 5 characters of password hash sent to HIBP API
- **No Password Storage:** Passwords are never stored or logged
- **Local Hashing:** All hashing done client-side before API calls
- **HTTPS Required:** All deployments use HTTPS encryption

---

## Disclaimer

**Educational Purpose Only**

This tool is designed for:
- Learning password security principles
- Demonstrating attack methodologies
- Promoting better security practices

**Do NOT use for:**
- Unauthorized access attempts
- Cracking passwords without permission
- Any illegal activities

Always ensure you have explicit permission before testing security.

---

## Key Learnings

- **Password Length Matters:** Each character exponentially increases security
- **Complexity is Key:** Mixing character types significantly improves strength
- **Breach Exposure:** Common passwords are highly vulnerable
- **Unique Passwords:** Random, unique passwords resist dictionary attacks
- **Modern Hashing:** Use bcrypt/Argon2 instead of MD5/SHA1

---

## Contributing

Contributions welcome! Areas for improvement:
- Additional hash algorithms
- More sophisticated pattern detection
- Enhanced visualizations
- Mobile app version

---

## License

Educational use only. Use responsibly and ethically.

---

## Resources

- [Have I Been Pwned](https://haveibeenpwned.com/) - Breach database
- [OWASP Password Guidelines](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [NIST Password Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)

---

<div align="center">

**Remember: Strong passwords are your first line of defense.**

Made for security education

</div>
