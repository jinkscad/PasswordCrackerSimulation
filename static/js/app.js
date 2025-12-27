// Socket.IO Connection
const socket = io();

// ============== INFO MODAL ==============
const attackInfo = {
    analyzer: {
        title: 'Password Strength Analyzer',
        content: `
            <p>The analyzer evaluates your password's security using multiple techniques inspired by <strong>zxcvbn</strong> (used by Dropbox, GitHub).</p>

            <h3>What We Check</h3>
            <ul>
                <li><strong>Common passwords:</strong> Compared against 1000+ leaked passwords</li>
                <li><strong>Keyboard patterns:</strong> qwerty, asdfgh, 1qaz2wsx, etc.</li>
                <li><strong>Sequential characters:</strong> abc, 123, cba, 321</li>
                <li><strong>Repeated characters:</strong> aaa, 111</li>
                <li><strong>Date patterns:</strong> Years like 2024, 1990</li>
                <li><strong>Leet speak:</strong> Detects p@ssw0rd as "password"</li>
            </ul>

            <h3>How Scoring Works</h3>
            <p>The score (0-100) is calculated from:</p>
            <div class="example-box">
                <code>Base Score = Entropy / 60 * 100</code>
                <code>Final = Base - Penalties + Bonuses</code>
            </div>

            <h3>Understanding Entropy</h3>
            <p>Entropy measures randomness in bits. Higher = more secure.</p>
            <ul>
                <li><strong>&lt;28 bits:</strong> Very weak (instant crack)</li>
                <li><strong>28-35 bits:</strong> Weak (minutes to hours)</li>
                <li><strong>36-59 bits:</strong> Moderate (days to months)</li>
                <li><strong>60-127 bits:</strong> Strong (years)</li>
                <li><strong>128+ bits:</strong> Very strong (centuries)</li>
            </ul>

            <h3>Crack Time Estimate</h3>
            <p>Based on 10 billion guesses/second (modern GPU attack speed). Real-world times vary based on:</p>
            <ul>
                <li>Online vs offline attacks</li>
                <li>Hash algorithm used</li>
                <li>Attacker's hardware</li>
            </ul>

            <h3>Tips for Strong Passwords</h3>
            <ul>
                <li>Use 12+ characters (16+ is better)</li>
                <li>Mix uppercase, lowercase, numbers, symbols</li>
                <li>Avoid dictionary words and personal info</li>
                <li>Use a password manager!</li>
            </ul>
        `
    },
    dictionary: {
        title: 'Dictionary Attack',
        content: `
            <p>A <strong>dictionary attack</strong> tries to crack passwords by testing words from a pre-made list (wordlist) of common passwords.</p>

            <h3>How It Works</h3>
            <p>1. You provide a <strong>hashed password</strong> (the encrypted version)<br>
               2. The tool loads a list of common passwords<br>
               3. It hashes each word and compares it to your target<br>
               4. If there's a match, the password is cracked!</p>

            <h3>What is a Hash?</h3>
            <p>A hash is a one-way encryption. For example, "password" becomes:</p>
            <div class="example-box">
                <code>MD5: 5f4dcc3b5aa765d61d8327deb882cf99</code>
                <code>SHA256: 5e884898da28047d...</code>
            </div>

            <h3>How to Use</h3>
            <ul>
                <li>Go to <strong>Hash Generator</strong> tab to create a hash from any password</li>
                <li>Paste the hash here and click "Start Attack"</li>
                <li>The tool will try common passwords + variations</li>
            </ul>

            <h3>Why It Works</h3>
            <p>Most people use simple, common passwords. Dictionary attacks are fast because they only try likely passwords instead of every possible combination.</p>
        `
    },
    bruteforce: {
        title: 'Brute Force Attack',
        content: `
            <p>A <strong>brute force attack</strong> tries <em>every possible combination</em> of characters until it finds the password.</p>

            <h3>How It Works</h3>
            <p>It systematically tries: a, b, c... then aa, ab, ac... then aaa, aab, and so on until it finds a match.</p>

            <h3>Settings Explained</h3>
            <ul>
                <li><strong>Character Set:</strong> What characters to try
                    <ul>
                        <li>Numeric: 0-9 (10 chars) - fastest</li>
                        <li>Lowercase: a-z (26 chars)</li>
                        <li>All: letters + numbers + symbols (95 chars) - slowest</li>
                    </ul>
                </li>
                <li><strong>Length:</strong> Password length range to try</li>
            </ul>

            <h3>Time Estimates</h3>
            <div class="example-box">
                <code>4-digit PIN: ~10,000 tries (instant)</code>
                <code>4-char password (all): ~81 million tries</code>
                <code>8-char password (all): ~6 quadrillion tries</code>
            </div>

            <h3>When to Use</h3>
            <p>Best for short passwords or when you know the character set (like PINs). Not practical for long, complex passwords.</p>
        `
    },
    mask: {
        title: 'Mask Attack',
        content: `
            <p>A <strong>mask attack</strong> is a smarter brute force. Instead of trying everything, you define a <em>pattern</em> the password follows.</p>

            <h3>Mask Placeholders</h3>
            <div class="example-box">
                <code>?d = digit (0-9)</code>
                <code>?l = lowercase letter (a-z)</code>
                <code>?u = uppercase letter (A-Z)</code>
                <code>?s = symbol (!@#$%...)</code>
                <code>?a = any character</code>
            </div>

            <h3>Example Masks</h3>
            <ul>
                <li><code>?d?d?d?d</code> = 4-digit PIN (0000-9999)</li>
                <li><code>?u?l?l?l?l?l</code> = Name like "Michael"</li>
                <li><code>?u?l?l?l?d?d?d?d</code> = Name + year like "John2024"</li>
                <li><code>?l?l?l?l?l?l?s</code> = 6 letters + symbol</li>
            </ul>

            <h3>Why It's Powerful</h3>
            <p>If you know someone uses a name + 4 digits, you can crack it much faster than pure brute force by only trying that pattern.</p>

            <h3>How to Use</h3>
            <p>1. Guess the password structure<br>
               2. Write a mask using placeholders<br>
               3. The tool tries all combinations matching that pattern</p>
        `
    },
    rainbow: {
        title: 'Rainbow Table Lookup',
        content: `
            <p>A <strong>rainbow table</strong> is a pre-computed database of passwords and their hashes. Instead of calculating hashes, you just look them up!</p>

            <h3>How It Works</h3>
            <p>1. Someone pre-computes millions of password hashes<br>
               2. They store them in a searchable table<br>
               3. You paste a hash, and it instantly finds the match</p>

            <h3>Speed Comparison</h3>
            <div class="example-box">
                <code>Brute Force: hours to years</code>
                <code>Rainbow Table: milliseconds</code>
            </div>

            <h3>Limitations</h3>
            <ul>
                <li>Only works for passwords that were pre-computed</li>
                <li>Tables can be huge (terabytes)</li>
                <li><strong>Defeated by salting</strong> - adding random data before hashing</li>
            </ul>

            <h3>What This Tool Does</h3>
            <p>It checks your hash against a local list of common passwords and optionally queries online hash databases.</p>

            <h3>Why Salting Matters</h3>
            <p>Modern systems add a random "salt" to passwords before hashing. This makes rainbow tables useless because each password has a unique hash.</p>
        `
    },
    rules: {
        title: 'Rule-based Attack',
        content: `
            <p>A <strong>rule-based attack</strong> takes a base word and applies transformations to generate password variations.</p>

            <h3>How It Works</h3>
            <p>Start with a word like "password" and apply rules:</p>
            <div class="example-box">
                <code>password → Password (capitalize)</code>
                <code>password → PASSWORD (uppercase)</code>
                <code>password → p@ssw0rd (leet speak)</code>
                <code>password → password123 (add numbers)</code>
                <code>password → password! (add symbol)</code>
            </div>

            <h3>Available Rules</h3>
            <ul>
                <li><strong>Case variations:</strong> upper, lower, capitalize</li>
                <li><strong>Leet speak:</strong> a→@, e→3, i→1, o→0, s→$</li>
                <li><strong>Append numbers:</strong> 1, 123, 2024, etc.</li>
                <li><strong>Append symbols:</strong> !, @, #, !@#</li>
                <li><strong>Prepend:</strong> add patterns at the start</li>
                <li><strong>Reverse:</strong> drowssap</li>
                <li><strong>Duplicate:</strong> passwordpassword</li>
            </ul>

            <h3>When to Use</h3>
            <p>When you suspect the password is based on a word (name, pet, favorite team) with common modifications. Much faster than brute force!</p>

            <h3>Tip</h3>
            <p>Click "Preview Rules" to see all generated variations before attacking.</p>
        `
    }
};

