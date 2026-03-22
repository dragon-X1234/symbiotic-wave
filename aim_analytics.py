#!/usr/bin/env python3
import math
from typing import List, Dict, Tuple
from dataclasses import dataclass
from collections import deque

@dataclass
class AimEvent:
    timestamp: float
    delta_x: float
    delta_y: float
    velocity: float
    accuracy: float

class AimAnalytics:
    """
    Analyze aim patterns for optimization suggestions.
    """
    
    def __init__(self, buffer_size: int = 1000):
        self.events: deque[AimEvent] = deque(maxlen=buffer_size)
    
    def record(self, dx: float, dy: float, target_dist: float = 0):
        """Record aim movement"""
        import time
        velocity = math.sqrt(dx**2 + dy**2)
        event = AimEvent(
            timestamp=time.time(),
            delta_x=dx,
            delta_y=dy,
            velocity=velocity,
            accuracy=max(0, 100 - target_dist)
        )
        self.events.append(event)
    
    def analyze_jitter(self) -> Dict:
        """Analyze aim jitter (micro-corrections)"""
        if len(self.events) < 20:
            return {'score': 0, 'recommendation': 'insufficient_data'}
        
        velocities = [e.velocity for e in self.events]
        changes = []
        
        for i in range(1, len(velocities)):
            changes.append(abs(velocities[i] - velocities[i-1]))
        
        avg_change = sum(changes) / len(changes) if changes else 0
        
        if avg_change > 15:
            return {'score': avg_change, 'recommendation': 'decrease_sensitivity'}
        elif avg_change < 3:
            return {'score': avg_change, 'recommendation': 'increase_sensitivity'}
        else:
            return {'score': avg_change, 'recommendation': 'optimal'}
    
    def get_suggestion(self) -> str:
        """Get human-readable suggestion"""
        analysis = self.analyze_jitter()
        rec = analysis['recommendation']
        
        if rec == 'decrease_sensitivity':
            return "⚠️ High jitter detected - Try lowering sensitivity by 5-10"
        elif rec == 'increase_sensitivity':
            return "✅ Aim too smooth - Can increase sensitivity by 5"
        else:
            return "🎯 Aim pattern optimal"