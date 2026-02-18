# NBG Presentations Plugin v3.0

Multi-agent presentation system for National Bank of Greece (NBG) corporate communications. Create McKinsey-quality, board-ready presentations using a coordinated agent pipeline.

## Overview

This plugin provides a complete workflow for creating professional presentations that follow NBG brand guidelines and McKinsey quality standards.

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

## Commands

| Command | Description |
|---------|-------------|
| `/create-presentation` | Create new NBG presentation from content |
| `/redesign-deck` | Redesign existing presentation to NBG standards |
| `/create-infographic` | Generate NBG-branded data visualization |
| `/create-icon` | Create NBG-compliant SVG icon |
| `/polish-slides` | Quick formatting to NBG standards |

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
nbg-presentations/
├── plugin.json              # Plugin manifest
├── README.md                # This file
│
├── orchestrator/
│   └── nbg-presenter/       # Master orchestrator
│       └── SKILL.md
│
├── agents/                  # Specialist agents
│   ├── storyline-architect/
│   ├── storyboard-designer/
│   ├── graphics-renderer/
│   ├── infographic-specialist/
│   └── icon-designer/
│
├── shared/nbg-brand-system/ # Brand specifications
│   ├── README.md            # Brand quick reference
│   ├── colors.md            # Color palette
│   ├── typography.md        # Font specifications
│   ├── layouts.md           # Slide layouts
│   ├── dimensions.md        # Positioning reference
│   ├── charts.md            # Chart configurations
│   ├── icons.md             # Icon design rules
│   └── ooxml-charts.md      # OOXML chart editing
│
├── commands/                # Slash commands
│   ├── create-presentation.md
│   ├── redesign-deck.md
│   ├── create-infographic.md
│   ├── create-icon.md
│   └── polish-slides.md
│
├── assets/                  # Brand assets
│   ├── nbg-logo-gr.svg
│   ├── nbg-logo.svg
│   ├── nbg-back-cover-logo.png
│   ├── NBG-PRESENTATION-SPEC.md
│   ├── bank-logos/
│   └── templates/
│
└── tools/                   # Build tools
    └── nbg-presentation/
```

## NBG Brand Quick Reference

### Slide Dimensions
```
Width:  13.33" (LAYOUT_WIDE)
Height: 7.5"
```

### Primary Colors
| Name | Hex | Usage |
|------|-----|-------|
| Dark Teal | `003841` | Titles, icons |
| NBG Teal | `007B85` | Brand, section numbers |
| Cyan | `00ADBF` | Primary chart color |
| Bright Cyan | `00DFF8` | Accents, bullets |
| Dark Text | `202020` | Body text |
| White | `FFFFFF` | Backgrounds |

### Chart Colors (in order)
```javascript
['00ADBF', '003841', '007B85', '939793', 'BEC1BE', '00DFF8']
```

## Quality Standards

Every presentation must pass:
- [ ] Dimensions: 13.33" x 7.5" (LAYOUT_WIDE)
- [ ] Background: white (#FFFFFF)
- [ ] Font: Aptos throughout
- [ ] Correct logo sizes and positions
- [ ] Page numbers on content slides only
- [ ] No pie charts (use doughnut)
- [ ] No "Thank You" slides (use plain back cover)
- [ ] One key message per slide
- [ ] Scannable in 5-7 seconds

## McKinsey Quality Standards

- **Pyramid Principle**: Lead with the answer
- **SCQA Framework**: Situation, Complication, Question, Answer
- **One Message Per Slide**: No exceptions
- **Action Titles**: Full sentences that tell the story
- **5-7 Second Rule**: Every slide scannable at a glance

## License

Proprietary - National Bank of Greece internal use only
