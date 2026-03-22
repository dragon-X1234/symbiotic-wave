#!/usr/bin/env python3
import os
import sys
import urllib.request
import json
import subprocess
from pathlib import Path

class AutoUpdater:
    """
    Self-updating system from GitHub releases.
    """
    
    def __init__(self, repo_owner: str, repo_name: str, current_version: str = "3.0.0"):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.current_version = current_version
        self.api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    
    def check_update(self):
        """Check for newer version"""
        try:
            req = urllib.request.Request(
                self.api_url,
                headers={'User-Agent': 'MN-SOS-Updater'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                latest = data['tag_name'].lstrip('v')
                
                # Simple version compare
                current_parts = [int(x) for x in self.current_version.split('.')]
                latest_parts = [int(x) for x in latest.split('.')]
                
                needs_update = False
                for i in range(max(len(current_parts), len(latest_parts))):
                    c = current_parts[i] if i < len(current_parts) else 0
                    l = latest_parts[i] if i < len(latest_parts) else 0
                    if l > c:
                        needs_update = True
                        break
                    elif l < c:
                        break
                
                return needs_update, latest
        except Exception as e:
            print(f"Update check failed: {e}")
            return False, self.current_version
    
    def update(self):
        """Perform update"""
        needs_update, latest = self.check_update()
        if not needs_update:
            print(f"Already on latest version (v{self.current_version})")
            return False
        
        print(f"Update available: v{self.current_version} -> v{latest}")
        confirm = input("Update now? [y/N]: ").lower()
        if confirm != 'y':
            return False
        
        # Re-run install script
        install_url = f"https://raw.githubusercontent.com/{self.repo_owner}/{self.repo_name}/main/install.sh"
        try:
            subprocess.run([
                'bash', '-c',
                f'curl -fsSL {install_url} | bash'
            ], check=True)
            return True
        except:
            print("Update failed")
            return False

def check_and_update():
    """Convenience function"""
    updater = AutoUpdater("YOURUSERNAME", "MN-SOS", "3.0.0")
    return updater.update()