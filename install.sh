#!/bin/bash
# Symbiote v3.0.0 Installer
# Repo: dragon-X1234/symbiotic-wave
# FIXED: Now matches actual repo filenames

set -e

REPO_OWNER="dragon-X1234"
REPO_NAME="symbiotic-wave"
RAW_URL="https://raw.githubusercontent.com/${REPO_OWNER}/${REPO_NAME}/main"
VERSION="3.0.0"

echo "🔥 Symbiote v${VERSION} Installation"
echo "============================="

# Detect Termux
if [[ "$PREFIX" == *"com.termux"* ]]; then
    INSTALL_DIR="$HOME/.symbiote"
    BIN_DIR="$PREFIX/bin"
    echo "[✓] Termux detected"
else
    INSTALL_DIR="$HOME/.local/share/symbiote"
    BIN_DIR="$HOME/.local/bin"
    mkdir -p "$BIN_DIR"
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[!] Python3 not found"
    if [[ "$PREFIX" == *"com.termux"* ]]; then
        echo "[*] Installing Python..."
        pkg update -y && pkg install python -y
    else
        echo "[!] Please install Python3 manually"
        exit 1
    fi
fi

# Create directories
echo "[*] Creating directories..."
mkdir -p "$INSTALL_DIR"/{core,interface,utils,config}

# Download function with URL encoding for spaces
download_file() {
    local repo_name="$1"
    local dest_folder="$2"
    local dest_name="$3"
    
    # URL encode spaces for the URL
    local encoded_name=$(printf '%s' "$repo_name" | sed 's/ /%20/g')
    local url="${RAW_URL}/${encoded_name}"
    local dest="${INSTALL_DIR}/${dest_folder}/${dest_name}"
    
    echo "  [↓] ${repo_name} → ${dest_folder}/${dest_name}"
    
    local success=false
    
    if command -v curl &> /dev/null; then
        if curl -fsSL --connect-timeout 15 "$url" -o "$dest" 2>/dev/null; then
            success=true
        fi
    elif command -v wget &> /dev/null; then
        if wget -q --timeout=15 "$url" -O "$dest" 2>/dev/null; then
            success=true
        fi
    fi
    
    if [ "$success" = false ]; then
        echo "  [!] Failed: ${repo_name}"
        echo "      URL: ${url}"
        return 1
    fi
}

echo "[*] Downloading files..."

# Root files
echo "  [↓] main.py"
curl -fsSL --connect-timeout 15 "${RAW_URL}/main.py" -o "${INSTALL_DIR}/main.py" 2>/dev/null || \
    wget -q --timeout=15 "${RAW_URL}/main.py" -O "${INSTALL_DIR}/main.py"

echo "  [↓] requirements.txt"
curl -fsSL --connect-timeout 15 "${RAW_URL}/requirements.txt" -o "${INSTALL_DIR}/requirements.txt" 2>/dev/null || \
    wget -q --timeout=15 "${RAW_URL}/requirements.txt" -O "${INSTALL_DIR}/requirements.txt"

# Core files - using ACTUAL repo filenames
download_file "_init_.py" "core" "__init__.py"
download_file "hardware_probe.py" "core" "hardware_probe.py"
download_file "neural_sensitivity.py" "core" "neural_sensitivity.py"
download_file "quantum_calculator.py" "core" "quantum_calculator.py"
download_file "molecular_valence.py" "core" "molecular_valence.py"
download_file "aim_analytics.py" "core" "aim_analytics.py"

# Weapon database - handles the SPACE in filename!
download_file "weapon _database.py" "core" "weapon_database.py"

# Interface files
download_file "molecular_cli.py" "interface" "molecular_cli.py"
download_file "neural_gui.py" "interface" "neural_gui.py"
download_file "hybrid_controller.py" "interface" "hybrid_controller.py"

# Utils files
download_file "validator.py" "utils" "validator.py"
download_file "logger.py" "utils" "logger.py"
download_file "biometric_bridge.py" "utils" "biometric_bridge.py"
download_file "cloud_sync.py" "utils" "cloud_sync.py"
download_file "auto_updater.py" "utils" "auto_updater.py"
download_file "termux_adapter.py" "utils" "termux_adapter.py"
download_file "crypto_store.py" "utils" "crypto_store.py"

# Config files
download_file "atoms.json" "config" "atoms.json"
download_file "bonds.json" "config" "bonds.json"

# Optional files (don't fail if missing)
download_file "dynamic_calculator.py" "core" "dynamic_calculator.py" || true

