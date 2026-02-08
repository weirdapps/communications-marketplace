# Comms Marketplace Upgrade Plan

## Overview

Transform the existing monolithic `nbg-presentation-format` plugin into a **multi-agent orchestration system** with specialized agents for different aspects of presentation creation.

## Current State

```
comms-marketplace/
├── plugins/
│   └── nbg-presentation-format/
│       ├── skills/nbg-presentation-format/
│       │   ├── SKILL.md (single monolithic skill)
│       │   └── references/ (colors, charts, icons, layouts)
│       └── commands/
│           └── create-nbg-infographic.md
└── assets/ (logos, specs)
```

## Proposed Architecture

```
comms-marketplace/
├── orchestrator/
│   └── nbg-presenter.md          # Master orchestrator agent
├── agents/
│   ├── storyline-architect/         # Strategic narrative agent
│   ├── storyboard-designer/         # Visual planning agent
│   ├── infographic-specialist/      # Data visualization agent
│   ├── icon-designer/               # SVG icon generation agent
│   └── graphics-renderer/           # Pixel-perfect PPTX agent
├── shared/
│   └── nbg-brand-system/            # Shared brand references
│       ├── colors.md
│       ├── typography.md
│       ├── layouts.md
│       ├── charts.md
│       └── icons.md
├── templates/
│   └── slide-templates/             # Reusable slide patterns
└── assets/                          # Logos, images, fonts
```

---

## Agent Definitions

### 1. NBG Presenter (Orchestrator)

**Role:** Master conductor that coordinates all specialist agents

**Responsibilities:**
- Analyze input (raw content, existing PPTX, or brief)
- Determine which agents to invoke and in what sequence
- Manage handoffs between agents
- Quality control final output
- Ensure brand consistency across all outputs

**Workflow:**
```
Input → Storyline Architect → Storyboard Designer →
  ├── Infographic Specialist (for data slides)
  ├── Icon Designer (for custom icons)
  └── Graphics Renderer (final assembly)
```

**Trigger Phrases:**
- "Create NBG presentation"
- "Redesign this deck"
- "Make this board-ready"
- "Polish this presentation"

---

### 2. Storyline Architect

**Role:** Strategic narrative designer

**Purpose:** Transform raw content into a compelling executive storyline

**Inputs:**
- Raw content (text, bullets, data)
- Existing messy presentation
- Brief or outline

**Outputs:**
- Slide-by-slide narrative outline
- Key message per slide
- Logical flow structure
- Executive summary points
- Recommended slide types (cover, divider, content, chart, etc.)

**Key Capabilities:**
- Identify the ONE key message per slide
- Create insight-driven slide titles (not generic)
- Structure content for 5-7 second scanability
- Determine optimal slide sequence
- Identify data that needs visualization vs. text

**Output Format:**
```yaml
presentation:
  title: "Q4 Digital Banking Performance"
  audience: "Board of Directors"
  slides:
    - type: cover
      title: "Q4 Digital Banking Results"
      subtitle: "Exceeding Expectations"

    - type: divider
      number: "01"
      title: "Executive Summary"

    - type: content
      key_message: "Digital adoption grew 47% YoY"
      supporting_points:
        - "Mobile app downloads: 2.3M"
        - "Active digital users: 1.8M"
      recommended_visual: "bar_chart"
```

---

### 3. Storyboard Designer

**Role:** Visual layout strategist

**Purpose:** Decide HOW each slide should look to best support its message

**Inputs:**
- Storyline from Storyline Architect
- Original content/data

**Outputs:**
- Visual layout recommendation per slide
- Placement grid specifications
- Visual element requirements
- Infographic briefs for complex data
- Icon requirements

**Key Capabilities:**
- Match content type to optimal NBG layout
- Balance text vs. visual elements
- Determine chart types for data
- Identify when custom infographics are needed
- Specify exact positioning (x, y, w, h)

