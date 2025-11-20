"""
Utility functions for password analysis and display
"""
import re
import time
from typing import Dict, Tuple
from colorama import Fore, Style, init

# Initialize colorama for cross-platform color support
init(autoreset=True)


class PasswordAnalyzer:
    """Analyzes password strength and characteristics"""
    
    @staticmethod
    def calculate_strength(password: str) -> Tuple[int, str, Dict]:
        """
        Calculate password strength score (0-100) and provide analysis
        
        Returns:
            Tuple of (score, strength_level, analysis_dict)
        """
        score = 0
        analysis = {
            'length': len(password),
            'has_lowercase': False,
            'has_uppercase': False,
            'has_digits': False,
            'has_symbols': False,
            'common_patterns': [],
            'entropy': 0
        }
        
        # Length scoring
        if len(password) >= 12:
            score += 25
        elif len(password) >= 8:
            score += 15
        elif len(password) >= 6:
            score += 10
        else:
            score += 5
        
        # Character variety
        if re.search(r'[a-z]', password):
            analysis['has_lowercase'] = True
            score += 15
        
        if re.search(r'[A-Z]', password):
            analysis['has_uppercase'] = True
            score += 15
        
        if re.search(r'\d', password):
            analysis['has_digits'] = True
            score += 15
        
        if re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/?]', password):
            analysis['has_symbols'] = True
            score += 20
        
        # Check for common patterns
        if re.search(r'(.)\1{2,}', password):  # Repeated characters
            analysis['common_patterns'].append('Repeated characters')
            score -= 10
        
        if re.search(r'(012|123|234|345|456|567|678|789|890)', password):
            analysis['common_patterns'].append('Sequential numbers')
            score -= 10
        
        if re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', password, re.IGNORECASE):
            analysis['common_patterns'].append('Sequential letters')
            score -= 10
        
        # Calculate entropy (simplified)
        char_variety = sum([
            analysis['has_lowercase'],
            analysis['has_uppercase'],
            analysis['has_digits'],
            analysis['has_symbols']
        ])
        analysis['entropy'] = len(password) * char_variety * 2.5
        
        # Determine strength level
        if score >= 80:
            strength = "Very Strong"
        elif score >= 60:
            strength = "Strong"
        elif score >= 40:
            strength = "Moderate"
        elif score >= 20:
            strength = "Weak"
        else:
            strength = "Very Weak"
        
        score = max(0, min(100, score))  # Clamp between 0-100
        
        return score, strength, analysis
    
    @staticmethod
    def display_analysis(password: str, show_password: bool = False):
        """Display password strength analysis"""
        score, strength, analysis = PasswordAnalyzer.calculate_strength(password)
        
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}Password Strength Analysis")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        if show_password:
            print(f"Password: {Fore.YELLOW}{'*' * len(password)}{Style.RESET_ALL}")
        print(f"Length: {Fore.WHITE}{analysis['length']} characters{Style.RESET_ALL}")
        print(f"Strength Score: {Fore.WHITE}{score}/100{Style.RESET_ALL}")
        print(f"Strength Level: {PasswordAnalyzer._get_strength_color(strength)}{strength}{Style.RESET_ALL}")
        print(f"Estimated Entropy: {Fore.WHITE}{analysis['entropy']:.1f} bits{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}Character Composition:{Style.RESET_ALL}")
        print(f"  Lowercase: {Fore.GREEN if analysis['has_lowercase'] else Fore.RED}{'✓' if analysis['has_lowercase'] else '✗'}{Style.RESET_ALL}")
        print(f"  Uppercase: {Fore.GREEN if analysis['has_uppercase'] else Fore.RED}{'✓' if analysis['has_uppercase'] else '✗'}{Style.RESET_ALL}")
        print(f"  Digits: {Fore.GREEN if analysis['has_digits'] else Fore.RED}{'✓' if analysis['has_digits'] else '✗'}{Style.RESET_ALL}")
        print(f"  Symbols: {Fore.GREEN if analysis['has_symbols'] else Fore.RED}{'✓' if analysis['has_symbols'] else '✗'}{Style.RESET_ALL}\n")
        
        if analysis['common_patterns']:
            print(f"{Fore.YELLOW}Warning: Common patterns detected:{Style.RESET_ALL}")
            for pattern in analysis['common_patterns']:
                print(f"  • {pattern}")
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

