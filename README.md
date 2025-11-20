# Password Cracking Simulation

<div align="center">

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

**Educational Security Tool Demonstrating Password Vulnerabilities**

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Web App](#web-application) • [Documentation](#documentation)

</div>

---

## 📋 Description

This project is a comprehensive educational tool that simulates two primary password-cracking techniques: **Brute Force Attacks** and **Dictionary Attacks**. The purpose is to demonstrate the vulnerabilities of weak passwords and highlight the importance of secure password practices and modern hashing algorithms.

### Key Features

- 🔓 **Brute Force Attack Simulator** - Demonstrates exhaustive password guessing
- 📚 **Dictionary Attack Simulator** - Shows how common passwords are easily cracked
- 📊 **Password Strength Analyzer** - Comprehensive password security analysis
- ⏱️ **Performance Statistics** - Real-time attack metrics and timing
- 🎨 **Professional CLI Interface** - Color-coded output with progress bars
- 🌐 **Modern Web Application** - Beautiful, responsive web interface
- 🔐 **Multiple Hash Algorithms** - Support for MD5, SHA1, SHA256, SHA512

---

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. **Clone or download the repository**
   ```bash
   cd PasswordCrackerSimulation
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python main.py --help
   ```

---

## 💻 Usage

### 🌐 Web Application (Recommended)

The easiest way to use this tool is through the web interface:

```bash
python app.py
```

Then open your browser and navigate to:
```
http://localhost:5000
```

**Web App Features:**
- 🎨 Beautiful, modern UI with dark theme
- 📊 Real-time progress updates via WebSocket
- 🔄 Interactive tabs for all features
- 📱 Fully responsive design
- ⚡ Live statistics and results

### 💻 Command Line Interface

#### Interactive Mode

##### Brute Force Attack
```bash
python main.py brute-force
```

##### Dictionary Attack
```bash
python main.py dictionary
```

#### Command-Line Options

##### Password Strength Analysis
```bash
# Analyze a password interactively
python main.py analyze

# Analyze a specific password
python main.py analyze --password "MyP@ssw0rd123"

# Show password in analysis (default is masked)
python main.py analyze --password "MyP@ssw0rd123" --show-password
```

##### Hash Generation
```bash
# Generate MD5 hash (default)
python main.py hash --password "test"

# Generate SHA256 hash
python main.py hash --password "test" --algorithm sha256

# Available algorithms: md5, sha1, sha256, sha512
```

##### Non-Interactive Dictionary Attack
```bash
python main.py dictionary --hash "098f6bcd4621d373cade4e832627b4f6" \
                          --dict "dictionary-attack-simulator/passwords.txt" \
                          --algorithm md5
```

##### Advanced Options
```bash
# Disable progress bar
python main.py brute-force --no-progress

# Quiet mode (reduce output)
python main.py dictionary --quiet
```

---

## 📖 Program Walk-through

### Web Application Interface

The web app provides four main tabs:

1. **Password Analyzer** - Analyze password strength instantly
2. **Hash Generator** - Generate hashes for any password
3. **Brute Force Attack** - Simulate brute force attacks with real-time progress
4. **Dictionary Attack** - Crack hashed passwords using wordlists

### Brute Force Attack Simulator

The brute force simulator demonstrates how attackers systematically try every possible password combination.

**Features:**
- Random generation mode (faster demo)
- Sequential generation mode (more realistic)
- Time estimation based on password complexity
- Real-time attempt tracking
- Performance statistics

**Example Output:**
```
Password Strength Analysis
============================================================
Length: 8 characters
Strength Score: 65/100
Strength Level: Strong
Estimated Entropy: 160.0 bits

Brute Force Time Estimate:
  Total possible combinations: 218,340,105,584,896
  Estimated time (at 1M attempts/sec): 6.91 years

✓ PASSWORD CRACKED!
Password found: Pass@123

Brute Force Attack Statistics
============================================================
Total Attempts: 1,234,567
Time Elapsed: 45.23 seconds
Attempts/Second: 27,293
```

**Security Insight:** This demonstrates that longer, more complex passwords exponentially increase the time required to crack them through brute force.

### Dictionary Attack Simulator

The dictionary attack simulator shows how attackers use pre-compiled wordlists to quickly crack common passwords.

**Features:**
- Automatic hash algorithm detection
- Support for multiple hash types (MD5, SHA1, SHA256, SHA512)
- Progress tracking with password preview
- Comprehensive statistics

**Example Usage:**
```bash
Enter the hashed password: 098f6bcd4621d373cade4e832627b4f6
Enter dictionary file path: dictionary-attack-simulator/passwords.txt
```

**Example Output:**
```
Detected hash algorithm: MD5
Loaded 20 password candidates

✓ PASSWORD CRACKED!
Password found: test

Password Strength Analysis
============================================================
Length: 4 characters
Strength Score: 15/100
Strength Level: Very Weak
```

**Security Insight:** Dictionary attacks are extremely fast for common passwords but fail against unique, random passwords not in the dictionary.

### Password Strength Analyzer

The analyzer provides comprehensive password security assessment:

**Metrics:**
- Strength score (0-100)
- Strength level (Very Weak to Very Strong)
- Character composition analysis
- Entropy calculation
- Common pattern detection

**Example:**
```bash
python main.py analyze --password "MySecureP@ssw0rd!"
```

---

## 🔒 Security Recommendations

### For Users
- ✅ Use passwords with **12+ characters**
- ✅ Include **uppercase, lowercase, numbers, and symbols**
- ✅ Avoid **common patterns** and dictionary words
- ✅ Use **unique passwords** for each account
- ✅ Consider using a **password manager**
- ✅ Use **passphrases** instead of single words

### For Developers
- ⚠️ **Never use MD5 or SHA1** for password hashing
- ✅ Use **modern algorithms**: bcrypt, Argon2, scrypt
- ✅ Implement **salting** (unique salt per password)
- ✅ Use **key stretching** (multiple iterations)
- ✅ Implement **rate limiting** on login attempts
- ✅ Consider **multi-factor authentication (MFA)**


---

## 🛠️ Technologies Used

- **Python 3.7+** - Core programming language
- **Flask** - Web framework
- **Flask-SocketIO** - Real-time WebSocket communication
- **colorama** - Cross-platform colored terminal output
- **tqdm** - Progress bars and visual feedback
- **pyfiglet** - ASCII art banners
- **hashlib** - Cryptographic hashing functions
- **HTML/CSS/JavaScript** - Modern web interface

---

## 📊 Key Learnings

This project demonstrates several important security concepts:

1. **Password Length Matters**: Each additional character exponentially increases cracking time
2. **Complexity is Key**: Mixing character types significantly improves security
3. **Dictionary Attacks are Fast**: Common passwords are vulnerable to pre-compiled wordlists
4. **Hashing Alone is Insufficient**: MD5/SHA1 are vulnerable; modern algorithms are essential
5. **Unique Passwords Resist Dictionary Attacks**: Random, unique passwords protect against wordlist attacks

---

## ⚠️ Disclaimer

**This tool is for educational purposes only.** It is designed to:
- Teach password security principles
- Demonstrate attack methodologies
- Highlight security vulnerabilities
- Promote better security practices

**Do not use this tool for:**
- Unauthorized access to systems
- Cracking passwords without permission
- Any illegal activities

Always ensure you have explicit permission before testing security on any system.

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional hash algorithm support
- GPU acceleration for brute force attacks
- More sophisticated password analysis
- Additional dictionary files
- Mobile app version

---

## 📝 License

This project is provided for educational purposes. Use responsibly and ethically.

---

## 👨‍💻 Author

Educational Security Tool - Version 2.0

---

## 🔗 Resources

- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [NIST Password Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)
- [Have I Been Pwned](https://haveibeenpwned.com/) - Check if your password has been compromised

---

<div align="center">

**Remember: Strong passwords are your first line of defense! 🔐**

Made with ❤️ for security education

</div>
