---
name: nbg-presentation-format
description: Create presentations and visual assets following National Bank of Greece (NBG) corporate brand guidelines. Use when creating presentations in NBG format, generating NBG-styled icons, charts, or any visual content for National Bank of Greece.
---

# NBG Presentation Format Skill

## Purpose

Generate **McKinsey-quality, board-ready** presentations that match the National Bank of Greece corporate design system. Every deck should meet the standard expected by C-level executives and Board of Directors.

## McKinsey-Quality Multi-Agent Workflow

For complex presentations, use the specialized agent pipeline:

### Agent Pipeline
```
INPUT → Storyline Architect → Storyboard Designer → Specialists → Graphics Renderer → OUTPUT
```

| Agent | Purpose | Skill Location |
|-------|---------|----------------|
| **Storyline Architect** | Strategic narrative, Pyramid Principle, SCQA | `skills/storyline-architect/` |
| **Storyboard Designer** | Visual layouts, exact positioning | `skills/storyboard-designer/` |
| **Infographic Specialist** | Charts, KPI dashboards, diagrams | `skills/infographic-specialist/` |
| **Icon Designer** | Custom NBG-compliant icons | `skills/icon-designer/` |
| **Graphics Renderer** | Pixel-perfect PPTX assembly | `skills/graphics-renderer/` |
| **NBG Presenter** | Master orchestrator | `skills/nbg-presenter/` |

### McKinsey Quality Standards
- **Pyramid Principle**: Lead with the answer, support with arguments
- **SCQA Framework**: Situation → Complication → Question → Answer
- **One Message Per Slide**: No exceptions
- **Action Titles**: Full sentences that tell the story, not labels
- **5-7 Second Rule**: Every slide scannable at a glance
- **"So What?" Test**: Every slide must matter

## Technical Specifications

## Quick Reference

### Slide Dimensions (CRITICAL)
- **EMU**: 12,192,000 x 6,858,000 (NBG template standard)
- **Inches**: 13.33" x 7.5" (use LAYOUT_WIDE in PptxGenJS)
- **Aspect Ratio**: 16:9 widescreen

**Note**: Use `pptx.layout = 'LAYOUT_WIDE'` - do NOT use custom defineLayout.

### Primary Colors
| Name | Hex | Usage |
|------|-----|-------|
| Dark Teal | `#003841` | Titles, headings, icons |
| NBG Teal | `#007B85` | Primary brand, section numbers |
| Bright Cyan | `#00DFF8` | Primary accent, bullets |
| Off-white | `#F5F8F6` | Light backgrounds |
| Dark Text | `#202020` | Body text |

### Fonts
- **Primary**: Aptos (all weights)
- **Bullets**: Arial
- **Fallback**: Calibri, Tahoma

### Logo Placement
- **Position**: Bottom-left corner (x=0.34", y=6.6")
- **Greek logo**: 2.14" x 0.62" (preferred)
- **English logo**: 2.94" x 0.62"
- **Assets**: `../../assets/` (relative to this skill)

## Automated Tools (Recommended)

Use the NBG presentation tools for streamlined workflow:

### NBG Builder (One-Step Creation)
```bash
python ~/.claude/plugins/marketplaces/comms-marketplace/tools/nbg-presentation/nbg_build.py outline.yaml output.pptx
```

### Chart Data Injection
```bash
python ~/.claude/plugins/marketplaces/comms-marketplace/tools/nbg-presentation/inject_chart_data.py input.pptx config.json output.pptx
```

### Table Data Injection
```bash
python ~/.claude/plugins/marketplaces/comms-marketplace/tools/nbg-presentation/inject_table_data.py input.pptx config.json output.pptx
```

### Brand Validation
```bash
python ~/.claude/plugins/marketplaces/comms-marketplace/tools/nbg-presentation/nbg_validate.py presentation.pptx
```

### Slide Catalog
See `~/.claude/plugins/marketplaces/comms-marketplace/assets/slide-catalog.yaml` for semantic slide type mappings.

---

## Manual Slide Creation Workflow

