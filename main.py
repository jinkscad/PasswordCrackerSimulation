#!/usr/bin/env python3
"""
Password Cracking Simulation - Main Entry Point
Educational tool demonstrating password security vulnerabilities
"""
import argparse
import sys
from pathlib import Path
from colorama import Fore, Style

from src.brute_force import BruteForceAttack
from src.dictionary_attack import DictionaryAttack
from src.utils import print_banner, PasswordAnalyzer


def main():
    """Main entry point for the application"""
    parser = argparse.ArgumentParser(
        description='Password Cracking Simulation - Educational Security Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run brute force attack interactively
  python main.py brute-force

  # Run dictionary attack interactively
  python main.py dictionary

  # Analyze password strength
  python main.py analyze --password "MyP@ssw0rd"

  # Hash a password
  python main.py hash --password "test" --algorithm md5
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Brute force command
    brute_parser = subparsers.add_parser('brute-force', 
                                         help='Run brute force attack simulator')
    brute_parser.add_argument('--no-progress', action='store_true',
                             help='Disable progress bar')
    brute_parser.add_argument('--quiet', action='store_true',
                             help='Reduce output verbosity')
    
    # Dictionary attack command
    dict_parser = subparsers.add_parser('dictionary',
                                       help='Run dictionary attack simulator')
    dict_parser.add_argument('--hash', type=str,
                            help='Target hash to crack')
    dict_parser.add_argument('--dict', type=str,
                            help='Path to dictionary file')
    dict_parser.add_argument('--algorithm', type=str, choices=['md5', 'sha1', 'sha256', 'sha512'],
                            help='Hash algorithm (auto-detected if not specified)')
    dict_parser.add_argument('--no-progress', action='store_true',
                            help='Disable progress bar')
    dict_parser.add_argument('--quiet', action='store_true',
                            help='Reduce output verbosity')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze',
                                          help='Analyze password strength')
    analyze_parser.add_argument('--password', type=str,
                               help='Password to analyze')
    analyze_parser.add_argument('--show-password', action='store_true',
                               help='Show password in analysis (default: masked)')
    
    # Hash command
    hash_parser = subparsers.add_parser('hash',
                                       help='Hash a password')
    hash_parser.add_argument('--password', type=str, required=True,
                            help='Password to hash')
    hash_parser.add_argument('--algorithm', type=str, 
                            choices=['md5', 'sha1', 'sha256', 'sha512'],
                            default='md5',
                            help='Hash algorithm (default: md5)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'brute-force':
            attack = BruteForceAttack(
                use_progress_bar=not args.no_progress,
                verbose=not args.quiet
            )
            attack.run_interactive()
        
        elif args.command == 'dictionary':
            attack = DictionaryAttack(
                use_progress_bar=not args.no_progress,
                verbose=not args.quiet
            )
            
            if args.hash and args.dict:
                # Non-interactive mode
                result = attack.attack(args.hash, args.dict, args.algorithm)
                if result:
                    print(f"\n{Fore.GREEN}Password found: {result}{Style.RESET_ALL}")
                else:
                    print(f"\n{Fore.RED}Password not found{Style.RESET_ALL}")
                attack.stats.display("Dictionary Attack")
            else:
                # Interactive mode
                attack.run_interactive()
        
        elif args.command == 'analyze':
            if args.password:
                password = args.password
            else:
                import getpass
                from colorama import Fore
                password = getpass.getpass(f"{Fore.CYAN}Enter password to analyze: {Style.RESET_ALL}")
            
            PasswordAnalyzer.display_analysis(password, show_password=args.show_password)
        
        elif args.command == 'hash':
            from src.dictionary_attack import DictionaryAttack
            attack = DictionaryAttack()
            hash_value = attack.hash_password(args.password, args.algorithm)
            print(f"\n{Fore.CYAN}Hash ({args.algorithm.upper()}): {Fore.WHITE}{hash_value}{Style.RESET_ALL}\n")
    
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Operation cancelled by user.{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == '__main__':
    main()