function showInfo(attackType) {
    const info = attackInfo[attackType];
    if (!info) return;

    document.getElementById('modal-title').textContent = info.title;
    document.getElementById('modal-body').innerHTML = info.content;
    document.getElementById('info-modal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeInfoModal() {
    document.getElementById('info-modal').classList.add('hidden');
    document.body.style.overflow = '';
}

// Close modal on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeInfoModal();
    }
});

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

    // Build the score section
    const scoreSection = document.getElementById('analyzer-score');
    scoreSection.innerHTML = `
        <div class="strength-meter">
            <div class="strength-bar">
                <div class="strength-fill ${strengthClass}" style="width: ${data.score}%"></div>
            </div>
            <div class="strength-label">${data.strength} (${data.score}/100)</div>
        </div>

        <div class="score-details">
            <div class="score-item">
                <span class="score-label">Length</span>
                <span class="score-value">${analysis.length} chars</span>
            </div>
            <div class="score-item">
                <span class="score-label">Entropy</span>
                <span class="score-value">${analysis.entropy.toFixed(1)} bits</span>
            </div>
            <div class="score-item">
                <span class="score-label">Crack Time</span>
                <span class="score-value crack-time">${analysis.crack_time_display || 'N/A'}</span>
            </div>
        </div>

        ${analysis.is_common ? '<div class="common-password-warning">This password appears in data breaches!</div>' : ''}
    `;

    // Character composition
    const compositionSection = document.getElementById('analyzer-composition');
    compositionSection.innerHTML = `
        <div class="section-title">Character Composition</div>
        <div class="char-composition">
            <span class="char-badge ${analysis.has_lowercase ? 'active' : ''}">a-z</span>
            <span class="char-badge ${analysis.has_uppercase ? 'active' : ''}">A-Z</span>
            <span class="char-badge ${analysis.has_digits ? 'active' : ''}">0-9</span>
            <span class="char-badge ${analysis.has_symbols ? 'active' : ''}">!@#</span>
        </div>
    `;

    // Warnings
    const warningsSection = document.getElementById('analyzer-warnings');
    if (analysis.warnings && analysis.warnings.length > 0) {
        warningsSection.innerHTML = `
            <div class="section-title warning-title">Warnings</div>
            <ul class="warning-list">
                ${analysis.warnings.map(w => `<li>${w}</li>`).join('')}
            </ul>
        `;
        warningsSection.style.display = 'block';
    } else {
        warningsSection.style.display = 'none';
    }

    // Suggestions
    const suggestionsSection = document.getElementById('analyzer-suggestions');
    if (analysis.suggestions && analysis.suggestions.length > 0) {
        suggestionsSection.innerHTML = `
            <div class="section-title suggestion-title">Suggestions</div>
            <ul class="suggestion-list">
                ${analysis.suggestions.map(s => `<li>${s}</li>`).join('')}
            </ul>
        `;
        suggestionsSection.style.display = 'block';
    } else {
        suggestionsSection.style.display = 'none';
    }

    // Score breakdown (collapsible)
    const breakdownSection = document.getElementById('analyzer-breakdown');
    if (analysis.score_breakdown) {
        const sb = analysis.score_breakdown;
        let breakdownHtml = `
            <details class="score-breakdown-details">
                <summary class="section-title">Score Breakdown</summary>
                <div class="breakdown-content">
                    <div class="breakdown-item">
                        <span>Base entropy score</span>
                        <span class="breakdown-value">${sb.base_entropy_score}</span>
                    </div>
        `;

        if (sb.penalties && sb.penalties.length > 0) {
            sb.penalties.forEach(([reason, value]) => {
                breakdownHtml += `
                    <div class="breakdown-item penalty">
                        <span>${reason}</span>
                        <span class="breakdown-value">${value}</span>
                    </div>
                `;
            });
        }

        if (sb.bonuses && sb.bonuses.length > 0) {
            sb.bonuses.forEach(([reason, value]) => {
                breakdownHtml += `
                    <div class="breakdown-item bonus">
                        <span>${reason}</span>
                        <span class="breakdown-value">+${value}</span>
                    </div>
                `;
            });
        }

        breakdownHtml += `
                    <div class="breakdown-item final">
                        <span>Final Score</span>
                        <span class="breakdown-value">${sb.final_score}</span>
                    </div>
                </div>
            </details>
        `;
        breakdownSection.innerHTML = breakdownHtml;
        breakdownSection.style.display = 'block';
    } else {
        breakdownSection.style.display = 'none';
    }

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

