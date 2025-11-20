// Socket.IO Connection
const socket = io();

// Tab Management
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabId = btn.dataset.tab;
        
        // Update buttons
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        // Update panes
        document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
        document.getElementById(tabId).classList.add('active');
    });
});

// Password Analyzer
async function analyzePassword() {
    const password = document.getElementById('analyze-password').value;
    const resultsDiv = document.getElementById('analyzer-results');
    
    if (!password) {
        showError(resultsDiv, 'Please enter a password to analyze');
        return;
    }
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayAnalysis(data, resultsDiv);
        } else {
            showError(resultsDiv, data.error || 'Analysis failed');
        }
    } catch (error) {
        showError(resultsDiv, 'Error analyzing password: ' + error.message);
    }
}

function displayAnalysis(data, container) {
    const analysis = data.analysis;
    const strengthClass = getStrengthClass(data.strength);
    
    container.innerHTML = `
        <div class="result-item">
            <strong>Password Strength</strong>
            <div class="strength-meter">
                <div class="strength-bar">
                    <div class="strength-fill ${strengthClass}" style="width: ${data.score}%"></div>
                </div>
                <div class="strength-label">${data.strength} (${data.score}/100)</div>
            </div>
        </div>
        <div class="result-item">
            <strong>Length</strong>
            ${analysis.length} characters
        </div>
        <div class="result-item">
            <strong>Character Composition</strong>
            Lowercase: ${analysis.has_lowercase ? '✓' : '✗'}<br>
            Uppercase: ${analysis.has_uppercase ? '✓' : '✗'}<br>
            Digits: ${analysis.has_digits ? '✓' : '✗'}<br>
            Symbols: ${analysis.has_symbols ? '✓' : '✗'}
        </div>
        <div class="result-item">
            <strong>Estimated Entropy</strong>
            ${analysis.entropy.toFixed(1)} bits
        </div>
        ${analysis.common_patterns.length > 0 ? `
            <div class="result-item result-error">
                <strong>⚠️ Common Patterns Detected</strong>
                ${analysis.common_patterns.join('<br>')}
            </div>
        ` : ''}
    `;
    container.classList.remove('hidden');
}

function getStrengthClass(strength) {
    const map = {
        'Very Weak': 'strength-very-weak',
        'Weak': 'strength-weak',
        'Moderate': 'strength-moderate',
        'Strong': 'strength-strong',
        'Very Strong': 'strength-very-strong'
    };
    return map[strength] || 'strength-moderate';
}

// Hash Generator
async function generateHash() {
    const password = document.getElementById('hash-password').value;
    const algorithm = document.getElementById('hash-algorithm').value;
    const resultsDiv = document.getElementById('hash-results');
    
    if (!password) {
        showError(resultsDiv, 'Please enter a password to hash');
        return;
    }
    
    try {
        const response = await fetch('/api/hash', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ password, algorithm })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            resultsDiv.innerHTML = `
                <div class="result-item">
                    <strong>Hash (${data.algorithm})</strong>
                    <code style="display: block; margin-top: 0.5rem; padding: 0.5rem; background: var(--bg); border-radius: 4px; word-break: break-all;">${data.hash}</code>
                </div>
            `;
            resultsDiv.classList.remove('hidden');
        } else {
            showError(resultsDiv, data.error || 'Hash generation failed');
        }
    } catch (error) {
        showError(resultsDiv, 'Error generating hash: ' + error.message);
    }
}

// Brute Force Attack
let currentBruteAttackId = null;

async function startBruteForce() {
    const password = document.getElementById('brute-password').value;
    const method = document.getElementById('brute-method').value;
    const estimatesDiv = document.getElementById('brute-estimates');
    const progressDiv = document.getElementById('brute-progress');
    const resultsDiv = document.getElementById('brute-results');
    const stopBtn = document.getElementById('stop-brute-btn');
    
    if (!password) {
        showError(resultsDiv, 'Please enter a password to crack');
        return;
    }
    
    try {
        const response = await fetch('/api/bruteforce/attack', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ password, method })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentBruteAttackId = data.attack_id;
            stopBtn.style.display = 'inline-block';
            
            // Show estimates
            estimatesDiv.innerHTML = `
                <h3>Time Estimates</h3>
                <p><strong>Total Combinations:</strong> ${data.estimates.total_combinations.toLocaleString()}</p>
                <p><strong>Estimated Time:</strong> ${data.estimates.estimated_time}</p>
            `;
            estimatesDiv.classList.remove('hidden');
            
            progressDiv.classList.remove('hidden');
            resultsDiv.classList.add('hidden');
        } else {
            showError(resultsDiv, data.error || 'Attack failed to start');
        }
    } catch (error) {
        showError(resultsDiv, 'Error starting attack: ' + error.message);
    }
}

// Dictionary Attack
let currentDictAttackId = null;

async function startDictionaryAttack() {
    const hash = document.getElementById('dict-hash').value;
    const dictFile = document.getElementById('dict-file').value;
    const algorithm = document.getElementById('dict-algorithm').value || null;
    const progressDiv = document.getElementById('dict-progress');
    const resultsDiv = document.getElementById('dict-results');
    const stopBtn = document.getElementById('stop-dict-btn');
    
    if (!hash) {
        showError(resultsDiv, 'Please enter a hash to crack');
        return;
    }
    
    try {
        const response = await fetch('/api/dictionary/attack', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                hash, 
                dictionary: dictFile || undefined,
                algorithm 
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentDictAttackId = data.attack_id;
            stopBtn.style.display = 'inline-block';
            progressDiv.classList.remove('hidden');
            resultsDiv.classList.add('hidden');
        } else {
            showError(resultsDiv, data.error || 'Attack failed to start');
        }
    } catch (error) {
        showError(resultsDiv, 'Error starting attack: ' + error.message);
    }
}

