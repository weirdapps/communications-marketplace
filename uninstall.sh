#!/bin/bash
#
# NBG Communications Marketplace Uninstaller
#
# Usage:
#   ./uninstall.sh
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

INSTALL_DIR="$HOME/.claude/plugins/marketplaces/communications-marketplace"
CLAUDE_MD="$HOME/.claude/CLAUDE.md"

echo ""
echo -e "${YELLOW}NBG Communications Marketplace Uninstaller${NC}"
echo ""

# Confirm
read -p "Are you sure you want to uninstall communications-marketplace? [y/N] " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Remove NBG section from CLAUDE.md
if [ -f "$CLAUDE_MD" ] && grep -q "NBG PRESENTATION FORMAT" "$CLAUDE_MD"; then
    echo -e "${YELLOW}→${NC} Removing NBG configuration from CLAUDE.md..."

    # Create backup
    cp "$CLAUDE_MD" "$CLAUDE_MD.backup"

    # Remove NBG section
    sed -i.tmp '/^---$/,/^## NBG PRESENTATION FORMAT/{/^## NBG PRESENTATION FORMAT/,/^---$/d}' "$CLAUDE_MD"
    rm -f "$CLAUDE_MD.tmp"

    echo -e "${GREEN}✓${NC} CLAUDE.md cleaned (backup: CLAUDE.md.backup)"
fi

# Remove installation directory
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}→${NC} Removing installation directory..."
    rm -rf "$INSTALL_DIR"
    echo -e "${GREEN}✓${NC} Directory removed"
fi

echo ""
echo -e "${GREEN}Uninstallation complete.${NC}"
echo ""
