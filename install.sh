#!/bin/bash
# Symbiote v3.1.3 "Evo" Installer - FIXED VERSION
# Repo: dragon-X1234/symbiotic-wave

set -e

REPO_OWNER="dragon-X1234"
REPO_NAME="symbiotic-wave"
RAW_URL="https://raw.githubusercontent.com/${REPO_OWNER}/${REPO_NAME}/main"
VERSION="3.1.3"

# Colors
C_BLUE="\e[38;5;33m"
C_CYAN="\e[38;5;51m"
C_GRAY="\e[38;5;241m"
C_GREEN="\e[38;5;82m"
C_RED="\e[38;5;196m"
C_WHITE="\e[1;37m"
C_RESET="\e[0m"
C_YELLOW="\e[38;5;220m"

# UI Helpers
draw_header() {
    clear 2>/dev/null || true
    echo -e "${C_BLUE}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓${C_RESET}"
    echo -e "${C_BLUE}┃${C_WHITE}  🧬 SYMBIOTE WAVE ${C_CYAN}v${VERSION}${C_WHITE} | ${C_GREEN}EVOLUTION ENGINE${C_BLUE}     ┃${C_RESET}"
    echo -e "${C_BLUE}┠────────────────────────────────────────────────────────┨${C_RESET}"
}

ui_step() { echo -e "${C_BLUE}┃${C_WHITE} [$1/${MAX_STEPS}]${C_CYAN} $2${C_RESET}"; }
ui_log()  { echo -e "${C_BLUE}┃${C_GRAY}        » $1${C_RESET}"; }
ui_dl()   { echo -ne "${C_BLUE}┃${C_DGRAY}          ↓ $1... \r${C_RESET}"; }
ui_ok()   { echo -e "${C_BLUE}┃${C_GREEN}        ✓ $1${C_RESET}"; }
ui_err()  { echo -e "${C_BLUE}┃${C_RED}        ✖ $1${C_RESET}"; }
ui_warn() { echo -e "${C_BLUE}┃${C_YELLOW}        ⚠ $1${C_RESET}"; }

draw_footer() {
    echo -e "${C_BLUE}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛${C_RESET}"
}

MAX_STEPS=6
draw_header

# --- Step 1: Environment Setup ---
ui_step 1 "Environment Diagnostics"
IS_TERMUX=false
if [[ "$PREFIX" == *"com.termux"* ]] || [[ -d "/data/data/com.termux" ]]; then
    IS_TERMUX=true
    INSTALL_DIR="$HOME/.symbiote"
    BIN_DIR="$PREFIX/bin"
    ui_log "Platform: Termux (Android)"
    
    ui_log "Updating package lists..."
    pkg update -y || true
    
    ui_log "Installing system dependencies..."
    # Install essential build tools and libraries
    pkg install -y \
        python \
        python-pip \
        build-essential \
        cmake \
        ninja \
        libffi \
        openssl \
        libxml2 \
        libxslt \
        libpng \
        libjpeg-turbo \
        freetype \
        libopenblas \
        lapack \
        fftw \
        libzmq \
        libcrypt \
        git \
        wget \
        curl \
        2>/dev/null || true
    
    ui_ok "Termux packages installed"
else
    INSTALL_DIR="$HOME/.local/share/symbiote"
    BIN_DIR="$HOME/.local/bin"
    mkdir -p "$BIN_DIR"
    ui_log "Platform: Standard Linux"
    
    if ! command -v python3 &> /dev/null; then
        ui_err "Python3 not found. Please install Python 3.8+"
        draw_footer
        exit 1
    fi
fi

# Ensure directories exist
mkdir -p "$INSTALL_DIR"/{core,interface,utils,config}

# --- Step 2: Download Files ---
ui_step 2 "Downloading Source Files"

download_file() {
    local r_name="$1"
    local t_folder="$2"
    local t_name="$3"
    
    local encoded_name=$(printf '%s' "$r_name" | sed 's/ /%20/g')
    local url="${RAW_URL}/${encoded_name}"
    local dest
    
    if [ "$t_folder" = "root" ]; then
        dest="${INSTALL_DIR}/${t_name}"
    else
        dest="${INSTALL_DIR}/${t_folder}/${t_name}"
    fi
    
    ui_dl "$t_name"
    
    local success=false
    local retries=3
    
    while [ $retries -gt 0 ]; do
        if command -v curl &> /dev/null; then
            if curl -fsSL --connect-timeout 15 --max-time 30 "$url" -o "$dest" 2>/dev/null; then
                if [ -s "$dest" ]; then
                    success=true
                    break
                fi
            fi
        elif command -v wget &> /dev/null; then
            if wget -q --timeout=15 "$url" -O "$dest" 2>/dev/null; then
                if [ -s "$dest" ]; then
                    success=true
                    break
                fi
            fi
        fi
        retries=$((retries - 1))
        sleep 1
    done
    
    if [ "$success" = false ]; then
        ui_err "Failed: $r_name"
        # Create placeholder to prevent crashes
        touch "$dest" 2>/dev/null || true
        return 1
    fi
    return 0
}

# File list: repo_name|folder|local_name
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

failed_downloads=0
for file_data in "${files[@]}"; do
    IFS="|" read -r r_name t_folder t_name <<< "$file_data"
    if ! download_file "$r_name" "$t_folder" "$t_name"; then
        ((failed_downloads++)) || true
    fi
done

echo -e "\n"
if [ $failed_downloads -eq 0 ]; then
    ui_ok "All files downloaded successfully"
else
    ui_warn "$failed_downloads files failed (check your repo)"
