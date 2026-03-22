#!/bin/bash
# MN-SOS Uninstaller

echo "Removing MN-SOS..."

INSTALL_DIR="$HOME/.mn-sos"
BIN_DIR="$PREFIX/bin"

# Remove installation
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "[✓] Removed $INSTALL_DIR"
fi

# Remove binaries
rm -f "$BIN_DIR/mn-sos"
rm -f "$BIN_DIR/mn-sos-update"

echo "[✓] Uninstallation complete"