---
description: "Generate an NBG-compliant SVG icon"
argument-hint: "[icon concept or description]"
allowed-tools: Write
---

<objective>
Create a custom SVG icon that matches NBG iconography exactly.

User request: $ARGUMENTS
</objective>

<icon_rules>
## NBG Icon Specifications

### Canvas
- Size: 64 x 64 px
- ViewBox: "0 0 64 64"
- Padding: 5-8px from edges

### Style
- **Fill only** - NO strokes
- **Monochrome** - Single color
- **Geometric** - Clean, simple shapes
- **Solid** - 100% opaque fills

### Colors
| Context | Fill Color |
|---------|------------|
| Standard (white bg) | #003841 |
| Dark background | #F5F8F6 |
| Accent/highlight | #00DEF8 |
| Success | #73AF3C |
| Alert | #AA0028 |

### Template
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">
  <path fill="#003841" d="[path data]"/>
</svg>
```

### What NOT to use
- Strokes or outlines
- Gradients
- Transparency/opacity
- Inline styles
- Complex details
- Colors outside NBG palette
</icon_rules>

<process>
1. Analyze the icon concept
2. Design using simple geometric shapes
3. Apply NBG fill color based on context
4. Output clean SVG code only
</process>

<success_criteria>
- [ ] Canvas is 64x64, viewBox="0 0 64 64"
- [ ] Uses solid fill (no strokes)
- [ ] Color is from NBG palette
- [ ] Optically centered with padding
- [ ] Simple, geometric design
- [ ] Recognizable at 24x24px
- [ ] Clean, minimal SVG structure
</success_criteria>
