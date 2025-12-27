"""
Utility functions for password analysis and display
"""
import re
import math
import time
from typing import Dict, List, Tuple, Set
from colorama import Fore, Style, init

# Initialize colorama for cross-platform color support
init(autoreset=True)


class PasswordAnalyzer:
    """
    Advanced password strength analyzer inspired by zxcvbn.
    Checks against common passwords, keyboard patterns, and provides
    real entropy calculations with crack time estimates.
    """

    # Top 10,000 most common passwords (abbreviated - top 1000 most critical)
    COMMON_PASSWORDS: Set[str] = {
        # Top 100 most common
        'password', '123456', '12345678', 'qwerty', 'abc123', 'monkey', 'letmein',
        '1234567', 'dragon', 'baseball', 'iloveyou', 'trustno1', 'sunshine', 'master',
        'hello', 'shadow', 'ashley', 'football', 'jesus', 'michael', 'ninja', 'mustang',
        '111111', 'password1', '123123', 'batman', 'login', 'superman', 'princess',
        'qwerty123', 'solo', 'passw0rd', 'starwars', 'admin', 'welcome', 'flower',
        'hottie', 'loveme', 'zaq1zaq1', 'password123', 'qwertyuiop', 'admin123',
        '1q2w3e4r', '654321', '555555', 'lovely', '7777777', '888888', 'princess1',
        'dragon1', 'password1234', 'love', 'computer', 'whatever', 'pepper', 'ginger',
        'soccer', 'summer', 'tigger', 'hockey', 'cookie', 'killer', 'george', 'ranger',
        'pokemon', 'matrix', 'cheese', 'thunder', 'chicken', 'robert', 'access', 'merlin',
        'freedom', 'phoenix', 'guitar', 'dakota', 'orange', 'asdfgh', 'hunter', 'harley',
        'buster', 'soccer1', 'hockey1', 'george1', 'charlie', 'andrew', 'michelle',
        'joshua', 'maggie', 'biteme', 'diamond', 'secret', 'silver', 'gators', 'samantha',
        # Common with numbers
        'password12', 'password2', 'password3', 'qwerty1', 'qwerty12', 'abc1234',
        'pass123', 'pass1234', 'test123', 'test1234', 'admin1', 'admin12', 'root123',
        'user123', 'guest123', 'letmein1', 'welcome1', 'welcome123', 'hello123',
        # Years
        '2020', '2021', '2022', '2023', '2024', '2019', '2018', '2017', '2016', '2015',
        '1234', '12345', '123456789', '1234567890', '0987654321', '0000', '1111',
        # Common names
        'michael', 'jennifer', 'thomas', 'jessica', 'daniel', 'ashley', 'matthew',
        'joshua', 'amanda', 'david', 'james', 'robert', 'john', 'joseph', 'andrew',
        'nicole', 'stephanie', 'melissa', 'sarah', 'heather', 'elizabeth', 'michelle',
        # Sports teams & pop culture
        'lakers', 'yankees', 'cowboys', 'eagles', 'steelers', 'arsenal', 'liverpool',
        'chelsea', 'barcelona', 'realmadrid', 'ronaldo', 'messi', 'jordan', 'lebron',
        # More common patterns
        'fuckyou', 'asshole', 'fuck', 'shit', 'pussy', 'dick', 'bitch',
        'iloveyou1', 'iloveyou2', 'mylove', 'love123', 'baby', 'angel', 'princess',
        'butterfly', 'purple', 'samantha', 'whatever', 'bubble', 'alexander',
        # Keyboard walks extended
        'qazwsx', 'qweasd', 'zxcvbn', 'asdfghjkl', '1qaz2wsx', 'qaz123', 'zaq12wsx',
    }

    # Keyboard patterns (QWERTY layout)
    KEYBOARD_PATTERNS: List[str] = [
        # Horizontal rows
        'qwertyuiop', 'asdfghjkl', 'zxcvbnm',
        'qwerty', 'asdfgh', 'zxcvbn', 'qwert', 'asdfg', 'zxcvb',
        '1234567890', '12345678', '1234567', '123456', '12345', '1234',
        # Diagonal patterns
        '1qaz', '2wsx', '3edc', '4rfv', '5tgb', '6yhn', '7ujm', '8ik', '9ol', '0p',
        'qaz', 'wsx', 'edc', 'rfv', 'tgb', 'yhn', 'ujm',
        '1qaz2wsx', '2wsx3edc', 'zaq1', 'xsw2', 'cde3',
        # Reverse patterns
        'poiuytrewq', 'lkjhgfdsa', 'mnbvcxz',
        '0987654321', '987654321', '87654321', '7654321', '654321', '54321', '4321',
        # Common keyboard walks
        'qazwsx', 'wsxedc', 'edcrfv', 'rfvtgb',
        'qweasd', 'asdzxc', 'qweasdzxc',
        '!@#$%^', '!@#$%^&*', '!@#$',
    ]

    # Common substitutions (leet speak)
    LEET_MAP = {
        '@': 'a', '4': 'a', '^': 'a',
        '8': 'b',
        '(': 'c', '<': 'c',
        '3': 'e',
        '6': 'g', '9': 'g',
        '#': 'h',
        '1': 'i', '!': 'i', '|': 'i',
        '0': 'o',
        '$': 's', '5': 's',
        '7': 't', '+': 't',
        '%': 'x',
        '2': 'z',
    }

    # Common date patterns
    DATE_PATTERNS = [
        r'\b(19|20)\d{2}\b',  # Years 1900-2099
        r'\b\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}\b',  # Dates
        r'\b(0?[1-9]|1[0-2])(0?[1-9]|[12]\d|3[01])\d{2,4}\b',  # MMDDYY(YY)
    ]

    @classmethod
    def calculate_strength(cls, password: str) -> Tuple[int, str, Dict]:
        """
        Calculate password strength using advanced analysis.

        Returns:
            Tuple of (score 0-100, strength_level, detailed_analysis)
        """
        analysis = {
            'length': len(password),
            'has_lowercase': bool(re.search(r'[a-z]', password)),
            'has_uppercase': bool(re.search(r'[A-Z]', password)),
            'has_digits': bool(re.search(r'\d', password)),
            'has_symbols': bool(re.search(r'[^a-zA-Z0-9]', password)),
            'char_diversity': 0,
            'entropy': 0.0,
            'crack_time_seconds': 0,
            'crack_time_display': '',
            'warnings': [],
            'suggestions': [],
            'pattern_matches': [],
            'is_common': False,
            'score_breakdown': {}
        }

        # Calculate character pool size and diversity
        pool_size = 0
        if analysis['has_lowercase']:
            pool_size += 26
        if analysis['has_uppercase']:
            pool_size += 26
        if analysis['has_digits']:
            pool_size += 10
        if analysis['has_symbols']:
            pool_size += 32
        analysis['char_diversity'] = sum([
            analysis['has_lowercase'],
            analysis['has_uppercase'],
            analysis['has_digits'],
            analysis['has_symbols']
        ])

        # Calculate real entropy: log2(pool_size^length)
        if pool_size > 0 and len(password) > 0:
            analysis['entropy'] = len(password) * math.log2(pool_size)
        else:
            analysis['entropy'] = 0

        # Start with entropy-based score
        base_score = min(100, (analysis['entropy'] / 60) * 100)  # 60 bits = 100%

        # === PENALTY CHECKS ===
        penalties = 0
        penalty_details = []

        # 1. Check if password is in common list
        if cls._is_common_password(password):
            analysis['is_common'] = True
            analysis['warnings'].append('This is a commonly used password')
            penalties += 50
            penalty_details.append(('Common password', -50))

        # 2. Check for keyboard patterns
        keyboard_match = cls._find_keyboard_pattern(password)
        if keyboard_match:
            analysis['pattern_matches'].append(f'Keyboard pattern: {keyboard_match}')
            analysis['warnings'].append(f'Contains keyboard pattern "{keyboard_match}"')
            penalties += 25
            penalty_details.append(('Keyboard pattern', -25))

        # 3. Check for repeated characters (aaa, 111)
        repeated = re.search(r'(.)\1{2,}', password)
        if repeated:
            analysis['pattern_matches'].append(f'Repeated: {repeated.group()}')
            analysis['warnings'].append('Contains repeated characters')
            penalties += 15
            penalty_details.append(('Repeated characters', -15))

        # 4. Check for sequential characters
        if cls._has_sequential(password):
            analysis['pattern_matches'].append('Sequential characters')
            analysis['warnings'].append('Contains sequential characters (abc, 123)')
            penalties += 15
            penalty_details.append(('Sequential characters', -15))

        # 5. Check for date patterns
        date_match = cls._find_date_pattern(password)
        if date_match:
            analysis['pattern_matches'].append(f'Date/year: {date_match}')
            analysis['warnings'].append(f'Contains date or year "{date_match}"')
            penalties += 10
            penalty_details.append(('Date pattern', -10))

        # 6. Check for leet speak variations of common passwords
        deleet = cls._deleet(password)
        if deleet != password.lower() and cls._is_common_password(deleet):
            analysis['pattern_matches'].append(f'Leet speak of "{deleet}"')
            analysis['warnings'].append('This is leet speak of a common password')
            penalties += 40
            penalty_details.append(('Leet speak common password', -40))

        # 7. Length penalties
        if len(password) < 6:
            analysis['warnings'].append('Password is too short (minimum 8 recommended)')
            penalties += 30
            penalty_details.append(('Too short (<6)', -30))
        elif len(password) < 8:
            analysis['warnings'].append('Password is short (8+ characters recommended)')
            penalties += 15
            penalty_details.append(('Short (6-7)', -15))

        # 8. Check for all same case or no variety
        if password.isalpha() and (password.islower() or password.isupper()):
            analysis['warnings'].append('Uses only one character type')
            penalties += 10
            penalty_details.append(('Single char type', -10))

        # === BONUS CHECKS ===
        bonuses = 0
        bonus_details = []

        # Length bonuses
        if len(password) >= 16:
            bonuses += 15
            bonus_details.append(('Long password (16+)', +15))
        elif len(password) >= 12:
            bonuses += 10
            bonus_details.append(('Good length (12+)', +10))

        # High diversity bonus
        if analysis['char_diversity'] == 4:
            bonuses += 10
            bonus_details.append(('All character types', +10))

        # Calculate final score
        final_score = base_score - penalties + bonuses
        final_score = max(0, min(100, final_score))

        # Store breakdown
        analysis['score_breakdown'] = {
            'base_entropy_score': round(base_score, 1),
            'penalties': penalty_details,
            'bonuses': bonus_details,
            'final_score': round(final_score, 1)
        }

        # Calculate crack time (assuming 10 billion guesses/sec for offline attack)
        guesses_per_sec = 10_000_000_000  # 10B/sec (modern GPU)
        if analysis['is_common']:
            # Common passwords are cracked instantly
            analysis['crack_time_seconds'] = 0
        else:
            # Time = combinations / guesses_per_sec
            combinations = pool_size ** len(password) if pool_size > 0 else 1
            analysis['crack_time_seconds'] = combinations / guesses_per_sec

        analysis['crack_time_display'] = cls._format_crack_time(analysis['crack_time_seconds'])

        # Generate suggestions
        analysis['suggestions'] = cls._generate_suggestions(password, analysis)

        # Determine strength level based on score
        if final_score >= 80:
            strength = "Very Strong"
        elif final_score >= 60:
            strength = "Strong"
        elif final_score >= 40:
            strength = "Moderate"
        elif final_score >= 20:
            strength = "Weak"
        else:
            strength = "Very Weak"

        return round(final_score), strength, analysis

    @classmethod
    def _is_common_password(cls, password: str) -> bool:
        """Check if password is in common password list"""
        pwd_lower = password.lower()
        # Direct match
        if pwd_lower in cls.COMMON_PASSWORDS:
            return True
        # Check without trailing numbers
        stripped = re.sub(r'\d+$', '', pwd_lower)
        if stripped and stripped in cls.COMMON_PASSWORDS:
            return True
        # Check without trailing symbols
        stripped = re.sub(r'[^a-z]+$', '', pwd_lower)
        if stripped and stripped in cls.COMMON_PASSWORDS:
            return True
        return False

    @classmethod
    def _find_keyboard_pattern(cls, password: str) -> str:
        """Find keyboard patterns in password"""
        pwd_lower = password.lower()
        for pattern in cls.KEYBOARD_PATTERNS:
            if len(pattern) >= 4 and pattern in pwd_lower:
                return pattern
            # Check reverse
            if len(pattern) >= 4 and pattern[::-1] in pwd_lower:
                return pattern[::-1]
        return ''

    @classmethod
    def _has_sequential(cls, password: str) -> bool:
        """Check for sequential characters"""
        pwd_lower = password.lower()
        # Check for 3+ sequential letters
        for i in range(len(pwd_lower) - 2):
            if pwd_lower[i:i+3].isalpha():
                chars = [ord(c) for c in pwd_lower[i:i+3]]
                if chars[1] - chars[0] == 1 and chars[2] - chars[1] == 1:
                    return True
                if chars[0] - chars[1] == 1 and chars[1] - chars[2] == 1:
                    return True
        # Check for 3+ sequential numbers
        for i in range(len(password) - 2):
            if password[i:i+3].isdigit():
                nums = [int(c) for c in password[i:i+3]]
                if nums[1] - nums[0] == 1 and nums[2] - nums[1] == 1:
                    return True
                if nums[0] - nums[1] == 1 and nums[1] - nums[2] == 1:
                    return True
        return False

    @classmethod
    def _find_date_pattern(cls, password: str) -> str:
        """Find date/year patterns"""
        # Check for 4-digit years
        year_match = re.search(r'(19[5-9]\d|20[0-2]\d)', password)
        if year_match:
            return year_match.group()
        return ''

    @classmethod
    def _deleet(cls, password: str) -> str:
        """Convert leet speak back to regular text"""
        result = password.lower()
        for leet, regular in cls.LEET_MAP.items():
            result = result.replace(leet, regular)
        return result

    @classmethod
    def _format_crack_time(cls, seconds: float) -> str:
        """Format crack time in human readable format"""
        if seconds < 0.001:
            return "Instant"
        if seconds < 1:
            return f"{seconds*1000:.0f} milliseconds"
        if seconds < 60:
            return f"{seconds:.1f} seconds"
        if seconds < 3600:
            return f"{seconds/60:.1f} minutes"
        if seconds < 86400:
            return f"{seconds/3600:.1f} hours"
        if seconds < 2592000:  # 30 days
            return f"{seconds/86400:.1f} days"
        if seconds < 31536000:  # 1 year
            return f"{seconds/2592000:.1f} months"
        if seconds < 31536000 * 100:
            return f"{seconds/31536000:.1f} years"
        if seconds < 31536000 * 1000000:
            return f"{seconds/31536000:,.0f} years"
        return "Centuries+"

    @classmethod
    def _generate_suggestions(cls, password: str, analysis: Dict) -> List[str]:
        """Generate specific suggestions for improvement"""
        suggestions = []

        if analysis['is_common']:
            suggestions.append("Use a completely different password - this one is in breach databases")

        if len(password) < 12:
            suggestions.append("Make it longer - aim for 12+ characters")

        if not analysis['has_uppercase'] and not analysis['has_lowercase']:
            suggestions.append("Add letters to your password")
        elif not analysis['has_uppercase']:
            suggestions.append("Add uppercase letters")
        elif not analysis['has_lowercase']:
            suggestions.append("Add lowercase letters")

        if not analysis['has_digits']:
            suggestions.append("Add numbers")

        if not analysis['has_symbols']:
            suggestions.append("Add symbols (!@#$%^&*)")

        if analysis['pattern_matches']:
            suggestions.append("Avoid predictable patterns")

        if len(suggestions) == 0:
            suggestions.append("Great password! Consider using a password manager to remember it")

        return suggestions

    @staticmethod
    def display_analysis(password: str, show_password: bool = False):
        """Display password strength analysis in terminal"""
        score, strength, analysis = PasswordAnalyzer.calculate_strength(password)

        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}Password Strength Analysis")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

        if show_password:
            print(f"Password: {Fore.YELLOW}{'*' * len(password)}{Style.RESET_ALL}")
        print(f"Length: {Fore.WHITE}{analysis['length']} characters{Style.RESET_ALL}")
        print(f"Strength Score: {Fore.WHITE}{score}/100{Style.RESET_ALL}")
        print(f"Strength Level: {PasswordAnalyzer._get_strength_color(strength)}{strength}{Style.RESET_ALL}")
        print(f"Entropy: {Fore.WHITE}{analysis['entropy']:.1f} bits{Style.RESET_ALL}")
        print(f"Crack Time: {Fore.WHITE}{analysis['crack_time_display']}{Style.RESET_ALL}\n")

        print(f"{Fore.CYAN}Character Composition:{Style.RESET_ALL}")
        print(f"  Lowercase: {Fore.GREEN if analysis['has_lowercase'] else Fore.RED}{'Yes' if analysis['has_lowercase'] else 'No'}{Style.RESET_ALL}")
        print(f"  Uppercase: {Fore.GREEN if analysis['has_uppercase'] else Fore.RED}{'Yes' if analysis['has_uppercase'] else 'No'}{Style.RESET_ALL}")
        print(f"  Digits: {Fore.GREEN if analysis['has_digits'] else Fore.RED}{'Yes' if analysis['has_digits'] else 'No'}{Style.RESET_ALL}")
        print(f"  Symbols: {Fore.GREEN if analysis['has_symbols'] else Fore.RED}{'Yes' if analysis['has_symbols'] else 'No'}{Style.RESET_ALL}\n")

        if analysis['warnings']:
            print(f"{Fore.YELLOW}Warnings:{Style.RESET_ALL}")
            for warning in analysis['warnings']:
                print(f"  - {warning}")
            print()

        if analysis['suggestions']:
            print(f"{Fore.CYAN}Suggestions:{Style.RESET_ALL}")
            for suggestion in analysis['suggestions']:
                print(f"  + {suggestion}")
            print()

    @staticmethod
    def _get_strength_color(strength: str) -> str:
        """Get color code for strength level"""
        colors = {
            "Very Strong": Fore.GREEN,
            "Strong": Fore.CYAN,
            "Moderate": Fore.YELLOW,
            "Weak": Fore.RED,
            "Very Weak": Fore.MAGENTA
        }
        return colors.get(strength, Fore.WHITE)


