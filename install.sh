#!/bin/bash
# Symbiote v3.0.0 Installer
# Repo: dragon-X1234/symbiotic-wave

set -e

REPO_OWNER="dragon-X1234"
REPO_NAME="symbiotic-wave"
RAW_URL="https://raw.githubusercontent.com/${REPO_OWNER}/${REPO_NAME}/main"
VERSION="3.0.0"

# --- ImGui-Style UI Theme ---
C_BLUE="\e[38;5;39m"
C_GRAY="\e[38;5;244m"
C_GREEN="\e[38;5;40m"
C_RED="\e[38;5;196m"
C_WHITE="\e[1;37m"
C_RESET="\e[0m"

draw_header() {
    clear
    echo -e "${C_BLUE}╭────────────────────────────────────────────────────────╮${C_RESET}"
    echo -e "${C_BLUE}│${C_WHITE}  🔥 Symbiote v${VERSION} Installer                          ${C_BLUE}│${C_RESET}"
    echo -e "${C_BLUE}├────────────────────────────────────────────────────────┤${C_RESET}"
}

ui_log() { echo -e "${C_BLUE}│${C_GRAY}  [*] $1${C_RESET}"; }
ui_success() { echo -e "${C_BLUE}│${C_GREEN}  [✓] $1${C_RESET}"; }
ui_err() { echo -e "${C_BLUE}│${C_RED}  [!] $1${C_RESET}"; }
ui_dl() { echo -e "${C_BLUE}│${C_GRAY}      ↳ $1${C_RESET}"; }

draw_footer() {
    echo -e "${C_BLUE}╰────────────────────────────────────────────────────────╯${C_RESET}"
}

draw_header

# --- Environment Detection ---
ui_log "Checking runtime environment..."
if [[ "$PREFIX" == *"com.termux"* ]]; then
    INSTALL_DIR="$HOME/.symbiote"
    BIN_DIR="$PREFIX/bin"
    ui_success "Termux environment detected"
else
    INSTALL_DIR="$HOME/.local/share/symbiote"
    BIN_DIR="$HOME/.local/bin"
    mkdir -p "$BIN_DIR"
    ui_success "Standard Linux environment detected"
fi

# --- Python Check ---
ui_log "Verifying dependencies..."
if ! command -v python3 &> /dev/null; then
    ui_err "Python3 not found"
    if [[ "$PREFIX" == *"com.termux"* ]]; then
        ui_log "Installing Python3 via pkg..."
        pkg update -y && pkg install python -y
    else
        ui_err "Please install Python3 manually and restart."
        draw_footer
        exit 1
    fi
else
    ui_success "Python3 is installed"
fi

# --- Directory Creation ---
ui_log "Structuring core directories..."
mkdir -p "$INSTALL_DIR"/{core,interface,utils,config}
touch "$INSTALL_DIR/interface/__init__.py"
touch "$INSTALL_DIR/utils/__init__.py"
touch "$INSTALL_DIR/config/__init__.py"
echo "$VERSION" > "$INSTALL_DIR/.version"

# --- Download Engine ---
download_file() {
    local repo_name="$1"
    local dest_folder="$2"
    local dest_name="$3"
    local optional="$4"
    
    local encoded_name=$(printf '%s' "$repo_name" | sed 's/ /%20/g')
    local url="${RAW_URL}/${encoded_name}"
    
    # Handle root folder mapping
    local dest=""
    if [ "$dest_folder" = "root" ]; then
        dest="${INSTALL_DIR}/${dest_name}"
    else
        dest="${INSTALL_DIR}/${dest_folder}/${dest_name}"
    fi
    
    ui_dl "${dest_name}"
    
    local success=false
    if command -v curl &> /dev/null; then
        if curl -fsSL --connect-timeout 15 "$url" -o "$dest" 2>/dev/null; then success=true; fi
    elif command -v wget &> /dev/null; then
        if wget -q --timeout=15 "$url" -O "$dest" 2>/dev/null; then success=true; fi
    fi
    
    if [ "$success" = false ] && [ "$optional" != "true" ]; then
        ui_err "Failed to download: ${repo_name}"
        draw_footer
        exit 1
    fi
}

ui_log "Downloading repository assets..."

# Array mapping: "Repo_Filename|Target_Folder|Target_Filename|Optional"
files=(
    "main.py|root|main.py|false"
    "requirements.txt|root|requirements.txt|false"
    "_init_.py|core|__init__.py|false"
    "hardware_probe.py|core|hardware_probe.py|false"
    "neural_sensitivity.py|core|neural_sensitivity.py|false"
    "quantum_calculator.py|core|quantum_calculator.py|false"
    "molecular_valence.py|core|molecular_valence.py|false"
    "aim_analytics.py|core|aim_analytics.py|false"
    "weapon _database.py|core|weapon_database.py|false"
    "dynamic_calculator.py|core|dynamic_calculator.py|true"
    "molecular_cli.py|interface|molecular_cli.py|false"
    "neural_gui.py|interface|neural_gui.py|false"
    "hybrid_controller.py|interface|hybrid_controller.py|false"
    "validator.py|utils|validator.py|false"
    "logger.py|utils|logger.py|false"
    "biometric_bridge.py|utils|biometric_bridge.py|false"
    "cloud_sync.py|utils|cloud_sync.py|false"
    "auto_updater.py|utils|auto_updater.py|false"
    "termux_adapter.py|utils|termux_adapter.py|false"
    "crypto_store.py|utils|crypto_store.py|false"
    "atoms.json|config|atoms.json|false"
    "bonds.json|config|bonds.json|false"
)

for file_data in "${files[@]}"; do
    IFS="|" read -r r_name t_folder t_name optional <<< "$file_data"
    download_file "$r_name" "$t_folder" "$t_name" "$optional"
done

ui_success "All assets downloaded"

# --- Dependencies ---
ui_log "Installing PIP dependencies..."
if pip3 install --user -r "$INSTALL_DIR/requirements.txt" 2>/dev/null || \
   pip3 install -r "$INSTALL_DIR/requirements.txt" 2>/dev/null; then
    ui_success "Requirements installed"
else
    ui_err "Standard pip install failed, attempting fallback..."
    pip3 install numpy rich prompt_toolkit 2>/dev/null || ui_err "Fallback pip failed (continuing anyway)"
fi

# --- Launchers ---
ui_log "Configuring executable hooks..."

cat > "$BIN_DIR/symbiote" << EOF
#!/bin/bash
export PYTHONPATH="${INSTALL_DIR}:\$PYTHONPATH"
cd "${INSTALL_DIR}"
python3 main.py "\$@"
EOF
chmod +x "$BIN_DIR/symbiote"

cat > "$BIN_DIR/symbiote-update" << EOF
#!/bin/bash
curl -fsSL ${RAW_URL}/install.sh | bash
EOF
chmod +x "$BIN_DIR/symbiote-update"

ui_success "Installation fully complete."
draw_footer

echo -e "\n${C_GREEN}▶ Quick Commands:${C_RESET}"
echo -e "  ${C_WHITE}symbiote${C_GRAY}        - Launch the Symbiote Interface${C_RESET}"
echo -e "  ${C_WHITE}symbiote-update${C_GRAY} - Pull latest updates from cloud${C_RESET}\n"
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
