---
description: "Quick polish of existing slides to NBG standards"
argument-hint: "[slide content or path to file]"
allowed-tools: Task, Write, Skill(document-skills:pptx)
---

<objective>
Apply NBG formatting and brand standards to existing slide content without full restructuring.

User request: $ARGUMENTS
</objective>

<process>
## Quick Polish Workflow

1. **Take Content As-Is**
   - Accept the existing structure
   - Focus on formatting, not narrative

2. **Apply NBG Formatting**
   - Dimensions: 13.33" x 7.5" (LAYOUT_WIDE)
   - Background: white (#FFFFFF)
   - Font: Aptos throughout
   - All text boxes: margin: 0

3. **Apply NBG Colors**
   - Titles: #003841 (Dark Teal)
   - Body text: #202020 (Dark Text)
   - Bullets: #00DFF8 (Bright Cyan)
   - Accents: #007B85 (NBG Teal)

4. **Apply Typography**
   - Page titles: 24pt
   - Body text: 11-12pt
   - Section numbers: 60pt, format "01"

5. **Add Brand Elements**
   - Logo in bottom-left (0.34", 5.9")
   - Proper margins (0.37" sides)

6. **Output**
   - Generate formatted PPTX
</process>

<nbg_quick_reference>
## NBG Formatting Specs

### Dimensions
- 13.33" x 7.5" (LAYOUT_WIDE) (NOT default)

### Colors (no # for PptxGenJS)
- darkTeal: '003841' (titles)
- teal: '007B85' (section numbers)
- brightCyan: '00DFF8' (bullets)
- darkText: '202020' (body)
- white: 'FFFFFF' (background)

### Fonts
- Primary: Aptos
- Fallback: Arial, Calibri

### Logo
- Position: x=0.34", y=6.6"
- Greek: 2.14" x 0.62"
- English: 2.94" x 0.62"

### Text Box Rule
- margin: 0 (always)
</nbg_quick_reference>

<success_criteria>
- [ ] Correct dimensions applied
- [ ] NBG colors used
- [ ] Aptos font throughout
- [ ] Logo on every slide
- [ ] Text boxes with margin: 0
- [ ] Professional appearance
</success_criteria>