**Output Format:**
```yaml
slide_3:
  layout: "Page 1/2 _Image Right"
  elements:
    - type: title
      content: "47% Digital Adoption Growth"
      position: {x: 0.37, y: 0.6, w: 5.5}

    - type: chart
      chart_type: bar
      position: {x: 6.5, y: 1.5, w: 5.2, h: 4.2}
      data_brief: "YoY comparison of digital metrics"
      colors: ["00ADBF", "007B85"]

    - type: callout
      content: "+47%"
      style: "large_number_highlight"
      position: {x: 6.5, y: 1.0}
```

---

### 4. Infographic Specialist

**Role:** Data visualization expert

**Purpose:** Transform complex data into clear, NBG-branded visual stories

**Inputs:**
- Data sets (tables, numbers, metrics)
- Visual brief from Storyboard Designer
- Context from Storyline Architect

**Outputs:**
- Infographic specifications
- Chart configurations
- Data visualization code
- Custom diagram SVGs

**Specialized Capabilities:**

#### A. Chart Generation
- Bar, column, line, doughnut, pie, area, waterfall
- Multi-series comparisons
- Trend analysis visuals

#### B. Process Diagrams
- Sequential steps (01, 02, 03...)
- Funnel/converging flows
- Timelines and roadmaps
- Horizontal process flows

#### C. Comparison Layouts
- Before/after
- Side-by-side metrics
- Grid comparisons (3x3, 2x3)

#### D. KPI Dashboards
- Large number displays
- Status indicators (RAG colors)
- Trend arrows

**Output Format:**
```javascript
// Chart specification
{
  type: "bar",
  data: [
    { name: "Q1", values: [12, 15, 18] },
    { name: "Q2", values: [18, 22, 28] }
  ],
  colors: ["00ADBF", "003841", "007B85"],
  config: {
    barGapWidthPct: 30,
    showValue: true,
    valueFontBold: true
  }
}
```

---

### 5. Icon Designer

**Role:** NBG-compliant icon generator

**Purpose:** Create custom SVG icons that match NBG iconography exactly

**Inputs:**
- Icon concept/description
- Context (slide type, background color)
- Size requirements

**Outputs:**
- Production-ready SVG code
- Multiple color variants if needed

**Design Rules:**
- 64x64 canvas, viewBox="0 0 64 64"
- Solid fill only (no strokes)
- Single color per icon (monochrome)
- Simple geometric shapes
- ~5-8px padding from edges
- Optically centered

**Color Mapping:**
| Context | Fill Color |
|---------|------------|
| Standard (white bg) | `#003841` |
| Dark background | `#F5F8F6` |
| Accent/highlight | `#00DEF8` |
| Success | `#73AF3C` |
| Alert | `#AA0028` |

**Output Format:**
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">
  <path fill="#003841" d="M32 8c-13.25 0-24 10.75-24 24s10.75 24 24 24 24-10.75 24-24-10.75-24-24-24zm0 44c-11.05 0-20-8.95-20-20s8.95-20 20-20 20 8.95 20 20-8.95 20-20 20z"/>
