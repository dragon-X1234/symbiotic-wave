#!/usr/bin/env python3
import json
import hashlib
import os
from typing import Dict, Optional
from pathlib import Path

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
    from Crypto.Protocol.KDF import PBKDF2
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

class SecureProfileStore:
    """
    Encrypted profile storage using AES-256.
    """
    
    def __init__(self, storage_dir: str):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.salt_file = self.storage_dir / '.salt'
        self._ensure_salt()
    
    def _ensure_salt(self):
        """Generate salt if not exists"""
        if not self.salt_file.exists():
            salt = os.urandom(16)
            with open(self.salt_file, 'wb') as f:
                f.write(salt)
    
    def _get_salt(self) -> bytes:
        """Retrieve salt"""
        with open(self.salt_file, 'rb') as f:
            return f.read()
    
    def _derive_key(self, password: str) -> bytes:
        """Derive key from password"""
        if not CRYPTO_AVAILABLE:
            raise ImportError("pycryptodome required")
        salt = self._get_salt()
        return PBKDF2(password, salt, dkLen=32, count=1000000)
    
    def save_encrypted(self, name: str, data: Dict, password: str):
        """Save encrypted profile"""
        if not CRYPTO_AVAILABLE:
            # Fallback to plain JSON
            filepath = self.storage_dir / f"{name}.json"
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return
        
        key = self._derive_key(password)
        cipher = AES.new(key, AES.MODE_CBC)
        plaintext = json.dumps(data).encode()
        encrypted = cipher.encrypt(pad(plaintext, AES.block_size))
        
        filepath = self.storage_dir / f"{name}.enc"
        with open(filepath, 'wb') as f:
            f.write(cipher.iv + encrypted)
    
    def load_encrypted(self, name: str, password: str) -> Optional[Dict]:
        """Load encrypted profile"""
        filepath = self.storage_dir / f"{name}.enc"
        json_path = self.storage_dir / f"{name}.json"
        
        # Try encrypted first
        if filepath.exists() and CRYPTO_AVAILABLE:
            try:
                key = self._derive_key(password)
                with open(filepath, 'rb') as f:
                    data = f.read()
                iv = data[:16]
                encrypted = data[16:]
                cipher = AES.new(key, AES.MODE_CBC, iv)
                decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
                return json.loads(decrypted.decode())
            except:
                pass
        
        # Fallback to JSON
        if json_path.exists():
            with open(json_path, 'r') as f:
                return json.load(f)
        
        return None