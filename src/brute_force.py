"""
Brute Force Attack Simulator
Demonstrates the inefficiency of brute force attacks on passwords
"""
import random
import getpass
import itertools
from typing import Optional
from colorama import Fore, Style
from tqdm import tqdm

from .utils import StatisticsTracker, PasswordAnalyzer, format_time


class BruteForceAttack:
    """Simulates a brute force password attack"""
    
    # Character sets
    LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
    UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    DIGITS = "0123456789"
    SYMBOLS = "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~"
    
    def __init__(self, use_progress_bar: bool = True, verbose: bool = True):
        """
        Initialize brute force attack simulator
        
        Args:
            use_progress_bar: Show progress bar during attack
            verbose: Print attempt details
        """
        self.use_progress_bar = use_progress_bar
        self.verbose = verbose
        self.stats = StatisticsTracker()
        self.all_chars = list(self.LOWERCASE + self.UPPERCASE + self.DIGITS + self.SYMBOLS)
    
    def estimate_time(self, password_length: int) -> dict:
        """
        Estimate time to crack password using brute force
        
        Args:
            password_length: Length of password to estimate
            
        Returns:
            Dictionary with time estimates
        """
        char_set_size = len(self.all_chars)
        total_combinations = char_set_size ** password_length
        
        # Assume 1 million attempts per second (conservative estimate)
        attempts_per_second = 1_000_000
        
        seconds = total_combinations / attempts_per_second
        
        estimates = {
            'total_combinations': total_combinations,
            'estimated_seconds': seconds,
            'estimated_time': format_time(seconds),
            'char_set_size': char_set_size
        }
        
        return estimates
    
    def attack_random(self, target_password: str) -> Optional[str]:
        """
        Attack using random password generation (inefficient method)
        
        Args:
            target_password: Password to crack
            
        Returns:
            Cracked password if found, None otherwise
        """
        print(f"\n{Fore.YELLOW}Starting Random Brute Force Attack...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Target length: {len(target_password)} characters{Style.RESET_ALL}\n")
        
        self.stats.start()
        attempts = 0
        max_attempts = 1_000_000  # Safety limit
        
        if self.use_progress_bar:
            pbar = tqdm(total=max_attempts, desc="Attempting", unit="attempts", 
                       bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]')
        
        while attempts < max_attempts:
            # Generate random password of same length
            guess = ''.join(random.choices(self.all_chars, k=len(target_password)))
            attempts += 1
            self.stats.increment()
            
            if self.use_progress_bar:
                pbar.update(1)
                pbar.set_postfix({'Current': guess[:20]})
            
            if self.verbose and attempts % 1000 == 0:
                print(f"{Fore.WHITE}Attempt {attempts:,}: {Fore.YELLOW}{guess}{Style.RESET_ALL}")
            
            if guess == target_password:
                self.stats.stop()
                if self.use_progress_bar:
                    pbar.close()
                return guess
        
        self.stats.stop()
        if self.use_progress_bar:
            pbar.close()
        
        return None
    
    def attack_sequential(self, target_password: str, max_length: Optional[int] = None) -> Optional[str]:
        """
        Attack using sequential password generation (more efficient)
        
        Args:
            target_password: Password to crack
            max_length: Maximum length to try (defaults to target length)
            
        Returns:
            Cracked password if found, None otherwise
        """
        print(f"\n{Fore.YELLOW}Starting Sequential Brute Force Attack...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Target length: {len(target_password)} characters{Style.RESET_ALL}\n")
        
        self.stats.start()
        max_length = max_length or len(target_password)
        
        # Try each length from 1 to max_length
        for length in range(1, max_length + 1):
            if self.verbose:
                print(f"{Fore.CYAN}Trying passwords of length {length}...{Style.RESET_ALL}")
            
            # Calculate total combinations for this length
            total_combos = len(self.all_chars) ** length
            
            if self.use_progress_bar:
                pbar = tqdm(total=total_combos, desc=f"Length {length}", 
                           unit="attempts", leave=False)
            
            # Generate all combinations of this length
            for attempt in itertools.product(self.all_chars, repeat=length):
                guess = ''.join(attempt)
                self.stats.increment()
                
                if self.use_progress_bar:
                    pbar.update(1)
                    if self.stats.attempts % 100 == 0:
                        pbar.set_postfix({'Current': guess[:20]})
                
                if guess == target_password:
                    self.stats.stop()
                    if self.use_progress_bar:
                        pbar.close()
                    return guess
            
            if self.use_progress_bar:
                pbar.close()
        
        self.stats.stop()
        return None
    
    def run_interactive(self):
        """Run interactive brute force attack simulation"""
        from .utils import print_banner
        print_banner()
        
        print(f"{Fore.CYAN}Brute Force Attack Simulator{Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}This simulator demonstrates how brute force attacks work.")
        print(f"It will attempt to guess your password through random or sequential methods.{Style.RESET_ALL}\n")
        
        # Get password
        password = getpass.getpass(f"{Fore.CYAN}Enter a password to crack: {Style.RESET_ALL}")
        
        if not password:
            print(f"{Fore.RED}Error: Password cannot be empty!{Style.RESET_ALL}")
            return
        
        # Validate password
        invalid_chars = [c for c in password if c not in self.all_chars]
        if invalid_chars:
            print(f"{Fore.RED}Error: Password contains invalid characters: {set(invalid_chars)}{Style.RESET_ALL}")
            return
        
        # Analyze password strength
        PasswordAnalyzer.display_analysis(password, show_password=False)
        
        # Show time estimate
        estimates = self.estimate_time(len(password))
        print(f"{Fore.CYAN}Brute Force Time Estimate:{Style.RESET_ALL}")
        print(f"  Total possible combinations: {Fore.WHITE}{estimates['total_combinations']:,}{Style.RESET_ALL}")
        print(f"  Estimated time (at 1M attempts/sec): {Fore.WHITE}{estimates['estimated_time']}{Style.RESET_ALL}\n")
        
        # Choose attack method
        print(f"{Fore.CYAN}Select attack method:{Style.RESET_ALL}")
        print(f"  1. Random generation (faster demo, less realistic)")
        print(f"  2. Sequential generation (slower, more realistic)")
        
        choice = input(f"{Fore.CYAN}Enter choice (1 or 2): {Style.RESET_ALL}").strip()
        
        # Perform attack
        if choice == "2":
            result = self.attack_sequential(password)
        else:
            result = self.attack_random(password)
        
        # Display results
        if result:
            print(f"\n{Fore.GREEN}{'='*60}")
            print(f"{Fore.GREEN}PASSWORD CRACKED{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Password found: {Fore.YELLOW}{result}{Style.RESET_ALL}\n")
        else:
            print(f"\n{Fore.RED}Password not found within attempt limit.{Style.RESET_ALL}\n")
        
        # Display statistics
        self.stats.display("Brute Force Attack")
        
        # Security recommendations
        print(f"{Fore.YELLOW}Security Recommendations:{Style.RESET_ALL}")
        print(f"  • Use passwords with 12+ characters")
        print(f"  • Include uppercase, lowercase, numbers, and symbols")
        print(f"  • Avoid common patterns and dictionary words")
        print(f"  • Consider using a password manager\n")

