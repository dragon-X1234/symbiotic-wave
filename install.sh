#!/bin/bash
# Symbiote v3.0 Installer
# Repo: dragon-X1234/symbiotic-wave

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
        pkg update -y && pkg install python -y
    else
        exit 1
    fi
fi

# Create directories
echo "[*] Creating directories..."
mkdir -p "$INSTALL_DIR"/{core,interface,utils,config}

# Download function
download_file() {
    local flat_name="$1"
    local dest_folder="$2"
    local dest_name="$3"
    local url="${RAW_URL}/${flat_name}"
    local dest="${INSTALL_DIR}/${dest_folder}/${dest_name}"
    
    if command -v curl &> /dev/null; then
        curl -fsSL "$url" -o "$dest" || {
            echo "[!] Failed: ${flat_name}"
            return 1
        }
    else
        wget -q "$url" -O "$dest" || {
            echo "[!] Failed: ${flat_name}"
            return 1
        }
    fi
}

# Download all 29 files
echo "[*] Downloading files..."

# Root files
echo "  [↓] main.py"
curl -fsSL "${RAW_URL}/main.py" -o "${INSTALL_DIR}/main.py" 2>/dev/null || wget -q "${RAW_URL}/main.py" -O "${INSTALL_DIR}/main.py"

echo "  [↓] requirements.txt"
curl -fsSL "${RAW_URL}/requirements.txt" -o "${INSTALL_DIR}/requirements.txt" 2>/dev/null || wget -q "${RAW_URL}/requirements.txt" -O "${INSTALL_DIR}/requirements.txt"

# Core (7 files)
download_file "core___init__.py" "core" "__init__.py"
download_file "core___hardware_probe.py" "core" "hardware_probe.py"
download_file "core___neural_sensitivity.py" "core" "neural_sensitivity.py"
download_file "core___quantum_calculator.py" "core" "quantum_calculator.py"
download_file "core___molecular_valence.py" "core" "molecular_valence.py"
download_file "core___weapon_database.py" "core" "weapon_database.py"
download_file "core___aim_analytics.py" "core" "aim_analytics.py"

# Interface (4 files)
download_file "interface___init__.py" "interface" "__init__.py"
download_file "interface___molecular_cli.py" "interface" "molecular_cli.py"
download_file "interface___neural_gui.py" "interface" "neural_gui.py"
download_file "interface___hybrid_controller.py" "interface" "hybrid_controller.py"

# Utils (8 files)
download_file "utils___init__.py" "utils" "__init__.py"
download_file "utils___validator.py" "utils" "validator.py"
download_file "utils___logger.py" "utils" "logger.py"
download_file "utils___biometric_bridge.py" "utils" "biometric_bridge.py"
download_file "utils___cloud_sync.py" "utils" "cloud_sync.py"
download_file "utils___auto_updater.py" "utils" "auto_updater.py"
download_file "utils___termux_adapter.py" "utils" "termux_adapter.py"
download_file "utils___crypto_store.py" "utils" "crypto_store.py"

# Config (3 files)
download_file "config___init__.py" "config" "__init__.py"
download_file "config___atoms.json" "config" "atoms.json"
download_file "config___bonds.json" "config" "bonds.json"

# Version file
echo "$VERSION" > "$INSTALL_DIR/.version"

# Install dependencies
echo "[*] Installing dependencies..."
pip3 install --user numpy rich 2>/dev/null || pip3 install numpy rich 2>/dev/null || echo "[!] pip install failed, continuing..."

# Create launcher
echo "[*] Creating launcher..."
echo '#!/bin/bash
export PYTHONPATH="$HOME/.symbiote:$PYTHONPATH"
cd "$HOME/.symbiote"
python3 main.py "$@"' > "$BIN_DIR/symbiote"

chmod +x "$BIN_DIR/symbiote"

# Create updater
echo "#!/bin/bash
curl -fsSL ${RAW_URL}/install.sh | bash" > "$BIN_DIR/symbiote-update"
chmod +x "$BIN_DIR/symbiote-update"

# Create uninstaller
echo '#!/bin/bash
rm -rf "$HOME/.symbiote"
rm -f "$PREFIX/bin/symbiote" "$PREFIX/bin/symbiote-update" 2>/dev/null
rm -f "$HOME/.local/bin/symbiote" "$HOME/.local/bin/symbiote-update" 2>/dev/null
echo "[✓] Symbiote removed"' > "$BIN_DIR/symbiote-uninstall"
chmod +x "$BIN_DIR/symbiote-uninstall"

echo "[✓] Installation complete!"
echo ""
echo "Run: symbiote"
