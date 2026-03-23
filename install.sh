#!/bin/bash
# Symbiote v3.0.1 Installer
# Repo: dragon-X1234/symbiotic-wave

set -e

REPO_OWNER="dragon-X1234"
REPO_NAME="symbiotic-wave"
RAW_URL="https://raw.githubusercontent.com/${REPO_OWNER}/${REPO_NAME}/main"
VERSION="3.0.1"

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

# --- Environment & Dependency Fix ---
if [[ "$PREFIX" == *"com.termux"* ]]; then
    INSTALL_DIR="$HOME/.symbiote"
    BIN_DIR="$PREFIX/bin"
    ui_log "Termux detected. Applying compilation fixes..."
    # This prevents the "Installing backend dependencies" hang
    pkg update -y
    pkg install python build-essential binutils python-numpy -y
    ui_success "Build tools & pre-compiled Numpy ready"
else
    INSTALL_DIR="$HOME/.local/share/symbiote"
    BIN_DIR="$HOME/.local/bin"
    mkdir -p "$BIN_DIR"
    ui_log "Standard Linux detected. Checking Python3..."
    if ! command -v python3 &> /dev/null; then
        ui_err "Python3 not found. Please install it manually."
        exit 1
    fi
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
    local dest="${INSTALL_DIR}/${dest_folder}/${dest_name}"
    
    # Handle root folder mapping
    if [ "$dest_folder" = "root" ]; then dest="${INSTALL_DIR}/${dest_name}"; fi
    
    ui_dl "${dest_name}"
    
    if command -v curl &> /dev/null; then
        curl -fsSL --connect-timeout 15 "$url" -o "$dest" 2>/dev/null || true
    else
        wget -q --timeout=15 "$url" -O "$dest" 2>/dev/null || true
    fi
}

ui_log "Downloading repository assets..."
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

# --- Finalizing Pip ---
ui_log "Finalizing Python requirements..."
# We use --no-deps if numpy is already installed to speed it up
pip3 install --user -r "$INSTALL_DIR/requirements.txt" 2>/dev/null || \
pip3 install -r "$INSTALL_DIR/requirements.txt" 2>/dev/null

# --- Launcher ---
cat > "$BIN_DIR/symbiote" << EOF
#!/bin/bash
export PYTHONPATH="${INSTALL_DIR}:\$PYTHONPATH"
cd "${INSTALL_DIR}"
python3 main.py "\$@"
EOF
chmod +x "$BIN_DIR/symbiote"

ui_success "Installation complete!"
draw_footer
