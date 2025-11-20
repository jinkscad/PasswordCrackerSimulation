"""
Password Breach Checker
Checks if passwords have been compromised in known data breaches
Uses Have I Been Pwned API with k-anonymity model
"""
import hashlib
import requests
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
import random


class PasswordBreachChecker:
    """Check passwords against Have I Been Pwned database"""
    
    HIBP_API_URL = "https://api.pwnedpasswords.com/range"
    
    # Simulated breach timeline data (for visualization)
    # In a real implementation, you might store actual breach dates
    BREACH_SOURCES = [
        "Adobe (2013)", "LinkedIn (2012)", "MySpace (2008)", "Dropbox (2012)",
        "Yahoo (2013-2014)", "eBay (2014)", "Ashley Madison (2015)",
        "Adult FriendFinder (2016)", "Equifax (2017)", "Marriott (2018)",
        "Canva (2019)", "Facebook (2019)", "Twitter (2020)", "SolarWinds (2020)",
        "Microsoft (2021)", "T-Mobile (2021)", "Neopets (2022)", "LastPass (2022)",
        "Twitter (2022)", "Reddit (2023)", "23andMe (2023)", "X (2023)"
    ]
    
    def __init__(self):
        """Initialize breach checker"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'PasswordCrackerSimulation-EducationalTool/2.0'
        })
    
    def check_password(self, password: str) -> Dict:
        """
        Check if password has been breached using HIBP API
        
        Args:
            password: Password to check
            
        Returns:
            Dictionary with breach information
        """
        try:
            # Hash password with SHA-1
            sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
            prefix = sha1_hash[:5]
            suffix = sha1_hash[5:]
            
            # Query HIBP API (k-anonymity model)
            url = f"{self.HIBP_API_URL}/{prefix}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                return {
                    'breached': False,
                    'count': 0,
                    'error': f'API error: {response.status_code}',
                    'risk_level': 'unknown'
                }
            
            # Parse response and check for match
            hashes = {}
            for line in response.text.splitlines():
                if ':' in line:
                    hash_suffix, count = line.split(':', 1)
                    hashes[hash_suffix] = int(count)
            
            # Check if our password's suffix is in the results
            if suffix in hashes:
                count = hashes[suffix]
                return {
                    'breached': True,
                    'count': count,
                    'risk_level': self._calculate_risk_level(count),
                    'message': f'This password has been found in {count:,} data breaches',
                    'breach_timeline': self._generate_breach_timeline(count),
                    'recommendation': self._get_recommendation(count)
                }
            else:
                return {
                    'breached': False,
                    'count': 0,
                    'risk_level': 'safe',
                    'message': 'This password has NOT been found in any known data breaches',
                    'breach_timeline': [],
                    'recommendation': 'Good! This password appears to be unique.'
                }
        
        except requests.exceptions.RequestException as e:
            return {
                'breached': False,
                'count': 0,
                'error': f'Network error: {str(e)}',
                'risk_level': 'unknown',
                'message': 'Unable to check password (network error)'
            }
        except Exception as e:
            return {
                'breached': False,
                'count': 0,
                'error': str(e),
                'risk_level': 'unknown',
                'message': 'An error occurred while checking the password'
            }
    
    def _calculate_risk_level(self, count: int) -> str:
        """Calculate risk level based on breach count"""
        if count == 0:
            return 'safe'
        elif count < 100:
            return 'low'
        elif count < 1000:
            return 'medium'
        elif count < 10000:
            return 'high'
        else:
            return 'critical'
    
    def _generate_breach_timeline(self, count: int) -> list:
        """
        Generate a simulated breach timeline for visualization
        Based on count, we estimate when breaches might have occurred
        """
        timeline = []
        
        # Estimate number of unique breaches (simplified)
        num_breaches = min(max(1, count // 1000), len(self.BREACH_SOURCES))
        
        # Generate timeline entries
        base_date = datetime(2008, 1, 1)
        selected_sources = random.sample(self.BREACH_SOURCES, min(num_breaches, len(self.BREACH_SOURCES)))
        
        for i, source in enumerate(selected_sources):
            # Distribute breaches over time
            years_ago = random.uniform(0, 15)
            breach_date = base_date + timedelta(days=365 * years_ago)
            
            # Estimate count per breach (distribute total count)
            breach_count = count // num_breaches if num_breaches > 0 else count
            if i == num_breaches - 1:  # Last one gets remainder
                breach_count = count - (breach_count * (num_breaches - 1))
            
            timeline.append({
                'date': breach_date.strftime('%Y-%m-%d'),
                'year': breach_date.year,
                'source': source,
                'count': breach_count,
                'formatted_date': breach_date.strftime('%B %Y')
            })
        
        # Sort by date
        timeline.sort(key=lambda x: x['date'])
        return timeline
    
    def _get_recommendation(self, count: int) -> str:
        """Get security recommendation based on breach count"""
        if count == 0:
            return "This password appears safe, but still use a unique password for each account."
        elif count < 100:
            return "This password has appeared in a few breaches. Consider changing it."
        elif count < 1000:
            return "This password has been compromised multiple times. You should change it immediately."
        elif count < 10000:
            return "⚠️ CRITICAL: This password is highly compromised. Change it immediately and never reuse it!"
        else:
            return "🚨 EXTREMELY CRITICAL: This password is massively compromised. Change it immediately on ALL accounts!"
    
    def get_risk_assessment(self, password: str, breach_data: Dict) -> Dict:
        """
        Get comprehensive risk assessment
        
        Args:
            password: The password
            breach_data: Breach check results
            
        Returns:
            Comprehensive risk assessment
        """
        from .utils import PasswordAnalyzer
        
        # Get password strength
        from .utils import PasswordAnalyzer
        score, strength, analysis = PasswordAnalyzer.calculate_strength(password)
        
        # Combine breach data with strength analysis
        risk_factors = []
        
        if breach_data.get('breached', False):
            risk_factors.append({
                'factor': 'Data Breach Exposure',
                'severity': breach_data['risk_level'],
                'description': f"Found in {breach_data['count']:,} breaches"
            })
        
        if analysis['length'] < 8:
            risk_factors.append({
                'factor': 'Password Length',
                'severity': 'high',
                'description': f"Only {analysis['length']} characters (recommend 12+)"
            })
        
        if not analysis['has_uppercase'] or not analysis['has_lowercase']:
            risk_factors.append({
                'factor': 'Character Variety',
                'severity': 'medium',
                'description': 'Missing uppercase or lowercase letters'
            })
        
        if not analysis['has_symbols']:
            risk_factors.append({
                'factor': 'Symbols',
                'severity': 'low',
                'description': 'No special characters included'
            })
        
        if analysis['common_patterns']:
            risk_factors.append({
                'factor': 'Common Patterns',
                'severity': 'medium',
                'description': f"Contains: {', '.join(analysis['common_patterns'])}"
            })
        
        # Calculate overall risk
        overall_risk = 'safe'
        if breach_data.get('breached', False):
            overall_risk = breach_data['risk_level']
        elif any(f['severity'] == 'high' for f in risk_factors):
            overall_risk = 'high'
        elif any(f['severity'] == 'medium' for f in risk_factors):
            overall_risk = 'medium'
        elif any(f['severity'] == 'low' for f in risk_factors):
            overall_risk = 'low'
        
        return {
            'overall_risk': overall_risk,
            'breach_status': breach_data,
            'strength_score': score,
            'strength_level': strength,
            'risk_factors': risk_factors,
            'recommendations': self._get_recommendations(overall_risk, breach_data, analysis)
        }
    
    def _get_recommendations(self, risk_level: str, breach_data: Dict, analysis: Dict) -> list:
        """Get actionable security recommendations"""
        recommendations = []
        
        if breach_data.get('breached', False):
            recommendations.append("🚨 Change this password immediately on ALL accounts")
            recommendations.append("Never reuse this password")
        
        if analysis['length'] < 12:
            recommendations.append(f"Increase password length to 12+ characters (currently {analysis['length']})")
        
        if not analysis['has_symbols']:
            recommendations.append("Add special characters (!@#$%^&*) to increase security")
        
        if analysis['common_patterns']:
            recommendations.append("Avoid common patterns and sequences")
        
        recommendations.append("Use a unique password for each account")
        recommendations.append("Consider using a password manager")
        
        return recommendations

