#!/bin/bash
#
# NBG Communications Marketplace Installer
# Creates McKinsey-quality presentations with NBG branding
#
# Usage:
#   curl -sSL https://raw.githubusercontent.com/weirdapps/communications-marketplace/main/install.sh | bash
#
# Or clone first, then run:
#   ./install.sh
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Configuration
REPO_URL="https://github.com/weirdapps/communications-marketplace.git"
REPO_SSH="git@github.com:weirdapps/communications-marketplace.git"
INSTALL_DIR="$HOME/.claude/plugins/marketplaces/communications-marketplace"
CLAUDE_MD="$HOME/.claude/CLAUDE.md"

# Print banner
print_banner() {
    echo ""
    echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC}  ${BOLD}NBG Communications Marketplace Installer${NC}                              ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC}  Create McKinsey-quality presentations with NBG branding       ${CYAN}║${NC}"
    echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# Print step
print_step() {
    echo -e "${BLUE}→${NC} $1"
}

# Print success
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

# Print warning
print_warning() {
    echo -e "${YELLOW}!${NC} $1"
}

# Print error
print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    print_step "Checking prerequisites..."

    if ! command_exists git; then
        print_error "Git is not installed"
        echo ""
        echo "Please install git first:"
        echo "  macOS:  brew install git"
        echo "  Ubuntu: sudo apt install git"
        echo "  Windows: https://git-scm.com/download/win"
        exit 1
    fi
    print_success "Git found"
}

# Create directory structure
create_directories() {
    print_step "Creating directory structure..."

    mkdir -p "$HOME/.claude/plugins/marketplaces"
    print_success "Directory created: ~/.claude/plugins/marketplaces/"
}

# Clone or update repository
clone_repository() {
    if [ -d "$INSTALL_DIR" ]; then
        print_warning "Existing installation found"
        echo ""
        read -p "Update existing installation? [Y/n] " -n 1 -r
        echo ""

        if [[ $REPLY =~ ^[Nn]$ ]]; then
            print_warning "Skipping repository update"
            return
        fi

        print_step "Updating repository..."
        cd "$INSTALL_DIR"
        git pull origin main
        print_success "Repository updated"
    else
        print_step "Cloning repository..."

        # Try SSH first, fall back to HTTPS
        if git clone "$REPO_SSH" "$INSTALL_DIR" 2>/dev/null; then
            print_success "Repository cloned (SSH)"
        elif git clone "$REPO_URL" "$INSTALL_DIR" 2>/dev/null; then
            print_success "Repository cloned (HTTPS)"
        else
            print_error "Failed to clone repository"
            echo ""
            echo "Please check:"
            echo "  1. You have access to the repository"
            echo "  2. Your SSH keys are configured (for private repos)"
            echo "  3. Your network connection"
            exit 1
        fi
    fi
}

# Generate CLAUDE.md content for NBG
generate_claude_md_content() {
    cat << 'CLAUDE_CONTENT'

---

## NBG PRESENTATION FORMAT (MANDATORY WORKFLOW)

**CRITICAL**: When asked to create ANY presentation for NBG or "in NBG format", you MUST follow the communications-marketplace multi-agent workflow. Do NOT skip to html2pptx or other shortcuts.

### Communications-Marketplace Location
`~/.claude/plugins/marketplaces/communications-marketplace/` (v3.0)

### MANDATORY WORKFLOW (Read These Files First)
Before creating any NBG presentation, read these files in order:

1. **Brand System**: `shared/nbg-brand-system/README.md` - Single source of truth for all specs
2. **Orchestrator**: `orchestrator/nbg-presenter/SKILL.md` - Master workflow
3. **Step 1**: `agents/storyline-architect/SKILL.md` - Create narrative structure
4. **Step 2**: `agents/storyboard-designer/SKILL.md` - Design visual layouts
5. **Step 3**: `agents/graphics-renderer/SKILL.md` - Generate PPTX

### Agent Pipeline (ALWAYS Follow This Order)
```
INPUT → Storyline Architect → Storyboard Designer → Graphics Renderer → OUTPUT
                                    ↓
                    Infographic Specialist (if data viz needed)
                    Icon Designer (if custom icons needed)
```

### Quality Standards (McKinsey-Level)
- **Pyramid Principle**: Lead with the answer, support with arguments
- **One Message Per Slide**: No exceptions
- **Action Titles**: Full sentences that tell the story (NOT labels)
- **5-7 Second Rule**: Every slide scannable at a glance
- **"So What?" Test**: Every slide must matter

### Commands Available
| Command | When to Use |
|---------|-------------|
| `/create-presentation` | New presentation from content |
| `/redesign-deck` | Redesign existing deck to NBG |
| `/create-infographic` | Data visualization only |
| `/create-icon` | Custom NBG-compliant icon |
| `/polish-slides` | Quick formatting fix |

### NBG Brand Essentials (Quick Reference)
```yaml
dimensions: 13.33" x 7.5" (LAYOUT_WIDE)
colors:
  title: "#003841" (Dark Teal)
  body: "#202020" (Dark Text)
  accent: "#007B85" (NBG Teal)
  bullet: "#00DFF8" (Bright Cyan)
  background: "#FFFFFF" (White)
fonts:
  primary: "Aptos"
  fallback: "Arial"
logo:
  small: { pos: [0.374", 7.071"], size: [0.822", 0.236"] }
  large: { pos: [0.374", 6.271"], size: [2.191", 0.630"] }
pageNumber:
  position: [12.2265", 7.1554"]
  size: [0.748", 0.152"]
  alignedWithLogo: true
chartColors: ['00ADBF', '003841', '007B85', '939793', 'BEC1BE', '00DFF8']
```

### Assets & Templates
- **Logo (Greek)**: `~/.claude/plugins/marketplaces/communications-marketplace/assets/nbg-logo-gr.svg`
- **Logo (English)**: `~/.claude/plugins/marketplaces/communications-marketplace/assets/nbg-logo.svg`
- **Back Cover Logo**: `~/.claude/plugins/marketplaces/communications-marketplace/assets/nbg-back-cover-logo.png`
- **Template EN**: `~/.claude/plugins/marketplaces/communications-marketplace/assets/templates/NBG-Template-EN.pptx`
- **Template GR**: `~/.claude/plugins/marketplaces/communications-marketplace/assets/templates/NBG-Template-GR.pptx`
- **Full Spec**: `~/.claude/plugins/marketplaces/communications-marketplace/assets/NBG-PRESENTATION-SPEC.md`

### Trigger Phrases (Activate NBG Workflow)
- "Create NBG presentation"
- "NBG format" / "in NBG format"
- "Make this board-ready"
- "Presentation for NBG"
- "National Bank of Greece"
- "Format for the board"

### What NOT To Do
- Skip reading the agent SKILL.md files
- Jump directly to html2pptx without storyline
- Use generic PowerPoint dimensions
- Create generic topic labels as titles
- Skip the logo on any slide (except back cover uses centered logo)
- Use non-NBG colors or fonts
- **Use pie charts** - ALWAYS use doughnut instead
- **Use "Thank You" slides** - Use plain back cover with centered oval logo
- **Put page numbers on cover, dividers, or back cover** - content slides only

---
CLAUDE_CONTENT
}

