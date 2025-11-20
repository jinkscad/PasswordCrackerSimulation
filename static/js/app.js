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

// Password Toggle Function
function togglePassword(inputId, toggleId) {
    const input = document.getElementById(inputId);
    const toggle = document.getElementById(toggleId);
    const eyeIcon = toggle.querySelector('.eye-icon');
    
    if (input.type === 'password') {
        input.type = 'text';
        toggle.classList.add('active');
        eyeIcon.textContent = '🙈'; // Closed eye when password is visible
    } else {
        input.type = 'password';
        toggle.classList.remove('active');
        eyeIcon.textContent = '👁️'; // Open eye when password is hidden
    }
}

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
            Lowercase: ${analysis.has_lowercase ? 'Yes' : 'No'}<br>
            Uppercase: ${analysis.has_uppercase ? 'Yes' : 'No'}<br>
            Digits: ${analysis.has_digits ? 'Yes' : 'No'}<br>
            Symbols: ${analysis.has_symbols ? 'Yes' : 'No'}
        </div>
        <div class="result-item">
            <strong>Estimated Entropy</strong>
            ${analysis.entropy.toFixed(1)} bits
        </div>
        ${analysis.common_patterns.length > 0 ? `
            <div class="result-item result-error">
                <strong>Warning: Common Patterns Detected</strong>
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

// Password Breach Checker
async function checkPasswordBreach() {
    const password = document.getElementById('breach-password').value;
    const loadingDiv = document.getElementById('breach-loading');
    const resultsDiv = document.getElementById('breach-results');
    const timelineDiv = document.getElementById('breach-timeline');
    const riskDiv = document.getElementById('breach-risk');
    
    if (!password) {
        showError(resultsDiv, 'Please enter a password to check');
        return;
    }
    
    // Show loading
    loadingDiv.classList.remove('hidden');
    resultsDiv.classList.add('hidden');
    timelineDiv.classList.add('hidden');
    riskDiv.classList.add('hidden');
    
    try {
        const response = await fetch('/api/breach/check', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayBreachResults(data);
        } else {
            showError(resultsDiv, data.error || 'Breach check failed');
            loadingDiv.classList.add('hidden');
        }
    } catch (error) {
        showError(resultsDiv, 'Error checking password: ' + error.message);
        loadingDiv.classList.add('hidden');
    }
}

function displayBreachResults(data) {
    const loadingDiv = document.getElementById('breach-loading');
    const resultsDiv = document.getElementById('breach-results');
    const timelineDiv = document.getElementById('breach-timeline');
    const riskDiv = document.getElementById('breach-risk');
    
    loadingDiv.classList.add('hidden');
    
    const breach = data.breach;
    const risk = data.risk_assessment;
    
    // Main results
    const riskColor = getRiskColor(breach.risk_level);
    const riskIcon = getRiskIcon(breach.risk_level);
    
    let resultsHTML = `
        <div class="result-item" style="border-left-color: ${riskColor}; background: ${riskColor}15;">
            <strong style="color: ${riskColor}; font-size: 1.2rem;">${riskIcon} ${breach.message}</strong>
    `;
    
    if (breach.breached) {
        resultsHTML += `
            <div style="margin-top: 1rem;">
                <div style="font-size: 2rem; font-weight: bold; color: ${riskColor};">
                    ${breach.count.toLocaleString()}
                </div>
                <div style="color: var(--text-muted);">times found in data breaches</div>
            </div>
        `;
    }
    
    resultsHTML += `</div>`;
    resultsDiv.innerHTML = resultsHTML;
    resultsDiv.classList.remove('hidden');
    
    // Timeline
    if (breach.breach_timeline && breach.breach_timeline.length > 0) {
        let timelineHTML = `
            <div class="result-item">
                <strong>📅 Breach Timeline</strong>
                <div class="timeline" style="margin-top: 1rem;">
        `;
        
        breach.breach_timeline.forEach((entry, index) => {
            timelineHTML += `
                <div class="timeline-item" style="animation-delay: ${index * 0.1}s;">
                    <div class="timeline-marker" style="background: ${riskColor};"></div>
                    <div class="timeline-content">
                        <div class="timeline-date">${entry.formatted_date}</div>
                        <div class="timeline-source">${entry.source}</div>
                        <div class="timeline-count">${entry.count.toLocaleString()} occurrences</div>
                    </div>
                </div>
            `;
        });
        
        timelineHTML += `</div></div>`;
        timelineDiv.innerHTML = timelineHTML;
        timelineDiv.classList.remove('hidden');
    }
    
    // Risk Assessment
    let riskHTML = `
        <div class="result-item">
            <strong>🛡️ Comprehensive Risk Assessment</strong>
            <div style="margin-top: 1rem;">
                <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                    <div style="font-size: 3rem; font-weight: bold; color: ${riskColor};">
                        ${getRiskIcon(risk.overall_risk)}
                    </div>
                    <div>
                        <div style="font-size: 1.5rem; font-weight: bold; color: ${riskColor}; text-transform: uppercase;">
                            ${risk.overall_risk} Risk
                        </div>
                        <div style="color: var(--text-muted);">Password Strength: ${risk.strength_level} (${risk.strength_score}/100)</div>
                    </div>
                </div>
    `;
    
    if (risk.risk_factors && risk.risk_factors.length > 0) {
        riskHTML += `<div style="margin-top: 1rem;"><strong>Risk Factors:</strong></div>`;
        risk.risk_factors.forEach(factor => {
            const factorColor = getRiskColor(factor.severity);
            riskHTML += `
                <div style="margin-top: 0.5rem; padding: 0.75rem; background: ${factorColor}15; border-left: 3px solid ${factorColor}; border-radius: 4px;">
                    <strong style="color: ${factorColor};">${factor.factor}</strong> - ${factor.description}
                </div>
            `;
        });
    }
    
    if (risk.recommendations && risk.recommendations.length > 0) {
        riskHTML += `<div style="margin-top: 1.5rem;"><strong>💡 Recommendations:</strong></div><ul style="margin-top: 0.5rem; padding-left: 1.5rem;">`;
        risk.recommendations.forEach(rec => {
            riskHTML += `<li style="margin-top: 0.5rem; color: var(--text);">${rec}</li>`;
        });
        riskHTML += `</ul>`;
    }
    
    riskHTML += `</div></div>`;
    riskDiv.innerHTML = riskHTML;
    riskDiv.classList.remove('hidden');
}

function getRiskColor(level) {
    const colors = {
        'safe': '#10b981',
        'low': '#f59e0b',
        'medium': '#f97316',
        'high': '#ef4444',
        'critical': '#dc2626',
        'unknown': '#64748b'
    };
    return colors[level] || colors.unknown;
}

function getRiskIcon(level) {
    const icons = {
        'safe': 'SAFE',
        'low': 'LOW',
        'medium': 'MEDIUM',
        'high': 'HIGH',
        'critical': 'CRITICAL',
        'unknown': 'UNKNOWN'
    };
    return icons[level] || icons.unknown;
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
    const algorithm = document.getElementById('dict-algorithm').value || null;
    const useVariations = document.getElementById('dict-variations').checked;
    const usePatterns = document.getElementById('dict-patterns').checked;
    const progressDiv = document.getElementById('dict-progress');
    const resultsDiv = document.getElementById('dict-results');
    const statsDiv = document.getElementById('dict-statistics');
    const startBtn = document.querySelector('#dictionary .btn-danger');
    const pauseBtn = document.getElementById('pause-dict-btn');
    const resumeBtn = document.getElementById('resume-dict-btn');
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
                algorithm,
                use_variations: useVariations,
                use_patterns: usePatterns
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentDictAttackId = data.attack_id;
            startBtn.style.display = 'none';
            pauseBtn.style.display = 'inline-block';
            stopBtn.style.display = 'inline-block';
            progressDiv.classList.remove('hidden');
            resultsDiv.classList.add('hidden');
            statsDiv.classList.add('hidden');
        } else {
            showError(resultsDiv, data.error || 'Attack failed to start');
        }
    } catch (error) {
        showError(resultsDiv, 'Error starting attack: ' + error.message);
    }
}

async function pauseDictionaryAttack() {
    if (!currentDictAttackId) return;
    
    try {
        await fetch('/api/dictionary/pause', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ attack_id: currentDictAttackId })
        });
        document.getElementById('pause-dict-btn').style.display = 'none';
        document.getElementById('resume-dict-btn').style.display = 'inline-block';
    } catch (error) {
        console.error('Error pausing attack:', error);
    }
}

async function resumeDictionaryAttack() {
    if (!currentDictAttackId) return;
    
    try {
        await fetch('/api/dictionary/resume', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ attack_id: currentDictAttackId })
        });
        document.getElementById('pause-dict-btn').style.display = 'inline-block';
        document.getElementById('resume-dict-btn').style.display = 'none';
    } catch (error) {
        console.error('Error resuming attack:', error);
    }
}

async function stopDictionaryAttack() {
    if (!currentDictAttackId) return;
    
    try {
        await fetch('/api/dictionary/stop', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ attack_id: currentDictAttackId })
        });
        currentDictAttackId = null;
        document.querySelector('#dictionary .btn-danger').style.display = 'inline-block';
        document.getElementById('pause-dict-btn').style.display = 'none';
        document.getElementById('resume-dict-btn').style.display = 'none';
        document.getElementById('stop-dict-btn').style.display = 'none';
    } catch (error) {
        console.error('Error stopping attack:', error);
    }
}

// Stop Attack (for brute force - dictionary has its own function)
function stopBruteForceAttack() {
    // Placeholder for brute force stop functionality
    if (currentBruteAttackId) {
        currentBruteAttackId = null;
        document.getElementById('stop-brute-btn').style.display = 'none';
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
                <strong>Password Cracked</strong>
                Password: <code>${data.password}</code><br>
                Attempts: ${data.attempts.toLocaleString()}<br>
                Time: ${data.time.toFixed(2)} seconds<br>
                Speed: ${data.attempts_per_second.toFixed(0)} attempts/second
            </div>
        `;
    } else {
        resultsDiv.innerHTML = `
            <div class="result-item result-error">
                <strong>${data.message || 'Attack failed'}</strong><br>
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
    const statsDiv = document.getElementById('dict-statistics');
    const progressDiv = document.getElementById('dict-progress');
    const startBtn = document.querySelector('#dictionary .btn-danger');
    const pauseBtn = document.getElementById('pause-dict-btn');
    const resumeBtn = document.getElementById('resume-dict-btn');
    const stopBtn = document.getElementById('stop-dict-btn');
    
    // Reset buttons
    startBtn.style.display = 'inline-block';
    pauseBtn.style.display = 'none';
    resumeBtn.style.display = 'none';
    stopBtn.style.display = 'none';
    
    if (data.status === 'success') {
        resultsDiv.innerHTML = `
            <div class="result-item result-success">
                <strong>Password Cracked</strong>
                Password: <code>${data.password}</code><br>
                Attempts: ${data.attempts.toLocaleString()}<br>
                Time: ${data.time.toFixed(2)} seconds<br>
                Speed: ${data.attempts_per_second.toFixed(0)} passwords/second
            </div>
        `;
    } else {
        resultsDiv.innerHTML = `
            <div class="result-item result-error">
                <strong>${data.message || 'Password not found'}</strong><br>
                Attempts: ${data.attempts.toLocaleString()}<br>
                Time: ${data.time.toFixed(2)} seconds<br>
                The password was not found in the dictionary.
            </div>
        `;
    }
    
    // Show statistics
    if (data.passwords_tested !== undefined) {
        let statsHTML = `
            <div class="result-item">
                <strong>Attack Statistics</strong><br>
                Total Passwords Tested: ${data.passwords_tested.toLocaleString()}<br>
                Attempts: ${data.attempts.toLocaleString()}<br>
                Time Elapsed: ${data.time.toFixed(2)} seconds<br>
                Speed: ${data.attempts_per_second.toFixed(0)} passwords/second
        `;
        
        if (data.tested_passwords && data.tested_passwords.length > 0) {
            statsHTML += `<br><br><strong>Last ${Math.min(20, data.tested_passwords.length)} Tested Passwords:</strong><br>`;
            statsHTML += '<div style="max-height: 200px; overflow-y: auto; margin-top: 0.5rem;">';
            data.tested_passwords.forEach(pwd => {
                statsHTML += `<div style="font-family: monospace; font-size: 0.85rem; padding: 0.25rem 0;">• ${pwd}</div>`;
            });
            statsHTML += '</div>';
        }
        
        statsHTML += '</div>';
        statsDiv.innerHTML = statsHTML;
        statsDiv.classList.remove('hidden');
    }
    
    resultsDiv.classList.remove('hidden');
    progressDiv.classList.add('hidden');
    currentDictAttackId = null;
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

document.getElementById('breach-password').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') checkPasswordBreach();
});