### Step 1: Set Up Presentation
```javascript
const PptxGenJS = require('pptxgenjs');
const pptx = new PptxGenJS();

// Use LAYOUT_WIDE (13.33" x 7.5") to match NBG template EMU values
pptx.layout = 'LAYOUT_WIDE';
```

### Step 2: Apply NBG Styles
```javascript
const NBG = {
  colors: {
    darkTeal: '003841',
    teal: '007B85',
    brightCyan: '00DFF8',
    offWhite: 'F5F8F6',
    darkText: '202020',
    white: 'FFFFFF',
  },
  fonts: {
    primary: 'Aptos',
    bullet: 'Arial',
  },
  chartColors: ['00ADBF', '003841', '007B85', '939793', 'BEC1BE', '00DFF8'],
};
```

### Step 3: Use White Backgrounds
**IMPORTANT**: Always use white/light backgrounds unless specifically requested.
- Slide background: `#FFFFFF` or `#F5F8F6`
- Text color: `#202020` (body) or `#003841` (titles)

### Step 4: Add Logo
```javascript
// Assets located in comms-marketplace/assets/
slide.addImage({
  path: 'assets/nbg-logo-gr.svg',  // or absolute path to marketplace assets
  x: 0.34, y: 6.6, w: 2.14, h: 0.62
});
```

## Slide Types

### Cover Slide
- Title: 48pt Aptos, Dark Teal
- Subtitle: 48pt Aptos, NBG Teal
- Location/Date at bottom

