#!/usr/bin/env python3
import logging
import sys
import os
from datetime import datetime
from pathlib import Path

class MNLogger:
    """
    Production-grade logging with rotation.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MNLogger, cls).__new__(cls)
            cls._instance._setup()
        return cls._instance
    
    def _setup(self):
        """Configure logger"""
        # Log directory
        log_dir = Path.home() / ".mn-sos" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d")
        log_file = log_dir / f"mn-sos-{timestamp}.log"
        
        # Formatters
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
        )
        console_formatter = logging.Formatter(
            '[%(levelname)s] %(message)s'
        )
        
        # File handler (debug level)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler (warning level)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.WARNING)
        
        # Logger
        self.logger = logging.getLogger("MN-SOS")
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def debug(self, msg): self.logger.debug(msg)
    def info(self, msg): self.logger.info(msg)
    def warning(self, msg): self.logger.warning(msg)
    def error(self, msg): self.logger.error(msg)
    def critical(self, msg): self.logger.critical(msg)

# Global instance
log = MNLogger()