async function startBruteForceAttack() {
    const hash = document.getElementById('brute-hash').value;
    const algorithm = document.getElementById('brute-algorithm').value || null;
    const charset = document.getElementById('brute-charset').value;
    const minLength = parseInt(document.getElementById('brute-min-length').value) || 1;
    const maxLength = parseInt(document.getElementById('brute-max-length').value) || 4;
    const estimatesDiv = document.getElementById('brute-estimates');
    const progressDiv = document.getElementById('brute-progress');
    const resultsDiv = document.getElementById('brute-results');
    const stopBtn = document.getElementById('stop-brute-btn');

    if (!hash) {
        showError(resultsDiv, 'Please enter a hash to crack');
        return;
    }

    try {
        const response = await fetch('/api/bruteforce/attack', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                hash,
                algorithm,
                charset,
                min_length: minLength,
                max_length: maxLength
            })
        });

        const data = await response.json();

        if (response.ok) {
            currentBruteAttackId = data.attack_id;
            stopBtn.style.display = 'inline-block';

            // Show estimates
            estimatesDiv.innerHTML = `
                <div class="result-item">
                    <strong>Attack Configuration</strong><br>
                    Total Combinations: ${data.estimates.total_combinations.toLocaleString()}<br>
                    Character Set Size: ${data.estimates.charset_size}<br>
                    Length Range: ${data.estimates.min_length} - ${data.estimates.max_length}
                </div>
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

async function stopBruteForceAttack() {
    if (!currentBruteAttackId) return;

    try {
        await fetch('/api/bruteforce/stop', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ attack_id: currentBruteAttackId })
        });
        currentBruteAttackId = null;
        document.getElementById('stop-brute-btn').style.display = 'none';
        document.getElementById('brute-progress').classList.add('hidden');
    } catch (error) {
        console.error('Error stopping attack:', error);
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

// ============== MASK ATTACK ==============
let currentMaskAttackId = null;

function setMask(mask) {
    document.getElementById('mask-pattern').value = mask;
}

async function startMaskAttack() {
    const hash = document.getElementById('mask-hash').value;
    const algorithm = document.getElementById('mask-algorithm').value || null;
    const mask = document.getElementById('mask-pattern').value;
    const estimatesDiv = document.getElementById('mask-estimates');
    const progressDiv = document.getElementById('mask-progress');
    const resultsDiv = document.getElementById('mask-results');
    const stopBtn = document.getElementById('stop-mask-btn');

    if (!hash) {
        showError(resultsDiv, 'Please enter a hash to crack');
        return;
    }

    if (!mask) {
        showError(resultsDiv, 'Please enter a mask pattern');
        return;
    }

    try {
        const response = await fetch('/api/mask/attack', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ hash, algorithm, mask })
        });

        const data = await response.json();

        if (response.ok) {
            currentMaskAttackId = data.attack_id;
            stopBtn.style.display = 'inline-block';

            estimatesDiv.innerHTML = `
                <div class="result-item">
                    <strong>Attack Configuration</strong><br>
                    Mask: <code>${data.estimates.mask}</code><br>
                    Total Combinations: ${data.estimates.total_combinations.toLocaleString()}
                </div>
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

async function stopMaskAttack() {
    if (!currentMaskAttackId) return;

    try {
        await fetch('/api/mask/stop', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ attack_id: currentMaskAttackId })
        });
        currentMaskAttackId = null;
        document.getElementById('stop-mask-btn').style.display = 'none';
        document.getElementById('mask-progress').classList.add('hidden');
    } catch (error) {
        console.error('Error stopping attack:', error);
    }
}

