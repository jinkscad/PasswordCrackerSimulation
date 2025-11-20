"""
Dictionary Attack Simulator
Demonstrates how dictionary attacks can quickly crack common passwords
Enhanced with variations, patterns, statistics, and pause/resume
"""
import hashlib
import os
import threading
from typing import Optional, List, Set, Dict, Callable
from pathlib import Path
from colorama import Fore, Style
from tqdm import tqdm

from .utils import StatisticsTracker, PasswordAnalyzer, format_time


class DictionaryAttack:
    """Simulates a dictionary-based password attack with advanced features"""
    
    SUPPORTED_HASHES = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512
    }
    
    # Common character substitutions
    SUBSTITUTIONS = {
        'a': ['@', '4', 'A'],
        'e': ['3', 'E'],
        'i': ['1', '!', 'I'],
        'o': ['0', 'O'],
        's': ['$', '5', 'S'],
        't': ['7', 'T'],
        'l': ['1', 'L'],
        'g': ['9', 'G'],
        'b': ['8', 'B']
    }
    
    # Common patterns to append
    COMMON_PATTERNS = [
        '123', '1234', '12345', '123456', '1234567', '12345678', '123456789',
        '!', '!!', '!!!', '!@#', '!@#$', '!@#$%', '!@#$%^', '!@#$%^&',
        '1', '12', '123', '2024', '2023', '2022', '2021', '2020',
        '01', '001', '0001', '2024!', '2023!', '2022!',
        '!@#', '!@#$', '!@#$%', '!@#$%^', '!@#$%^&', '!@#$%^&*'
    ]
    
    def __init__(self, use_progress_bar: bool = True, verbose: bool = True):
        """
        Initialize dictionary attack simulator
        
        Args:
            use_progress_bar: Show progress bar during attack
            verbose: Print attempt details
        """
        self.use_progress_bar = use_progress_bar
        self.verbose = verbose
        self.stats = StatisticsTracker()
        self.tested_passwords: List[str] = []
        self.is_paused = False
        self.should_stop = False
        self.pause_lock = threading.Lock()
    
    def detect_hash_type(self, hash_value: str) -> Optional[str]:
        """
        Detect hash algorithm based on hash length
        
        Args:
            hash_value: Hash string to analyze
            
        Returns:
            Hash algorithm name or None
        """
        length = len(hash_value)
        hash_map = {
            32: 'md5',
            40: 'sha1',
            64: 'sha256',
            128: 'sha512'
        }
        return hash_map.get(length)
    
    def hash_password(self, password: str, algorithm: str = 'md5') -> str:
        """
        Hash a password using specified algorithm
        
        Args:
            password: Password to hash
            algorithm: Hash algorithm to use
            
        Returns:
            Hexadecimal hash string
        """
        if algorithm not in self.SUPPORTED_HASHES:
            raise ValueError(f"Unsupported hash algorithm: {algorithm}")
        
        hash_func = self.SUPPORTED_HASHES[algorithm]
        return hash_func(password.encode('utf-8')).hexdigest()
    
    def generate_variations(self, base_password: str) -> List[str]:
        """
        Generate password variations with substitutions, case changes, and patterns
        
        Args:
            base_password: Base password to generate variations from
            
        Returns:
            List of password variations
        """
        variations: Set[str] = {base_password}  # Use set to avoid duplicates
        
        # Original variations
        variations.add(base_password.lower())
        variations.add(base_password.upper())
        variations.add(base_password.capitalize())
        
        # Character substitutions
        def substitute_char(pwd: str, pos: int = 0) -> List[str]:
            if pos >= len(pwd):
                return [pwd]
            
            results = []
            char = pwd[pos].lower()
            
            # Try original character
            for variant in substitute_char(pwd, pos + 1):
                results.append(variant)
            
            # Try substitutions
            if char in self.SUBSTITUTIONS:
                for sub in self.SUBSTITUTIONS[char]:
                    new_pwd = pwd[:pos] + sub + pwd[pos + 1:]
                    for variant in substitute_char(new_pwd, pos + 1):
                        results.append(variant)
            
            return results
        
        # Generate substitution variations (limit to avoid explosion)
        if len(base_password) <= 8:
            sub_variants = substitute_char(base_password.lower())
            variations.update(sub_variants[:50])  # Limit to prevent too many
        
        # Add common patterns
        for pattern in self.COMMON_PATTERNS:
            variations.add(base_password + pattern)
            variations.add(base_password.lower() + pattern)
            variations.add(base_password.upper() + pattern)
            variations.add(base_password.capitalize() + pattern)
            variations.add(pattern + base_password)
            variations.add(pattern + base_password.lower())
            variations.add(pattern + base_password.upper())
            variations.add(pattern + base_password.capitalize())
        
        # Add numbers at end
        for num in ['1', '12', '123', '1234', '2024', '2023']:
            variations.add(base_password + num)
            variations.add(base_password.lower() + num)
            variations.add(base_password.upper() + num)
        
        # Add symbols at end
        for sym in ['!', '!!', '!@#', '!@#$']:
            variations.add(base_password + sym)
            variations.add(base_password.lower() + sym)
            variations.add(base_password.upper() + sym)
        
        return list(variations)
    
    def generate_pattern_variations(self, base_password: str) -> List[str]:
        """
        Generate common password patterns
        
        Args:
            base_password: Base password
            
        Returns:
            List of pattern variations
        """
        patterns = []
        
        # Pattern: Password123
        patterns.append(base_password.capitalize() + '123')
        patterns.append(base_password.capitalize() + '1234')
        patterns.append(base_password.capitalize() + '12345')
        
        # Pattern: password123!
        patterns.append(base_password.lower() + '123!')
        patterns.append(base_password.lower() + '1234!')
        
        # Pattern: PASSWORD123!
        patterns.append(base_password.upper() + '123!')
        patterns.append(base_password.upper() + '1234!')
        
        # Pattern: Password123!
        patterns.append(base_password.capitalize() + '123!')
        patterns.append(base_password.capitalize() + '1234!')
        
        # Pattern: Password@123
        patterns.append(base_password.capitalize() + '@123')
        patterns.append(base_password.capitalize() + '@1234')
        
        # Pattern: password@123
        patterns.append(base_password.lower() + '@123')
        patterns.append(base_password.lower() + '@1234')
        
        # Pattern: Password2024
        patterns.append(base_password.capitalize() + '2024')
        patterns.append(base_password.capitalize() + '2023')
        
        # Pattern: password2024!
        patterns.append(base_password.lower() + '2024!')
        patterns.append(base_password.lower() + '2023!')
        
        return patterns
    
    def load_dictionary(self, file_path: str) -> List[str]:
        """
        Load dictionary file and return list of passwords
        
        Args:
            file_path: Path to dictionary file
            
        Returns:
            List of password candidates
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dictionary file not found: {file_path}")
        
        passwords = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    password = line.strip()
                    if password:  # Skip empty lines
                        passwords.append(password)
        except Exception as e:
            raise IOError(f"Error reading dictionary file: {e}")
        
        return passwords
    
    def pause(self):
        """Pause the attack"""
        with self.pause_lock:
            self.is_paused = True
    
    def resume(self):
        """Resume the attack"""
        with self.pause_lock:
            self.is_paused = False
    
    def stop(self):
        """Stop the attack"""
        with self.pause_lock:
            self.should_stop = True
            self.is_paused = False
    
    def _wait_if_paused(self):
        """Wait if attack is paused"""
        while True:
            with self.pause_lock:
                if not self.is_paused or self.should_stop:
                    break
            import time
            time.sleep(0.1)
    
    def attack(self, target_hash: str, dictionary_path: str, 
               hash_algorithm: Optional[str] = None,
               use_variations: bool = True,
               use_patterns: bool = True,
               progress_callback: Optional[Callable] = None) -> Optional[str]:
        """
        Perform dictionary attack on hashed password with advanced features
        
        Args:
            target_hash: Target hash to crack
            dictionary_path: Path to dictionary file
            hash_algorithm: Hash algorithm (auto-detected if None)
            use_variations: Generate password variations
            use_patterns: Use pattern matching
            progress_callback: Optional callback for progress updates
            
        Returns:
            Cracked password if found, None otherwise
        """
        print(f"\n{Fore.YELLOW}Starting Dictionary Attack...{Style.RESET_ALL}")
        
        # Reset state
        self.tested_passwords = []
        self.is_paused = False
        self.should_stop = False
        
        # Auto-detect hash algorithm if not provided
        if hash_algorithm is None:
            hash_algorithm = self.detect_hash_type(target_hash)
            if hash_algorithm:
                print(f"{Fore.CYAN}Detected hash algorithm: {hash_algorithm.upper()}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}Could not detect hash algorithm, defaulting to MD5{Style.RESET_ALL}")
                hash_algorithm = 'md5'
        else:
            hash_algorithm = hash_algorithm.lower()
            if hash_algorithm not in self.SUPPORTED_HASHES:
                raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")
        
        # Load dictionary
        print(f"{Fore.CYAN}Loading dictionary from: {dictionary_path}{Style.RESET_ALL}")
        try:
            base_passwords = self.load_dictionary(dictionary_path)
            print(f"{Fore.GREEN}Loaded {len(base_passwords):,} base passwords{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            return None
        
        # Generate all password candidates
        all_passwords = []
        password_set = set()  # To avoid duplicates
        
        print(f"{Fore.CYAN}Generating password candidates...{Style.RESET_ALL}")
        for base_pwd in base_passwords:
            # Add base password
            if base_pwd not in password_set:
                all_passwords.append(base_pwd)
                password_set.add(base_pwd)
            
            # Add variations if enabled
            if use_variations:
                variations = self.generate_variations(base_pwd)
                for var in variations:
                    if var not in password_set and len(var) <= 50:  # Reasonable length limit
                        all_passwords.append(var)
                        password_set.add(var)
            
            # Add pattern variations if enabled
            if use_patterns:
                patterns = self.generate_pattern_variations(base_pwd)
                for pattern in patterns:
                    if pattern not in password_set and len(pattern) <= 50:
                        all_passwords.append(pattern)
                        password_set.add(pattern)
        
        total_candidates = len(all_passwords)
        print(f"{Fore.GREEN}Generated {total_candidates:,} total password candidates{Style.RESET_ALL}\n")
        
        # Perform attack
        self.stats.start()
        
        if self.use_progress_bar:
            pbar = tqdm(total=total_candidates, desc="Testing passwords", 
                       unit="passwords", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]')
        
        for password in all_passwords:
            # Check if paused
            self._wait_if_paused()
            
            # Check if stopped
            if self.should_stop:
                self.stats.stop()
                if self.use_progress_bar:
                    pbar.close()
                return None
            
            # Hash the password
            try:
                password_hash = self.hash_password(password, hash_algorithm)
                self.stats.increment()
                self.tested_passwords.append(password)
                
                if self.use_progress_bar:
                    pbar.update(1)
                    if self.stats.attempts % 100 == 0:
                        pbar.set_postfix({'Current': password[:30]})
                
                # Progress callback for web interface
                if progress_callback and self.stats.attempts % 100 == 0:
                    progress_callback({
                        'attempts': self.stats.attempts,
                        'total': total_candidates,
                        'current': password[:30],
                        'progress': (self.stats.attempts / total_candidates) * 100
                    })
                
                # Check if hash matches
                if password_hash.lower() == target_hash.lower():
                    self.stats.stop()
                    if self.use_progress_bar:
                        pbar.close()
                    return password
                
                # Show progress for verbose mode
                if self.verbose and self.stats.attempts % 1000 == 0:
                    print(f"{Fore.WHITE}Tested {self.stats.attempts:,} passwords...{Style.RESET_ALL}")
            
            except Exception as e:
                if self.verbose:
                    print(f"{Fore.RED}Error processing password: {e}{Style.RESET_ALL}")
                continue
        
        self.stats.stop()
        if self.use_progress_bar:
            pbar.close()
        
        return None
    
    def get_statistics(self) -> Dict:
        """
        Get detailed attack statistics
        
        Returns:
            Dictionary with statistics
        """
        elapsed = self.stats.get_elapsed_time()
        aps = self.stats.get_attempts_per_second()
        
        return {
            'total_attempts': self.stats.attempts,
            'time_elapsed': elapsed,
            'attempts_per_second': aps,
            'passwords_tested': len(self.tested_passwords),
            'tested_passwords': self.tested_passwords[-100:] if len(self.tested_passwords) > 100 else self.tested_passwords,  # Last 100
            'success_rate': 1.0 if self.stats.attempts > 0 and any(self.tested_passwords) else 0.0
        }
    
    def run_interactive(self):
        """Run interactive dictionary attack simulation"""
        from .utils import print_banner
        print_banner()
        
        print(f"{Fore.CYAN}Dictionary Attack Simulator{Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}This simulator demonstrates how dictionary attacks work.")
        print(f"It will test passwords from a dictionary file against a hashed password.{Style.RESET_ALL}\n")
        
        # Get hash
        target_hash = input(f"{Fore.CYAN}Enter the hashed password: {Style.RESET_ALL}").strip()
        if not target_hash:
            print(f"{Fore.RED}Error: Hash cannot be empty!{Style.RESET_ALL}")
            return
        
        # Detect hash type
        hash_type = self.detect_hash_type(target_hash)
        if hash_type:
            print(f"{Fore.GREEN}Detected hash type: {hash_type.upper()}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Could not auto-detect hash type. Using MD5.{Style.RESET_ALL}")
            hash_type = 'md5'
        
        # Get dictionary file
        dict_path = input(f"{Fore.CYAN}Enter dictionary file path (or press Enter for default): {Style.RESET_ALL}").strip()
        
        if not dict_path:
            # Use default dictionary
            default_path = Path(__file__).parent.parent / "dictionary-attack-simulator" / "passwords.txt"
            if default_path.exists():
                dict_path = str(default_path)
                print(f"{Fore.CYAN}Using default dictionary: {dict_path}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Error: No dictionary file specified and default not found!{Style.RESET_ALL}")
                return
        else:
            # Expand user path
            dict_path = os.path.expanduser(dict_path)
        
        # Ask about variations
        use_variations = input(f"{Fore.CYAN}Use password variations? (y/n, default: y): {Style.RESET_ALL}").strip().lower()
        use_variations = use_variations != 'n'
        
        use_patterns = input(f"{Fore.CYAN}Use pattern matching? (y/n, default: y): {Style.RESET_ALL}").strip().lower()
        use_patterns = use_patterns != 'n'
        
        # Perform attack
        result = self.attack(target_hash, dict_path, hash_type, use_variations, use_patterns)
        
        # Display results
        if result:
            print(f"\n{Fore.GREEN}{'='*60}")
            print(f"{Fore.GREEN}✓ PASSWORD CRACKED!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Password found: {Fore.YELLOW}{result}{Style.RESET_ALL}\n")
            
            # Analyze the cracked password
            PasswordAnalyzer.display_analysis(result, show_password=True)
        else:
            print(f"\n{Fore.RED}{'='*60}")
            print(f"{Fore.RED}✗ PASSWORD NOT FOUND{Style.RESET_ALL}")
            print(f"{Fore.RED}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}The password was not found in the dictionary.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}This demonstrates that unique passwords are resistant to dictionary attacks.{Style.RESET_ALL}\n")
        
        # Display statistics
        self.stats.display("Dictionary Attack")
        stats = self.get_statistics()
        print(f"\n{Fore.CYAN}Detailed Statistics:{Style.RESET_ALL}")
        print(f"  Passwords tested: {stats['passwords_tested']:,}")
        print(f"  Success rate: {stats['success_rate']:.2%}")
        if stats['tested_passwords']:
            print(f"\n  Last 10 tested passwords:")
            for pwd in stats['tested_passwords'][-10:]:
                print(f"    • {pwd}")
        
        # Security recommendations
        print(f"\n{Fore.YELLOW}Security Recommendations:{Style.RESET_ALL}")
        print(f"  • Avoid common passwords and dictionary words")
        print(f"  • Use unique, random passwords for each account")
        print(f"  • Consider using passphrases instead of single words")
        print(f"  • Use modern hashing algorithms (bcrypt, Argon2) instead of MD5/SHA1")
        print(f"  • Implement salting and key stretching in password storage\n")