// Stop Attack
function stopAttack(type) {
    // Note: In a real implementation, you'd need to add a stop endpoint
    // For now, this is a placeholder
    if (type === 'bruteforce') {
        currentBruteAttackId = null;
        document.getElementById('stop-brute-btn').style.display = 'none';
    } else if (type === 'dictionary') {
        currentDictAttackId = null;
        document.getElementById('stop-dict-btn').style.display = 'none';
    }
}

// Socket.IO Event Handlers
socket.on('attack_progress', (data) => {
    if (data.type === 'bruteforce' && data.attack_id === currentBruteAttackId) {
        updateBruteProgress(data);
    } else if (data.type === 'dictionary' && data.attack_id === currentDictAttackId) {
        updateDictProgress(data);
    }
});

socket.on('attack_complete', (data) => {
    if (data.type === 'bruteforce' && data.attack_id === currentBruteAttackId) {
        showBruteResults(data);
        currentBruteAttackId = null;
        document.getElementById('stop-brute-btn').style.display = 'none';
    } else if (data.type === 'dictionary' && data.attack_id === currentDictAttackId) {
        showDictResults(data);
        currentDictAttackId = null;
        document.getElementById('stop-dict-btn').style.display = 'none';
    }
});

socket.on('attack_error', (data) => {
    const resultsDiv = data.type === 'bruteforce' 
        ? document.getElementById('brute-results')
        : document.getElementById('dict-results');
    showError(resultsDiv, data.error || 'Attack error occurred');
    
    if (data.type === 'bruteforce') {
        currentBruteAttackId = null;
        document.getElementById('stop-brute-btn').style.display = 'none';
    } else {
        currentDictAttackId = null;
        document.getElementById('stop-dict-btn').style.display = 'none';
    }
});

function updateBruteProgress(data) {
    const progressFill = document.getElementById('brute-progress-fill');
    const progressText = document.getElementById('brute-progress-text');
    
    if (data.attempts) {
        const progress = Math.min((data.attempts / 1000000) * 100, 100);
        progressFill.style.width = progress + '%';
        progressText.textContent = `Attempt ${data.attempts.toLocaleString()}: ${data.current || '...'}`;
    } else {
        progressText.textContent = data.message || 'Running...';
    }
}

function updateDictProgress(data) {
    const progressFill = document.getElementById('dict-progress-fill');
    const progressText = document.getElementById('dict-progress-text');
    
    if (data.progress !== undefined) {
        progressFill.style.width = data.progress + '%';
        progressText.textContent = `Testing: ${data.current || '...'} (${data.attempts || 0}/${data.total || 0})`;
    } else {
        progressText.textContent = data.message || 'Running...';
    }
}

function showBruteResults(data) {
    const resultsDiv = document.getElementById('brute-results');
    const progressDiv = document.getElementById('brute-progress');
    
    if (data.status === 'success') {
        resultsDiv.innerHTML = `
            <div class="result-item result-success">
                <strong>✓ Password Cracked!</strong>
                Password: <code>${data.password}</code><br>
                Attempts: ${data.attempts.toLocaleString()}<br>
                Time: ${data.time.toFixed(2)} seconds<br>
                Speed: ${data.attempts_per_second.toFixed(0)} attempts/second
            </div>
        `;
    } else {
        resultsDiv.innerHTML = `
            <div class="result-item result-error">
                <strong>✗ ${data.message || 'Attack failed'}</strong><br>
                Attempts: ${data.attempts.toLocaleString()}<br>
                Time: ${data.time.toFixed(2)} seconds
            </div>
        `;
    }
    
    resultsDiv.classList.remove('hidden');
    progressDiv.classList.add('hidden');
}

function showDictResults(data) {
    const resultsDiv = document.getElementById('dict-results');
    const progressDiv = document.getElementById('dict-progress');
    
    if (data.status === 'success') {
        resultsDiv.innerHTML = `
            <div class="result-item result-success">
                <strong>✓ Password Cracked!</strong>
                Password: <code>${data.password}</code><br>
                Attempts: ${data.attempts.toLocaleString()}<br>
                Time: ${data.time.toFixed(2)} seconds<br>
                Speed: ${data.attempts_per_second.toFixed(0)} passwords/second
            </div>
        `;
    } else {
        resultsDiv.innerHTML = `
            <div class="result-item result-error">
                <strong>✗ ${data.message || 'Password not found'}</strong><br>
                Attempts: ${data.attempts.toLocaleString()}<br>
                Time: ${data.time.toFixed(2)} seconds<br>
                The password was not found in the dictionary.
            </div>
        `;
    }
    
    resultsDiv.classList.remove('hidden');
    progressDiv.classList.add('hidden');
}

// Utility Functions
function showError(container, message) {
    container.innerHTML = `
        <div class="result-item result-error">
            <strong>Error</strong>
            ${message}
        </div>
    `;
    container.classList.remove('hidden');
}

// Enter key support
document.getElementById('analyze-password').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') analyzePassword();
});

document.getElementById('hash-password').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') generateHash();
});

document.getElementById('brute-password').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') startBruteForce();
});

document.getElementById('dict-hash').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') startDictionaryAttack();
});