### Section Divider
- Section number: 60pt Aptos, NBG Teal (#007B85)
- Title: 60pt Aptos, Dark Teal (#003841)
- Format: "01", "02", "03" etc.

### Content Slide
- Title: 24pt Aptos, Dark Teal
- Body: 11-12pt Aptos, Dark Text (#202020)
- Bullets: Bright Cyan (#00DFF8)
- Text box margins: 0 on all sides

### Back Cover Slide
- **Always include** a plain back cover slide as the final slide
- Use template slides 190-193 (plain with NBG logo only)
- **Do NOT use "Thank You" slides** (slide 195) - these are not wanted

## Text Formatting Rules

### Font Sizes
| Element | Size |
|---------|------|
| Cover title | 48pt |
| Divider number | 60pt |
| Page title | 24pt |
| Body text | 11-12pt |
| Bullet L1 | 24pt |
| Bullet L2 | 20pt |
| Bullet L3 | 18pt |
| Footnotes | 8pt |

### Text Box Settings
**CRITICAL**: All text boxes must use zero margins:
```javascript
margin: 0  // or margin: [0, 0, 0, 0]
```

### Bullet Points
- Character: • (Unicode 2022)
- Font: Arial
- Color: Bright Cyan (#00DFF8)

## Charts

### Color Sequence (in order)
1. `#00ADBF` - Cyan (primary)
2. `#003841` - Dark Teal
3. `#007B85` - NBG Teal
4. `#939793` - Medium Gray
5. `#BEC1BE` - Light Gray
6. `#00DFF8` - Bright Cyan

### Chart Types Available
- Bar/Column charts
- Line charts
- Doughnut charts
- Pie charts
- Area charts
- Waterfall charts

### Best Practices
- Use max 3-4 colors per chart
- Remove unnecessary gridlines
- Position data labels at "outEnd"
- Legend at top or right

## Tables

### Table Style
- Header: Dark Teal (#003841) with white text
- Body cells: Light teal tint
- Borders: White (#FFFFFF), 1pt
- Font: Aptos, 10-11pt

## Icons

See `references/icons.md` for complete icon specifications.

### Icon Quick Reference
- **Canvas**: 64 x 64 px, viewBox="0 0 64 64"
- **Style**: Solid fill, no strokes (stroke-width="0")
- **Colors**:
  - Standard: `#003841` (Dark Teal)
  - On dark backgrounds: `#F5F8F6` (Off-white)
  - Accent: `#00DEF8` (Bright Cyan)
- **Design**: Simple geometric shapes, monochrome

## Detailed References

- **Icons**: See [references/icons.md](references/icons.md) for complete icon design specifications
- **Colors**: See [references/colors.md](references/colors.md) for full color palette
- **Charts**: See [references/charts.md](references/charts.md) for chart configurations
- **Layouts**: See [references/layouts.md](references/layouts.md) for slide layout catalog

## Template Files

- **EN Template**: `~/.claude/plugins/marketplaces/comms-marketplace/assets/templates/NBG-Template-EN.pptx`
- **GR Template**: `~/.claude/plugins/marketplaces/comms-marketplace/assets/templates/NBG-Template-GR.pptx`
- **Logo assets**: `~/.claude/plugins/marketplaces/comms-marketplace/assets/`
  - `nbg-logo-gr.svg` - Greek logo (214 × 62 px)
  - `nbg-logo.svg` - English logo (294 × 62 px)
  - `nbg-logo-fallback.png` - PNG fallback
- **Full spec**: `~/.claude/plugins/marketplaces/comms-marketplace/assets/NBG-PRESENTATION-SPEC.md`

## Common Patterns

### Infographic Layouts
- **Numbered grid**: 3x3 items with numbers 1-9
- **Sequential steps**: "01", "02", "03" format
- **Funnel/process**: Converging stages
- **Timeline**: Month headers with date markers

### Two-Column Layout
Preferred for slides with charts/tables:
- Text/bullets in left column (40%)
- Chart/table in right column (60%)

### Status Colors (for tables/charts only)
| Status | Hex |
|--------|-----|
| Deep Red | `#CB0030` |
| Red | `#F60037` |
| Orange | `#FF7F1A` |
| Yellow | `#FFDC00` |
| Green | `#5D8D2F` |
| Bright Green | `#90DC48` |

### Segment Colors
| Segment | Hex |
|---------|-----|
| Business | `#0D90FF` |
| Corporate | `#73AF3C` |
| Premium | `#D9A757` |
| Private | `#AA0028` |

## Quality Checklist

### McKinsey Standards (Content)
- [ ] Pyramid Principle applied: Answer first, then support
- [ ] Every slide has exactly ONE key message
- [ ] All titles are insight-driven ACTION TITLES (full sentences)
- [ ] Every slide passes "So What?" test
- [ ] Read-through test: Titles alone tell the complete story
- [ ] Arguments are MECE (Mutually Exclusive, Collectively Exhaustive)

### NBG Brand Compliance (Visual)
- [ ] Slide dimensions: 12192000 x 6858000 EMU (LAYOUT_WIDE = 13.33" x 7.5")
- [ ] Background is white (#FFFFFF) or off-white (#F5F8F6)
- [ ] Titles use Dark Teal (#003841)
- [ ] Body text uses Dark Text (#202020)
- [ ] All text boxes have margin: 0
- [ ] Logo placed in bottom-left corner (0.34", 6.6")
- [ ] Font is Aptos (or Arial fallback)
- [ ] Section numbers use "01", "02" format with NBG Teal
- [ ] Charts use NBG color sequence
- [ ] Bullets use Bright Cyan (#00DFF8)
- [ ] Scannable in 5-7 seconds
- [ ] Plain back cover (no "Thank You" slides)
- [ ] Quiet covers/dividers preferred (minimal decorative elements)

### Accessibility & Readability
- [ ] **Contrast ratio**: Minimum 4.5:1 for body text, 3:1 for large text (WCAG AA)
- [ ] **Font colors match backgrounds**:
  - Light backgrounds (#FFFFFF, #F5F8F6): Use Dark Teal (#003841) or Dark Text (#202020)
  - Dark backgrounds (#003841, #007B85): Use White (#FFFFFF) or Off-white (#F5F8F6)
- [ ] **Minimum font sizes**: 24pt body for large rooms, 12pt minimum for handouts
- [ ] **Elements within bounds**: All content inside safe margins (0.37" from edges)
- [ ] **No text on busy backgrounds**: Avoid placing text over complex images/patterns
- [ ] **Color not sole indicator**: Don't rely only on color to convey meaning