# Create __init__.py files for empty folders if they don't exist
touch "$INSTALL_DIR/interface/__init__.py"
touch "$INSTALL_DIR/utils/__init__.py"
touch "$INSTALL_DIR/config/__init__.py"

# Version file
echo "$VERSION" > "$INSTALL_DIR/.version"

# Install dependencies
echo "[*] Installing dependencies..."
pip3 install --user -r "$INSTALL_DIR/requirements.txt" 2>/dev/null || \
    pip3 install -r "$INSTALL_DIR/requirements.txt" 2>/dev/null || \
    pip3 install --user numpy rich prompt_toolkit 2>/dev/null || \
    pip3 install numpy rich prompt_toolkit 2>/dev/null || \
    echo "[!] pip install failed, continuing..."

# Create launcher
echo "[*] Creating launcher..."
cat > "$BIN_DIR/symbiote" << 'EOF'
#!/bin/bash
export PYTHONPATH="$HOME/.symbiote:$PYTHONPATH"
cd "$HOME/.symbiote"
python3 main.py "$@"
EOF
chmod +x "$BIN_DIR/symbiote"

# Create updater
cat > "$BIN_DIR/symbiote-update" << EOF
#!/bin/bash
curl -fsSL ${RAW_URL}/install.sh | bash
EOF
chmod +x "$BIN_DIR/symbiote-update"

# Create uninstaller
cat > "$BIN_DIR/symbiote-uninstall" << 'EOF'
#!/bin/bash
INSTALL_DIR="$HOME/.symbiote"
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "[✓] Removed $INSTALL_DIR"
fi
rm -f "$PREFIX/bin/symbiote" "$PREFIX/bin/symbiote-update" "$PREFIX/bin/symbiote-uninstall" 2>/dev/null
rm -f "$HOME/.local/bin/symbiote" "$HOME/.local/bin/symbiote-update" "$HOME/.local/bin/symbiote-uninstall" 2>/dev/null
echo "[✓] Symbiote removed"
EOF
chmod +x "$BIN_DIR/symbiote-uninstall"

echo ""
echo "[✓] Installation complete!"
echo ""
echo "Usage:"
echo "  symbiote           - Launch Symbiote"
echo "  symbiote-update    - Update to latest version"
echo "  symbiote-uninstall - Remove Symbiote"
echo ""#!/bin/bash
# Symbiote v3.0.0 Installer
# Repo: dragon-X1234/symbiotic-wave
# FIXED: Now matches actual repo filenames

set -e

REPO_OWNER="dragon-X1234"
REPO_NAME="symbiotic-wave"
RAW_URL="https://raw.githubusercontent.com/${REPO_OWNER}/${REPO_NAME}/main"
VERSION="3.0.0"

echo "🔥 Symbiote v${VERSION} Installation"
echo "============================="

# Detect Termux
if [[ "$PREFIX" == *"com.termux"* ]]; then
    INSTALL_DIR="$HOME/.symbiote"
    BIN_DIR="$PREFIX/bin"
    echo "[✓] Termux detected"
else
    INSTALL_DIR="$HOME/.local/share/symbiote"
    BIN_DIR="$HOME/.local/bin"
    mkdir -p "$BIN_DIR"
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[!] Python3 not found"
    if [[ "$PREFIX" == *"com.termux"* ]]; then
        echo "[*] Installing Python..."
        pkg update -y && pkg install python -y
    else
        echo "[!] Please install Python3 manually"
        exit 1
    fi
fi

# Create directories
echo "[*] Creating directories..."
mkdir -p "$INSTALL_DIR"/{core,interface,utils,config}

# Download function with URL encoding for spaces
download_file() {
    local repo_name="$1"
    local dest_folder="$2"
    local dest_name="$3"
    
    # URL encode spaces for the URL
    local encoded_name=$(printf '%s' "$repo_name" | sed 's/ /%20/g')
    local url="${RAW_URL}/${encoded_name}"
    local dest="${INSTALL_DIR}/${dest_folder}/${dest_name}"
    
    echo "  [↓] ${repo_name} → ${dest_folder}/${dest_name}"
    
    local success=false
    
    if command -v curl &> /dev/null; then
        if curl -fsSL --connect-timeout 15 "$url" -o "$dest" 2>/dev/null; then
            success=true
        fi
    elif command -v wget &> /dev/null; then
        if wget -q --timeout=15 "$url" -O "$dest" 2>/dev/null; then
            success=true
        fi
    fi
    
    if [ "$success" = false ]; then
        echo "  [!] Failed: ${repo_name}"
        echo "      URL: ${url}"
        return 1
    fi
}