// ============== RAINBOW TABLE LOOKUP ==============

async function lookupRainbowTable() {
    const hash = document.getElementById('rainbow-hash').value;
    const algorithm = document.getElementById('rainbow-algorithm').value || null;
    const useOnline = document.getElementById('rainbow-online').checked;
    const loadingDiv = document.getElementById('rainbow-loading');
    const resultsDiv = document.getElementById('rainbow-results');

    if (!hash) {
        showError(resultsDiv, 'Please enter a hash to lookup');
        return;
    }

    loadingDiv.classList.remove('hidden');
    resultsDiv.classList.add('hidden');

    try {
        const response = await fetch('/api/rainbow/lookup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ hash, algorithm, use_online: useOnline })
        });

        const data = await response.json();
        loadingDiv.classList.add('hidden');

        if (response.ok) {
            if (data.found) {
                resultsDiv.innerHTML = `
                    <div class="result-item result-success">
                        <strong>Hash Found!</strong><br>
                        Password: <code style="font-size: 1.2rem;">${data.password}</code><br>
                        Algorithm: ${data.algorithm.toUpperCase()}<br>
                        Source: ${data.sources.join(', ')}
                    </div>
                `;
            } else {
                resultsDiv.innerHTML = `
                    <div class="result-item result-error">
                        <strong>Hash Not Found</strong><br>
                        ${data.message || 'The hash was not found in any rainbow table.'}<br>
                        Algorithm: ${data.algorithm.toUpperCase()}
                    </div>
                `;
            }
            resultsDiv.classList.remove('hidden');
        } else {
            showError(resultsDiv, data.error || 'Lookup failed');
        }
    } catch (error) {
        loadingDiv.classList.add('hidden');
        showError(resultsDiv, 'Error looking up hash: ' + error.message);
    }
}

