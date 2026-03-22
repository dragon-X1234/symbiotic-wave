
---

## 📄 **FILE 3: `install.sh`** (Termux/Unix Installer)
```bash
#!/bin/bash
# MN-SOS v3.0 Installation Script
# Usage: curl -fsSL [URL] | bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${CYAN}MN-SOS v3.0 Installation${NC}"
echo "========================"

# Detect environment
if [[ "$PREFIX" == *"com.termux"* ]]; then
    IS_TERMUX=1
    INSTALL_DIR="$HOME/.mn-sos"
    BIN_DIR="$PREFIX/bin"
    echo -e "${GREEN}[✓] Termux detected${NC}"
else
    IS_TERMUX=0
    INSTALL_DIR="$HOME/.local/share/mn-sos"
    BIN_DIR="$HOME/.local/bin"
    mkdir -p "$BIN_DIR"
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[!] Python3 not found${NC}"
    if [ "$IS_TERMUX" -eq 1 ]; then
        pkg update -y && pkg install python -y
    else
        exit 1
    fi
fi

# Create directories
echo "[*] Creating directories..."
mkdir -p "$INSTALL_DIR"/{core,interface,utils,config}

# Download source (placeholder for GitHub raw)
GITHUB_URL="https://github.com/YOURUSERNAME/MN-SOS/archive/main.zip"
TEMP_ZIP="/tmp/mn-sos-install.zip"

if command -v curl &> /dev/null; then
    curl -fsSL "$GITHUB_URL" -o "$TEMP_ZIP" || {
        echo -e "${YELLOW}[!] Download failed, using local files${NC}"
        cp -r . "$INSTALL_DIR/"
    }
elif command -v wget &> /dev/null; then
    wget -q "$GITHUB_URL" -O "$TEMP_ZIP" || {
        echo -e "${YELLOW}[!] Download failed, using local files${NC}"
        cp -r . "$INSTALL_DIR/"
    }
fi

# Extract if downloaded
if [ -f "$TEMP_ZIP" ]; then
    cd /tmp
    unzip -q -o "$TEMP_ZIP"
    cp -r MN-SOS-main/* "$INSTALL_DIR/"
    rm -f "$TEMP_ZIP"
fi

# Install dependencies
echo "[*] Installing dependencies..."
pip3 install --user -q numpy rich 2>/dev/null || pip3 install -q numpy rich

# Create launcher
cat > "$BIN_DIR/mn-sos" << 'EOF'
#!/bin/bash
export PYTHONPATH="$HOME/.mn-sos:$PYTHONPATH"
cd "$HOME/.mn-sos"
python3 main.py "$@"
EOF
chmod +x "$BIN_DIR/mn-sos"

# Create updater
cat > "$BIN_DIR/mn-sos-update" << EOF
#!/bin/bash
cd "$INSTALL_DIR"
git pull 2>/dev/null || {
    echo "Updating from remote..."
    curl -fsSL https://raw.githubusercontent.com/YOURUSERNAME/MN-SOS/main/install.sh | bash
}
EOF
chmod +x "$BIN_DIR/mn-sos-update"

echo -e "${GREEN}[✓] Installation complete${NC}"
echo "Run: mn-sos"