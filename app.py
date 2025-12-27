#!/usr/bin/env python3
"""
Flask Web Application for Password Cracking Simulation
"""
import os
import random
import itertools
import threading
import time
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

from src.brute_force import BruteForceAttack
from src.dictionary_attack import DictionaryAttack
from src.utils import PasswordAnalyzer
from src.breach_checker import PasswordBreachChecker

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'password-cracker-simulation-educational-tool'
app.config['CORS_HEADERS'] = 'Content-Type'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
CORS(app, resources={r"/*": {"origins": "*"}})

# Global attack threads and attack objects
active_attacks = {}
attack_objects = {}  # Store attack objects for pause/resume


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze_password():
    """Analyze password strength"""
    data = request.json
    password = data.get('password', '')
    
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    
    score, strength, analysis = PasswordAnalyzer.calculate_strength(password)
    
    return jsonify({
        'score': score,
        'strength': strength,
        'analysis': analysis
    })


@app.route('/api/hash', methods=['POST'])
def hash_password():
    """Generate password hash"""
    data = request.json
    password = data.get('password', '')
    algorithm = data.get('algorithm', 'md5').lower()
    
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    
    try:
        attack = DictionaryAttack()
        hash_value = attack.hash_password(password, algorithm)
        return jsonify({
            'hash': hash_value,
            'algorithm': algorithm.upper()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/breach/check', methods=['POST'])
def check_breach():
    """Check if password has been breached"""
    data = request.json
    password = data.get('password', '')
    
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    
    try:
        checker = PasswordBreachChecker()
        breach_result = checker.check_password(password)
        
        # Get comprehensive risk assessment
        risk_assessment = checker.get_risk_assessment(password, breach_result)
        
        return jsonify({
            'breach': breach_result,
            'risk_assessment': risk_assessment
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/dictionary/attack', methods=['POST'])
def dictionary_attack():
    """Start dictionary attack"""
    data = request.json
    target_hash = data.get('hash', '')
    dictionary_path = data.get('dictionary', '')
    algorithm = data.get('algorithm', None)
    use_variations = data.get('use_variations', True)
    use_patterns = data.get('use_patterns', True)
    
    if not target_hash:
        return jsonify({'error': 'Hash is required'}), 400
    
    if not dictionary_path:
        # Use default dictionary
        default_path = os.path.join(
            os.path.dirname(__file__),
            'dictionary-attack-simulator',
            'passwords.txt'
        )
        dictionary_path = default_path
    
    # Expand user path
    dictionary_path = os.path.expanduser(dictionary_path)
    
    if not os.path.exists(dictionary_path):
        return jsonify({'error': 'Dictionary file not found'}), 400
    
    # Start attack in background thread
    attack_id = f"dict_{int(time.time())}"
    attack = DictionaryAttack(use_progress_bar=False, verbose=False)
    attack_objects[attack_id] = attack
    
    thread = threading.Thread(
        target=run_dictionary_attack,
        args=(attack_id, target_hash, dictionary_path, algorithm, use_variations, use_patterns)
    )
    thread.daemon = True
    thread.start()
    active_attacks[attack_id] = thread
    
    return jsonify({
        'attack_id': attack_id,
        'status': 'started'
    })


@app.route('/api/dictionary/pause', methods=['POST'])
def pause_dictionary_attack():
    """Pause dictionary attack"""
    data = request.json
    attack_id = data.get('attack_id', '')
    
    if attack_id in attack_objects:
        attack_objects[attack_id].pause()
        return jsonify({'status': 'paused'})
    return jsonify({'error': 'Attack not found'}), 404


@app.route('/api/dictionary/resume', methods=['POST'])
def resume_dictionary_attack():
    """Resume dictionary attack"""
    data = request.json
    attack_id = data.get('attack_id', '')
    
    if attack_id in attack_objects:
        attack_objects[attack_id].resume()
        return jsonify({'status': 'resumed'})
    return jsonify({'error': 'Attack not found'}), 404


@app.route('/api/dictionary/stop', methods=['POST'])
def stop_dictionary_attack():
    """Stop dictionary attack"""
    data = request.json
    attack_id = data.get('attack_id', '')
    
    if attack_id in attack_objects:
        attack_objects[attack_id].stop()
        if attack_id in active_attacks:
            del active_attacks[attack_id]
        return jsonify({'status': 'stopped'})
    return jsonify({'error': 'Attack not found'}), 404


@app.route('/api/dictionary/stats', methods=['POST'])
def get_dictionary_stats():
    """Get dictionary attack statistics"""
    data = request.json
    attack_id = data.get('attack_id', '')
    
    if attack_id in attack_objects:
        stats = attack_objects[attack_id].get_statistics()
        return jsonify(stats)
    return jsonify({'error': 'Attack not found'}), 404


def run_dictionary_attack(attack_id, target_hash, dictionary_path, algorithm, use_variations, use_patterns):
    """Run dictionary attack and emit progress via SocketIO"""
    attack = attack_objects.get(attack_id)
    if not attack:
        attack = DictionaryAttack(use_progress_bar=False, verbose=False)
        attack_objects[attack_id] = attack
    
    def progress_callback(progress_data):
        """Callback for progress updates"""
        socketio.emit('attack_progress', {
            'attack_id': attack_id,
            'type': 'dictionary',
            'status': 'running',
            **progress_data
        })
    
    try:
        socketio.emit('attack_progress', {
            'attack_id': attack_id,
            'type': 'dictionary',
            'status': 'loading',
            'message': 'Loading dictionary and generating variations...'
        })
        
        # Perform attack with new enhanced method
        result = attack.attack(
            target_hash, 
            dictionary_path, 
            algorithm,
            use_variations=use_variations,
            use_patterns=use_patterns,
            progress_callback=progress_callback
        )
        
        if result:
            stats = attack.get_statistics()
            attack.stats.stop()
            socketio.emit('attack_complete', {
                'attack_id': attack_id,
                'type': 'dictionary',
                'status': 'success',
                'password': result,
                'attempts': attack.stats.attempts,
                'time': attack.stats.get_elapsed_time(),
                'attempts_per_second': attack.stats.get_attempts_per_second(),
                'passwords_tested': stats['passwords_tested'],
                'tested_passwords': stats['tested_passwords'][-20:]  # Last 20 tested
            })
        else:
            stats = attack.get_statistics()
            attack.stats.stop()
            socketio.emit('attack_complete', {
                'attack_id': attack_id,
                'type': 'dictionary',
                'status': 'failed',
                'message': 'Password not found in dictionary',
                'attempts': attack.stats.attempts,
                'time': attack.stats.get_elapsed_time(),
                'attempts_per_second': attack.stats.get_attempts_per_second(),
                'passwords_tested': stats['passwords_tested'],
                'tested_passwords': stats['tested_passwords'][-20:]  # Last 20 tested
            })
        
        # Cleanup
        if attack_id in active_attacks:
            del active_attacks[attack_id]
        if attack_id in attack_objects:
            del attack_objects[attack_id]
            
    except Exception as e:
        socketio.emit('attack_error', {
            'attack_id': attack_id,
            'type': 'dictionary',
            'error': str(e)
        })
        if attack_id in active_attacks:
            del active_attacks[attack_id]
        if attack_id in attack_objects:
            del attack_objects[attack_id]


@app.route('/api/bruteforce/attack', methods=['POST'])
def bruteforce_attack():
    """Start brute force attack on hash"""
    data = request.json
    target_hash = data.get('hash', '')
    algorithm = data.get('algorithm', None)
    charset = data.get('charset', 'all')
    min_length = data.get('min_length', 1)
    max_length = data.get('max_length', 4)

    if not target_hash:
        return jsonify({'error': 'Hash is required'}), 400

    # Auto-detect algorithm
    if not algorithm:
        length = len(target_hash)
        hash_map = {32: 'md5', 40: 'sha1', 64: 'sha256', 128: 'sha512'}
        algorithm = hash_map.get(length, 'md5')

    # Start attack in background thread
    attack_id = f"brute_{int(time.time())}"
    thread = threading.Thread(
        target=run_bruteforce_hash_attack,
        args=(attack_id, target_hash, algorithm, charset, min_length, max_length)
    )
    thread.daemon = True
    thread.start()
    active_attacks[attack_id] = thread

    # Calculate estimates
    charsets = {
        'numeric': '0123456789',
        'lower': 'abcdefghijklmnopqrstuvwxyz',
        'upper': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'alpha': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'alphanumeric': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
        'all': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{}|;:\'",.<>?/`~'
    }
    char_set = charsets.get(charset, charsets['all'])
    total = sum(len(char_set) ** l for l in range(min_length, max_length + 1))

    return jsonify({
        'attack_id': attack_id,
        'status': 'started',
        'estimates': {
            'total_combinations': total,
            'charset_size': len(char_set),
            'min_length': min_length,
            'max_length': max_length
        }
    })


def run_bruteforce_attack(attack_id, password, method):
    """Run brute force attack and emit progress via SocketIO"""
    attack = BruteForceAttack(use_progress_bar=False, verbose=False)
    attack.stats.start()
    
    try:
        max_attempts = 1_000_000 if method == 'random' else None
        
        if method == 'sequential':
            # Sequential attack
            socketio.emit('attack_progress', {
                'attack_id': attack_id,
                'type': 'bruteforce',
                'status': 'running',
                'method': 'sequential',
                'message': 'Starting sequential brute force attack'
            })
            
            for length in range(1, len(password) + 1):
                socketio.emit('attack_progress', {
                    'attack_id': attack_id,
                    'type': 'bruteforce',
                    'status': 'running',
                    'method': 'sequential',
                    'current_length': length,
                    'target_length': len(password),
                    'message': f'Trying passwords of length {length}'
                })
                
                for attempt in itertools.product(attack.all_chars, repeat=length):
                    guess = ''.join(attempt)
                    attack.stats.increment()
                    
                    if attack.stats.attempts % 1000 == 0:
                        socketio.emit('attack_progress', {
                            'attack_id': attack_id,
                            'type': 'bruteforce',
                            'status': 'running',
                            'attempts': attack.stats.attempts,
                            'current': guess[:30],
                            'message': f'Attempt {attack.stats.attempts:,}'
                        })
                    
                    if guess == password:
                        attack.stats.stop()
                        socketio.emit('attack_complete', {
                            'attack_id': attack_id,
                            'type': 'bruteforce',
                            'status': 'success',
                            'password': guess,
                            'attempts': attack.stats.attempts,
                            'time': attack.stats.get_elapsed_time(),
                            'attempts_per_second': attack.stats.get_attempts_per_second()
                        })
                        return
        else:
            # Random attack
            socketio.emit('attack_progress', {
                'attack_id': attack_id,
                'type': 'bruteforce',
                'status': 'running',
                'method': 'random',
                'message': 'Starting random brute force attack'
            })
            
            attempts = 0
            while attempts < max_attempts:
                guess = ''.join(random.choices(attack.all_chars, k=len(password)))
                attempts += 1
                attack.stats.increment()
                
                if attempts % 1000 == 0:
                    socketio.emit('attack_progress', {
                        'attack_id': attack_id,
                        'type': 'bruteforce',
                        'status': 'running',
                        'attempts': attack.stats.attempts,
                        'current': guess[:30],
                        'message': f'Attempt {attack.stats.attempts:,}'
                    })
                
                if guess == password:
                    attack.stats.stop()
                    socketio.emit('attack_complete', {
                        'attack_id': attack_id,
                        'type': 'bruteforce',
                        'status': 'success',
                        'password': guess,
                        'attempts': attack.stats.attempts,
                        'time': attack.stats.get_elapsed_time(),
                        'attempts_per_second': attack.stats.get_attempts_per_second()
                    })
                    return
        
        attack.stats.stop()
        socketio.emit('attack_complete', {
            'attack_id': attack_id,
            'type': 'bruteforce',
            'status': 'failed',
            'message': 'Password not found within attempt limit',
            'attempts': attack.stats.attempts,
            'time': attack.stats.get_elapsed_time(),
            'attempts_per_second': attack.stats.get_attempts_per_second()
        })
    except Exception as e:
        socketio.emit('attack_error', {
            'attack_id': attack_id,
            'type': 'bruteforce',
            'error': str(e)
        })


def run_bruteforce_hash_attack(attack_id, target_hash, algorithm, charset, min_length, max_length):
    """Run brute force attack on hash and emit progress via SocketIO"""
    import hashlib

    charsets = {
        'numeric': '0123456789',
        'lower': 'abcdefghijklmnopqrstuvwxyz',
        'upper': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'alpha': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'alphanumeric': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
        'all': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{}|;:\'",.<>?/`~'
    }
    char_set = list(charsets.get(charset, charsets['all']))

    hash_funcs = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512
    }
    hash_func = hash_funcs.get(algorithm, hashlib.md5)

    start_time = time.time()
    attempts = 0
    total = sum(len(char_set) ** l for l in range(min_length, max_length + 1))

    try:
        socketio.emit('attack_progress', {
            'attack_id': attack_id,
            'type': 'bruteforce',
            'status': 'running',
            'message': f'Starting brute force attack ({charset} charset, length {min_length}-{max_length})'
        })

        for length in range(min_length, max_length + 1):
            socketio.emit('attack_progress', {
                'attack_id': attack_id,
                'type': 'bruteforce',
                'status': 'running',
                'current_length': length,
                'message': f'Trying passwords of length {length}'
            })

            for attempt in itertools.product(char_set, repeat=length):
                if attack_id not in active_attacks:
                    return  # Attack was stopped

                guess = ''.join(attempt)
                guess_hash = hash_func(guess.encode('utf-8')).hexdigest()
                attempts += 1

                if attempts % 5000 == 0:
                    elapsed = time.time() - start_time
                    progress = (attempts / total) * 100 if total > 0 else 0
                    socketio.emit('attack_progress', {
                        'attack_id': attack_id,
                        'type': 'bruteforce',
                        'status': 'running',
                        'attempts': attempts,
                        'total': total,
                        'progress': progress,
                        'current': guess[:30],
                        'speed': int(attempts / elapsed) if elapsed > 0 else 0,
                        'message': f'Attempt {attempts:,} of {total:,}'
                    })

                if guess_hash.lower() == target_hash.lower():
                    elapsed = time.time() - start_time
                    socketio.emit('attack_complete', {
                        'attack_id': attack_id,
                        'type': 'bruteforce',
                        'status': 'success',
                        'password': guess,
                        'attempts': attempts,
                        'time': elapsed,
                        'attempts_per_second': int(attempts / elapsed) if elapsed > 0 else 0
                    })
                    if attack_id in active_attacks:
                        del active_attacks[attack_id]
                    return

        elapsed = time.time() - start_time
        socketio.emit('attack_complete', {
            'attack_id': attack_id,
            'type': 'bruteforce',
            'status': 'failed',
            'message': 'Password not found in search space',
            'attempts': attempts,
            'time': elapsed,
            'attempts_per_second': int(attempts / elapsed) if elapsed > 0 else 0
        })
    except Exception as e:
        socketio.emit('attack_error', {
            'attack_id': attack_id,
            'type': 'bruteforce',
            'error': str(e)
        })
    finally:
        if attack_id in active_attacks:
            del active_attacks[attack_id]


@app.route('/api/bruteforce/stop', methods=['POST'])
def stop_bruteforce_attack():
    """Stop brute force attack"""
    data = request.json
    attack_id = data.get('attack_id', '')

    if attack_id in active_attacks:
        del active_attacks[attack_id]
        return jsonify({'status': 'stopped'})
    return jsonify({'error': 'Attack not found'}), 404


# ============== MASK ATTACK ==============

@app.route('/api/mask/attack', methods=['POST'])
def mask_attack():
    """Start mask attack"""
    data = request.json
    target_hash = data.get('hash', '')
    algorithm = data.get('algorithm', None)
    mask = data.get('mask', '?d?d?d?d')

    if not target_hash:
        return jsonify({'error': 'Hash is required'}), 400

    # Auto-detect algorithm
    if not algorithm:
        length = len(target_hash)
        hash_map = {32: 'md5', 40: 'sha1', 64: 'sha256', 128: 'sha512'}
        algorithm = hash_map.get(length, 'md5')

    # Calculate total combinations
    placeholders = {
        '?d': '0123456789',
        '?l': 'abcdefghijklmnopqrstuvwxyz',
        '?u': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        '?s': '!@#$%^&*()-_=+[]{}|;:\'",.<>?/`~',
        '?a': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{}|;:\'",.<>?/`~'
    }

    total = 1
    i = 0
    while i < len(mask):
        if i + 1 < len(mask) and mask[i:i+2] in placeholders:
            total *= len(placeholders[mask[i:i+2]])
            i += 2
        else:
            i += 1

    # Start attack in background thread
    attack_id = f"mask_{int(time.time())}"
    thread = threading.Thread(
        target=run_mask_attack,
        args=(attack_id, target_hash, algorithm, mask)
    )
    thread.daemon = True
    thread.start()
    active_attacks[attack_id] = thread

    return jsonify({
        'attack_id': attack_id,
        'status': 'started',
        'estimates': {
            'total_combinations': total,
            'mask': mask
        }
    })


def run_mask_attack(attack_id, target_hash, algorithm, mask):
    """Run mask attack and emit progress via SocketIO"""
    import hashlib

    placeholders = {
        '?d': '0123456789',
        '?l': 'abcdefghijklmnopqrstuvwxyz',
        '?u': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        '?s': '!@#$%^&*()-_=+[]{}|;:\'",.<>?/`~',
        '?a': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{}|;:\'",.<>?/`~'
    }

    hash_funcs = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512
    }
    hash_func = hash_funcs.get(algorithm, hashlib.md5)

    # Parse mask into character sets
    char_sets = []
    i = 0
    while i < len(mask):
        if i + 1 < len(mask) and mask[i:i+2] in placeholders:
            char_sets.append(list(placeholders[mask[i:i+2]]))
            i += 2
        else:
            char_sets.append([mask[i]])
            i += 1

    total = 1
    for cs in char_sets:
        total *= len(cs)

    start_time = time.time()
    attempts = 0

    try:
        socketio.emit('attack_progress', {
            'attack_id': attack_id,
            'type': 'mask',
            'status': 'running',
            'message': f'Starting mask attack with pattern: {mask}'
        })

        for combo in itertools.product(*char_sets):
            if attack_id not in active_attacks:
                return  # Attack was stopped

            guess = ''.join(combo)
            guess_hash = hash_func(guess.encode('utf-8')).hexdigest()
            attempts += 1

            if attempts % 5000 == 0:
                elapsed = time.time() - start_time
                progress = (attempts / total) * 100 if total > 0 else 0
                socketio.emit('attack_progress', {
                    'attack_id': attack_id,
                    'type': 'mask',
                    'status': 'running',
                    'attempts': attempts,
                    'total': total,
                    'progress': progress,
                    'current': guess,
                    'speed': int(attempts / elapsed) if elapsed > 0 else 0,
                    'message': f'Attempt {attempts:,} of {total:,}'
                })

            if guess_hash.lower() == target_hash.lower():
                elapsed = time.time() - start_time
                socketio.emit('attack_complete', {
                    'attack_id': attack_id,
                    'type': 'mask',
                    'status': 'success',
                    'password': guess,
                    'attempts': attempts,
                    'time': elapsed,
                    'attempts_per_second': int(attempts / elapsed) if elapsed > 0 else 0
                })
                if attack_id in active_attacks:
                    del active_attacks[attack_id]
                return

        elapsed = time.time() - start_time
        socketio.emit('attack_complete', {
            'attack_id': attack_id,
            'type': 'mask',
            'status': 'failed',
            'message': 'Password not found with given mask',
            'attempts': attempts,
            'time': elapsed,
            'attempts_per_second': int(attempts / elapsed) if elapsed > 0 else 0
        })
    except Exception as e:
        socketio.emit('attack_error', {
            'attack_id': attack_id,
            'type': 'mask',
            'error': str(e)
        })
    finally:
        if attack_id in active_attacks:
            del active_attacks[attack_id]


@app.route('/api/mask/stop', methods=['POST'])
def stop_mask_attack():
    """Stop mask attack"""
    data = request.json
    attack_id = data.get('attack_id', '')

    if attack_id in active_attacks:
        del active_attacks[attack_id]
        return jsonify({'status': 'stopped'})
    return jsonify({'error': 'Attack not found'}), 404


# ============== RAINBOW TABLE LOOKUP ==============

@app.route('/api/rainbow/lookup', methods=['POST'])
def rainbow_lookup():
    """Lookup hash in rainbow tables"""
    import hashlib
    import urllib.request
    import urllib.error
    import json as json_lib

    data = request.json
    target_hash = data.get('hash', '')
    algorithm = data.get('algorithm', None)
    use_online = data.get('use_online', True)

    if not target_hash:
        return jsonify({'error': 'Hash is required'}), 400

    # Auto-detect algorithm
    if not algorithm:
        length = len(target_hash)
        hash_map = {32: 'md5', 40: 'sha1', 64: 'sha256', 128: 'sha512'}
        algorithm = hash_map.get(length, 'md5')

    results = {
        'hash': target_hash,
        'algorithm': algorithm,
        'found': False,
        'password': None,
        'sources': []
    }

    # Local rainbow table (common passwords)
    common_passwords = [
        'password', '123456', '12345678', 'qwerty', 'abc123', 'monkey', '1234567',
        'letmein', 'trustno1', 'dragon', 'baseball', 'iloveyou', 'master', 'sunshine',
        'ashley', 'bailey', 'shadow', '123123', '654321', 'superman', 'qazwsx',
        'michael', 'football', 'password1', 'password123', 'welcome', 'jesus',
        'ninja', 'mustang', 'password!', 'admin', 'admin123', 'root', 'toor',
        'pass', 'test', 'guest', 'master', 'changeme', 'hello', 'love', '1234',
        '12345', '123456789', '1234567890', '0000', '1111', '1212', '7777', '2024'
    ]

    hash_funcs = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512
    }
    hash_func = hash_funcs.get(algorithm, hashlib.md5)

    # Check local table
    for pwd in common_passwords:
        if hash_func(pwd.encode('utf-8')).hexdigest().lower() == target_hash.lower():
            results['found'] = True
            results['password'] = pwd
            results['sources'].append('Local rainbow table')
            return jsonify(results)

    # Try online lookup if enabled
    if use_online and algorithm == 'md5':
        try:
            # Use md5decrypt.net API (free tier)
            url = f'https://md5decrypt.net/Api/api.php?hash={target_hash}&hash_type=md5&email=demo@demo.com&code=demo'
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                result = response.read().decode('utf-8')
                if result and result != target_hash and 'ERROR' not in result.upper():
                    results['found'] = True
                    results['password'] = result
                    results['sources'].append('Online MD5 database')
        except Exception:
            pass  # Online lookup failed, continue

    if not results['found']:
        results['message'] = 'Hash not found in rainbow tables. The password may be unique or complex.'

    return jsonify(results)


# ============== RULE-BASED ATTACK ==============

@app.route('/api/rules/preview', methods=['POST'])
def preview_rules():
    """Preview rule transformations"""
    data = request.json
    base_word = data.get('base_word', '')
    rules = data.get('rules', {})

    if not base_word:
        return jsonify({'error': 'Base word is required'}), 400

    candidates = generate_rule_candidates(base_word, rules)
    return jsonify({
        'base_word': base_word,
        'candidates': candidates[:100],  # Limit preview to 100
        'total': len(candidates)
    })


@app.route('/api/rules/attack', methods=['POST'])
def rules_attack():
    """Start rule-based attack"""
    data = request.json
    target_hash = data.get('hash', '')
    algorithm = data.get('algorithm', None)
    base_word = data.get('base_word', '')
    rules = data.get('rules', {})

    if not target_hash:
        return jsonify({'error': 'Hash is required'}), 400
    if not base_word:
        return jsonify({'error': 'Base word is required'}), 400

    # Auto-detect algorithm
    if not algorithm:
        length = len(target_hash)
        hash_map = {32: 'md5', 40: 'sha1', 64: 'sha256', 128: 'sha512'}
        algorithm = hash_map.get(length, 'md5')

    candidates = generate_rule_candidates(base_word, rules)

    # Start attack in background thread
    attack_id = f"rules_{int(time.time())}"
    thread = threading.Thread(
        target=run_rules_attack,
        args=(attack_id, target_hash, algorithm, candidates)
    )
    thread.daemon = True
    thread.start()
    active_attacks[attack_id] = thread

    return jsonify({
        'attack_id': attack_id,
        'status': 'started',
        'estimates': {
            'total_candidates': len(candidates),
            'base_word': base_word
        }
    })


def generate_rule_candidates(base_word, rules):
    """Generate password candidates based on rules"""
    candidates = set()
    candidates.add(base_word)

    # Case variations
    if rules.get('case', True):
        candidates.add(base_word.lower())
        candidates.add(base_word.upper())
        candidates.add(base_word.capitalize())
        candidates.add(base_word.swapcase())

    # Leet speak
    if rules.get('leet', True):
        leet_map = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 't': '7', 'l': '1'}
        leet_word = base_word.lower()
        for char, replacement in leet_map.items():
            leet_word = leet_word.replace(char, replacement)
        candidates.add(leet_word)
        candidates.add(leet_word.capitalize())

    # Append numbers
    if rules.get('append_numbers', True):
        numbers = ['1', '12', '123', '1234', '12345', '2024', '2023', '2022', '01', '99', '69', '007']
        for base in list(candidates):
            for num in numbers:
                candidates.add(base + num)

    # Append symbols
    if rules.get('append_symbols', True):
        symbols = ['!', '!!', '@', '#', '$', '!@#', '!@#$', '*']
        for base in list(candidates):
            for sym in symbols:
                candidates.add(base + sym)

    # Prepend patterns
    if rules.get('prepend', True):
        prepends = ['123', '!', '@', '1', '12']
        for base in list(candidates):
            for pre in prepends:
                candidates.add(pre + base)

    # Reverse
    if rules.get('reverse', False):
        for base in list(candidates):
            candidates.add(base[::-1])

    # Duplicate
    if rules.get('duplicate', False):
        for base in list(candidates):
            candidates.add(base + base)
            candidates.add(base + base[::-1])

    # Toggle case at positions
    if rules.get('toggle', False):
        for base in list(candidates):
            if len(base) > 0:
                candidates.add(base[0].upper() + base[1:].lower() if len(base) > 1 else base.upper())
            if len(base) > 1:
                toggled = ''.join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(base))
                candidates.add(toggled)

    return list(candidates)