// ============== RULE-BASED ATTACK ==============
let currentRulesAttackId = null;

function getRuleSettings() {
    return {
        case: document.getElementById('rule-case').checked,
        leet: document.getElementById('rule-leet').checked,
        append_numbers: document.getElementById('rule-append-numbers').checked,
        append_symbols: document.getElementById('rule-append-symbols').checked,
        prepend: document.getElementById('rule-prepend').checked,
        reverse: document.getElementById('rule-reverse').checked,
        duplicate: document.getElementById('rule-duplicate').checked,
        toggle: document.getElementById('rule-toggle').checked
    };
}

async function previewRules() {
    const baseWord = document.getElementById('rules-base').value;
    const rules = getRuleSettings();
    const previewDiv = document.getElementById('rules-preview');

    if (!baseWord) {
        showError(previewDiv, 'Please enter a base word');
        return;
    }

    try {
        const response = await fetch('/api/rules/preview', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ base_word: baseWord, rules })
        });

        const data = await response.json();

        if (response.ok) {
            let html = `
                <div class="result-item">
                    <strong>Rule Preview</strong> (showing ${Math.min(100, data.total)} of ${data.total} candidates)<br><br>
                    <div style="max-height: 300px; overflow-y: auto; font-family: monospace; font-size: 0.85rem;">
            `;
            data.candidates.forEach(candidate => {
                html += `<div style="padding: 0.25rem 0;">- ${candidate}</div>`;
            });
            html += '</div></div>';
            previewDiv.innerHTML = html;
            previewDiv.classList.remove('hidden');
        } else {
            showError(previewDiv, data.error || 'Preview failed');
        }
    } catch (error) {
        showError(previewDiv, 'Error generating preview: ' + error.message);
    }
}

