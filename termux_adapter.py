#!/usr/bin/env python3
import os
import subprocess
from typing import Dict, Optional

class TermuxAdapter:
    """
    Android/Termux specific functionality.
    """
    
    def __init__(self):
        self.is_termux = 'com.termux' in os.environ.get('PREFIX', '')
        self.prefix = os.environ.get('PREFIX', '/usr')
    
    def vibrate(self, duration_ms: int = 50):
        """Vibrate device"""
        if not self.is_termux:
            return
        try:
            with open('/sys/class/timed_output/vibrator/enable', 'w') as f:
                f.write(str(duration_ms))
        except:
            pass
    
    def get_device_info(self) -> Dict[str, str]:
        """Get Android device info"""
        info = {}
        if not self.is_termux:
            return info
        
        props = {
            'model': 'ro.product.model',
            'manufacturer': 'ro.product.manufacturer',
            'android_version': 'ro.build.version.release'
        }
        
        for key, prop in props.items():
            try:
                result = subprocess.run(
                    ['getprop', prop],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                info[key] = result.stdout.strip()
            except:
                info[key] = 'unknown'
        
        return info
    
    def copy_to_clipboard(self, text: str):
        """Copy to Android clipboard"""
        if not self.is_termux:
            return
        try:
            subprocess.run(
                ['termux-clipboard-set'],
                input=text,
                text=True,
                timeout=2
            )
        except:
            pass
    
    def show_notification(self, title: str, content: str):
        """Show Android notification"""
        if not self.is_termux:
            return
        try:
            subprocess.run([
                'termux-notification',
                '--title', title,
                '--content', content
            ], timeout=2)
        except:
            pass