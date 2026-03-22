# MN-SOS v3.0: Molecular-Native Sensitivity OS

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Termux|Linux-green.svg)](https://termux.com)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

**Hardware-native sensitivity calculation for Free Fire.** No static databases. Real-time device probing with molecular bond physics.

## Features

- **Dynamic Hardware Probing**: DPI, refresh rate, CPU, RAM, thermal zones
- **Physics-Based Calculation**: Inverse-square DPI scaling, performance indexing
- **Molecular Interface**: Chemical valence bonding for sensitivity relationships
- **Complete Arsenal**: 50+ weapons with recoil compensation
- **Self-Updating**: GitHub-integrated auto-updater
- **Termux Optimized**: Native Android hardware access

## Installation

```bash
curl -fsSL https://raw.githubusercontent.com/YOURUSERNAME/MN-SOS/main/install.sh | bash
**Or manual:

```git clone https://github.com/YOURUSERNAME/MN-SOS.git
cd MN-SOS
pip install -r requirements.txt
python3 main.py

##Usage

```# Auto-detect hardware and calculate
mn-sos

# Manual hardware specification
mn-sos --manual

# Specific weapon optimization
mn-sos --weapon mp40 --dpi 400

# Export configuration
mn-sos --export config.json

## Architecture

```MN-SOS/
├── core/               # Calculation engines
├── interface/          # CLI/GUI renderers
├── utils/             # System integration
└── config/            # Molecular definitions

##Calculation Methodology
**Sensitivity = Base × (DPI_Factor) × (Performance_Factor) × (Refresh_Factor)**
Where:
**DPI_Factor: (320/DPI)^0.7 (inverse relationship)
Performance_Factor: 0.8 + (Benchmark_Score × 0.4)
Refresh_Factor: 1 + ((Hz - 60) / 1000)**

##Hardware Support
**DPI Detection: ro.sf.lcd_density (Android), X11 (Linux)
Refresh Rate: SurfaceFlinger parsing (60/90/120/144Hz)
Thermal: /sys/class/thermal/ zone monitoring
CPU: /proc/cpuinfo + cpufreq analysis
Touch: Input event sampling rate detection
License**

##MIT License - See LICENSE file##