#!/usr/bin/env python3
import math
from typing import List, Tuple

class QuantumCalculator:
    """Advanced mathematical operations for sensitivity curves"""
    
    @staticmethod
    def catmull_rom_spline(points: List[Tuple[float, float]], samples: int = 100) -> List[Tuple[float, float]]:
        """Generate smooth curve through control points"""
        if len(points) < 4:
            return points
            
        result = []
        for i in range(len(points) - 3):
            p0, p1, p2, p3 = points[i], points[i+1], points[i+2], points[i+3]
            
            for t in [j/samples for j in range(samples)]:
                t2, t3 = t*t, t*t*t
                
                x = 0.5 * ((2*p1[0]) + (-p0[0]+p2[0])*t + (2*p0[0]-5*p1[0]+4*p2[0]-p3[0])*t2 + (-p0[0]+3*p1[0]-3*p2[0]+p3[0])*t3)
                y = 0.5 * ((2*p1[1]) + (-p0[1]+p2[1])*t + (2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*t2 + (-p0[1]+3*p1[1]-3*p2[1]+p3[1])*t3)
                result.append((x, y))
        return result
    
    @staticmethod
    def bezier_cubic(p0, p1, p2, p3, t: float) -> Tuple[float, float]:
        """Cubic Bezier interpolation"""
        mt = 1 - t
        mt2, mt3 = mt*mt, mt*mt*mt
        t2, t3 = t*t, t*t*t
        
        x = mt3*p0[0] + 3*mt2*t*p1[0] + 3*mt*t2*p2[0] + t3*p3[0]
        y = mt3*p0[1] + 3*mt2*t*p1[1] + 3*mt*t2*p2[1] + t3*p3[1]
        return (x, y)
    
    @staticmethod
    def dpi_scaling_factor(dpi: int, physical_size: float) -> float:
        """Calculate sensitivity scaling based on screen physics"""
        ref_dpi, ref_size = 320, 5.5
        dpi_factor = (ref_dpi / dpi) ** 0.7
        size_factor = (ref_size / physical_size) ** 0.3
        return math.sqrt(dpi_factor * size_factor)
    
    @staticmethod
    def latency_compensation(latency_ms: float, base_sens: int) -> float:
        """Compensate for input lag"""
        if latency_ms <= 10: return 1.0
        return 1.0 + ((latency_ms - 10) * 0.005)
    
    @staticmethod
    def sigmoid(x: float, steepness: float = 1.0) -> float:
        return 1 / (1 + math.exp(-steepness * (x - 0.5)))