fi

# Create __init__.py files
for dir in core interface utils config; do
    touch "$INSTALL_DIR/$dir/__init__.py"
done
echo "$VERSION" > "$INSTALL_DIR/.version"

# --- Step 3: Fix Requirements ---
ui_step 3 "Preparing Dependencies"

# Create a working requirements.txt with available packages
cat > "$INSTALL_DIR/requirements.txt" << 'REQEOF'
# Core dependencies - stable versions for Termux
numpy>=1.21.0,<1.25.0
Pillow>=9.0.0
rich>=13.0.0
prompt-toolkit>=3.0.0
requests>=2.28.0
pycryptodome>=3.15.0
REQEOF

ui_ok "Requirements file created"

# --- Step 4: Install Python Dependencies ---
ui_step 4 "Installing Python Packages (This may take 5-10 minutes)"

# Upgrade pip first
ui_log "Upgrading pip..."
python3 -m pip install --upgrade pip --user 2>/dev/null || \
python3 -m pip install --upgrade pip 2>/dev/null || true

# Install packages one by one with error handling
install_pkg() {
    local pkg="$1"
    ui_log "Installing $pkg..."
    
    # Try multiple methods
    if python3 -m pip install --user --no-cache-dir "$pkg" 2>/dev/null; then
        return 0
    elif python3 -m pip install --no-cache-dir "$pkg" 2>/dev/null; then
        return 0
    elif pip3 install --user --no-cache-dir "$pkg" 2>/dev/null; then
        return 0
    else
        return 1
    fi
}

# Essential packages
packages=("numpy" "Pillow" "rich" "prompt-toolkit" "requests" "pycryptodome")
failed_pkgs=()

for pkg in "${packages[@]}"; do
    if ! install_pkg "$pkg"; then
        failed_pkgs+=("$pkg")
        ui_err "Failed: $pkg"
    else
        ui_ok "Installed: $pkg"
    fi
done

# Try alternative for failed packages
if [ ${#failed_pkgs[@]} -gt 0 ]; then
    ui_log "Retrying failed packages with pre-built wheels..."
    for pkg in "${failed_pkgs[@]}"; do
        if python3 -m pip install --user --only-binary :all: "$pkg" 2>/dev/null; then
            ui_ok "Installed (wheel): $pkg"
        else
            ui_warn "Could not install: $pkg (may need manual install)"
        fi
    done
fi

ui_ok "Python dependencies installed"

# --- Step 5: Create Launcher ---
ui_step 5 "Creating Executables"

# Main launcher
cat > "$BIN_DIR/symbiote" << 'EOF'
#!/bin/bash
export PYTHONPATH="${HOME}/.symbiote:${HOME}/.local/share/symbiote:${PYTHONPATH}"
export PYTHONDONTWRITEBYTECODE=1
cd "${HOME}/.symbiote" 2>/dev/null || cd "${HOME}/.local/share/symbiote" 2>/dev/null
python3 main.py "$@"
EOF
chmod +x "$BIN_DIR/symbiote"

# Updater
cat > "$BIN_DIR/symbiote-update" << EOF
#!/bin/bash
curl -fsSL ${RAW_URL}/install.sh | bash
EOF
chmod +x "$BIN_DIR/symbiote-update"

# Uninstaller
cat > "$BIN_DIR/symbiote-uninstall" << 'EOF'
#!/bin/bash
rm -rf "$HOME/.symbiote" "$HOME/.local/share/symbiote"
rm -f "$PREFIX/bin/symbiote" "$PREFIX/bin/symbiote-update" "$PREFIX/bin/symbiote-uninstall"
rm -f "$HOME/.local/bin/symbiote" "$HOME/.local/bin/symbiote-update" "$HOME/.local/bin/symbiote-uninstall"
echo "[✓] Symbiote removed"
EOF
chmod +x "$BIN_DIR/symbiote-uninstall"

ui_ok "Commands created: symbiote, symbiote-update, symbiote-uninstall"

# --- Step 6: Finalize ---
ui_step 6 "Finalizing Installation"

# Fix PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    ui_log "Adding $BIN_DIR to PATH..."
    echo "export PATH=\"\$PATH:$BIN_DIR\"" >> "$HOME/.bashrc"
    export PATH="$PATH:$BIN_DIR"
fi

# Verify installation
if [ -f "$INSTALL_DIR/main.py" ] && [ -s "$INSTALL_DIR/main.py" ]; then
    ui_ok "Installation verified"
else
    ui_err "Installation incomplete - main.py missing"
    draw_footer
    exit 1
fi

# Test Python imports
ui_log "Testing Python environment..."
if python3 -c "import numpy, PIL, rich" 2>/dev/null; then
    ui_ok "All core modules working"
else
    ui_warn "Some modules may need restart to load"
fi

echo "$VERSION" > "$INSTALL_DIR/.version"
draw_footer

echo -e "\n${C_GREEN}✓ INSTALLATION COMPLETE!${C_RESET}"
echo -e "${C_WHITE}Commands available:${C_RESET}"
echo -e "  ${C_CYAN}symbiote${C_RESET}           - Launch Symbiote"
echo -e "  ${C_CYAN}symbiote-update${C_RESET}    - Update to latest version"
echo -e "  ${C_CYAN}symbiote-uninstall${C_RESET} - Remove Symbiote"
echo -e "\n${C_YELLOW}Note:${C_RESET} If 'symbiote' command not found, restart Termux or run:"
echo -e "  ${C_GRAY}source ~/.bashrc${C_RESET}\n"#!/bin/bash
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