echo "[*] Downloading files..."

# Root files
echo "  [↓] main.py"
curl -fsSL --connect-timeout 15 "${RAW_URL}/main.py" -o "${INSTALL_DIR}/main.py" 2>/dev/null || \
    wget -q --timeout=15 "${RAW_URL}/main.py" -O "${INSTALL_DIR}/main.py"

echo "  [↓] requirements.txt"
curl -fsSL --connect-timeout 15 "${RAW_URL}/requirements.txt" -o "${INSTALL_DIR}/requirements.txt" 2>/dev/null || \
    wget -q --timeout=15 "${RAW_URL}/requirements.txt" -O "${INSTALL_DIR}/requirements.txt"

# Core files - using ACTUAL repo filenames
download_file "_init_.py" "core" "__init__.py"
download_file "hardware_probe.py" "core" "hardware_probe.py"
download_file "neural_sensitivity.py" "core" "neural_sensitivity.py"
download_file "quantum_calculator.py" "core" "quantum_calculator.py"
download_file "molecular_valence.py" "core" "molecular_valence.py"
download_file "aim_analytics.py" "core" "aim_analytics.py"

# Weapon database - handles the SPACE in filename!
download_file "weapon _database.py" "core" "weapon_database.py"

# Interface files
download_file "molecular_cli.py" "interface" "molecular_cli.py"
download_file "neural_gui.py" "interface" "neural_gui.py"
download_file "hybrid_controller.py" "interface" "hybrid_controller.py"

# Utils files
download_file "validator.py" "utils" "validator.py"
download_file "logger.py" "utils" "logger.py"
download_file "biometric_bridge.py" "utils" "biometric_bridge.py"
download_file "cloud_sync.py" "utils" "cloud_sync.py"
download_file "auto_updater.py" "utils" "auto_updater.py"
download_file "termux_adapter.py" "utils" "termux_adapter.py"
download_file "crypto_store.py" "utils" "crypto_store.py"

# Config files
download_file "atoms.json" "config" "atoms.json"
download_file "bonds.json" "config" "bonds.json"

# Optional files (don't fail if missing)
download_file "dynamic_calculator.py" "core" "dynamic_calculator.py" || true

# Create __init__.py files for empty folders if they don't exist
touch "$INSTALL_DIR/interface/__init__.py"
touch "$INSTALL_DIR/utils/__init__.py"
touch "$INSTALL_DIR/config/__init__.py"

# Version file
echo "$VERSION" > "$INSTALL_DIR/.version"

# Install dependencies
echo "[*] Installing dependencies..."
pip3 install --user -r "$INSTALL_DIR/requirements.txt" 2>/dev/null || \
    pip3 install -r "$INSTALL_DIR/requirements.txt" 2>/dev/null || \
    pip3 install --user numpy rich prompt_toolkit 2>/dev/null || \
    pip3 install numpy rich prompt_toolkit 2>/dev/null || \
    echo "[!] pip install failed, continuing..."

# Create launcher
echo "[*] Creating launcher..."
cat > "$BIN_DIR/symbiote" << 'EOF'
#!/bin/bash
export PYTHONPATH="$HOME/.symbiote:$PYTHONPATH"
cd "$HOME/.symbiote"
python3 main.py "$@"
EOF
chmod +x "$BIN_DIR/symbiote"

# Create updater
cat > "$BIN_DIR/symbiote-update" << EOF
#!/bin/bash
curl -fsSL ${RAW_URL}/install.sh | bash
EOF
chmod +x "$BIN_DIR/symbiote-update"

# Create uninstaller
cat > "$BIN_DIR/symbiote-uninstall" << 'EOF'
#!/bin/bash
INSTALL_DIR="$HOME/.symbiote"
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "[✓] Removed $INSTALL_DIR"
fi
rm -f "$PREFIX/bin/symbiote" "$PREFIX/bin/symbiote-update" "$PREFIX/bin/symbiote-uninstall" 2>/dev/null
rm -f "$HOME/.local/bin/symbiote" "$HOME/.local/bin/symbiote-update" "$HOME/.local/bin/symbiote-uninstall" 2>/dev/null
echo "[✓] Symbiote removed"
EOF
chmod +x "$BIN_DIR/symbiote-uninstall"

echo ""
echo "[✓] Installation complete!"
echo ""
echo "Usage:"
echo "  symbiote           - Launch Symbiote"
echo "  symbiote-update    - Update to latest version"
echo "  symbiote-uninstall - Remove Symbiote"
echo ""
