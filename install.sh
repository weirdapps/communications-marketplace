#!/bin/bash
#
# Communications Marketplace Installer
# Install communication and productivity plugins for Claude Code
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
    echo -e "${CYAN}║${NC}  ${BOLD}Communications Marketplace Installer${NC}                         ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC}  Install communication plugins for Claude Code                 ${CYAN}║${NC}"
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

# List available plugins
list_plugins() {
    print_step "Available plugins:"
    echo ""

    local plugin_num=1
    AVAILABLE_PLUGINS=()

    for plugin_dir in "$INSTALL_DIR/plugins"/*/; do
        if [ -d "$plugin_dir" ] && [ -f "$plugin_dir/plugin.json" ]; then
            plugin_name=$(basename "$plugin_dir")

            # Skip template
            if [ "$plugin_name" = "_template" ]; then
                continue
            fi

            # Read plugin description from plugin.json
            if command_exists jq; then
                description=$(jq -r '.description // "No description"' "$plugin_dir/plugin.json" 2>/dev/null | head -c 60)
            else
                description=$(grep -o '"description"[[:space:]]*:[[:space:]]*"[^"]*"' "$plugin_dir/plugin.json" 2>/dev/null | head -1 | sed 's/.*: *"//;s/"$//' | head -c 60)
            fi

            echo -e "  ${BOLD}[$plugin_num]${NC} ${CYAN}$plugin_name${NC}"
            echo "      $description..."
            echo ""

            AVAILABLE_PLUGINS+=("$plugin_name")
            plugin_num=$((plugin_num + 1))
        fi
    done
}

# Select plugins to install
select_plugins() {
    local plugin_count=${#AVAILABLE_PLUGINS[@]}

    if [ $plugin_count -eq 0 ]; then
        print_warning "No plugins found in marketplace"
        return
    fi

    echo -e "  ${BOLD}[A]${NC} Install ALL plugins"
    echo ""

    read -p "Enter plugin numbers to install (comma-separated) or 'A' for all: " selection

    SELECTED_PLUGINS=()

    if [[ "$selection" =~ ^[Aa]$ ]]; then
        SELECTED_PLUGINS=("${AVAILABLE_PLUGINS[@]}")
    else
        IFS=',' read -ra selections <<< "$selection"
        for sel in "${selections[@]}"; do
            sel=$(echo "$sel" | tr -d ' ')
            if [[ "$sel" =~ ^[0-9]+$ ]] && [ "$sel" -ge 1 ] && [ "$sel" -le $plugin_count ]; then
                SELECTED_PLUGINS+=("${AVAILABLE_PLUGINS[$((sel-1))]}")
            fi
        done
    fi

    echo ""
    if [ ${#SELECTED_PLUGINS[@]} -eq 0 ]; then
        print_warning "No plugins selected"
    else
        print_success "Selected: ${SELECTED_PLUGINS[*]}"
    fi
}

# Generate CLAUDE.md content for a plugin
generate_plugin_config() {
    local plugin_name=$1
    local plugin_dir="$INSTALL_DIR/plugins/$plugin_name"

    case "$plugin_name" in
        "presentation-maker")
            generate_presentation_maker_config
            ;;
        "creative-toolkit")
            generate_creative_toolkit_config
            ;;
        "email-drafter")
            generate_email_drafter_config
            ;;
        *)
            generate_generic_config "$plugin_name" "$plugin_dir"
            ;;
    esac
}

# Generate presentation-maker configuration
generate_presentation_maker_config() {
    cat << 'CLAUDE_CONTENT'

---

## PRESENTATION-MAKER Plugin (MANDATORY WORKFLOW)

**CRITICAL**: When asked to create ANY presentation for NBG or "in NBG format", you MUST follow the communications-marketplace multi-agent workflow. Do NOT skip to html2pptx or other shortcuts.

### Location
`~/.claude/plugins/marketplaces/communications-marketplace/plugins/presentation-maker/` (v3.1)

### Dependencies
Requires the `creative-toolkit` plugin for icons, infographics, and device mockups.

### MANDATORY WORKFLOW (Read These Files First)
Before creating any presentation, read these files in order:

1. **Brand System**: `plugins/presentation-maker/shared/nbg-brand-system/README.md` - Single source of truth
2. **Orchestrator**: `plugins/presentation-maker/orchestrator/nbg-presenter/SKILL.md` - Master workflow
3. **Step 1**: `plugins/presentation-maker/agents/storyline-architect/SKILL.md` - Narrative structure
4. **Step 2**: `plugins/presentation-maker/agents/storyboard-designer/SKILL.md` - Visual layouts
5. **Step 3**: `plugins/presentation-maker/agents/graphics-renderer/SKILL.md` - Generate PPTX
6. **Utilities**: `plugins/creative-toolkit/agents/` - Icons, infographics, mockups (as needed)

### Agent Pipeline (ALWAYS Follow This Order)
```
INPUT → Storyline Architect → Storyboard Designer → Graphics Renderer → OUTPUT
                                    ↓
                    Infographic Specialist (creative-toolkit, if data viz needed)
                    Icon Designer (creative-toolkit, if custom icons needed)
                    Device Mockup (creative-toolkit, if app screenshots needed)
```

### Commands Available
| Command | Plugin | When to Use |
|---------|--------|-------------|
| `/create-presentation` | presentation-maker | New presentation from content |
| `/redesign-deck` | presentation-maker | Redesign existing deck to NBG |
| `/polish-slides` | presentation-maker | Quick formatting fix |
| `/create-infographic` | creative-toolkit | Data visualization only |
| `/create-icon` | creative-toolkit | Custom SVG icon |

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
chartColors: ['00ADBF', '003841', '007B85', '939793', 'BEC1BE', '00DFF8']
```

---
CLAUDE_CONTENT
}

# Generate creative-toolkit configuration
generate_creative_toolkit_config() {
    cat << 'CLAUDE_CONTENT'

---

## CREATIVE-TOOLKIT Plugin

**Location**: `~/.claude/plugins/marketplaces/communications-marketplace/plugins/creative-toolkit/`

### What It Does
Reusable creative agents for icon design, data visualization, and device mockups. Brand-configurable with NBG defaults.

### Agents
- **Icon Designer**: SVG icon generation — solid fill, monochrome, geometric
- **Infographic Specialist**: Charts, diagrams, KPI dashboards, data visualizations
- **Device Mockup**: Pixel-perfect iPhone mockups from app screenshots

### Commands Available
| Command | When to Use |
|---------|-------------|
| `/create-icon` | Generate an SVG icon |
| `/create-infographic` | Create a data visualization |

### Used By
- `presentation-maker` — calls these agents during the presentation pipeline

---
CLAUDE_CONTENT
}

# Generate email-drafter configuration
generate_email_drafter_config() {
    cat << 'CLAUDE_CONTENT'

---

## EMAIL-DRAFTER Plugin

**Location**: `~/.claude/plugins/marketplaces/communications-marketplace/plugins/email-drafter/`

### What It Does
Reads Outlook 365 emails via Playwright browser automation, triages them, and drafts replies matching your communication style. Learns from comparing drafts to actual responses.

### Dependencies
Requires the `outlook-mailer` plugin for creating draft emails in Outlook.

### Commands Available
| Command | When to Use |
|---------|-------------|
| `/draft` | Read inbox emails, triage, draft replies |
| `/draft-review` | Compare drafts to actual responses, update style guide |

### Key Files
- **Style Guide**: `plugins/email-drafter/shared/style-guide.md` — your communication patterns
- **Agent**: `plugins/email-drafter/agents/email-drafter/SKILL.md` — 5-phase workflow

### Prerequisites
- Outlook Web access (logged into https://outlook.office.com)
- Playwright MCP server (for browser automation)

---
CLAUDE_CONTENT
}

# Generate generic plugin configuration
generate_generic_config() {
    local plugin_name=$1
    local plugin_dir=$2

    cat << CLAUDE_CONTENT

---

## ${plugin_name^^} Plugin

**Location**: \`~/.claude/plugins/marketplaces/communications-marketplace/plugins/$plugin_name/\`

### Usage
See \`plugins/$plugin_name/README.md\` for documentation.

---
CLAUDE_CONTENT
}

# Update CLAUDE.md with selected plugins
update_claude_md() {
    if [ ${#SELECTED_PLUGINS[@]} -eq 0 ]; then
        return
    fi

    print_step "Checking CLAUDE.md configuration..."

    echo ""
    read -p "Add plugin configurations to ~/.claude/CLAUDE.md? [Y/n] " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Nn]$ ]]; then
        print_warning "Skipping CLAUDE.md update"
        return
    fi

    # Create CLAUDE.md if it doesn't exist
    if [ ! -f "$CLAUDE_MD" ]; then
        mkdir -p "$HOME/.claude"
        echo "# CLAUDE.md - User Configuration" > "$CLAUDE_MD"
        echo "" >> "$CLAUDE_MD"
        echo "Add your Claude Code instructions below." >> "$CLAUDE_MD"
    fi

    # Create backup
    cp "$CLAUDE_MD" "$CLAUDE_MD.backup"

    for plugin in "${SELECTED_PLUGINS[@]}"; do
        print_step "Configuring $plugin..."

        # Check if plugin config already exists
        local marker="${plugin^^}"
        if grep -q "$marker" "$CLAUDE_MD" 2>/dev/null; then
            print_warning "$plugin configuration already exists, skipping"
            continue
        fi

        # Append plugin configuration
        generate_plugin_config "$plugin" >> "$CLAUDE_MD"
        print_success "$plugin configured"
    done

    print_success "CLAUDE.md updated (backup: CLAUDE.md.backup)"
}

# Verify installation
verify_installation() {
    print_step "Verifying installation..."

    local errors=0

    # Check marketplace files exist
    for file in "README.md" ".claude-plugin/marketplace.json"; do
        if [ ! -f "$INSTALL_DIR/$file" ]; then
            print_error "Missing: $file"
            errors=$((errors + 1))
        fi
    done

    # Check selected plugins
    for plugin in "${SELECTED_PLUGINS[@]}"; do
        if [ ! -f "$INSTALL_DIR/plugins/$plugin/plugin.json" ]; then
            print_error "Missing plugin manifest: $plugin/plugin.json"
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

    if [ ${#SELECTED_PLUGINS[@]} -gt 0 ]; then
        echo -e "${BOLD}Installed plugins:${NC}"
        echo ""
        for plugin in "${SELECTED_PLUGINS[@]}"; do
            echo "  - $plugin"
        done
        echo ""
    fi

    echo -e "${BOLD}Commands available:${NC}"
    echo ""
    for plugin in "${SELECTED_PLUGINS[@]}"; do
        local cmd_dir="$INSTALL_DIR/plugins/$plugin/commands"
        if [ -d "$cmd_dir" ]; then
            for cmd_file in "$cmd_dir"/*.md; do
                if [ -f "$cmd_file" ]; then
                    local cmd_name=$(basename "$cmd_file" .md)
                    local cmd_desc=""
                    if command_exists grep; then
                        cmd_desc=$(grep -m1 '^description:' "$cmd_file" 2>/dev/null | sed 's/^description: *"*//;s/"*$//' | head -c 50)
                    fi
                    printf "  %-24s %s\n" "/$cmd_name" "$cmd_desc"
                fi
            done
        fi
    done
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

    # Change to install directory for plugin discovery
    cd "$INSTALL_DIR"

    list_plugins
    select_plugins
    update_claude_md
    verify_installation
    print_completion
}

# Run main
main "$@"
