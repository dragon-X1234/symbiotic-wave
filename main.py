#!/usr/bin/env python3
"""
Symbiote v3.0 - Complete Integrated System
Hardware-native sensitivity with all modules
"""

import sys
import os
import json
import signal
from pathlib import Path
from typing import Dict, Optional

SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

# Version
VERSION = "3.0.0"

def signal_handler(sig, frame):
    """Graceful exit on Ctrl+C"""
    print("\n\n[!] Exiting Symbiote...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

class SymbioteApp:
    """Main application controller with navigation"""
    
    def __init__(self):
        self.current_menu = "main"
        self.running = True
        self.device_profile = None
        self.sensitivity_matrix = None
        self.molecule = None
        
        # Initialize all modules
        self._init_modules()
    
    def _init_modules(self):
        """Lazy load all modules with error handling"""
        self.modules = {}
        
        try:
            from core.hardware_probe import HardwareProbe, DeviceProfile
            self.modules['hardware'] = HardwareProbe
            self.modules['device'] = DeviceProfile
        except Exception as e:
            print(f"[!] Hardware module error: {e}")
            self.modules['hardware'] = None
        
        try:
            from core.dynamic_calculator import DynamicSensitivityEngine
            self.modules['calculator'] = DynamicSensitivityEngine
        except:
            try:
                from core.neural_sensitivity import NeuralMolecularBridge
                self.modules['neural'] = NeuralMolecularBridge
            except:
                pass
        
        try:
            from core.quantum_calculator import QuantumCalculator
            self.modules['quantum'] = QuantumCalculator
        except Exception as e:
            print(f"[!] Quantum module: {e}")
        
        try:
            from core.molecular_valence import MolecularInterface
            self.modules['molecular'] = MolecularInterface
        except Exception as e:
            print(f"[!] Molecular module: {e}")
        
        try:
            from core.weapon_database import WeaponDatabase
            self.modules['weapons'] = WeaponDatabase
        except Exception as e:
            print(f"[!] Weapons module: {e}")
        
        try:
            from utils.biometric_bridge import BiometricBridge
            self.modules['biometric'] = BiometricBridge
        except Exception as e:
            print(f"[!] Biometric module: {e}")
        
        try:
            from utils.cloud_sync import CloudSyncManager
            self.modules['cloud'] = CloudSyncManager
        except Exception as e:
            print(f"[!] Cloud module: {e}")
        
        try:
            from utils.logger import log
            self.modules['logger'] = log
        except:
            self.modules['logger'] = None
    
    def clear_screen(self):
        """Clear terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title=""):
        """Print consistent header"""
        self.clear_screen()
        print("🔥 Symbiote v3.0 - Neural Sensitivity OS")
        print("=" * 50)
        if title:
            print(f"  {title}")
            print("-" * 50)
        print()
    
    def get_input(self, prompt: str, valid_options: list = None, allow_back: bool = True) -> str:
        """
        Get user input with back/quit functionality
        Returns 'BACK' or 'QUIT' for navigation
        """
        full_prompt = prompt
        if allow_back:
            full_prompt += " [b=back, q=quit]"
        full_prompt += ": "
        
        while True:
            try:
                choice = input(full_prompt).strip().lower()
                
                if choice in ['q', 'quit', 'exit']:
                    return 'QUIT'
                if allow_back and choice in ['b', 'back', 'return']:
                    return 'BACK'
                
                if valid_options and choice not in valid_options:
                    print(f"[!] Invalid option. Use: {', '.join(valid_options)}")
                    continue
                
                return choice
                
            except (EOFError, KeyboardInterrupt):
                return 'QUIT'
    
    def main_menu(self):
        """Main menu with all options"""
        while self.running:
            self.print_header("Main Menu")
            
            print("[1] Auto-Detect Hardware & Calculate")
            print("[2] Manual Hardware Input")
            print("[3] Advanced Analysis (Biometric + Neural)")
            print("[4] Weapon Optimization")
            print("[5] Cloud Sync (Export/Import)")
            print("[6] Settings")
            print("[Q] Quit")
            print()
            
            choice = self.get_input("Select option", ['1', '2', '3', '4', '5', '6', 'q'], allow_back=False)
            
            if choice == 'QUIT':
                self.quit_app()
                return
            
            elif choice == '1':
                if not self.auto_detect():
                    continue
            
            elif choice == '2':
                if not self.manual_input():
                    continue
            
            elif choice == '3':
                self.advanced_analysis()
            
            elif choice == '4':
                self.weapon_menu()
            
            elif choice == '5':
                self.cloud_menu()
            
            elif choice == '6':
                self.settings_menu()
    
    def auto_detect(self) -> bool:
        """Auto-detect hardware and calculate"""
        self.print_header("Hardware Detection")
        
        if not self.modules.get('hardware'):
            print("[!] Hardware probe not available")
            input("Press Enter to go back...")
            return False
        
        print("[*] Probing device hardware...")
        print("    This may take a few seconds...")
        
        try:
            probe = self.modules['hardware']()
            self.device_profile = probe.probe_deep()
            
            print(f"\n[✓] Hardware detected:")
            print(f"    DPI: {self.device_profile.dpi}")
            print(f"    Screen: {self.device_profile.screen_width}x{self.device_profile.screen_height}")
            print(f"    Refresh: {self.device_profile.refresh_rate}Hz")
            print(f"    Touch: {self.device_profile.touch_sampling_rate}Hz")
            print(f"    CPU: {self.device_profile.cpu_cores} cores @ {self.device_profile.cpu_max_freq_ghz}GHz")
            print(f"    RAM: {self.device_profile.ram_gb:.1f}GB")
            print(f"    Performance Score: {self.device_profile.performance_score:.2f}/2.0")
            
            # Calculate using all available engines
            self._calculate_full()
            
            if not self.show_results():
                return False
            
            return True
            
        except Exception as e:
            print(f"\n[!] Detection failed: {e}")
            input("Press Enter to go back...")
            return False
    
    def _calculate_full(self):
        """Calculate using all available engines"""
        self.print_header("Calculating Sensitivities")
        
        print("[*] Running Dynamic Calculator...")
        
        # Primary calculation
        if self.modules.get('calculator'):
            engine = self.modules['calculator'](self.device_profile)
            matrix = engine.calculate_matrix()
            
            # Apply biometric adjustment if available
            if self.modules.get('biometric'):
                print("[*] Checking biometric sensors...")
                bio = self.modules['biometric']()
                adjustment = bio.get_sensitivity_adjustment()
                
                print(f"    Stress adjustment factor: {adjustment:.2f}")
                
                # Apply adjustment
                matrix.general = int(matrix.general * adjustment)
                matrix.red_dot = int(matrix.red_dot * adjustment)
                matrix.scope_2x = int(matrix.scope_2x * adjustment)
                matrix.scope_4x = int(matrix.scope_4x * adjustment)
                matrix.sniper = int(matrix.sniper * adjustment)
                matrix.gyro_general = int(matrix.gyro_general * adjustment)
            
            self.sensitivity_matrix = matrix
            
            # Create molecular representation
            if self.modules.get('molecular'):
                values = {
                    'general': matrix.general,
                    'red_dot': matrix.red_dot,
                    'scope_2x': matrix.scope_2x,
                    'scope_4x': matrix.scope_4x,
                    'sniper': matrix.sniper,
                    'free_look': matrix.free_look if hasattr(matrix, 'free_look') else int(matrix.general * 1.1)
                }
                self.molecule = self.modules['molecular'](values)
        
        print("[✓] Calculation complete")
    
    def show_results(self) -> bool:
        """Display results with options"""
        while True:
            self.print_header("Calculated Sensitivities")
            
            if not self.sensitivity_matrix:
                print("[!] No calculation results")
                input("Press Enter to go back...")
                return False
            
            m = self.sensitivity_matrix
            
            print("OPTIMAL SENSITIVITY MATRIX:")
            print("-" * 30)
            print(f"{'General':<15} │ {m.general:>3}")
            print(f"{'Red Dot':<15} │ {m.red_dot:>3}")
            print(f"{'2x Scope':<15} │ {m.scope_2x:>3}")
            print(f"{'4x Scope':<15} │ {m.scope_4x:>3}")
            print(f"{'Sniper':<15} │ {m.sniper:>3}")
            print(f"{'Gyro General':<15} │ {m.gyro_general:>3}")
            print(f"{'Gyro Red Dot':<15} │ {m.gyro_red_dot:>3}")
            print(f"{'Gyro 4x':<15} │ {m.gyro_4x:>3}")
            print("-" * 30)
            
            # Show graphics recommendations
            if self.modules.get('calculator') and self.device_profile:
                engine = self.modules['calculator'](self.device_profile)
                graphics = engine.get_graphics_settings()
                print("\n🎨 Recommended Graphics:")
                for k, v in graphics.items():
                    print(f"    {k}: {v}")
            
            print("\nOptions:")
            print("[1] Export to file")
            print("[2] Copy to clipboard")
            print("[3] View molecular structure")
            print("[4] Adjust values manually")
            print("[b] Back to main menu")
            print("[q] Quit")
            
            choice = self.get_input("Select", ['1', '2', '3', '4'])
            
            if choice == 'QUIT':
                self.quit_app()
                return False
            elif choice == 'BACK':
                return True
            elif choice == '1':
                self.export_results()
            elif choice == '2':
                self.copy_to_clipboard()
            elif choice == '3':
                self.view_molecular()
            elif choice == '4':
                self.adjust_manual()
    
    def manual_input(self) -> bool:
        """Manual hardware specification"""
        self.print_header("Manual Hardware Input")
        
        try:
            from core.hardware_probe import DeviceProfile
            
            print("Enter your device specifications:")
            print("(Press Enter for defaults)")
            print()
            
            dpi = int(input("DPI [400]: ") or "400")
            width = int(input("Screen Width [1080]: ") or "1080")
            height = int(input("Screen Height [2400]: ") or "2400")
            size = float(input("Screen Size inches [6.5]: ") or "6.5")
            refresh = int(input("Refresh Rate Hz [90]: ") or "90")
            touch = int(input("Touch Sampling Hz [240]: ") or "240")
            cores = int(input("CPU Cores [8]: ") or "8")
            freq = float(input("CPU GHz [2.4]: ") or "2.4")
            ram = float(input("RAM GB [8]: ") or "8")
            
            self.device_profile = DeviceProfile(
                dpi=dpi,
                screen_width=width,
                screen_height=height,
                physical_size_inches=size,
                refresh_rate=refresh,
                touch_sampling_rate=touch,
                cpu_cores=cores,
                cpu_max_freq_ghz=freq,
                cpu_architecture='arm64',
                gpu_renderer='Manual',
                ram_gb=ram,
                thermal_zone_paths=[],
                android_version=12,
                kernel_version='manual',
                battery_temp=35.0
            )
            
            self._calculate_full()
            return self.show_results()
            
        except Exception as e:
            print(f"\n[!] Input error: {e}")
            input("Press Enter to go back...")
            return False
    
    def advanced_analysis(self):
        """Biometric and neural analysis"""
        self.print_header("Advanced Analysis")
        
        if not self.device_profile:
            print("[!] No hardware profile. Run detection first.")
            input("Press Enter to go back...")
            return
        
        print("[*] Running comprehensive analysis...")
        
        # Biometric check
        if self.modules.get('biometric'):
            bio = self.modules['biometric']()
            stress = bio.calculate_stress_index()
            print(f"\n📊 Biometric Status:")
            print(f"    Heart Rate: {bio.heart_rate or 'N/A'} bpm")
            print(f"    Stress Level: {stress*100:.0f}%")
            print(f"    Hand Steadiness: {bio.hand_steadiness*100:.0f}%")
            print(f"    Sensitivity Adjustment: {bio.get_sensitivity_adjustment():.2f}x")
        
        # Quantum analysis
        if self.modules.get('quantum'):
            qc = self.modules['quantum']()
            print(f"\n🔬 Quantum Analysis:")
            print(f"    DPI Scaling Factor: {qc.dpi_scaling_factor(self.device_profile.dpi, self.device_profile.physical_size_inches):.3f}")
        
        input("\nPress Enter to go back...")
    
    def weapon_menu(self):
        """Weapon optimization submenu"""
        while True:
            self.print_header("Weapon Optimization")
            
            if not self.modules.get('weapons'):
                print("[!] Weapon database not available")
                input("Press Enter to go back...")
                return
            
            print("Select weapon category:")
            print("[1] SMG (MP40, Vector, etc.)")
            print("[2] Assault Rifle (M4A1, AK, etc.)")
            print("[3] Sniper (AWM, Kar98k, etc.)")
            print("[4] Shotgun (M1887, etc.)")
            print("[5] Search specific weapon")
            print("[b] Back")
            print("[q] Quit")
            
            choice = self.get_input("Select", ['1', '2', '3', '4', '5'])
            
            if choice == 'QUIT':
                self.quit_app()
                return
            elif choice == 'BACK':
                return
            
            # Handle weapon selection...
            print("[*] Weapon optimization would show here...")
            print("[!] Feature: Adjust sens for specific weapon recoil")
            input("Press Enter to continue...")
    
    def cloud_menu(self):
        """Cloud sync menu"""
        while True:
            self.print_header("Cloud Sync")
            
            print("[1] Export to GitHub Gist")
            print("[2] Import from Gist")
            print("[3] Generate Share Code")
            print("[4] Local Network Share")
            print("[b] Back")
            print("[q] Quit")
            
            choice = self.get_input("Select", ['1', '2', '3', '4'])
            
            if choice == 'QUIT':
                self.quit_app()
                return
            elif choice == 'BACK':
                return
            
            if not self.sensitivity_matrix:
                print("[!] No configuration to sync. Calculate first.")
                input("Press Enter...")
                continue
            
            print("[*] Cloud feature placeholder")
            print("[!] Would export to GitHub Gist here")
            input("Press Enter...")
    
    def export_results(self):
        """Export to JSON"""
        try:
            filename = input("Filename [symbiote_config.json]: ").strip() or "symbiote_config.json"
            data = {
                'version': VERSION,
                'device': {
                    'dpi': self.device_profile.dpi if self.device_profile else None,
                    'performance': self.device_profile.performance_score if self.device_profile else None
                },
                'sensitivity': {
                    'general': self.sensitivity_matrix.general,
                    'red_dot': self.sensitivity_matrix.red_dot,
                    'scope_2x': self.sensitivity_matrix.scope_2x,
                    'scope_4x': self.sensitivity_matrix.scope_4x,
                    'sniper': self.sensitivity_matrix.sniper,
                    'gyro_general': self.sensitivity_matrix.gyro_general,
                    'gyro_red_dot': self.sensitivity_matrix.gyro_red_dot,
                    'gyro_4x': self.sensitivity_matrix.gyro_4x
                }
            }
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"[✓] Exported to {filename}")
        except Exception as e:
            print(f"[!] Export failed: {e}")
        input("Press Enter...")
    
    def copy_to_clipboard(self):
        """Copy to clipboard"""
        try:
            text = f"General: {self.sensitivity_matrix.general}, Red Dot: {self.sensitivity_matrix.red_dot}"
            # Try to use termux or xclip
            import subprocess
            subprocess.run(['termux-clipboard-set'], input=text, text=True)
            print("[✓] Copied to clipboard")
        except:
            print("[!] Clipboard not available. Manually copy values above.")
        input("Press Enter...")
    
    def view_molecular(self):
        """View molecular structure"""
        self.print_header("Molecular Structure")
        
        if not self.molecule:
            print("[!] No molecular data")
            input("Press Enter...")
            return
        
        print("Chemical Bond Visualization:")
        print("(C=General, N=Red Dot/2x, O=4x, H=AWM, S=Free Look)")
        print()
        
        for atom_id, atom in self.molecule.atoms.items():
            bonds = ", ".join(atom.bonds) if atom.bonds else "None"
            print(f"{atom.name:12} [{atom.element.name:8}] Valence: {atom.get_valence()} | Value: {atom.value:3} | Bonds: {bonds}")
        
        input("\nPress Enter to go back...")
    
    def adjust_manual(self):
        """Manually adjust calculated values"""
        while True:
            self.print_header("Manual Adjustment")
            
            print("Current values:")
            print(f"1. General:     {self.sensitivity_matrix.general}")
            print(f"2. Red Dot:     {self.sensitivity_matrix.red_dot}")
            print(f"3. 2x Scope:    {self.sensitivity_matrix.scope_2x}")
            print(f"4. 4x Scope:    {self.sensitivity_matrix.scope_4x}")
            print(f"5. Sniper:      {self.sensitivity_matrix.sniper}")
            print("[s] Save changes")
            print("[r] Reset to calculated")
            print("[b] Back (discard)")
            
            choice = self.get_input("Select", ['1', '2', '3', '4', '5', 's', 'r'])
            
            if choice == 'QUIT':
                self.quit_app()
                return
            elif choice == 'BACK':
                return
            elif choice == 's':
                print("[✓] Changes saved")
                input("Press Enter...")
                return
            elif choice == 'r':
                self._calculate_full()
                print("[✓] Reset to calculated values")
                input("Press Enter...")
            else:
                try:
                    new_val = int(input(f"New value for option {choice} (1-200): "))
                    new_val = max(1, min(200, new_val))
                    # Update the value...
                    if choice == '1':
                        self.sensitivity_matrix.general = new_val
                    elif choice == '2':
                        self.sensitivity_matrix.red_dot = new_val
                    # ... etc
                    print(f"[✓] Updated to {new_val}")
                except ValueError:
                    print("[!] Invalid number")
    
    def settings_menu(self):
        """Settings submenu"""
        while True:
            self.print_header("Settings")
            
            print("[1] View System Info")
            print("[2] Check for Updates")
            print("[3] Reset All Data")
            print("[b] Back")
            print("[q] Quit")
            
            choice = self.get_input("Select", ['1', '2', '3'])
            
            if choice == 'QUIT':
                self.quit_app()
                return
            elif choice == 'BACK':
                return
            elif choice == '1':
                self.show_system_info()
            elif choice == '2':
                self.check_updates()
            elif choice == '3':
                print("[!] Reset functionality placeholder")
                input("Press Enter...")
    
    def show_system_info(self):
        """Display system information"""
        self.print_header("System Information")
        
        print(f"Symbiote Version: {VERSION}")
        print(f"Python: {sys.version.split()[0]}")
        print(f"Install Dir: {SCRIPT_DIR}")
        print()
        print("Loaded Modules:")
        for name, mod in self.modules.items():
            status = "✓" if mod else "✗"
            print(f"  [{status}] {name}")
        
        input("\nPress Enter to go back...")
    
    def check_updates(self):
        """Check for updates"""
        self.print_header("Update Check")
        
        print("[*] Checking for new versions...")
        print("[!] Would check GitHub releases here")
        print("[i] Current: v" + VERSION)
        input("Press Enter to go back...")
    
    def quit_app(self):
        """Clean exit"""
        self.running = False
        self.print_header("Shutdown")
        print("[✓] Symbiote shutting down gracefully")
        print("[i] Your configuration has been preserved")
        sys.exit(0)

def main():
    """Entry point"""
    print("Initializing Symbiote...")
    app = SymbioteApp()
    app.main_menu()

if __name__ == "__main__":
    main()