def run_rules_attack(attack_id, target_hash, algorithm, candidates):
    """Run rule-based attack and emit progress via SocketIO"""
    import hashlib

    hash_funcs = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512
    }
    hash_func = hash_funcs.get(algorithm, hashlib.md5)

    total = len(candidates)
    start_time = time.time()

    try:
        socketio.emit('attack_progress', {
            'attack_id': attack_id,
            'type': 'rules',
            'status': 'running',
            'message': f'Starting rule-based attack with {total} candidates'
        })

        for i, guess in enumerate(candidates):
            if attack_id not in active_attacks:
                return  # Attack was stopped

            guess_hash = hash_func(guess.encode('utf-8')).hexdigest()

            if (i + 1) % 100 == 0:
                elapsed = time.time() - start_time
                progress = ((i + 1) / total) * 100
                socketio.emit('attack_progress', {
                    'attack_id': attack_id,
                    'type': 'rules',
                    'status': 'running',
                    'attempts': i + 1,
                    'total': total,
                    'progress': progress,
                    'current': guess[:30],
                    'speed': int((i + 1) / elapsed) if elapsed > 0 else 0,
                    'message': f'Testing candidate {i + 1:,} of {total:,}'
                })

            if guess_hash.lower() == target_hash.lower():
                elapsed = time.time() - start_time
                socketio.emit('attack_complete', {
                    'attack_id': attack_id,
                    'type': 'rules',
                    'status': 'success',
                    'password': guess,
                    'attempts': i + 1,
                    'time': elapsed,
                    'attempts_per_second': int((i + 1) / elapsed) if elapsed > 0 else 0
                })
                if attack_id in active_attacks:
                    del active_attacks[attack_id]
                return

        elapsed = time.time() - start_time
        socketio.emit('attack_complete', {
            'attack_id': attack_id,
            'type': 'rules',
            'status': 'failed',
            'message': 'Password not found with given rules',
            'attempts': total,
            'time': elapsed,
            'attempts_per_second': int(total / elapsed) if elapsed > 0 else 0
        })
    except Exception as e:
        socketio.emit('attack_error', {
            'attack_id': attack_id,
            'type': 'rules',
            'error': str(e)
        })
    finally:
        if attack_id in active_attacks:
            del active_attacks[attack_id]


@app.route('/api/rules/stop', methods=['POST'])
def stop_rules_attack():
    """Stop rule-based attack"""
    data = request.json
    attack_id = data.get('attack_id', '')

    if attack_id in active_attacks:
        del active_attacks[attack_id]
        return jsonify({'status': 'stopped'})
    return jsonify({'error': 'Attack not found'}), 404


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    # Default to 0.0.0.0 for production (Render, etc.), 127.0.0.1 for local dev
    host = os.environ.get('HOST', '0.0.0.0' if os.environ.get('PORT') else '127.0.0.1')
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print("=" * 60)
    print("Password Security Lab - Web Application")
    print("=" * 60)
    print(f"Starting server on http://{host}:{port}")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    socketio.run(app, debug=debug, host=host, port=port, allow_unsafe_werkzeug=True)

