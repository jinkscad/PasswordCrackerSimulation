# Password Security Lab

<div align="center">

![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

**Educational Password Security Simulation Tool**

[Live Demo](https://passcheck-pro.onrender.com) | [Quick Start](#quick-start) | [Features](#features)

</div>

---

## Overview

An educational web application for learning about password security through interactive simulations of various attack methods. Understand why strong passwords matter by seeing how weak ones can be cracked.

---

## Features

### Password Strength Analyzer
Advanced analysis inspired by zxcvbn (used by Dropbox, GitHub):
- **Common password detection** - checks against 1000+ leaked passwords
- **Keyboard pattern detection** - qwerty, asdfgh, 1qaz2wsx
- **Leet speak detection** - recognizes p@ssw0rd as "password"
- **Sequential/repeated character detection**
- **Real entropy calculation** - mathematically accurate
- **Crack time estimates** - based on 10B guesses/sec (modern GPU)
- **Score breakdown** - see exactly how your score is calculated

### Hash Generator
Generate hashes for testing:
- MD5, SHA1, SHA256, SHA512
- Copy-friendly output

### Password Breach Checker
- Real breach data from Have I Been Pwned API
- Privacy-focused k-anonymity (only 5 hash chars sent)
- Visual breach timeline

### Dictionary Attack
- 500+ common passwords with variations
- Leet speak substitutions and pattern matching
- Pause/Resume/Stop controls
- Real-time WebSocket progress

### Brute Force Attack
- Tries every character combination
- Configurable character sets (numeric, alpha, alphanumeric, all)
- Adjustable length range
- Real-time progress and speed stats

### Mask Attack
Hashcat-style pattern-based attack:
- `?d` = digit, `?l` = lowercase, `?u` = uppercase, `?s` = symbol
- Preset patterns for common formats (PINs, name+year)
- Example: `?u?l?l?l?d?d?d?d` matches "John2024"

### Rainbow Table Lookup
- Instant hash lookup in pre-computed tables
- Local common password database
- Optional online MD5 lookup

### Rule-based Attack
Apply transformations to base words:
- Case variations
- Leet speak (a->@, e->3)
- Append numbers/symbols
- Prepend patterns
- Reverse, duplicate, toggle case
- Preview generated candidates before attacking

---

## Quick Start

```bash
# Clone and enter directory
git clone https://github.com/jinkscad/PasswordCrackerSimulation.git
cd PasswordCrackerSimulation

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Open http://localhost:5001
```

---

## Live Demo
https://passcheck-pro.onrender.com/

---

## Tech Stack

- **Backend:** Flask, Flask-SocketIO
- **Frontend:** Vanilla HTML/CSS/JavaScript
- **APIs:** Have I Been Pwned

---

## Project Structure

```
PasswordCrackerSimulation/
├── app.py                    # Flask web app + API endpoints
├── main.py                   # CLI entry point
├── requirements.txt
├── src/
│   ├── utils.py              # Password analyzer
│   ├── dictionary_attack.py  # Dictionary attack engine
│   └── brute_force.py        # Brute force engine
├── templates/
│   └── index.html            # Web UI
└── static/
    ├── css/style.css
    └── js/app.js
```

---

## Security & Privacy

- **k-Anonymity:** Only first 5 chars of hash sent to breach API
- **No Storage:** Passwords never stored or logged
- **Local Processing:** All analysis done locally

---

## Disclaimer

**Educational Purpose Only**

This tool demonstrates password security concepts. Do NOT use for unauthorized access or illegal activities. Always obtain permission before security testing.

---

## License

MIT License - Educational use only. Use responsibly.

---

<div align="center">

**Strong passwords are your first line of defense.**

</div>