async function startRuleAttack() {
    const hash = document.getElementById('rules-hash').value;
    const algorithm = document.getElementById('rules-algorithm').value || null;
    const baseWord = document.getElementById('rules-base').value;
    const rules = getRuleSettings();
    const progressDiv = document.getElementById('rules-progress');
    const resultsDiv = document.getElementById('rules-results');
    const previewDiv = document.getElementById('rules-preview');
    const stopBtn = document.getElementById('stop-rules-btn');

    if (!hash) {
        showError(resultsDiv, 'Please enter a hash to crack');
        return;
    }

    if (!baseWord) {
        showError(resultsDiv, 'Please enter a base word');
        return;
    }

    try {
        const response = await fetch('/api/rules/attack', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ hash, algorithm, base_word: baseWord, rules })
        });

        const data = await response.json();

        if (response.ok) {
            currentRulesAttackId = data.attack_id;
            stopBtn.style.display = 'inline-block';

            previewDiv.innerHTML = `
                <div class="result-item">
                    <strong>Attack Started</strong><br>
                    Base Word: ${data.estimates.base_word}<br>
                    Total Candidates: ${data.estimates.total_candidates.toLocaleString()}
                </div>
            `;
            previewDiv.classList.remove('hidden');

            progressDiv.classList.remove('hidden');
            resultsDiv.classList.add('hidden');
        } else {
            showError(resultsDiv, data.error || 'Attack failed to start');
        }
    } catch (error) {
        showError(resultsDiv, 'Error starting attack: ' + error.message);
    }
}

async function stopRuleAttack() {
    if (!currentRulesAttackId) return;

    try {
        await fetch('/api/rules/stop', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ attack_id: currentRulesAttackId })
        });
        currentRulesAttackId = null;
        document.getElementById('stop-rules-btn').style.display = 'none';
        document.getElementById('rules-progress').classList.add('hidden');
    } catch (error) {
        console.error('Error stopping attack:', error);
    }
}

// Socket.IO Event Handlers
socket.on('attack_progress', (data) => {
    if (data.type === 'bruteforce' && data.attack_id === currentBruteAttackId) {
        updateBruteProgress(data);
    } else if (data.type === 'dictionary' && data.attack_id === currentDictAttackId) {
        updateDictProgress(data);
    } else if (data.type === 'mask' && data.attack_id === currentMaskAttackId) {
        updateMaskProgress(data);
    } else if (data.type === 'rules' && data.attack_id === currentRulesAttackId) {
        updateRulesProgress(data);
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
    } else if (data.type === 'mask' && data.attack_id === currentMaskAttackId) {
        showMaskResults(data);
        currentMaskAttackId = null;
        document.getElementById('stop-mask-btn').style.display = 'none';
    } else if (data.type === 'rules' && data.attack_id === currentRulesAttackId) {
        showRulesResults(data);
        currentRulesAttackId = null;
        document.getElementById('stop-rules-btn').style.display = 'none';
    }
});

socket.on('attack_error', (data) => {
    let resultsDiv;
    switch (data.type) {
        case 'bruteforce':
            resultsDiv = document.getElementById('brute-results');
            currentBruteAttackId = null;
            document.getElementById('stop-brute-btn').style.display = 'none';
            break;
        case 'dictionary':
            resultsDiv = document.getElementById('dict-results');
            currentDictAttackId = null;
            document.getElementById('stop-dict-btn').style.display = 'none';
            break;
        case 'mask':
            resultsDiv = document.getElementById('mask-results');
            currentMaskAttackId = null;
            document.getElementById('stop-mask-btn').style.display = 'none';
            break;
        case 'rules':
            resultsDiv = document.getElementById('rules-results');
            currentRulesAttackId = null;
            document.getElementById('stop-rules-btn').style.display = 'none';
            break;
        default:
            resultsDiv = document.getElementById('dict-results');
    }
    showError(resultsDiv, data.error || 'Attack error occurred');
});

