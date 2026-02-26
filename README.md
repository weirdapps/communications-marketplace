# Communications Marketplace

A marketplace of communication and productivity plugins for Claude Code. Install specialized agents, tools, and workflows for various communication needs.

## Installation

### Quick Install (Recommended)

```bash
curl -sSL https://raw.githubusercontent.com/weirdapps/communications-marketplace/main/install.sh | bash
```

This will:
1. Create `~/.claude/plugins/marketplaces/communications-marketplace/` directory
2. Clone the marketplace repository
3. Present available plugins for installation
4. Configure selected plugins in your `~/.claude/CLAUDE.md`

### Manual Install

```bash
# Create directory
mkdir -p ~/.claude/plugins/marketplaces

# Clone repository
git clone git@github.com:weirdapps/communications-marketplace.git ~/.claude/plugins/marketplaces/communications-marketplace

# Run installer
cd ~/.claude/plugins/marketplaces/communications-marketplace
./install.sh
```

### Update

```bash
cd ~/.claude/plugins/marketplaces/communications-marketplace && git pull
```

## Available Plugins

| Plugin | Category | Description |
|--------|----------|-------------|
| [nbg-presentations](./plugins/nbg-presentations/) | Presentations | Multi-agent presentation system for NBG. Create McKinsey-quality, board-ready presentations. |

## Directory Structure

```
communications-marketplace/
├── .claude-plugin/
│   └── marketplace.json         # Marketplace manifest
│
├── plugins/                     # Available plugins
│   ├── nbg-presentations/       # NBG presentation system
│   │   ├── plugin.json          # Plugin manifest
│   │   ├── README.md            # Plugin documentation
│   │   ├── orchestrator/        # Master orchestrator
│   │   ├── agents/              # Specialist agents
│   │   ├── shared/              # Brand specifications
│   │   ├── commands/            # Slash commands
│   │   ├── assets/              # Brand assets
│   │   └── tools/               # Build tools
│   │
│   └── _template/               # Template for new plugins
│       ├── plugin.json
│       ├── README.md
│       ├── agents/
│       └── commands/
│
├── docs/                        # Marketplace documentation
│   └── creating-plugins.md
│
├── install.sh                   # Marketplace installer
├── uninstall.sh                 # Marketplace uninstaller
└── README.md                    # This file
```

## Creating a New Plugin

See [docs/creating-plugins.md](./docs/creating-plugins.md) for a complete guide.

### Quick Start

1. Copy the template:
```bash
cp -r plugins/_template plugins/my-plugin
```

2. Edit `plugins/my-plugin/plugin.json`:
```json
{
  "name": "my-plugin",
  "description": "What your plugin does",
  "version": "1.0.0",
  "type": "plugin",
  "commands": "./commands",
  "agents": {
    "my-agent": {
      "path": "./agents/my-agent/SKILL.md",
      "description": "What this agent does"
    }
  }
}
```

3. Add your agents and commands

4. Register in marketplace `.claude-plugin/marketplace.json` by adding to the `plugins` array:
```json
{
  "name": "my-plugin",
  "description": "What it does",
  "version": "1.0.0",
  "author": { "name": "Your Name" },
  "source": "./plugins/my-plugin",
  "category": "category-id"
}
```

## Plugin Categories

| Category | Description |
|----------|-------------|
| `presentations` | Tools for creating professional presentations |
| `documents` | Document generation and formatting tools |
| `communications` | Email, messaging, and communication tools |
| `data-viz` | Charts, graphs, and data visualization tools |

## Commands by Plugin

### NBG Presentations

| Command | Description |
|---------|-------------|
| `/create-presentation` | Create new NBG presentation |
| `/redesign-deck` | Redesign existing deck |
| `/create-infographic` | Generate data visualization |
| `/create-icon` | Create SVG icon |
| `/polish-slides` | Quick formatting fix |

## How Plugins Work

Each plugin in this marketplace can contain:

- **Agents**: Specialized AI agents with specific skills (defined in `SKILL.md` files)
- **Commands**: Slash commands that trigger workflows (defined in markdown files)
- **Assets**: Logos, templates, and other resources
- **Tools**: Build scripts and utilities
- **Shared**: Common configurations and specifications

When installed, plugins are registered with Claude Code and their commands become available in your sessions.

## Contributing

1. Fork this repository
2. Create your plugin in `plugins/your-plugin/`
3. Follow the plugin template structure
4. Submit a pull request

## Version History

### v1.0.0 (Marketplace Launch)
- Restructured as a marketplace for multiple plugins
- NBG Presentations plugin moved to `plugins/nbg-presentations/`
- Added plugin template and documentation
- Added plugin categories and discovery

### Previous (as NBG-only)
- v3.0.0: Clean, deduplicated NBG architecture
- v2.0.0: Multi-agent architecture
- v1.0.0: Monolithic plugin

## License

MIT - See individual plugins for their specific licenses.
