#!/usr/bin/env python3
import sys
import os
import argparse

class HybridController:
    """
    Determines and routes to appropriate interface mode.
    """
    
    def __init__(self):
        self.args = self._parse_args()
        self.mode = self._detect_mode()
    
    def _parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--mode', choices=['cli', 'tui', 'gui', 'auto'], default='auto')
        parser.add_argument('--manual', action='store_true')
        parser.add_argument('--weapon', default='m4a1')
        return parser.parse_args()
    
    def _detect_mode(self):
        """Auto-detect best available mode"""
        if self.args.mode != 'auto':
            return self.args.mode
        
        # Check GUI availability
        try:
            import customtkinter
            if os.environ.get('DISPLAY') or sys.platform == 'darwin':
                return 'gui'
        except:
            pass
        
        # Check TUI availability
        try:
            import rich
            if sys.stdout.isatty():
                return 'tui'
        except:
            pass
        
        return 'cli'
    
    def run(self):
        """Execute selected mode"""
        if self.mode == 'gui':
            from .neural_gui import launch_gui
            launch_gui()
        elif self.mode == 'tui':
            from .molecular_cli import launch_tui
            from core.molecular_valence import MolecularInterface
            mol = MolecularInterface()
            launch_tui(mol)
        else:
            # CLI mode is default in main.py
            print("Running in CLI mode...")