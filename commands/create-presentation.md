---
description: "Create a new NBG-branded presentation from content or brief"
argument-hint: "[topic, content, or brief]"
allowed-tools: Task, Read, Write, Bash, Skill(manage-nano-banana), Skill(document-skills:pptx)
---

<objective>
Create a professional, board-ready presentation following NBG brand guidelines.

User request: $ARGUMENTS
</objective>

<process>
## McKinsey-Quality Orchestration Workflow

### 1. Analyze Input & Apply Pyramid Principle
- Determine input type (raw content, brief, data)
- Identify audience and purpose
- **Lead with the answer**: What is the main recommendation?
- Structure using SCQA (Situation-Complication-Question-Answer)

### 2. Storyline Creation (Storyline Architect)
Use the Storyline Architect skill to create narrative structure:
- Apply **Pyramid Principle**: Answer first, then support
- Define **ONE key message per slide** (no exceptions)
- Create **insight-driven ACTION TITLES** (full sentences, not labels)
- Apply **"So What?" test**: Why does each slide matter?
- Ensure arguments are **MECE** (Mutually Exclusive, Collectively Exhaustive)
- Recommend slide types and visualizations
- Create executive summary using SCR framework

### 3. Storyboard Design (Storyboard Designer)
Use the Storyboard Designer skill for visual layout:
- Select appropriate NBG layouts for each slide type
- Specify exact positioning (pixels, not approximations)
- Apply visual hierarchy to emphasize key message
- Identify custom visual needs (charts, icons, infographics)
- Ensure adequate white space (don't crowd slides)

### 4. Asset Generation (if needed)
- **Infographic Specialist**: Charts, diagrams, KPI dashboards
- **Icon Designer**: Custom NBG-compliant icons
- **manage-nano-banana**: Complex infographics requiring image generation
- Apply semantic colors: green=good, red=bad, gray=neutral

### 5. Final Assembly (Graphics Renderer)
Use Graphics Renderer or document-skills:pptx to create pixel-perfect PPTX:
- Dimensions: 13.33" x 7.5" (LAYOUT_WIDE) (NBG custom, NOT standard)
- Background: white (#FFFFFF)
- Font: Aptos (Arial fallback)
- Logo in bottom-left (0.34", 5.9")
- Bullets: Bright Cyan (#00DFF8)
- All text boxes: margin: 0

### 6. McKinsey Quality Check
- **Read-Through Test**: Read only titles - do they tell the story?
- **5-7 Second Test**: Is each slide scannable?
- **Brand Compliance**: All NBG specs followed?
- **"So What?" Passed**: Does every slide contribute?
- **Professional Appearance**: Board-ready?
</process>

<nbg_essentials>
## NBG Quick Reference

### Dimensions
- EMU: 12,192,000 x 6,858,000
- Inches: 13.33" x 7.5" (use LAYOUT_WIDE)

### Colors (no # for PptxGenJS)
- Title: 003841 (Dark Teal)
- Body: 202020 (Dark Text)
- Section numbers: 007B85 (NBG Teal)
- Bullets: 00DFF8 (Bright Cyan)
- Background: FFFFFF (White)

### Logo
- Position: (0.34", 6.6")
- Size (Greek): 2.14" x 0.62"
</nbg_essentials>

<success_criteria>
## McKinsey Quality Standards

### Structure
- [ ] Pyramid Principle applied: Answer first, then support
- [ ] SCQA framework followed
- [ ] Executive summary uses SCR format
- [ ] Arguments are MECE

### Content
- [ ] Every slide has exactly ONE key message
- [ ] All titles are insight-driven ACTION TITLES (full sentences)
- [ ] Every slide passes "So What?" test
- [ ] Maximum 5 points per slide
- [ ] Read-through test passed (titles tell the story)

### Visual Design
- [ ] NBG dimensions: 13.33" x 7.5" (LAYOUT_WIDE)
- [ ] Aptos font throughout
- [ ] NBG color palette only
- [ ] Logo on every slide (0.34", 5.9")
- [ ] Adequate white space
- [ ] Scannable in 5-7 seconds

### Quality Assurance
- [ ] Brand compliance verified
- [ ] Professional, board-ready appearance
- [ ] No chartjunk - every element serves a purpose
</success_criteria>
