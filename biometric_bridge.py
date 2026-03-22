#!/usr/bin/env python3
import time
import random
from typing import Optional, Dict, Callable

class BiometricBridge:
    """Integrates Android sensors for adaptive sensitivity"""
    
    def __init__(self):
        self.is_available = self._check_sensors()
        self.heart_rate: Optional[int] = None
        self.stress_level: float = 0.0
        self.hand_steadiness: float = 1.0
        
    def _check_sensors(self) -> bool:
        """Check for Termux sensor API"""
        try:
            import subprocess
            result = subprocess.run(['termux-sensor', '-h'], capture_output=True, timeout=2)
            return result.returncode == 0
        except:
            return False
    
    def read_heart_rate(self) -> Optional[int]:
        """Get heart rate (simulated if unavailable)"""
        if not self.is_available:
            return random.randint(60, 100)
        try:
            import subprocess, json
            result = subprocess.run(['termux-sensor', '-s', 'heart_rate', '-n', '1'], 
                                  capture_output=True, text=True, timeout=5)
            data = json.loads(result.stdout)
            hr = data.get('values', [0])[0]
            self.heart_rate = hr
            return hr
        except:
            return None
    
    def read_accelerometer(self) -> Dict[str, float]:
        """Detect hand shake/steadiness"""
        if not self.is_available:
            return {'steadiness': 1.0, 'variance': 0.1}
        try:
            import subprocess, json, numpy as np
            result = subprocess.run(['termux-sensor', '-s', 'accelerometer', '-n', '10'], 
                                  capture_output=True, text=True, timeout=2)
            readings = []
            for line in result.stdout.strip().split('\n'):
                try:
                    data = json.loads(line)
                    readings.append(data.get('values', [0,0,0]))
                except: pass
            
            if readings:
                variance = np.var([r[0] for r in readings]) + np.var([r[1] for r in readings])
                steadiness = max(0, 1 - (variance / 10))
                return {'steadiness': steadiness, 'variance': variance}
        except:
            pass
        return {'steadiness': 1.0, 'variance': 0.0}
    
    def calculate_stress_index(self) -> float:
        """0-1 stress level (affects sensitivity)"""
        hr = self.read_heart_rate()
        motion = self.read_accelerometer()
        
        if hr is None:
            return 0.0
            
        hr_factor = max(0, (hr - 60) / 60)
        motion_factor = 1 - motion['steadiness']
        stress = (hr_factor * 0.6) + (motion_factor * 0.4)
        self.stress_level = min(1.0, stress)
        return self.stress_level
    
    def get_sensitivity_adjustment(self) -> float:
        """Return multiplier (high stress = lower sens)"""
        stress = self.calculate_stress_index()
        if stress > 0.8: return 0.85
        elif stress > 0.6: return 0.92
        elif stress > 0.4: return 0.97
        return 1.0