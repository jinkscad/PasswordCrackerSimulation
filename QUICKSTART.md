# Quick Start Guide

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Basic Usage

### 1. Brute Force Attack
```bash
python main.py brute-force
```
Enter a password when prompted and watch the simulation attempt to crack it.

### 2. Dictionary Attack
```bash
python main.py dictionary
```
Enter a hashed password (e.g., MD5 hash) and dictionary file path.

### 3. Analyze Password Strength
```bash
python main.py analyze --password "YourPassword123!"
```

### 4. Generate Hash
```bash
python main.py hash --password "test" --algorithm md5
```

## Example Workflow

1. **Generate a hash for testing:**
   ```bash
   python main.py hash --password "sunshine" --algorithm md5
   # Output: 5e8ff9bf55ba3508199d22e984129be6
   ```

2. **Try to crack it with dictionary attack:**
   ```bash
   python main.py dictionary
   # Enter hash: 5e8ff9bf55ba3508199d22e984129be6
   # Enter dictionary: dictionary-attack-simulator/passwords.txt
   ```

3. **Analyze the cracked password:**
   ```bash
   python main.py analyze --password "sunshine"
   ```

## Tips

- Start with short passwords (3-4 chars) for brute force to see quick results
- Use the default dictionary file for dictionary attacks
- Try different hash algorithms (md5, sha1, sha256, sha512)
- Use `--no-progress` flag if progress bars cause display issues
- Use `--quiet` flag for less verbose output