class StatisticsTracker:
    """Tracks and displays attack statistics"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.attempts = 0
        self.passwords_tested = 0
    
    def start(self):
        """Start tracking"""
        self.start_time = time.time()
        self.attempts = 0
        self.passwords_tested = 0
    
    def increment(self, count: int = 1):
        """Increment attempt counter"""
        self.attempts += count
        self.passwords_tested += count
    
    def stop(self):
        """Stop tracking"""
        self.end_time = time.time()
    
    def get_elapsed_time(self) -> float:
        """Get elapsed time in seconds"""
        if self.start_time is None:
            return 0.0
        end = self.end_time if self.end_time else time.time()
        return end - self.start_time
    
    def get_attempts_per_second(self) -> float:
        """Calculate attempts per second"""
        elapsed = self.get_elapsed_time()
        if elapsed == 0:
            return 0.0
        return self.attempts / elapsed
    
    def display(self, attack_type: str = "Attack"):
        """Display statistics"""
        elapsed = self.get_elapsed_time()
        aps = self.get_attempts_per_second()
        
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}{attack_type} Statistics")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        print(f"Total Attempts: {Fore.WHITE}{self.attempts:,}{Style.RESET_ALL}")
        print(f"Time Elapsed: {Fore.WHITE}{elapsed:.2f} seconds{Style.RESET_ALL}")
        print(f"Attempts/Second: {Fore.WHITE}{aps:,.0f}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")


def format_time(seconds: float) -> str:
    """Format seconds into human-readable time"""
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.2f} minutes"
    else:
        hours = seconds / 3600
        return f"{hours:.2f} hours"


def print_banner():
    """Print application banner"""
    try:
        from pyfiglet import Figlet
        f = Figlet(font='slant')
        print(f"{Fore.CYAN}{f.renderText('Password Cracker')}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'='*60}")
        print(f"{Fore.YELLOW}Educational Security Simulation Tool v2.0")
        print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}\n")
    except ImportError:
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}Password Cracking Simulation")
        print(f"{Fore.CYAN}Educational Security Tool v2.0")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

