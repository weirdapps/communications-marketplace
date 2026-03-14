# Communications Marketplace

A marketplace of communication and productivity plugins for Claude Code. Install specialized agents, tools, and workflows for presentations, creative assets, and email management.

## Available Plugins

| Plugin | Version | Category | Description |
|--------|---------|----------|-------------|
| [presentation-maker](./plugins/presentation-maker/) | v3.2 | Presentations | Multi-agent system for McKinsey-quality, board-ready NBG presentations |
| [creative-toolkit](./plugins/creative-toolkit/) | v1.0 | Creative | Reusable agents for icon design, data visualization, and device mockups |
| [email-handler](./plugins/email-handler/) | v2.0 | Communications | Email command center with inbox briefings, style-matched drafts, and self-learning |

### Plugin Dependencies

```
presentation-maker ──depends on──> creative-toolkit
```

The `presentation-maker` calls `creative-toolkit` agents (icon designer, infographic specialist, device mockup) during the presentation pipeline. The `email-handler` is standalone.

## Commands

| Command | Plugin | Description |
|---------|--------|-------------|
| `/create-presentation` | presentation-maker | Create a new NBG presentation from content or brief |
| `/redesign-deck` | presentation-maker | Redesign an existing deck to NBG brand standards |
| `/polish-slides` | presentation-maker | Quick formatting fix on existing slides |
| `/create-icon` | creative-toolkit | Generate an SVG icon (NBG brand defaults) |
| `/create-infographic` | creative-toolkit | Create a data visualization or infographic |
| `/inbox-briefing` | email-handler | Quick inbox scan — summaries, action flags, insights (read-only) |
| `/mail-review` | email-handler | Full inbox briefing + draft replies + self-learning |
| `/draft-review` | email-handler | Compare drafted replies with actual responses to improve style guide |
| `/send-mail` | email-handler | Send an email via Microsoft Outlook on macOS |

## Installation

### Quick Install

```bash
curl -sSL https://raw.githubusercontent.com/weirdapps/communications-marketplace/main/install.sh | bash
```

This will:
1. Create `~/.claude/plugins/marketplaces/communications-marketplace/`
2. Clone the marketplace repository
3. Present available plugins for installation
4. Configure selected plugins in your `~/.claude/CLAUDE.md`

### Manual Install

```bash
mkdir -p ~/.claude/plugins/marketplaces
git clone git@github.com:weirdapps/communications-marketplace.git ~/.claude/plugins/marketplaces/communications-marketplace
cd ~/.claude/plugins/marketplaces/communications-marketplace
./install.sh
```

### Update

```bash
cd ~/.claude/plugins/marketplaces/communications-marketplace && git pull
```

### Uninstall

```bash
cd ~/.claude/plugins/marketplaces/communications-marketplace
./uninstall.sh
```

## Directory Structure

```
communications-marketplace/
├── .claude-plugin/
│   └── marketplace.json         # Marketplace manifest (lists all plugins)
├── plugins/
│   ├── presentation-maker/      # NBG presentation system (v3.2)
│   │   ├── plugin.json          # Plugin manifest
│   │   ├── orchestrator/        # Master orchestrator (nbg-presenter)
│   │   ├── agents/              # Storyline Architect, Storyboard Designer, Graphics Renderer
│   │   ├── shared/              # NBG brand system (colors, typography, dimensions, charts)
│   │   ├── commands/            # /create-presentation, /redesign-deck, /polish-slides
│   │   ├── assets/              # Logos, templates, icons, illustrations, screenshots
│   │   ├── tools/               # Python build tools (nbg_build, chart/table injection)
│   │   └── examples/            # Sample storyline YAML files
│   │
│   ├── creative-toolkit/        # Reusable creative agents (v1.0)
│   │   ├── plugin.json
│   │   ├── agents/              # Icon Designer, Infographic Specialist, Device Mockup
│   │   ├── commands/            # /create-icon, /create-infographic
│   │   ├── assets/              # Device frames
│   │   └── tools/               # Python tools (iphone_mockup)
│   │
│   ├── email-handler/           # Email command center (v2.0)
│   │   ├── plugin.json
│   │   ├── agents/              # Email handler agent (10-phase workflow)
│   │   ├── commands/            # /inbox-briefing, /mail-review, /draft-review, /send-mail
│   │   └── shared/              # Style guide, recipient profiles
│   │
│   └── _template/               # Template for new plugins
│
├── docs/
│   ├── creating-plugins.md      # Guide for creating new plugins
│   └── agent-contracts.md       # Cross-plugin API contracts
│
├── schemas/
│   └── plugin.schema.json       # JSON Schema for plugin.json validation
│
├── .github/workflows/
│   └── validate.yml             # CI validation pipeline
│
├── install.sh                   # Interactive installer
├── uninstall.sh                 # Uninstaller
├── CONTRIBUTING.md
├── CHANGELOG.md
└── SECURITY.md
```

## Agent Architecture

### Presentation Maker Pipeline

```
INPUT → Storyline Architect → Storyboard Designer → Graphics Renderer → PPTX OUTPUT
                                     ↓
                     Icon Designer (creative-toolkit)
                     Infographic Specialist (creative-toolkit)
                     Device Mockup (creative-toolkit)
```

| Agent | Role |
|-------|------|
| **NBG Presenter** | Master orchestrator — coordinates the full pipeline |
| **Storyline Architect** | Narrative structure using Pyramid Principle and SCQA framework |
| **Storyboard Designer** | Visual layouts with exact positioning for each slide |
| **Graphics Renderer** | Pixel-perfect PPTX assembly using PptxGenJS |

### Creative Toolkit Agents

| Agent | Role |
|-------|------|
| **Icon Designer** | SVG icon generation — solid fill, monochrome, geometric |
| **Infographic Specialist** | Charts, diagrams, KPI dashboards, data visualizations |
| **Device Mockup** | Pixel-perfect iPhone mockups from app screenshots |

### Email Handler Agent

| Agent | Role |
|-------|------|
| **Email Handler** | 10-phase workflow: inbox review, triage, briefing, draft replies, send via Outlook, self-learning |

## Creating a New Plugin

See [docs/creating-plugins.md](./docs/creating-plugins.md) for the complete guide.

### Quick Start

1. Copy the template:
```bash
cp -r plugins/_template plugins/my-plugin
```

2. Edit `plugins/my-plugin/plugin.json` with your plugin manifest

3. Add your agents (`agents/*/SKILL.md`) and commands (`commands/*.md`)

4. Register in `.claude-plugin/marketplace.json`

## Plugin Categories

| Category | Description |
|----------|-------------|
| `presentations` | Presentation creation and formatting tools |
| `creative` | Icons, infographics, mockups, and visual assets |
| `communications` | Email, messaging, and communication tools |
| `documents` | Document generation and formatting tools |
| `data-viz` | Charts, graphs, and data visualization tools |

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## License

MIT — See individual plugins for their specific licenses.
