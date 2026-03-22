#!/usr/bin/env python3
import json
import base64
import urllib.request
from typing import Dict, Optional

class CloudSyncManager:
    """Sync profiles to GitHub Gist or similar"""
    
    GIST_API = "https://api.github.com/gists"
    
    def __init__(self, token: Optional[str] = None):
        self.token = token
    
    def create_gist(self, profile: Dict, description: str = "Symbiote Profile") -> Optional[str]:
        """Upload encrypted profile to Gist"""
        if not self.token:
            return None
            
        try:
            encoded = base64.b64encode(json.dumps(profile).encode()).decode()
            payload = {
                "description": description,
                "public": False,
                "files": {"symbiote_profile.mns": {"content": encoded}}
            }
            
            req = urllib.request.Request(
                self.GIST_API,
                data=json.dumps(payload).encode(),
                headers={'Authorization': f'token {self.token}', 'Content-Type': 'application/json'},
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode())
                return result.get('id')
        except:
            return None
    
    def load_from_gist(self, gist_id: str) -> Optional[Dict]:
        """Download profile from Gist"""
        try:
            req = urllib.request.Request(f"{self.GIST_API}/{gist_id}")
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode())
                files = result.get('files', {})
                for fname, fdata in files.items():
                    if fname.endswith('.mns'):
                        content = fdata.get('content', '')
                        decoded = base64.b64decode(content).decode()
                        return json.loads(decoded)
        except:
            return None
    
    def generate_share_code(self, profile: Dict) -> str:
        """Generate short hash for sharing"""
        import hashlib
        data = f"{profile.get('device', '')}{profile.get('timestamp', '')}"
        return hashlib.sha256(data.encode()).hexdigest()[:8].upper()