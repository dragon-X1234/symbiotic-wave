import subprocess
import platform
import re
import os
from typing import Dict, Optional, Tuple, List
from dataclasses import dataclass

@dataclass
class DeviceProfile:
    """Complete hardware fingerprint for sensitivity calculation"""
    dpi: int
    screen_width: int
    screen_height: int
    physical_size_inches: float
    refresh_rate: int
    touch_sampling_rate: int
    cpu_cores: int
    cpu_max_freq_ghz: float
    cpu_architecture: str
    gpu_renderer: str
    ram_gb: float
    thermal_zone_paths: List[str]
    android_version: int
    kernel_version: str
    battery_temp: Optional[float] = None
    
    @property
    def aspect_ratio(self) -> float:
        """Calculate display aspect ratio"""
        return self.screen_width / self.screen_height if self.screen_height > 0 else 2.0
    
    @property
    def ppi(self) -> float:
        """Pixels per inch diagonal"""
        diag_pixels = (self.screen_width ** 2 + self.screen_height ** 2) ** 0.5
        return diag_pixels / self.physical_size_inches if self.physical_size_inches > 0 else 400
    
    @property
    def performance_score(self) -> float:
        """
        Calculate composite performance score (0.0 - 2.0)
        Based on CPU, RAM, Display, and Thermal capacity
        """
        score = 0.0
        
        # CPU Performance (40% weight)
        freq_score = min(self.cpu_max_freq_ghz / 3.0, 1.0) * 0.25
        core_score = min(self.cpu_cores / 8, 1.0) * 0.15
        score += freq_score + core_score
        
        # Memory (20% weight)
        ram_score = min(self.ram_gb / 12, 1.0) * 0.20
        score += ram_score
        
        # Display Quality (25% weight)
        refresh_score = min(self.refresh_rate / 120, 1.0) * 0.10
        touch_score = min(self.touch_sampling_rate / 240, 1.0) * 0.15
        score += refresh_score + touch_score
        
        # Thermal Headroom (15% weight)
        # Assume good thermal management if not specified
        score += 0.15
        
        return score

