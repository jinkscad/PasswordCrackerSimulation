"""
Dictionary Attack Simulator
Demonstrates how dictionary attacks can quickly crack common passwords
"""
import hashlib
import os
from typing import Optional, List
from pathlib import Path
from colorama import Fore, Style
from tqdm import tqdm

from .utils import StatisticsTracker, PasswordAnalyzer, format_time


class DictionaryAttack:
    """Simulates a dictionary-based password attack"""
    
    SUPPORTED_HASHES = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512
    }
    
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
    
    def attack(self, target_hash: str, dictionary_path: str, 
               hash_algorithm: Optional[str] = None) -> Optional[str]:
        """
        Perform dictionary attack on hashed password
        
        Args:
            target_hash: Target hash to crack
            dictionary_path: Path to dictionary file
            hash_algorithm: Hash algorithm (auto-detected if None)
            
        Returns:
            Cracked password if found, None otherwise
        """
        print(f"\n{Fore.YELLOW}Starting Dictionary Attack...{Style.RESET_ALL}")
        
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
            passwords = self.load_dictionary(dictionary_path)
            print(f"{Fore.GREEN}Loaded {len(passwords):,} password candidates{Style.RESET_ALL}\n")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            return None
        
        # Perform attack
        self.stats.start()
        
        if self.use_progress_bar:
            pbar = tqdm(total=len(passwords), desc="Testing passwords", 
                       unit="passwords", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]')
        
        for password in passwords:
            # Hash the password
            try:
                password_hash = self.hash_password(password, hash_algorithm)
                self.stats.increment()
                
                if self.use_progress_bar:
                    pbar.update(1)
                    if self.stats.attempts % 100 == 0:
                        pbar.set_postfix({'Current': password[:30]})
                
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
        
        # Perform attack
        result = self.attack(target_hash, dict_path, hash_type)
        
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
        
        # Security recommendations
        print(f"{Fore.YELLOW}Security Recommendations:{Style.RESET_ALL}")
        print(f"  • Avoid common passwords and dictionary words")
        print(f"  • Use unique, random passwords for each account")
        print(f"  • Consider using passphrases instead of single words")
        print(f"  • Use modern hashing algorithms (bcrypt, Argon2) instead of MD5/SHA1")
        print(f"  • Implement salting and key stretching in password storage\n")

