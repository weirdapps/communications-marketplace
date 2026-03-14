#!/bin/bash
#
# Communications Marketplace Uninstaller
#
# Usage:
#   ./uninstall.sh
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

INSTALL_DIR="$HOME/.claude/plugins/marketplaces/communications-marketplace"
CLAUDE_MD="$HOME/.claude/CLAUDE.md"

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║${NC}  ${BOLD}Communications Marketplace Uninstaller${NC}                        ${CYAN}║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# List installed plugins
echo -e "${BOLD}Installed plugins:${NC}"
echo ""
plugin_count=0
for plugin_dir in "$INSTALL_DIR/plugins"/*/; do
    if [ -d "$plugin_dir" ] && [ -f "$plugin_dir/plugin.json" ]; then
        plugin_name=$(basename "$plugin_dir")
        if [ "$plugin_name" != "_template" ]; then
            echo "  - $plugin_name"
            plugin_count=$((plugin_count + 1))
        fi
    fi
done
if [ $plugin_count -eq 0 ]; then
    echo "  (none)"
fi
echo ""

# Confirm
read -p "Uninstall entire marketplace and all plugins? [y/N] " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Remove plugin configurations from CLAUDE.md
if [ -f "$CLAUDE_MD" ]; then
    echo -e "${YELLOW}→${NC} Cleaning CLAUDE.md..."

    # Create backup
    cp "$CLAUDE_MD" "$CLAUDE_MD.backup"

    # Remove NBG section if present
    if grep -q "NBG PRESENTATION FORMAT" "$CLAUDE_MD"; then
        # Use perl for more reliable multi-line removal
        perl -i -0pe 's/\n---\n\n## NBG PRESENTATION FORMAT.*?---\n//s' "$CLAUDE_MD" 2>/dev/null || true
        echo -e "${GREEN}✓${NC} NBG configuration removed"
    fi

    # Remove other plugin sections (generic pattern)
    for plugin_dir in "$INSTALL_DIR/plugins"/*/; do
        if [ -d "$plugin_dir" ]; then
            plugin_name=$(basename "$plugin_dir")
            if [ "$plugin_name" != "_template" ]; then
                marker="${plugin_name^^} Plugin"
                if grep -q "$marker" "$CLAUDE_MD" 2>/dev/null; then
                    perl -i -0pe "s/\n---\n\n## ${marker}.*?---\n//s" "$CLAUDE_MD" 2>/dev/null || true
                    echo -e "${GREEN}✓${NC} $plugin_name configuration removed"
                fi
            fi
        fi
    done

    echo -e "${GREEN}✓${NC} CLAUDE.md cleaned (backup: CLAUDE.md.backup)"
fi

# Remove installation directory
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}→${NC} Removing installation directory..."
    rm -rf "$INSTALL_DIR"
    echo -e "${GREEN}✓${NC} Directory removed: $INSTALL_DIR"
fi

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Uninstallation complete.${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo "To reinstall:"
echo "  curl -sSL https://raw.githubusercontent.com/weirdapps/communications-marketplace/main/install.sh | bash"
echo ""