class HardwareProbe:
    """
    Deep hardware probing for Android devices via Termux, ADB, or system interfaces.
    Extracts real specifications for dynamic sensitivity calculation.
    """
    
    def __init__(self):
        self.is_termux = 'com.termux' in os.environ.get('PREFIX', '')
        self.is_adb_available = self._check_adb()
        
    def _check_adb(self) -> bool:
        """Check if Android Debug Bridge is available"""
        try:
            result = subprocess.run(['adb', 'version'], capture_output=True, timeout=2)
            return result.returncode == 0
        except:
            return False
    
    def probe_deep(self) -> DeviceProfile:
        """
        Aggressive hardware probing using multiple methods.
        Falls back gracefully if methods fail.
        """
        # Priority: Termux > ADB > System > Fallback
        if self.is_termux:
            result = self._probe_termux()
            if result:
                return result
        
        if self.is_adb_available:
            result = self._probe_adb()
            if result:
                return result
        
        result = self._probe_system()
        if result:
            return result
        
        return self._fallback_estimate()
    
    def _probe_termux(self) -> Optional[DeviceProfile]:
        """Probe using Termux API (most accurate for Android)"""
        try:
            # Display metrics via wm command
            size_output = self._exec_termux(['wm', 'size'])
            width, height = self._parse_resolution(size_output)
            
            density_output = self._exec_termux(['wm', 'density'])
            dpi = self._parse_dpi(density_output)
            
            # Calculate physical size
            physical_size = self._calculate_physical_size(width, height, dpi)
            
            # CPU information
            cpu_info = self._exec_termux(['cat', '/proc/cpuinfo'])
            cores, freq, arch = self._parse_cpu_info(cpu_info)
            
            # Memory
            mem_info = self._exec_termux(['cat', '/proc/meminfo'])
            ram = self._parse_ram(mem_info)
            
            # Display refresh rate
            refresh = self._get_refresh_rate_termux()
            
            # Touch sampling
            touch = self._get_touch_sampling_termux()
            
            # Android version
            android_ver = self._get_android_version()
            
            # Thermal zones
            thermal_paths = self._find_thermal_zones()
            
            return DeviceProfile(
                dpi=dpi,
                screen_width=width,
                screen_height=height,
                physical_size_inches=physical_size,
                refresh_rate=refresh,
                touch_sampling_rate=touch,
                cpu_cores=cores,
                cpu_max_freq_ghz=freq,
                cpu_architecture=arch,
                gpu_renderer=self._get_gpu_termux(),
                ram_gb=ram,
                thermal_zone_paths=thermal_paths,
                android_version=android_ver,
                kernel_version=platform.release(),
                battery_temp=self._get_battery_temp()
            )
            
        except Exception as e:
            return None
    
    def _probe_adb(self) -> Optional[DeviceProfile]:
        """Probe using ADB (for development machines)"""
        try:
            # Check for connected device
            devices = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
            if 'device' not in devices.stdout:
                return None
            
            def get_prop(prop):
                result = subprocess.run(['adb', 'shell', 'getprop', prop], 
                                      capture_output=True, text=True)
                return result.stdout.strip()
            
            dpi = int(get_prop('ro.sf.lcd_density') or 320)
            width = int(get_prop('ro.sf.lcd_width') or 1080)
            height = int(get_prop('ro.sf.lcd_height') or 2400)
            physical = self._calculate_physical_size(width, height, dpi)
            
            # CPU info via ADB
            cpu_out = subprocess.run(['adb', 'shell', 'cat', '/proc/cpuinfo'], 
                                   capture_output=True, text=True)
            cores, freq, arch = self._parse_cpu_info(cpu_out.stdout)
            
            # RAM
            ram_out = subprocess.run(['adb', 'shell', 'cat', '/proc/meminfo'], 
                                   capture_output=True, text=True)
            ram = self._parse_ram(ram_out.stdout)
            
            return DeviceProfile(
                dpi=dpi,
                screen_width=width,
                screen_height=height,
                physical_size_inches=physical,
                refresh_rate=60,
                touch_sampling_rate=120,
                cpu_cores=cores,
                cpu_max_freq_ghz=freq,
                cpu_architecture=arch,
                gpu_renderer='Unknown',
                ram_gb=ram,
                thermal_zone_paths=[],
                android_version=28,
                kernel_version='unknown'
            )
        except:
            return None
    
    def _probe_system(self) -> Optional[DeviceProfile]:
        """Probe using standard Linux interfaces"""
        try:
            # Read CPU info
            with open('/proc/cpuinfo', 'r') as f:
                cpu_info = f.read()
            cores, freq, arch = self._parse_cpu_info(cpu_info)
            
            # Read memory
            with open('/proc/meminfo', 'r') as f:
                mem_info = f.read()
            ram = self._parse_ram(mem_info)
            
            # Environment variables or defaults
            dpi = int(os.environ.get('DPI', 400))
            width = int(os.environ.get('WIDTH', 1080))
            height = int(os.environ.get('HEIGHT', 2400))
            
            physical = self._calculate_physical_size(width, height, dpi)
            
            return DeviceProfile(
                dpi=dpi,
                screen_width=width,
                screen_height=height,
                physical_size_inches=physical,
                refresh_rate=60,
                touch_sampling_rate=120,
                cpu_cores=cores,
                cpu_max_freq_ghz=freq,
                cpu_architecture=arch,
                gpu_renderer='Linux',
                ram_gb=ram,
                thermal_zone_paths=[],
                android_version=0,
                kernel_version=platform.release()
            )
        except:
            return None
    
    def _fallback_estimate(self) -> DeviceProfile:
        """Last resort estimation based on mid-range 2024 specs"""
        return DeviceProfile(
            dpi=400,
            screen_width=1080,
            screen_height=2400,
            physical_size_inches=6.5,
            refresh_rate=90,
            touch_sampling_rate=120,
            cpu_cores=8,
            cpu_max_freq_ghz=2.4,
            cpu_architecture='arm64',
            gpu_renderer='Mali-G78',
            ram_gb=8,
            thermal_zone_paths=[],
            android_version=12,
            kernel_version='5.4',
            battery_temp=35.0
        )
    
    def _exec_termux(self, cmd: list) -> str:
        """Execute command in Termux environment"""
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout
    
    def _parse_resolution(self, output: str) -> Tuple[int, int]:
        """Parse WxH from wm size output"""
        match = re.search(r'(\\d+)x(\\d+)', output)
        if match:
            return int(match.group(1)), int(match.group(2))
        return 1080, 2400
    
    def _parse_dpi(self, output: str) -> int:
        """Parse density value"""
        match = re.search(r'(\\d+)', output)
        return int(match.group(1)) if match else 400
    
    def _calculate_physical_size(self, width: int, height: int, dpi: int) -> float:
        """Calculate diagonal screen size in inches"""
        if dpi <= 0:
            return 6.5
        diag_pixels = (width ** 2 + height ** 2) ** 0.5
        return diag_pixels / dpi
    
    def _parse_cpu_info(self, cpuinfo: str) -> Tuple[int, float, str]:
        """Extract CPU cores, max frequency, and architecture"""
        cores = cpuinfo.count('processor')
        if cores == 0:
            cores = os.cpu_count() or 4
        
        # Try to read max frequency
        max_freq = 2.4  # Default assumption
        try:
            with open('/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq', 'r') as f:
                max_freq = int(f.read().strip()) / 1000000
        except:
            pass
        
        # Detect architecture
        arch = 'arm64'
        if 'aarch64' in cpuinfo:
            arch = 'arm64'
        elif 'armv7' in cpuinfo:
            arch = 'armv7'
        elif 'x86_64' in cpuinfo:
            arch = 'x86_64'
        
        return cores, max_freq, arch
    
    def _parse_ram(self, meminfo: str) -> float:
        """Parse total RAM in GB"""
        match = re.search(r'MemTotal:\\s+(\\d+)', meminfo)
        if match:
            kb = int(match.group(1))
            return kb / 1048576
        return 6.0
    
    def _get_refresh_rate_termux(self) -> int:
        """Extract refresh rate from dumpsys"""
        try:
            result = self._exec_termux(['dumpsys', 'display'])
            match = re.search(r'refreshRate:\\s*([\\d.]+)', result)
            if match:
                return int(float(match.group(1)))
        except:
            pass
        return 60
    
    def _get_touch_sampling_termux(self) -> int:
        """Detect touch sampling rate from input devices"""
        try:
            result = self._exec_termux(['getevent', '-il'])
            if '480Hz' in result:
                return 480
            elif '240Hz' in result or '240' in result:
                return 240
            elif '120Hz' in result:
                return 120
        except:
            pass
        return 60
    
    def _get_gpu_termux(self) -> str:
        """Detect GPU renderer"""
        try:
            result = self._exec_termux(['dumpsys', 'gfxinfo'])
            if 'Mali' in result:
                return 'Mali-G78'
            elif 'Adreno' in result:
                return 'Adreno-650'
            elif 'PowerVR' in result:
                return 'PowerVR'
        except:
            pass
        return 'Unknown'
    
    def _find_thermal_zones(self) -> list:
        """Locate thermal sensor paths"""
        zones = []
        try:
            base = '/sys/class/thermal/'
            if os.path.exists(base):
                for entry in os.listdir(base):
                    if 'thermal_zone' in entry:
                        zones.append(os.path.join(base, entry))
        except:
            pass
        return zones
    
    def _get_android_version(self) -> int:
        """Get Android API level"""
        try:
            result = self._exec_termux(['getprop', 'ro.build.version.sdk'])
            return int(result.strip())
        except:
            return 28
    
    def _get_battery_temp(self) -> Optional[float]:
        """Read battery temperature in Celsius"""
        try:
            with open('/sys/class/power_supply/battery/temp', 'r') as f:
                return int(f.read().strip()) / 10
        except:
            return None