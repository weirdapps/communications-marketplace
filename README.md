# Comms Marketplace v2.1

Multi-agent presentation system for National Bank of Greece (NBG) corporate communications.

## Architecture

```
                    NBG PRESENTER
                  (Master Orchestrator)
                          |
        +-----------------+-----------------+
        v                 v                 v
  STORYLINE         STORYBOARD         GRAPHICS
  ARCHITECT          DESIGNER          RENDERER
        |                 |
        |    +------------+------------+
        |    v            v            v
        | INFOGRAPHIC    ICON       (Other)
        | SPECIALIST   DESIGNER
```

## Quick Start

```bash
# Create a presentation
/create-presentation Q4 Digital Banking Results for Board

# Redesign existing deck
/redesign-deck /path/to/presentation.pptx

# Create infographic or icon
/create-infographic Timeline for 2024 milestones
/create-icon Mobile banking app
```

## NBG Brand Essentials

### Slide Dimensions
```
Width:  13.33" (LAYOUT_WIDE)
Height: 7.5"
EMU:    12,192,000 x 6,858,000
```

### Colors (no # prefix for PptxGenJS)
| Name | Hex | Usage |
|------|-----|-------|
| Dark Teal | `003841` | Titles, icons |
| NBG Teal | `007B85` | Brand, section numbers |
| Cyan | `00ADBF` | Primary chart color |
| Bright Cyan | `00DFF8` | Accents, bullets |
| Dark Text | `202020` | Body text |
| Medium Gray | `939793` | Page numbers, muted text |
| Light Gray | `BEC1BE` | Subtle elements |
| Off-white | `F5F8F6` | Light backgrounds |
| White | `FFFFFF` | Default background |

### Chart Colors (in order)
```javascript
chartColors: ['00ADBF', '003841', '007B85', '939793', 'BEC1BE', '00DFF8']
```

### Typography
- **Primary Font**: Aptos
- **Fallback**: Arial, Calibri
- **Bullet Font**: Arial (character code '2022')

### Logo Placement (from Template)

**Small logo - for content slides (most common):**
```javascript
{ x: 0.374, y: 7.071, w: 0.822, h: 0.236 }
```

**Large logo - for covers and dividers:**
```javascript
{ x: 0.374, y: 6.271, w: 2.191, h: 0.630 }
```

### Page Numbers (Content Slides Only)
```javascript
{
  x: 12.2265, y: 7.1554, w: 0.748, h: 0.152,
  fontFace: 'Aptos', fontSize: 10, color: '939793',
  align: 'right', valign: 'middle', margin: 0
}
```
**Note:** Logo and page number are aligned at 0.19" from bottom edge.

### Back Cover
Plain white slide with centered oval NBG building logo:
```javascript
{ x: 5.44, y: 2.98, w: 2.45, h: 1.54 }  // Centered on slide
```

## Critical Rules

| Rule | Requirement |
|------|-------------|
| **NO pie charts** | Always use doughnut charts instead |
| **NO "Thank You" slides** | Use plain back cover with centered oval logo |
| **Page numbers** | Content slides ONLY - not cover, dividers, back cover |
| **Line charts** | Smooth curves, 3pt lines, visible markers (size 10) |
| **Chart axis colors** | Always specify explicit NBG colors to avoid defaults |
| **Text margins** | Always set `margin: 0` on all text boxes |
| **Text alignment** | Always use `valign: 'top'` - never middle or bottom |
| **Title box sizing** | Size to fit text (~0.4" for single-line, ~0.7" for two-line) |

## Agents

| Agent | Purpose | Output |
|-------|---------|--------|
| **NBG Presenter** | Master orchestrator | Workflow coordination |
| **Storyline Architect** | Narrative design | Slide-by-slide story with key messages |
| **Storyboard Designer** | Visual layout | Layout specs, positioning, element requirements |
| **Infographic Specialist** | Data visualization | Chart configs, diagram specs |
| **Icon Designer** | SVG icons | NBG-compliant SVG code |
| **Graphics Renderer** | PPTX production | Board-ready .pptx file |

## Commands

| Command | Description |
|---------|-------------|
| `/create-presentation` | Create new NBG presentation from content |
| `/redesign-deck` | Redesign existing presentation to NBG standards |
| `/create-infographic` | Generate NBG-branded data visualization |
| `/create-icon` | Create NBG-compliant SVG icon |
| `/polish-slides` | Quick formatting to NBG standards |

## Quality Standards

Every presentation must pass:
- [ ] Dimensions: 13.33" x 7.5" (LAYOUT_WIDE)
- [ ] Background: white (#FFFFFF)
- [ ] Font: Aptos throughout
- [ ] Small logo on content slides (0.822" x 0.236")
- [ ] Page numbers on content slides only (not cover, dividers, back cover)
- [ ] Page number and logo aligned at 0.19" from bottom
- [ ] All text boxes: `margin: 0`, `valign: 'top'`
- [ ] Title boxes sized to fit text (not oversized)
- [ ] No pie charts (use doughnut)
- [ ] No "Thank You" slides (use plain back cover)
- [ ] One key message per slide
- [ ] Scannable in 5-7 seconds

## Directory Structure

```
comms-marketplace/
├── orchestrator/nbg-presenter/     # Master orchestrator
├── agents/                         # Agent duplicates (legacy)
├── skills/                         # Active agent skills
│   ├── storyline-architect/
│   ├── storyboard-designer/
│   ├── infographic-specialist/
│   ├── icon-designer/
│   ├── graphics-renderer/
│   └── nbg-presenter/
├── shared/nbg-brand-system/        # Brand specifications
│   ├── colors.md
│   ├── typography.md
│   ├── layouts.md
│   ├── charts.md
│   ├── icons.md
│   └── dimensions.md
├── commands/                       # Slash commands
├── assets/                         # Logos, images
│   ├── nbg-logo-gr.svg            # Greek logo
│   ├── nbg-logo.svg               # English logo
│   ├── nbg-back-cover-logo.png    # Centered oval for back cover
│   └── NBG-PRESENTATION-SPEC.md   # Complete specification
└── plugins/nbg-presentation-format/ # Legacy plugin
```

## Assets

| Asset | Path | Size | Usage |
|-------|------|------|-------|
| Greek Logo | `assets/nbg-logo-gr.svg` | 214 x 62 px | Greek presentations |
| English Logo | `assets/nbg-logo.svg` | 294 x 62 px | English presentations |
| Back Cover Logo | `assets/nbg-back-cover-logo.png` | 245 x 154 px | Centered on back cover |

## Version History

### v2.2.0 (Current)
- All text boxes: margin: 0, valign: 'top'
- Title boxes sized to fit text (reduced heights)
- Updated layout constants with correct body positioning

### v2.1.0
- Fixed logo sizing (small for content, large for covers)
- Fixed page number positioning from template
- Added explicit chart axis color handling
- Updated back cover specifications
- Comprehensive documentation cleanup

### v2.0.0
- Multi-agent architecture
- Specialized agents for each task

### v1.0.0 (Legacy)
- Monolithic nbg-presentation-format plugin

## License

Proprietary - National Bank of Greece internal use only