</svg>
```

---

### 6. Graphics Renderer

**Role:** Pixel-perfect PPTX production specialist

**Purpose:** Assemble final presentation with exact NBG formatting

**Inputs:**
- Storyboard specifications
- Generated infographics
- Custom icons
- Content text

**Outputs:**
- Production-ready .pptx file
- Exact NBG brand compliance

**Technical Specifications:**

#### Slide Setup
- Dimensions: 12.192" x 6.858" (custom NBG)
- Background: #FFFFFF (default)
- Font: Aptos (Arial fallback)

#### Text Formatting
| Element | Size | Color | Weight |
|---------|------|-------|--------|
| Cover title | 48pt | #003841 | Regular |
| Section number | 60pt | #007B85 | Regular |
| Page title | 24pt | #003841 | Regular |
| Body text | 11pt | #202020 | Regular |
| Bullets | 24/20/18pt | #202020 | Regular |

#### Bullet Points
- Character: • (Unicode 2022)
- Font: Arial
- Color: #00DFF8

#### Logo Placement
- Position: (0.34", 5.9")
- Greek: 2.14" x 0.62"
- English: 2.94" x 0.62"

#### Text Box Rules
- All margins: 0
- Line spacing: 0.9-1.1 depending on element

**Quality Checklist:**
- [ ] Slide dimensions are 12.192" x 6.858"
- [ ] Background is white (#FFFFFF)
- [ ] Titles use Dark Teal (#003841)
- [ ] Body text uses #202020
- [ ] All text boxes have margin: 0
- [ ] Logo in bottom-left corner
- [ ] Font is Aptos
- [ ] Section numbers use "01", "02" format
- [ ] Charts use NBG color sequence
- [ ] Bullets use Bright Cyan (#00DFF8)

---

## Orchestration Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     NBG PRESENTER                             │
│                    (Master Orchestrator)                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   STORYLINE ARCHITECT                            │
│  • Analyze input content                                         │
│  • Create narrative structure                                    │
│  • Define key message per slide                                  │
│  • Recommend slide types                                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   STORYBOARD DESIGNER                            │
│  • Choose layouts for each slide                                 │
│  • Specify visual elements                                       │
│  • Define positioning                                            │
│  • Identify custom visual needs                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┼─────────┐
                    ▼         ▼         ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ INFOGRAPHIC  │  │    ICON      │  │              │
│ SPECIALIST   │  │   DESIGNER   │  │   (Other)    │
│              │  │              │  │              │
│ Charts       │  │ Custom SVG   │  │              │
│ Diagrams     │  │ icons        │  │              │
│ Timelines    │  │              │  │              │
└──────────────┘  └──────────────┘  └──────────────┘
                    │         │         │
                    └─────────┼─────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    GRAPHICS RENDERER                             │
│  • Assemble all elements                                         │
│  • Apply exact formatting                                        │
│  • Generate pixel-perfect PPTX                                   │
│  • Quality assurance                                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                      [Final PPTX Output]
```

---

## Implementation Phases

### Phase 1: Foundation (Week 1)
- [ ] Create new directory structure
- [ ] Migrate shared brand references
- [ ] Create NBG Presenter orchestrator skeleton
- [ ] Define inter-agent communication format (YAML/JSON)

### Phase 2: Core Agents (Week 2)
- [ ] Implement Storyline Architect agent
- [ ] Implement Storyboard Designer agent
- [ ] Create communication protocol between agents
- [ ] Test end-to-end flow with simple presentation

### Phase 3: Specialist Agents (Week 3)
- [ ] Implement Infographic Specialist agent
- [ ] Implement Icon Designer agent
- [ ] Enhance Graphics Renderer with PptxGenJS patterns
- [ ] Create template library

### Phase 4: Integration & Polish (Week 4)
- [ ] Full orchestration testing
- [ ] Error handling and fallbacks
- [ ] Performance optimization
- [ ] Documentation and examples

---

## File Structure (Detailed)