# Update CLAUDE.md
update_claude_md() {
    print_step "Checking CLAUDE.md configuration..."

    # Check if NBG section already exists
    if [ -f "$CLAUDE_MD" ] && grep -q "NBG PRESENTATION FORMAT" "$CLAUDE_MD"; then
        print_warning "NBG configuration already exists in CLAUDE.md"
        echo ""
        read -p "Replace existing NBG configuration? [y/N] " -n 1 -r
        echo ""

        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_warning "Skipping CLAUDE.md update"
            return
        fi

        # Remove existing NBG section (between --- markers)
        print_step "Removing old NBG configuration..."
        # Create backup
        cp "$CLAUDE_MD" "$CLAUDE_MD.backup"

        # Remove the NBG section using sed
        sed -i.tmp '/^## NBG PRESENTATION FORMAT/,/^---$/d' "$CLAUDE_MD"
        rm -f "$CLAUDE_MD.tmp"

        print_success "Old configuration removed (backup: CLAUDE.md.backup)"
    fi

    echo ""
    read -p "Add NBG workflow configuration to ~/.claude/CLAUDE.md? [Y/n] " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Nn]$ ]]; then
        print_warning "Skipping CLAUDE.md update"
        echo ""
        echo "You can manually add the configuration later."
        echo "See: $INSTALL_DIR/docs/CLAUDE-CONFIG.md"
        return
    fi

    print_step "Updating CLAUDE.md..."

    # Create CLAUDE.md if it doesn't exist
    if [ ! -f "$CLAUDE_MD" ]; then
        mkdir -p "$HOME/.claude"
        echo "# CLAUDE.md - User Configuration" > "$CLAUDE_MD"
        echo "" >> "$CLAUDE_MD"
        echo "Add your Claude Code instructions below." >> "$CLAUDE_MD"
    fi

    # Append NBG configuration
    generate_claude_md_content >> "$CLAUDE_MD"

    print_success "CLAUDE.md updated"
}

# Verify installation
verify_installation() {
    print_step "Verifying installation..."

    local errors=0

    # Check key files exist
    for file in "README.md" "orchestrator/nbg-presenter/SKILL.md" "shared/nbg-brand-system/README.md" ".claude-plugin/plugin.json"; do
        if [ ! -f "$INSTALL_DIR/$file" ]; then
            print_error "Missing: $file"
            errors=$((errors + 1))
        fi
    done

    # Check assets
    for asset in "assets/nbg-logo-gr.svg" "assets/nbg-logo.svg" "assets/nbg-back-cover-logo.png"; do
        if [ ! -f "$INSTALL_DIR/$asset" ]; then
            print_error "Missing asset: $asset"
            errors=$((errors + 1))
        fi
    done

    if [ $errors -gt 0 ]; then
        print_error "Installation verification failed with $errors errors"
        exit 1
    fi

    print_success "All files verified"
}

# Print completion message
print_completion() {
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  Installation complete!${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${BOLD}Commands available in Claude Code:${NC}"
    echo ""
    echo "  /create-presentation  Create a new NBG presentation"
    echo "  /redesign-deck        Redesign existing deck to NBG standards"
    echo "  /create-infographic   Create NBG-branded data visualization"
    echo "  /create-icon          Create NBG-compliant SVG icon"
    echo "  /polish-slides        Quick formatting to NBG standards"
    echo ""
    echo -e "${BOLD}Trigger phrases:${NC}"
    echo ""
    echo "  \"Create NBG presentation about...\""
    echo "  \"Make this board-ready\""
    echo "  \"Format this for NBG\""
    echo ""
    echo -e "${BOLD}To update later:${NC}"
    echo ""
    echo "  cd $INSTALL_DIR && git pull"
    echo ""
    echo -e "${BOLD}Documentation:${NC}"
    echo ""
    echo "  $INSTALL_DIR/README.md"
    echo ""
}

# Main installation flow
main() {
    print_banner
    check_prerequisites
    create_directories
    clone_repository
    update_claude_md
    verify_installation
    print_completion
}

# Run main
main "$@"
