import re
from typing import Tuple, Any

class InputValidator:
    """Input validation and sanitization"""
    
    MAX_SENSITIVITY = 200
    MIN_SENSITIVITY = 1
    
    @staticmethod
    def dpi(value: Any) -> Tuple[bool, int]:
        """Validate DPI input"""
        try:
            dpi = int(value)
            if 72 <= dpi <= 1600:
                return True, dpi
            return False, 320
        except (ValueError, TypeError):
            return False, 320
    
    @staticmethod
    def sensitivity(value: Any) -> Tuple[bool, int]:
        """Validate and clamp sensitivity to 1-200"""
        try:
            sens = int(value)
            sens = max(InputValidator.MIN_SENSITIVITY, 
                      min(InputValidator.MAX_SENSITIVITY, sens))
            return True, sens
        except (ValueError, TypeError):
            return False, 50
    
    @staticmethod
    def weapon(code: str) -> Tuple[bool, str]:
        """Validate weapon code exists"""
        from core.weapon_database import WeaponDatabase
        code = code.lower().strip()
        valid = WeaponDatabase.list_all_codes()
        if code in valid:
            return True, code
        return False, 'm4a1'
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Remove dangerous characters from filenames"""
        safe = re.sub(r'[^a-zA-Z0-9_-]', '', filename)
        return safe[:50]