```
comms-marketplace/
├── .claude-plugin/
│   └── plugin.json                    # Updated plugin manifest
│
├── orchestrator/
│   ├── nbg-presenter/
│   │   ├── SKILL.md                   # Master orchestrator skill
│   │   ├── workflow.md                # Orchestration logic
│   │   └── quality-gates.md           # QA checkpoints
│   └── triggers.md                    # Phrase triggers
│
├── agents/
│   ├── storyline-architect/
│   │   ├── SKILL.md                   # Agent skill definition
│   │   ├── prompts/
│   │   │   ├── analyze-content.md
│   │   │   ├── create-narrative.md
│   │   │   └── executive-summary.md
│   │   └── examples/
│   │       └── sample-storylines.yaml
│   │
│   ├── storyboard-designer/
│   │   ├── SKILL.md
│   │   ├── layout-selector.md         # Layout decision logic
│   │   ├── visual-rules.md            # Visual hierarchy rules
│   │   └── examples/
│   │       └── sample-storyboards.yaml
│   │
│   ├── infographic-specialist/
│   │   ├── SKILL.md
│   │   ├── chart-generator.md
│   │   ├── diagram-patterns.md
│   │   ├── timeline-builder.md
│   │   └── templates/
│   │       ├── bar-chart.yaml
│   │       ├── process-flow.yaml
│   │       └── kpi-dashboard.yaml
│   │
│   ├── icon-designer/
│   │   ├── SKILL.md
│   │   ├── design-rules.md
│   │   ├── svg-patterns.md
│   │   └── icon-library/
│   │       └── common-icons.md        # Pre-built icons
│   │
│   └── graphics-renderer/
│       ├── SKILL.md
│       ├── pptx-generator.md          # PptxGenJS patterns
│       ├── formatting-rules.md
│       ├── quality-checklist.md
│       └── templates/
│           ├── cover-slide.js
│           ├── divider-slide.js
│           ├── content-slide.js
│           └── chart-slide.js
│
├── shared/
│   └── nbg-brand-system/
│       ├── README.md                  # Brand overview
│       ├── colors.md                  # Complete color palette
│       ├── typography.md              # Font specifications
│       ├── layouts.md                 # Slide layout catalog
│       ├── charts.md                  # Chart configurations
│       ├── icons.md                   # Icon design specs
│       └── dimensions.md              # Slide dimensions & margins
│
├── templates/
│   └── slide-templates/
│       ├── cover-variants.md
│       ├── divider-variants.md
│       ├── content-layouts.md
│       └── infographic-patterns.md
│
├── assets/
│   ├── nbg-logo-gr.svg
│   ├── nbg-logo.svg
│   ├── nbg-logo-fallback.png
│   └── NBG-PRESENTATION-SPEC.md
│
├── commands/
│   ├── create-presentation.md         # /create-presentation
│   ├── redesign-deck.md               # /redesign-deck
│   ├── create-infographic.md          # /create-infographic
│   ├── create-icon.md                 # /create-icon
│   └── polish-slides.md               # /polish-slides
│
└── README.md
```

---

## Inter-Agent Communication Protocol

### Message Format

```yaml
# Standard message envelope
message:
  from: "storyline-architect"
  to: "storyboard-designer"
  type: "storyline_complete"
  correlation_id: "pres-2024-001"
  payload:
    # Agent-specific content
```

### Storyline → Storyboard Handoff

```yaml
handoff:
  presentation_id: "pres-2024-001"
  title: "Q4 Digital Banking Performance"
  audience: "Board of Directors"
  total_slides: 12

  slides:
    - slide_id: 1
      type: cover
      key_message: "Digital Banking Exceeds Expectations"
      content:
        title: "Q4 Digital Banking Results"
        subtitle: "Exceeding All Targets"
        date: "January 2024"
        location: "Athens, Greece"

    - slide_id: 2
      type: divider
      key_message: "Executive Summary Introduction"
      content:
        number: "01"
        title: "Executive Summary"

    - slide_id: 3
      type: content
      key_message: "47% digital adoption growth"
      content:
        title: "Digital Adoption Accelerates"
        points:
          - "Mobile app downloads: 2.3M (+47% YoY)"
          - "Active digital users: 1.8M"
          - "Digital transactions: €4.2B"
      data_for_visualization:
        - metric: "YoY Growth"
          values: [{"Q4 2023": 1.2M}, {"Q4 2024": 1.8M}]
      recommended_visual: "bar_chart_with_callout"
```

### Storyboard → Graphics Renderer Handoff

```yaml
handoff:
  presentation_id: "pres-2024-001"

  slides:
    - slide_id: 3
      layout: "Page 1/2 _Image Right"
      background: "#FFFFFF"

      elements:
        - id: "title"
          type: text
          content: "Digital Adoption Accelerates"
          position: {x: 0.37, y: 0.6, w: 5.5, h: 0.8}
          style:
            font: "Aptos"
            size: 24
            color: "003841"
            bold: false

        - id: "bullets"
          type: text
          content:
            - "Mobile app downloads: 2.3M (+47% YoY)"
            - "Active digital users: 1.8M"
            - "Digital transactions: €4.2B"
          position: {x: 0.37, y: 1.5, w: 5.5, h: 3.5}
          style:
            font: "Aptos"
            size: 12
            color: "202020"
            bullet_color: "00DFF8"

        - id: "chart_1"
          type: chart
          chart_type: bar
          position: {x: 6.2, y: 1.2, w: 5.5, h: 4.0}
          data:
            categories: ["Q4 2023", "Q4 2024"]
            series:
              - name: "Digital Users"
                values: [1.2, 1.8]
          config:
            colors: ["00ADBF", "007B85"]
            showValue: true
            barGapWidthPct: 30

        - id: "callout"
          type: shape
          shape_type: rectangle
          position: {x: 6.2, y: 0.8, w: 1.5, h: 0.6}
          style:
            fill: "00DFF8"
            text: "+47%"
            textColor: "003841"
            fontSize: 18
            bold: true

        - id: "logo"
          type: image
          path: "assets/nbg-logo-gr.svg"
          position: {x: 0.34, y: 5.9, w: 2.14, h: 0.62}
```

