# Comms Marketplace v2.0

Multi-agent presentation system for National Bank of Greece (NBG) corporate communications.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     NBG PRESENTER                             │
│                    (Master Orchestrator)                         │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   STORYLINE   │    │  STORYBOARD   │    │   GRAPHICS    │
│   ARCHITECT   │ → │   DESIGNER    │ → │   RENDERER    │
└───────────────┘    └───────────────┘    └───────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
       ┌───────────┐   ┌───────────┐   ┌───────────┐
       │INFOGRAPHIC│   │   ICON    │   │  (Other)  │
       │SPECIALIST │   │ DESIGNER  │   │           │
       └───────────┘   └───────────┘   └───────────┘
```

## Agents

### NBG Presenter (Orchestrator)
Master conductor that coordinates all specialist agents.
- **Path**: `orchestrator/nbg-presenter/SKILL.md`
- **Purpose**: Analyze input, plan workflow, delegate to specialists, ensure quality

### Storyline Architect
Strategic narrative designer.
- **Path**: `agents/storyline-architect/SKILL.md`
- **Purpose**: Transform raw content into compelling executive storylines
- **Output**: Slide-by-slide narrative with key messages

### Storyboard Designer
Visual layout strategist.
- **Path**: `agents/storyboard-designer/SKILL.md`
- **Purpose**: Decide HOW each slide should look
- **Output**: Layout specs, positioning, visual element requirements

### Infographic Specialist
Data visualization expert.
- **Path**: `agents/infographic-specialist/SKILL.md`
- **Purpose**: Transform data into clear, NBG-branded visuals
- **Output**: Chart configs, diagram specs, SVG code

### Icon Designer
NBG-compliant icon generator.
- **Path**: `agents/icon-designer/SKILL.md`
- **Purpose**: Create custom SVG icons matching NBG style
- **Output**: Production-ready SVG code

### Graphics Renderer
Pixel-perfect PPTX production.
- **Path**: `agents/graphics-renderer/SKILL.md`
- **Purpose**: Assemble final presentation with exact formatting
- **Output**: Board-ready .pptx file

## Commands

| Command | Description |
|---------|-------------|
| `/create-presentation` | Create new NBG presentation from content |
| `/redesign-deck` | Redesign existing presentation to NBG standards |
| `/create-infographic` | Generate NBG-branded data visualization |
| `/create-icon` | Create NBG-compliant SVG icon |
| `/polish-slides` | Quick formatting to NBG standards |

## NBG Brand Essentials

### Slide Dimensions
- **EMU**: 12,192,000 x 6,858,000
- **Inches**: 13.33" x 7.5" (use LAYOUT_WIDE in PptxGenJS)

### Primary Colors
| Name | Hex | Usage |
|------|-----|-------|
| Dark Teal | `#003841` | Titles, icons |
| NBG Teal | `#007B85` | Brand, section numbers |
| Bright Cyan | `#00DFF8` | Accents, bullets |
| Dark Text | `#202020` | Body text |

### Typography
- **Primary Font**: Aptos
- **Fallback**: Arial, Calibri

### Logo
- **Position**: (0.34", 6.6")
- **Greek**: 2.14" x 0.62"
- **English**: 2.94" x 0.62"

## Directory Structure

```
comms-marketplace/
├── orchestrator/
│   └── nbg-presenter/       # Master orchestrator
├── agents/
│   ├── storyline-architect/    # Narrative design
│   ├── storyboard-designer/    # Visual layout
│   ├── infographic-specialist/ # Data visualization
│   ├── icon-designer/          # SVG icons
│   └── graphics-renderer/      # PPTX production
├── shared/
│   └── nbg-brand-system/       # Shared brand references
├── commands/                   # Slash commands
├── assets/                     # Logos, images
├── plugins/
│   └── nbg-presentation-format/ # Legacy plugin (maintained)
└── templates/                  # Slide templates
```

## Shared Brand System

All agents reference the shared brand system at `shared/nbg-brand-system/`:
- `colors.md` - Complete color palette
- `typography.md` - Font specifications
- `layouts.md` - Slide layout catalog
- `charts.md` - Chart configurations
- `icons.md` - Icon design rules
- `dimensions.md` - Positioning reference

## Assets

| Asset | Path | Size |
|-------|------|------|
| Greek Logo | `assets/nbg-logo-gr.svg` | 214 x 62 px |
| English Logo | `assets/nbg-logo.svg` | 294 x 62 px |
| PNG Fallback | `assets/nbg-logo-fallback.png` | - |

## Template Files

- **EN**: `/Users/plessas/Downloads/Powerpoint - Version 1.0_EN.pptx`
- **GR**: `/Users/plessas/Downloads/Powerpoint - Version 1.0_GR.pptx`

## Installation

```bash
cd ~/.claude/plugins/marketplaces/
git clone https://github.com/weirdapps/comms-marketplace.git
```

## Usage Examples

### Create a Presentation
```
/create-presentation Q4 Digital Banking Results for Board
```

### Redesign Existing Deck
```
/redesign-deck /path/to/messy-presentation.pptx
```

### Create an Infographic
```
/create-infographic Timeline showing project milestones for 2024
```

### Create an Icon
```
/create-icon Mobile banking app icon
```

### Quick Polish
```
/polish-slides [paste content or path]
```

## Quality Standards

Every presentation must pass:
- [ ] Dimensions: 13.33" x 7.5" (LAYOUT_WIDE)
- [ ] Background: white (#FFFFFF)
- [ ] Font: Aptos throughout
- [ ] Logo: bottom-left on every slide
- [ ] One key message per slide
- [ ] Scannable in 5-7 seconds
- [ ] Board-ready appearance

## Version History

### v2.0.0 (Current)
- Multi-agent architecture
- Specialized agents for each task
- New commands
- Shared brand system

### v1.0.0 (Legacy)
- Monolithic nbg-presentation-format plugin
- Basic formatting guidelines

## License

Proprietary - Internal use only
