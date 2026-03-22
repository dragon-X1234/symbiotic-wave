from typing import Dict, List
from dataclasses import dataclass

@dataclass
class Weapon:
    """Free Fire weapon specifications"""
    name: str
    category: str  # SMG, AR, Sniper, Shotgun, LMG, Pistol, Special
    fire_rate: float      # Rounds per second
    vertical_recoil: int  # 0-100 scale
    horizontal_recoil: int # 0-100 scale
    mobility: float       # Movement speed modifier
    range_meters: int

class WeaponDatabase:
    """Complete Free Fire weapon database"""
    
    WEAPONS: Dict[str, Weapon] = {
        # === SMGs (12 weapons) ===
        'mp40': Weapon('MP40', 'SMG', 12.5, 65, 45, 0.95, 50),
        'mp5': Weapon('MP5', 'SMG', 11.0, 55, 40, 0.93, 60),
        'ump': Weapon('UMP', 'SMG', 9.5, 50, 35, 0.90, 70),
        'p90': Weapon('P90', 'SMG', 13.0, 60, 50, 0.94, 45),
        'vector': Weapon('Vector', 'SMG', 14.0, 58, 48, 0.96, 40),
        'thompson': Weapon('Thompson', 'SMG', 10.0, 52, 38, 0.88, 55),
        'mac10': Weapon('MAC10', 'SMG', 15.0, 70, 60, 0.97, 35),
        'uzi': Weapon('UZI', 'SMG', 13.5, 62, 52, 0.95, 40),
        'pp19': Weapon('PP19 Bizon', 'SMG', 9.0, 48, 32, 0.89, 60),
        'vss': Weapon('VSS', 'SMG', 8.5, 45, 30, 0.85, 65),
        'qcw': Weapon('QCW', 'SMG', 11.5, 56, 42, 0.92, 58),
        'cbrr': Weapon('CBR4', 'SMG', 12.0, 59, 44, 0.94, 52),
        
        # === Assault Rifles (14 weapons) ===
        'm4a1': Weapon('M4A1', 'AR', 10.0, 60, 35, 0.88, 80),
        'ak': Weapon('AK', 'AR', 9.0, 75, 60, 0.85, 75),
        'groza': Weapon('Groza', 'AR', 11.0, 70, 55, 0.87, 70),
        'scar': Weapon('SCAR', 'AR', 9.5, 58, 33, 0.89, 85),
        'xm8': Weapon('XM8', 'AR', 10.5, 62, 38, 0.90, 78),
        'm14': Weapon('M14', 'AR', 8.0, 65, 40, 0.86, 90),
        'an94': Weapon('AN94', 'AR', 9.8, 63, 36, 0.88, 82),
        'aug': Weapon('AUG', 'AR', 10.2, 59, 34, 0.89, 83),
        'famas': Weapon('FAMAS', 'AR', 11.5, 67, 42, 0.87, 75),
        'g36': Weapon('G36', 'AR', 9.2, 57, 32, 0.90, 86),
        'qbz': Weapon('QBZ', 'AR', 9.6, 61, 37, 0.89, 81),
        'ac80': Weapon('AC80', 'AR', 8.5, 55, 30, 0.91, 88),
        'svd': Weapon('SVD', 'AR', 7.5, 50, 28, 0.87, 95),
        'parafal': Weapon('Parafal', 'AR', 8.2, 54, 29, 0.88, 92),
        
        # === Snipers (8 weapons) ===
        'awm': Weapon('AWM', 'Sniper', 0.8, 85, 30, 0.70, 400),
        'kar98k': Weapon('Kar98k', 'Sniper', 1.0, 75, 25, 0.75, 300),
        'dragunov': Weapon('Dragunov', 'Sniper', 2.5, 70, 40, 0.78, 250),
        'm82b': Weapon('M82B', 'Sniper', 0.6, 90, 35, 0.65, 500),
        'sks': Weapon('SKS', 'Sniper', 3.0, 68, 45, 0.80, 200),
        'winchester': Weapon('Winchester', 'Sniper', 1.2, 72, 28, 0.77, 280),
        'svd': Weapon('SVD', 'Sniper', 2.2, 69, 38, 0.79, 240),
        'lynx': Weapon('Lynx', 'Sniper', 0.9, 82, 32, 0.72, 350),
        
        # === Shotguns (6 weapons) ===
        'm1887': Weapon('M1887', 'Shotgun', 1.2, 90, 70, 0.85, 25),
        'mp90': Weapon('MP90', 'Shotgun', 2.0, 80, 60, 0.88, 20),
        'm1014': Weapon('M1014', 'Shotgun', 1.8, 85, 65, 0.86, 30),
        'spas12': Weapon('SPAS12', 'Shotgun', 1.5, 82, 62, 0.87, 28),
        'usas': Weapon('USAS', 'Shotgun', 3.5, 78, 58, 0.89, 35),
        'mag7': Weapon('MAG-7', 'Shotgun', 2.2, 83, 63, 0.88, 32),
        
        # === LMGs (4 weapons) ===
        'm249': Weapon('M249', 'LMG', 8.0, 80, 55, 0.75, 100),
        'm60': Weapon('M60', 'LMG', 7.5, 85, 60, 0.73, 110),
        'gatling': Weapon('Gatling', 'LMG', 12.0, 88, 65, 0.70, 90),
        'pkp': Weapon('PKP', 'LMG', 7.8, 83, 58, 0.74, 105),
        
        # === Pistols (6 weapons) ===
        'deagle': Weapon('Desert Eagle', 'Pistol', 4.0, 70, 50, 0.95, 50),
        'm500': Weapon('M500', 'Pistol', 2.5, 75, 45, 0.93, 45),
        'g18': Weapon('G18', 'Pistol', 6.0, 55, 40, 0.98, 35),
        'm1873': Weapon('M1873', 'Pistol', 2.0, 65, 35, 0.94, 40),
        'usp': Weapon('USP', 'Pistol', 5.0, 50, 30, 0.96, 38),
        'm9': Weapon('M9', 'Pistol', 4.5, 52, 32, 0.97, 36),
        
        # === Special ===
        'cg15': Weapon('CG15', 'Special', 10.0, 50, 30, 0.85, 60),
        'm79': Weapon('M79', 'Launcher', 1.0, 0, 0, 0.80, 150),
        'rgs': Weapon('RGS', 'Special', 8.5, 45, 25, 0.82, 55),
    }
    
    @classmethod
    def get_weapon(cls, code: str) -> Weapon:
        """Get weapon by code (case insensitive)"""
        return cls.WEAPONS.get(code.lower(), cls.WEAPONS['m4a1'])
    
    @classmethod
    def get_by_category(cls, category: str) -> List[Weapon]:
        """Get all weapons in a category"""
        cat = category.upper()
        return [w for w in cls.WEAPONS.values() if w.category.upper() == cat]
    
    @classmethod
    def list_all_codes(cls) -> List[str]:
        """List all available weapon codes"""
        return list(cls.WEAPONS.keys())
    
    @classmethod
    def get_recommendation(cls, playstyle: str) -> List[str]:
        """Get weapon recommendations for playstyle"""
        recommendations = {
            'aggressive': ['mp40', 'mp5', 'm1887', 'mac10'],
            'tactical': ['m4a1', 'scar', 'ump', 'an94'],
            'sniper': ['awm', 'kar98k', 'm82b'],
            'versatile': ['m4a1', 'mp5', 'groza']
        }
        return recommendations.get(playstyle.lower(), ['m4a1'])