function updateBruteProgress(data) {
    const progressFill = document.getElementById('brute-progress-fill');
    const progressText = document.getElementById('brute-progress-text');

    if (data.progress !== undefined) {
        progressFill.style.width = data.progress + '%';
        progressText.textContent = `Testing: ${data.current || '...'} | ${data.attempts?.toLocaleString() || 0}/${data.total?.toLocaleString() || 0} | ${data.speed?.toLocaleString() || 0}/sec`;
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

function updateMaskProgress(data) {
    const progressFill = document.getElementById('mask-progress-fill');
    const progressText = document.getElementById('mask-progress-text');

    if (data.progress !== undefined) {
        progressFill.style.width = data.progress + '%';
        progressText.textContent = `Testing: ${data.current || '...'} | ${data.attempts?.toLocaleString() || 0}/${data.total?.toLocaleString() || 0} | ${data.speed?.toLocaleString() || 0}/sec`;
    } else {
        progressText.textContent = data.message || 'Running...';
    }
}

function updateRulesProgress(data) {
    const progressFill = document.getElementById('rules-progress-fill');
    const progressText = document.getElementById('rules-progress-text');

    if (data.progress !== undefined) {
        progressFill.style.width = data.progress + '%';
        progressText.textContent = `Testing: ${data.current || '...'} | ${data.attempts?.toLocaleString() || 0}/${data.total?.toLocaleString() || 0}`;
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

function showMaskResults(data) {
    const resultsDiv = document.getElementById('mask-results');
    const progressDiv = document.getElementById('mask-progress');

    if (data.status === 'success') {
        resultsDiv.innerHTML = `
            <div class="result-item result-success">
                <strong>Password Cracked!</strong><br>
                Password: <code style="font-size: 1.2rem;">${data.password}</code><br>
                Attempts: ${data.attempts.toLocaleString()}<br>
                Time: ${data.time.toFixed(2)} seconds<br>
                Speed: ${data.attempts_per_second.toLocaleString()} attempts/second
            </div>
        `;
    } else {
        resultsDiv.innerHTML = `
            <div class="result-item result-error">
                <strong>${data.message || 'Password not found'}</strong><br>
                Attempts: ${data.attempts.toLocaleString()}<br>
                Time: ${data.time.toFixed(2)} seconds<br>
                The password did not match the given mask pattern.
            </div>
        `;
    }

    resultsDiv.classList.remove('hidden');
    progressDiv.classList.add('hidden');
    currentMaskAttackId = null;
}

function showRulesResults(data) {
    const resultsDiv = document.getElementById('rules-results');
    const progressDiv = document.getElementById('rules-progress');

    if (data.status === 'success') {
        resultsDiv.innerHTML = `
            <div class="result-item result-success">
                <strong>Password Cracked!</strong><br>
                Password: <code style="font-size: 1.2rem;">${data.password}</code><br>
                Attempts: ${data.attempts.toLocaleString()}<br>
                Time: ${data.time.toFixed(2)} seconds<br>
                Speed: ${data.attempts_per_second.toLocaleString()} attempts/second
            </div>
        `;
    } else {
        resultsDiv.innerHTML = `
            <div class="result-item result-error">
                <strong>${data.message || 'Password not found'}</strong><br>
                Attempts: ${data.attempts.toLocaleString()}<br>
                Time: ${data.time.toFixed(2)} seconds<br>
                The password was not found with the given rules.
            </div>
        `;
    }

    resultsDiv.classList.remove('hidden');
    progressDiv.classList.add('hidden');
    currentRulesAttackId = null;
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
document.getElementById('analyze-password')?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') analyzePassword();
});

document.getElementById('hash-password')?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') generateHash();
});

document.getElementById('dict-hash')?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') startDictionaryAttack();
});

document.getElementById('breach-password')?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') checkPasswordBreach();
});

document.getElementById('brute-hash')?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') startBruteForceAttack();
});

document.getElementById('mask-hash')?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') startMaskAttack();
});

document.getElementById('rainbow-hash')?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') lookupRainbowTable();
});

document.getElementById('rules-hash')?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') startRuleAttack();
});

