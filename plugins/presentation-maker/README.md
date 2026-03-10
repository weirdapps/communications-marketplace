# Presentation Maker v3.1

Multi-agent presentation system for National Bank of Greece (NBG) corporate communications. Create McKinsey-quality, board-ready presentations using a coordinated agent pipeline.

**Depends on**: `creative-toolkit` (icon-designer, infographic-specialist, device-mockup)

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
| `/create-infographic` | Generate data visualization *(via creative-toolkit)* |
| `/create-icon` | Create SVG icon *(via creative-toolkit)* |
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
presentation-maker/
├── plugin.json              # Plugin manifest (depends on creative-toolkit)
├── README.md                # This file
│
├── orchestrator/
│   └── nbg-presenter/       # Master orchestrator
│       └── SKILL.md
│
├── agents/                  # Core presentation agents
│   ├── storyline-architect/ # Narrative structure
│   ├── storyboard-designer/ # Visual layout
│   └── graphics-renderer/   # PPTX assembly
│   # icon-designer, infographic-specialist, device-mockup → creative-toolkit
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
│   └── polish-slides.md
│   # create-icon, create-infographic → creative-toolkit
│
├── assets/                  # Brand assets
│   ├── nbg-logo-gr.svg
│   ├── nbg-logo.svg
│   ├── nbg-back-cover-logo.png
│   ├── NBG-PRESENTATION-SPEC.md
│   ├── slide-catalog.yaml
│   ├── icons/               # Icon library (338 icons)
│   ├── illustrations/       # Illustration library
│   ├── bank-logos/
│   ├── screenshots/         # App screenshots for mockups
│   └── templates/
│
├── examples/                # Sample storylines
│   ├── executive-summary.yaml
│   ├── quarterly-report.yaml
│   └── strategy-deck.yaml
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

## Examples

Sample YAML storylines are available in `examples/`:

| Example | Use Case |
|---------|----------|
| `executive-summary.yaml` | Board-level summary presentations |
| `quarterly-report.yaml` | Detailed performance reports |
| `strategy-deck.yaml` | Strategic initiative proposals |

## Validation

Run the validation tool to check brand compliance:

```bash
python tools/nbg-presentation/nbg_validate.py presentation.pptx
```

The validator checks:
- Dimensions and aspect ratio
- Color palette compliance
- Font usage (Aptos required)
- Logo presence and sizing
- Back cover format (no "Thank You")
- Chart types (doughnut, not pie)
- Text margins and positioning

## Troubleshooting

### Font Issues: Aptos Not Displaying

**Problem**: Aptos font appears as placeholder or substitutes to another font.

**Solution**:
- Aptos is included with Microsoft 365 (2023+) and Windows 11
- For older systems, install Aptos from Microsoft fonts
- Use Arial as fallback - the system will automatically substitute if Aptos is unavailable
- Graphics Renderer will set both Aptos and Arial as font options

### Template Not Found

**Problem**: Build tool cannot find the NBG template.

**Solution**:
1. Verify templates exist in `assets/templates/`
2. Check that paths in `slide-catalog.yaml` are relative (not absolute)
3. Run from the plugin root directory

### Logo Not Appearing

**Problem**: Logo placeholder appears empty or shows wrong image.

**Solution**:
- Ensure `assets/nbg-logo-gr.svg` and `assets/nbg-logo.svg` exist
- For back cover, use `assets/nbg-back-cover-logo.png`
- Check that the logo is being inserted at the correct position (see dimensions.md)

### Validation Failures

**Problem**: `nbg_validate.py` reports errors.

| Error | Fix |
|-------|-----|
| "Pie chart found" | Replace all pie charts with doughnut charts |
| "Thank You slide" | Remove text, use plain back cover with centered logo only |
| "Wrong dimensions" | Ensure slide size is 13.33" x 7.5" (LAYOUT_WIDE) |
| "Non-NBG colors" | Use only colors from the approved palette in colors.md |
| "Font not Aptos" | Set all text to Aptos (Arial fallback) |

### Charts Not Rendering Correctly

**Problem**: Charts have wrong colors or formatting.

**Solution**:
- Use `nbg_chart_config.js` settings for chart configuration
- Apply colors in order: `['00ADBF', '003841', '007B85', '939793', 'BEC1BE', '00DFF8']`
- For line charts: use 3pt lines, no markers, smooth curves
- Never use pie charts - always use doughnut

### PPTX Build Fails

**Problem**: `nbg_build.py` throws an error.

**Solution**:
1. Install dependencies: `pip install -r tools/nbg-presentation/requirements.txt`
2. Ensure YAML storyline is valid: check for syntax errors
3. Verify all referenced assets exist

## License

Proprietary - National Bank of Greece internal use only
