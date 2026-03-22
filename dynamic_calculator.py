import math
from typing import Dict
from dataclasses import dataclass
from .hardware_probe import DeviceProfile

@dataclass
class SensitivityMatrix:
    """Complete sensitivity configuration for Free Fire"""
    general: int
    red_dot: int
    scope_2x: int
    scope_4x: int
    sniper: int
    free_look: int
    gyro_general: int
    gyro_red_dot: int
    gyro_4x: int

class DynamicSensitivityEngine:
    """
    Calculates sensitivities based purely on hardware physics.
    No static values - all derived from device specifications.
    """
    
    def __init__(self, device: DeviceProfile):
        self.device = device
        self.base_general = self._calculate_base_general()
    
    def _calculate_base_general(self) -> float:
        """
        Calculate base general sensitivity using physics:
        
        Formula components:
        1. DPI Factor: Inverse relationship (higher DPI = lower sens needed)
        2. Size Factor: Larger screens need adjustment
        3. Performance Factor: Better hardware = higher stable sensitivity
        4. Refresh Factor: Higher Hz = can increase slightly
        5. Touch Factor: Higher sampling = more responsive
        
        Reference: 320 DPI on 5.5" screen at 60Hz = 100 sensitivity
        """
        # DPI factor (inverse square root for natural feel)
        if self.device.dpi <= 0:
            dpi_factor = 1.0
        else:
            dpi_ratio = 320 / self.device.dpi
            dpi_factor = dpi_ratio ** 0.7
        
        # Screen size factor (larger screens need slightly lower sens)
        if self.device.physical_size_inches <= 0:
            size_factor = 1.0
        else:
            size_ratio = 5.5 / self.device.physical_size_inches
            size_factor = size_ratio ** 0.3
        
        # Performance factor (0.8 to 1.2 range)
        perf_factor = 0.8 + (self.device.performance_score * 0.4)
        
        # Refresh rate factor (small boost for high refresh)
        refresh_factor = 1.0 + ((self.device.refresh_rate - 60) / 1000)
        
        # Touch sampling factor
        touch_factor = 1.0 + ((self.device.touch_sampling_rate - 120) / 2000)
        
        # Base calculation
        base = 100.0 * dpi_factor * size_factor * perf_factor * refresh_factor * touch_factor
        
        # Thermal compensation (reduce if device is hot)
        if self.device.battery_temp and self.device.battery_temp > 40:
            base *= 0.95
        
        return base
    
    def calculate_matrix(self) -> SensitivityMatrix:
        """Calculate complete sensitivity matrix clamped to 1-200"""
        b = self.base_general
        
        def clamp(value: float) -> int:
            """Clamp to Free Fire limits (1-200)"""
            return max(1, min(200, int(round(value))))
        
        # Scope multipliers based on engagement physics
        # Closer range = higher sens, Long range = lower sens
        return SensitivityMatrix(
            general=clamp(b),
            red_dot=clamp(b * 0.95),      # Slight reduction for precision
            scope_2x=clamp(b * 0.75),     # Mid range
            scope_4x=clamp(b * 0.55),     # Long range precision
            sniper=clamp(b * 0.35),       # Long range stability
            free_look=clamp(b * 1.10),    # Camera movement
            gyro_general=clamp(b * 1.2),  # Gyro typically 20% higher
            gyro_red_dot=clamp(b * 1.15),
            gyro_4x=clamp(b * 0.90)
        )
    
    def calculate_weapon_compensation(self, weapon_fire_rate: float, 
                                    vertical_recoil: float) -> Dict[str, float]:
        """
        Calculate dynamic recoil compensation based on current sensitivity.
        
        Args:
            weapon_fire_rate: Shots per second
            vertical_recoil: Recoil value 0-100
            
        Returns:
            Dictionary with swipe recommendations
        """
        sens_factor = self.base_general / 100.0
        
        # Time between shots in ms
        if weapon_fire_rate > 0:
            interval_ms = 1000.0 / weapon_fire_rate
        else:
            interval_ms = 100.0
        
        # Compensation inversely proportional to sensitivity
        # Higher sens = smaller physical movement needed
        comp_amount = (vertical_recoil / 100.0) * 50.0 / sens_factor
        
        return {
            'swipe_distance_pixels': comp_amount,
            'swipe_duration_ms': interval_ms * 0.8,  # Slightly faster than fire rate
            'sensitivity_factor': sens_factor,
            'stability_rating': min(100, int(self.device.performance_score * 50))
        }
    
    def get_graphics_settings(self) -> Dict[str, str]:
        """Recommend graphics settings based on hardware capability"""
        score = self.device.performance_score
        
        if score > 1.5:
            return {
                'smooth': 'Ultra',
                'shadow': 'On',
                'anti_aliasing': 'On',
                'auto_adjust': 'Off'
            }
        elif score > 1.0:
            return {
                'smooth': 'High',
                'shadow': 'On',
                'anti_aliasing': 'Off',
                'auto_adjust': 'Off'
            }
        elif score > 0.6:
            return {
                'smooth': 'Medium',
                'shadow': 'Off',
                'anti_aliasing': 'Off',
                'auto_adjust': 'On'
            }
        else:
            return {
                'smooth': 'Low',
                'shadow': 'Off',
                'anti_aliasing': 'Off',
                'auto_adjust': 'On'
            }