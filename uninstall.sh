#!/bin/bash
# Symbiote v3.0.0 Uninstaller
# Repo: dragon-X1234/symbiotic-wave

set -e

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
    echo -e "${C_BLUE}│${C_WHITE}  🗑️ Symbiote Uninstaller                               ${C_BLUE}│${C_RESET}"
    echo -e "${C_BLUE}├────────────────────────────────────────────────────────┤${C_RESET}"
}

ui_log() { echo -e "${C_BLUE}│${C_GRAY}  [*] $1${C_RESET}"; }
ui_success() { echo -e "${C_BLUE}│${C_GREEN}  [✓] $1${C_RESET}"; }
ui_err() { echo -e "${C_BLUE}│${C_RED}  [!] $1${C_RESET}"; }
ui_prompt() { echo -ne "${C_BLUE}│${C_WHITE}  [?] $1 [Y/n]: ${C_RESET}"; }

draw_footer() {
    echo -e "${C_BLUE}╰────────────────────────────────────────────────────────╯${C_RESET}"
}

draw_header

# --- Environment Detection ---
ui_log "Locating Symbiote installation..."
if [[ "$PREFIX" == *"com.termux"* ]]; then
    INSTALL_DIR="$HOME/.symbiote"
    BIN_DIR="$PREFIX/bin"
else
    INSTALL_DIR="$HOME/.local/share/symbiote"
    BIN_DIR="$HOME/.local/bin"
fi

if [ ! -d "$INSTALL_DIR" ]; then
    ui_err "Symbiote installation not found at ${INSTALL_DIR}"
    draw_footer
    exit 1
fi

ui_success "Found installation at ${INSTALL_DIR}"

# --- Confirmation ---
ui_prompt "Are you sure you want to completely remove Symbiote?"
read -r CONFIRM

if [[ "$CONFIRM" =~ ^[Nn]$ ]]; then
    ui_log "Uninstallation aborted by user."
    draw_footer
    exit 0
fi

# --- Removal ---
ui_log "Purging source directories..."
rm -rf "$INSTALL_DIR"
ui_success "Removed $INSTALL_DIR"

ui_log "Removing executable hooks..."
# Remove from Termux paths (if they exist there)
rm -f "$PREFIX/bin/symbiote" "$PREFIX/bin/symbiote-update" "$PREFIX/bin/symbiote-uninstall" 2>/dev/null
# Remove from Standard Linux paths (if they exist there)
rm -f "$HOME/.local/bin/symbiote" "$HOME/.local/bin/symbiote-update" "$HOME/.local/bin/symbiote-uninstall" 2>/dev/null

ui_success "Executables removed"

ui_success "Symbiote has been successfully uninstalled."
draw_footer
echo ""
