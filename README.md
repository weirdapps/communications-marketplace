# Comms Marketplace v3.0

Multi-agent presentation system for National Bank of Greece (NBG) corporate communications. Create McKinsey-quality, board-ready presentations using a coordinated agent pipeline.

## Architecture

```
                    NBG PRESENTER
                  (Master Orchestrator)
                          |
        +-----------------+-----------------+
        v                 v                 v
  STORYLINE         STORYBOARD         GRAPHICS
  ARCHITECT          DESIGNER          RENDERER
                          |
            +-------------+-------------+
            v             v             v
       INFOGRAPHIC      ICON         (Other)
       SPECIALIST     DESIGNER
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

# Quick polish
/polish-slides [content]
```

## Directory Structure

```
comms-marketplace/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
│
├── orchestrator/
│   └── nbg-presenter/           # Master orchestrator
│       └── SKILL.md
│
├── agents/                      # Specialist agents
│   ├── storyline-architect/
│   │   └── SKILL.md
│   ├── storyboard-designer/
│   │   └── SKILL.md
│   ├── graphics-renderer/
│   │   └── SKILL.md
│   ├── infographic-specialist/
│   │   └── SKILL.md
│   └── icon-designer/
│       └── SKILL.md
│
├── shared/nbg-brand-system/     # SINGLE SOURCE OF TRUTH
│   ├── README.md                # Brand quick reference
│   ├── colors.md                # Complete color palette
│   ├── typography.md            # Font specifications
│   ├── layouts.md               # Slide layout catalog
│   ├── dimensions.md            # Positioning reference
│   ├── charts.md                # Chart configurations
│   ├── icons.md                 # Icon design rules
│   └── ooxml-charts.md          # OOXML chart editing
│
├── commands/                    # Slash commands
│   ├── create-presentation.md
│   ├── redesign-deck.md
│   ├── create-infographic.md
│   ├── create-icon.md
│   └── polish-slides.md
│
├── assets/                      # Brand assets
│   ├── nbg-logo-gr.svg          # Greek logo
│   ├── nbg-logo.svg             # English logo
│   ├── nbg-back-cover-logo.png  # Centered oval for back cover
│   ├── nbg-logo-fallback.png    # PNG fallback
│   ├── NBG-PRESENTATION-SPEC.md # Complete specification
│   ├── bank-logos/              # External bank logos
│   └── templates/               # PPTX templates
│       ├── NBG-Template-EN.pptx
│       └── NBG-Template-GR.pptx
│
└── README.md                    # This file
```

## NBG Brand Quick Reference

**Full Specification**: See `shared/nbg-brand-system/README.md`

### Slide Dimensions
```
Width:  13.33" (LAYOUT_WIDE)
Height: 7.5"
EMU:    12,192,000 x 6,858,000
```

### Primary Colors (no # prefix for PptxGenJS)
| Name | Hex | Usage |
|------|-----|-------|
| Dark Teal | `003841` | Titles, icons |
| NBG Teal | `007B85` | Brand, section numbers |
| Cyan | `00ADBF` | Primary chart color |
| Bright Cyan | `00DFF8` | Accents, bullets |
| Dark Text | `202020` | Body text |
| White | `FFFFFF` | **ALWAYS** for backgrounds |
| Off-white | `F5F8F6` | Light backgrounds for cards |

### Chart Colors (in order)
```javascript
['00ADBF', '003841', '007B85', '939793', 'BEC1BE', '00DFF8']
```

### Logo Placement (from Template)
| Type | Position | Size | Usage |
|------|----------|------|-------|
| Small | 0.374", 7.071" | 0.822" x 0.236" | Content slides |
| Large | 0.374", 6.271" | 2.191" x 0.630" | Covers, dividers |
| Back Cover | 5.44", 2.98" | 2.45" x 1.54" | Centered oval |

### Page Numbers
- **Position**: 12.2265", 7.1554" (0.748" x 0.152")
- **On**: Content, chart, table, infographic slides
- **NOT on**: Cover, divider, back cover

## Critical Rules

| Rule | Enforcement |
|------|-------------|
| **White backgrounds ONLY** | Never use dark themes |
| **NO pie charts** | Always use doughnut instead |
| **NO "Thank You" slides** | Use plain back cover with centered logo |
| **Page numbers** | Content slides only |
| **Content titles** | 24pt action titles (full sentences) |
| **Cover subtitle** | 36pt (not 48pt) |
| **Title weight** | Aptos Regular (not SemiBold) |
| **Text boxes** | `margin: 0`, `valign: 'top'` ALWAYS |
| **Line charts** | Smooth curves, 3pt lines, visible markers |
| **Chart colors** | ALWAYS specify explicit NBG colors |

## Agents

| Agent | Purpose | Output |
|-------|---------|--------|
| **NBG Presenter** | Master orchestrator | Workflow coordination |
| **Storyline Architect** | Narrative design | Slide-by-slide story with key messages |
| **Storyboard Designer** | Visual layout | Layout specs, positioning |
| **Infographic Specialist** | Data visualization | Chart configs, diagrams |
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
- [ ] Correct logo sizes and positions
- [ ] Page numbers on content slides only
- [ ] All text boxes: `margin: 0`, `valign: 'top'`
- [ ] No pie charts (use doughnut)
- [ ] No "Thank You" slides (use plain back cover)
- [ ] One key message per slide
- [ ] Scannable in 5-7 seconds

## McKinsey Quality Standards

- **Pyramid Principle**: Lead with the answer, support with arguments
- **SCQA Framework**: Situation, Complication, Question, Answer
- **One Message Per Slide**: No exceptions
- **Action Titles**: Full sentences that tell the story, not labels
- **5-7 Second Rule**: Every slide scannable at a glance
- **"So What?" Test**: Every slide must matter

## Version History

### v3.0.0 (Current)
- **Restructured**: Clean, deduplicated architecture
- **Single source of truth**: All brand specs in `shared/nbg-brand-system/`
- **Removed duplicates**: Eliminated `skills/` folder, merged into `agents/`
- **Removed legacy**: Removed `plugins/nbg-presentation-format/`
- **Enhanced plugin.json**: Proper agent registration for Claude Code
- **Harmonized specs**: Consistent specifications across all files

### v2.3.0
- User preference updates (cover subtitle: 36pt, content title: 24pt)
- Contents/TOC slide component
- Metric card component

### v2.0.0
- Multi-agent architecture
- Specialized agents for each task

### v1.0.0 (Legacy)
- Monolithic nbg-presentation-format plugin

## License

Proprietary - National Bank of Greece internal use only
