#!/bin/bash
# Symbiote v3.1.3 "Evo" Installer
# Repo: dragon-X1234/symbiotic-wave

set -e

REPO_OWNER="dragon-X1234"
REPO_NAME="symbiotic-wave"
RAW_URL="https://raw.githubusercontent.com/${REPO_OWNER}/${REPO_NAME}/main"
VERSION="3.1.3"

# --- ImGui "Evo" UI Theme ---
C_BLUE="\e[38;5;33m"
C_CYAN="\e[38;5;51m"
C_GRAY="\e[38;5;241m"
C_DGRAY="\e[38;5;236m"
C_GREEN="\e[38;5;82m"
C_RED="\e[38;5;196m"
C_WHITE="\e[1;37m"
C_RESET="\e[0m"

# UI Helpers
draw_header() {
    clear
    echo -e "${C_BLUE}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓${C_RESET}"
    echo -e "${C_BLUE}┃${C_WHITE}  🧬 SYMBIOTE WAVE ${C_CYAN}v${VERSION}${C_WHITE} | ${C_GREEN}EVOLUTION ENGINE${C_BLUE}     ┃${C_RESET}"
    echo -e "${C_BLUE}┠────────────────────────────────────────────────────────┨${C_RESET}"
}

ui_step() { echo -e "${C_BLUE}┃${C_WHITE} [$1/${MAX_STEPS}]${C_CYAN} $2${C_RESET}"; }
ui_log()  { echo -e "${C_BLUE}┃${C_GRAY}        » $1${C_RESET}"; }
ui_dl()   { echo -ne "${C_BLUE}┃${C_DGRAY}          ↓ $1... \r${C_RESET}"; }
ui_ok()   { echo -e "${C_BLUE}┃${C_GREEN}        ✓ $1${C_RESET}"; }
ui_err()  { echo -e "${C_BLUE}┃${C_RED}        ✖ $1${C_RESET}"; }

draw_footer() {
    echo -e "${C_BLUE}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛${C_RESET}"
}

MAX_STEPS=5
draw_header

# --- Step 1: Environment Logic ---
ui_step 1 "Environment Diagnostics"
if [[ "$PREFIX" == *"com.termux"* ]]; then
    INSTALL_DIR="$HOME/.symbiote"
    BIN_DIR="$PREFIX/bin"
    ui_log "Platform: Termux (Android)"
    
    ui_log "Synchronizing mirrors..."
    pkg update -y
    pkg install termux-tools tur-repo -y || true
    pkg update -y
    
    ui_log "Installing binary algebra & GUI backends..."
    # Added python-tkinter for customtkinter support
    pkg install python build-essential binutils libopenblas python-numpy python-scikit-learn python-pillow python-tkinter -y
    ui_ok "Termux environment stabilized"
else
    INSTALL_DIR="$HOME/.local/share/symbiote"
    BIN_DIR="$HOME/.local/bin"
    mkdir -p "$BIN_DIR"
    ui_log "Platform: Standard Linux"
    if ! command -v python3 &> /dev/null; then
        ui_err "Python3 Missing"
        draw_footer
        exit 1
    fi
fi

# --- Step 2: Architecture ---
ui_step 2 "Virtualizing Directory Structure"
mkdir -p "$INSTALL_DIR"/{core,interface,utils,config}
# Ensure package capability
for dir in core interface utils config; do
    touch "$INSTALL_DIR/$dir/__init__.py"
done
echo "$VERSION" > "$INSTALL_DIR/.version"
ui_ok "Filesystem initialized at $INSTALL_DIR"

# --- Step 3: Deployment ---
ui_step 3 "Fetching Remote Assets"
download_file() {
    local r_name="$1"
    local t_folder="$2"
    local t_name="$3"
    
    local encoded_name=$(printf '%s' "$r_name" | sed 's/ /%20/g')
    local url="${RAW_URL}/${encoded_name}"
    local dest="${INSTALL_DIR}/${t_folder}/${t_name}"
    if [ "$t_folder" = "root" ]; then dest="${INSTALL_DIR}/${t_name}"; fi
    
    ui_dl "$t_name"
    
    if command -v curl &> /dev/null; then
        curl -fsSL --connect-timeout 10 "$url" -o "$dest" 2>/dev/null || true
    else
        wget -q --timeout=10 "$url" -O "$dest" 2>/dev/null || true
    fi
}

files=(
    "main.py|root|main.py"
    "requirements.txt|root|requirements.txt"
    "_init_.py|core|__init__.py"
    "hardware_probe.py|core|hardware_probe.py"
    "neural_sensitivity.py|core|neural_sensitivity.py"
    "quantum_calculator.py|core|quantum_calculator.py"
    "molecular_valence.py|core|molecular_valence.py"
    "aim_analytics.py|core|aim_analytics.py"
    "weapon _database.py|core|weapon_database.py"
    "molecular_cli.py|interface|molecular_cli.py"
    "neural_gui.py|interface|neural_gui.py"
    "hybrid_controller.py|interface|hybrid_controller.py"
    "validator.py|utils|validator.py"
    "logger.py|utils|logger.py"
    "biometric_bridge.py|utils|biometric_bridge.py"
    "cloud_sync.py|utils|cloud_sync.py"
    "auto_updater.py|utils|auto_updater.py"
    "termux_adapter.py|utils|termux_adapter.py"
    "crypto_store.py|utils|crypto_store.py"
    "atoms.json|config|atoms.json"
    "bonds.json|config|bonds.json"
)

for file_data in "${files[@]}"; do
    IFS="|" read -r r_name t_folder t_name <<< "$file_data"
    download_file "$r_name" "$t_folder" "$t_name"
done
echo -e "\n"
ui_ok "Source code synchronized"

# --- Step 4: Neural Mapping ---
ui_step 4 "Binding Neural Dependencies"
ui_log "Finalizing Python modules..."
# Added --break-system-packages for PEP 668 compatibility and --no-cache-dir to save space
PIP_CMD="pip3 install --user --prefer-binary --no-cache-dir --break-system-packages"
$PIP_CMD -r "$INSTALL_DIR/requirements.txt" 2>/dev/null || \
pip3 install --prefer-binary -r "$INSTALL_DIR/requirements.txt" 2>/dev/null || true
ui_ok "Neural environment compiled"

# --- Step 5: Integration ---
ui_step 5 "Injecting Execution Hooks"
cat > "$BIN_DIR/symbiote" << EOF
#!/bin/bash
export PYTHONPATH="${INSTALL_DIR}:\$PYTHONPATH"
export TERMUX_VERSION="${VERSION}"
# Fix for GUI apps in some Termux setups
export DISPLAY=:0 2>/dev/null || true 
cd "${INSTALL_DIR}"
python3 main.py "\$@"
EOF
chmod +x "$BIN_DIR/symbiote"

# Path Check & Fix
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    ui_log "Patching PATH variable..."
    SHELL_CONFIG="$HOME/.bashrc"
    [ -f "$HOME/.zshrc" ] && SHELL_CONFIG="$HOME/.zshrc"
    echo "export PATH=\"\$PATH:$BIN_DIR\"" >> "$SHELL_CONFIG"
    # Execute immediately for current session
    export PATH="$PATH:$BIN_DIR"
fi

ui_ok "Symbiote bridge established"
draw_footer

echo -e "\n${C_CYAN}SYSTEM READY.${C_RESET}"
echo -e "${C_WHITE}Type '${C_GREEN}symbiote${C_WHITE}' to initialize.${C_RESET}"
echo -e "${C_GRAY}(Note: If command not found, restart Termux or type 'source ~/.bashrc')${C_RESET}\n"
