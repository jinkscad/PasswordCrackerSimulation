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
    """Start brute force attack"""
    data = request.json
    password = data.get('password', '')
    method = data.get('method', 'random')  # 'random' or 'sequential'
    
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    
    # Validate password characters
    attack = BruteForceAttack()
    invalid_chars = [c for c in password if c not in attack.all_chars]
    if invalid_chars:
        return jsonify({
            'error': f'Invalid characters: {set(invalid_chars)}'
        }), 400
    
    # Start attack in background thread
    attack_id = f"brute_{int(time.time())}"
    thread = threading.Thread(
        target=run_bruteforce_attack,
        args=(attack_id, password, method)
    )
    thread.daemon = True
    thread.start()
    active_attacks[attack_id] = thread
    
    # Calculate estimates
    estimates = attack.estimate_time(len(password))
    
    return jsonify({
        'attack_id': attack_id,
        'status': 'started',
        'estimates': estimates
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


if __name__ == '__main__':
    print("=" * 60)
    print("Password Cracking Simulation - Web Application")
    print("=" * 60)
    print("Starting server on http://localhost:5001")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    socketio.run(app, debug=True, host='127.0.0.1', port=5001, allow_unsafe_werkzeug=True)