---

## Commands (Slash Commands)

### /create-presentation

```markdown
---
description: "Create a new NBG-branded presentation from content"
argument-hint: "[topic or content]"
allowed-tools: Task(nbg-presenter), Task(storyline-architect), Task(storyboard-designer), Task(graphics-renderer)
---

Orchestrate full presentation creation using all specialist agents.
```

### /redesign-deck

```markdown
---
description: "Redesign an existing presentation to NBG standards"
argument-hint: "[path to PPTX]"
allowed-tools: Task(nbg-presenter), Task(storyline-architect), Task(storyboard-designer), Task(graphics-renderer)
---

Analyze and redesign an existing presentation.
```

### /create-infographic

```markdown
---
description: "Create an NBG-branded infographic"
argument-hint: "[data or description]"
allowed-tools: Task(infographic-specialist), Skill(manage-nano-banana)
---

Generate infographic using the Infographic Specialist.
```

### /create-icon

```markdown
---
description: "Generate an NBG-compliant SVG icon"
argument-hint: "[icon concept]"
allowed-tools: Task(icon-designer)
---

Create a custom icon following NBG iconography rules.
```

### /polish-slides

```markdown
---
description: "Quick polish of existing slides"
argument-hint: "[slide numbers or content]"
allowed-tools: Task(graphics-renderer)
---

Apply NBG formatting to existing content without full redesign.
```

---

## Quality Gates

### Gate 1: Storyline Review
- [ ] Every slide has ONE clear key message
- [ ] Slide titles are insight-driven (not generic)
- [ ] Logical flow from slide to slide
- [ ] Appropriate slide type for each content block

### Gate 2: Storyboard Review
- [ ] Layout matches content type
- [ ] Visual elements support (not distract from) message
- [ ] Proper white space and breathing room
- [ ] All positioning within NBG margins

### Gate 3: Visual Assets Review
- [ ] Charts use NBG color sequence
- [ ] Icons are 64x64, solid fill, monochrome
- [ ] Infographics follow NBG patterns
- [ ] All colors from NBG palette

### Gate 4: Final Output Review
- [ ] Slide dimensions: 12.192" x 6.858"
- [ ] Background: white (#FFFFFF)
- [ ] All fonts: Aptos (or Arial fallback)
- [ ] All margins: 0 on text boxes
- [ ] Logo: bottom-left, correct size
- [ ] Section numbers: "01" format, NBG Teal
- [ ] Scannable in 5-7 seconds per slide
- [ ] Board-ready appearance

---

## Migration Strategy

### Step 1: Parallel Operation
- Keep existing `nbg-presentation-format` functional
- Build new multi-agent system alongside
- Test with controlled inputs

### Step 2: Feature Parity
- Ensure new system can do everything old system does
- Add new capabilities (storyline, storyboard)
- Validate output quality

### Step 3: Cutover
- Deprecate old monolithic skill
- Update triggers to point to new orchestrator
- Monitor and iterate

### Step 4: Enhancement
- Add more infographic patterns
- Expand icon library
- Improve automation

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Brand compliance | 100% |
| Slides per hour | 10+ |
| First-time quality pass | 90% |
| User satisfaction | 4.5/5 |
| Error rate | < 5% |

---

## Next Steps

1. **Immediate:** Review and approve this architecture
2. **Week 1:** Create directory structure and shared brand system
3. **Week 2:** Implement core agents (Storyline, Storyboard)
4. **Week 3:** Implement specialist agents (Infographic, Icon, Renderer)
5. **Week 4:** Full integration, testing, and documentation
