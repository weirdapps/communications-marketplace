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
## Orchestration Workflow

1. **Analyze Input**
   - Determine input type (raw content, brief, data)
   - Identify audience and purpose
   - Assess complexity

2. **Storyline Creation**
   - Use the Storyline Architect agent to create narrative structure
   - Define ONE key message per slide
   - Create insight-driven titles
   - Recommend slide types and visualizations

3. **Storyboard Design**
   - Use the Storyboard Designer agent to plan visual layouts
   - Select appropriate NBG layouts for each slide
   - Specify exact positioning
   - Identify custom visual needs

4. **Asset Generation** (if needed)
   - Use Infographic Specialist for charts/diagrams
   - Use Icon Designer for custom icons
   - Use manage-nano-banana for complex infographics

5. **Final Assembly**
   - Use Graphics Renderer to create pixel-perfect PPTX
   - Apply all NBG specifications:
     - Dimensions: 12.192" x 6.858"
     - Background: white
     - Font: Aptos
     - Logo in bottom-left

6. **Quality Check**
   - Verify brand compliance
   - Ensure scannable in 5-7 seconds
   - Confirm professional appearance
</process>

<nbg_essentials>
## NBG Quick Reference

### Dimensions
- Width: 12.192" (NOT 13.33")
- Height: 6.858" (NOT 7.5")

### Colors (no # for PptxGenJS)
- Title: 003841 (Dark Teal)
- Body: 202020 (Dark Text)
- Section numbers: 007B85 (NBG Teal)
- Bullets: 00DFF8 (Bright Cyan)
- Background: FFFFFF (White)

### Logo
- Position: (0.34", 5.9")
- Size (Greek): 2.14" x 0.62"
</nbg_essentials>

<success_criteria>
- [ ] Presentation created successfully
- [ ] All slides have correct dimensions
- [ ] NBG branding applied consistently
- [ ] One key message per slide
- [ ] Scannable in 5-7 seconds
- [ ] Logo on every slide
- [ ] Professional, board-ready appearance
</success_criteria>
