# NBG PowerPoint Template Specification

This document contains the complete design specifications for creating presentations in the National Bank of Greece (NBG) corporate format.

## Template Overview
- **Total Slides**: 205 example slides
- **Slide Layouts**: 131 unique layouts
- **Slide Masters**: 16 masters
- **Themes**: 18 theme files + 6 theme overrides
- **Languages**: Available in EN (English) and GR (Greek)

## Slide Dimensions

**EMU Values** (from template):
- **Width**: 12,192,000 EMUs
- **Height**: 6,858,000 EMUs

**Standard Inch Conversion** (914,400 EMU = 1 inch):
- **Width**: 13.33 inches
- **Height**: 7.5 inches
- **Aspect Ratio**: 16:9 Widescreen

**PptxGenJS**: Use `pptx.layout = 'LAYOUT_WIDE'` (matches NBG template EMU values)

## Color Scheme ("NBG Colors 2")

### Primary Colors
| Color Name | Hex Code | RGB | Usage |
|------------|----------|-----|-------|
| Dark 1 (Black) | `#000000` | 0, 0, 0 | Text |
| Light 1 (White) | `#FFFFFF` | 255, 255, 255 | Backgrounds |
| Dark 2 (NBG Teal) | `#007B85` | 0, 123, 133 | Primary brand color, headers |
| Light 2 (Off-white) | `#F5F8F6` | 245, 248, 246 | Light backgrounds |

### Accent Colors (Theme Definition)
| Accent | Hex Code | RGB | Usage |
|--------|----------|-----|-------|
| Accent 1 (Dark Teal) | `#003841` | 0, 56, 65 | Primary titles, headings |
| Accent 2 (NBG Teal) | `#007B85` | 0, 123, 133 | Section numbers, highlights |
| Accent 3 (Cyan) | `#00ADBF` | 0, 173, 191 | Secondary accents |
| Accent 4 (Bright Cyan) | `#00CFE7` (EN) / `#00DEF8` (GR) | varies | Feature accent |
| Accent 5 (Light Gray) | `#BEC1BE` | 190, 193, 190 | Subtle elements |
| Accent 6 (Medium Gray) | `#939793` | 147, 151, 147 | Secondary text |

### Extended Color Palette (Frequently Used in Slides)
| Hex Code | RGB | Usage | Frequency |
|----------|-----|-------|-----------|
| `#00DFF8` | 0, 223, 248 | **Primary bright accent** (use this!) | Very High (365+) |
| `#007B85` | 0, 123, 133 | NBG Teal - brand color | Very High (814+) |
| `#047A85` | 4, 122, 133 | Teal variant (alternative) | High (188+) |
| `#F5F9F6` | 245, 249, 246 | Light background variant | High (168+) |
| `#003841` | 0, 56, 65 | Dark Teal - titles | High (89+) |
| `#202020` | 32, 32, 32 | Dark text (preferred over pure black) | Medium |
| `#252D30` | 37, 45, 48 | Dark charcoal backgrounds | Medium |
| `#0A091B` | 10, 9, 27 | Near-black for dark slides | Low |

### Status/Semantic Colors
| Hex Code | RGB | Usage |
|----------|-----|-------|
| `#73AF3C` | 115, 175, 60 | Success/positive (green) |
| `#AA0028` | 170, 0, 40 | Alert/negative (red) |
| `#D9A757` | 217, 167, 87 | Gold accent |
| `#1E478E` | 30, 71, 142 | Blue accent |

### Link Colors
| Type | Hex Code |
|------|----------|
| Hyperlink | `#0D90FF` |
| Followed Link | `#59C3FF` |

## Typography

### Primary Fonts (by usage frequency)
| Font | Occurrences | Usage | Weight |
|------|-------------|-------|--------|
| **Aptos** | 4841 | Body text, general content | Regular |
| **Arial** | 1910 | Bullet characters only | Regular |
| **Aptos SemiBold** | 323 | Emphasis, subheadings | SemiBold |
| **Tahoma** | 172 | Legacy content | Regular |
| **Lato Light** | 169 | Alternative body text | Light |
| **Roboto Medium** | 102 | Charts/data | Medium |
| **Calibri** | 84 | Fallback | Regular |
| **Lato Semibold** | 64 | Alternative emphasis | Semibold |
| **Helvetica Neue** | 36 | System fallback | Regular |
| **Poppins Medium** | 28 | Alternative headings | Medium |
| **Aptos Light** | 16 | Subtle text | Light |
| **Aptos Display** | 2 | Major headings (GR theme) | Display |
| **Aptos ExtraBold** | 2 | Strong emphasis | ExtraBold |
| **Aptos Black** | 2 | Maximum emphasis | Black |

### Theme Font Definitions
| Theme | Major Font (Headings) | Minor Font (Body) |
|-------|----------------------|-------------------|
| EN Template | Calibri Light | Calibri |
| GR Template | Aptos Display | Calibri |

### Font Sizes
| Level | Size (points) | Centipoints | Usage |
|-------|---------------|-------------|-------|
| Title | 44pt | 4400 | Slide titles |
| Level 1 Body | 28pt | 2800 | Main bullet points |
| Level 2 Body | 24pt | 2400 | Sub-bullets |
| Level 3 Body | 20pt | 2000 | Third-level bullets |
| Subheadings | 18pt | 1800 | Section subheadings |
| Default Body | **12pt** | 1200 | General text (most common) |
| Secondary | 11pt | 1100 | Secondary body text |
| Small Text | 10pt | 1000 | Captions, notes |
| Footnotes | 8pt | 800 | Footnotes, legal text |

### Text Box Settings
**IMPORTANT: All text boxes must use zero margins/insets:**
```
lIns="0" tIns="0" rIns="0" bIns="0"
```
- **Left Inset (lIns)**: 0 EMUs
- **Top Inset (tIns)**: 0 EMUs
- **Right Inset (rIns)**: 0 EMUs
- **Bottom Inset (bIns)**: 0 EMUs

### Text Formatting
- **Line Spacing**: 90% (spcPct val="90000")
- **Bullet Character**: • (Unicode 8226 / characterCode '2022')
- **Bullet Font**: Arial
- **Text Alignment**: Left-aligned (default)
- **Paragraph Spacing Before**: 10pt (Level 1), 5pt (Levels 2+)
- **Bullet Indent**: 228600 EMUs (0.25 inches)
- **Text Anchor**: Center vertical (anchor="ctr") for titles

## Logo Specifications

### Available Logos
| Logo | File | Dimensions | Language | Use Case |
|------|------|------------|----------|----------|
| English | `nbg-logo.svg` | 294 x 62 px | EN | English presentations |
| Greek | `nbg-logo-gr.svg` | 214 x 62 px | GR | **Greek presentations (preferred)** |

### Logo Colors
- **Text**: Dark Teal `#003841`
- **Building icon**: Bright Cyan `#00DEF8`

### Logo Placement - TEMPLATE STANDARD

**Two logo sizes in template:**

| Type | Position (x, y) | Size (w × h) | Usage |
|------|-----------------|--------------|-------|
| **Small (content)** | 0.374", 7.071" | 0.822" × 0.236" | Content slides, charts, tables |
| Large (covers) | 0.374", 6.271" | 2.191" × 0.630" | Cover slides, section dividers |

**For most slides, use the SMALL logo** - it's positioned 0.19" from the bottom edge, aligned with the page number.

## Page Numbers

### Page Number Placement
Page numbers appear on **content slides only** (not on cover, dividers, or back cover).

| Element | Position (x, y) | Size (w × h) | Edge Distance |
|---------|-----------------|--------------|---------------|
| Page Number | 12.2265", 7.1554" | 0.748" × 0.152" | 0.36" right, 0.19" bottom |

**Note:** Page number and logo are aligned at the same distance from bottom (0.19").

### Page Number Styling
- **Font**: Aptos
- **Size**: 10pt
- **Color**: Medium Gray `#939793`
- **Alignment**: Right

### Which Slides Get Page Numbers
| Slide Type | Page Number |
|------------|-------------|
| Cover | No |
| Divider | No |
| Content | Yes |
| Chart | Yes |
| Infographic | Yes |
| Table | Yes |
| Back Cover | No |

### PptxGenJS Implementation
```javascript
// Logo for content slides (small version)
const NBG_LOGO = {
  x: 0.374,
  y: 7.071,
  w: 0.822,
  h: 0.236
};

// Page number (content slides only)
let pageNumber = 0;

function addPageNumber(slide) {
  pageNumber++;
  slide.addText(String(pageNumber), {
    x: 12.2265, y: 7.1554, w: 0.748, h: 0.152,
    fontFace: 'Aptos',
    fontSize: 10,
    color: '939793',
    align: 'right',
    valign: 'middle',
    margin: 0,
  });
}
```

---

### Legacy Large Logo (avoid)
The original template uses a larger logo which can look oversized:
- **Width**: ~4.01 inches (TOO LARGE)
- **Height**: ~0.84 inches

**Prefer the smaller sizing above for modern, clean presentations.**

## Slide Layout Categories

Based on the template structure:

### Cover Slides (Section 02)
- Title/opening slides with full-bleed imagery
- Large typography for presentation titles

### Content Slides (Section 03)
- Standard content with headers
- Bulleted lists
- Two-column layouts

### Data Slides
- Charts and graphs
- Tables
- Infographics

### Section Dividers
- Numbered sections (01, 02, 03...)
- Section titles with teal accent numbers

### Closing Slides
- Thank you slides
- Contact information

## Design Patterns

### Section Numbering
- Numbers displayed in teal (`#007B85`) color
- Format: "01", "02", "03" etc.
- Tab-separated from section titles

### Header Bar
- Title position: x=838,201 EMUs, y=365,126 EMUs
- Title width: 10,515,600 EMUs
- Title height: 1,325,563 EMUs

### Content Area
- Standard content position: x=345,226 EMUs, y=1,217,046 EMUs
- Content width: 11,510,224 EMUs
- Content height: 5,092,274 EMUs

## Creating New NBG Presentations

When creating presentations in NBG format:

1. **Use LAYOUT_WIDE** (13.33" x 7.5" = 12192000 x 6858000 EMU)
2. **Apply NBG color scheme** with primary teal (#007B85) and bright cyan (#00DFF8)
3. **Use Aptos font family** (or Arial as fallback)
4. **Set all text box margins to 0** (lIns, tIns, rIns, bIns = 0)
5. **Include NBG logo** in bottom-left corner
6. **Follow section numbering pattern** with teal-colored numbers
7. **Use 12pt as default body text size** (not 18pt)
8. **Maintain consistent spacing** per the specifications above

## Template Files Location
- EN Template: `/Users/plessas/Downloads/Powerpoint - Version 1.0_EN.pptx`
- GR Template: `/Users/plessas/Downloads/Powerpoint - Version 1.0_GR.pptx`
- Logo assets: `~/.claude/nbg-template-assets/`

## PptxGenJS Configuration

```javascript
const pptx = new PptxGenJS();

// Use LAYOUT_WIDE to match NBG template EMU values (12192000 x 6858000)
pptx.layout = 'LAYOUT_WIDE';

// Define NBG colors
const NBG_COLORS = {
  // Primary palette
  darkTeal: '003841',      // Accent 1 - Titles, headings
  teal: '007B85',          // Accent 2 - Brand color, headers
  tealVariant: '047A85',   // Alternative teal (common in slides)
  cyan: '00ADBF',          // Accent 3 - Secondary accents
  brightCyan: '00DFF8',    // Primary bright accent (most common)
  brightCyanAlt: '00DEF8', // Logo/feature accent (GR theme)

  // Neutrals
  black: '000000',
  darkText: '202020',      // Preferred dark text
  charcoal: '252D30',      // Dark backgrounds
  mediumGray: '939793',    // Accent 6
  lightGray: 'BEC1BE',     // Accent 5
  offWhite: 'F5F8F6',      // Light 2
  offWhiteAlt: 'F5F9F6',   // Common variant
  white: 'FFFFFF',

  // Status colors
  success: '73AF3C',       // Green
  alert: 'AA0028',         // Red
  gold: 'D9A757',
  blue: '1E478E',

  // Links
  hyperlink: '0D90FF',
  followedLink: '59C3FF',
};

// Default text style (with zero margins)
const defaultTextStyle = {
  fontFace: 'Aptos',
  fontSize: 12,
  color: NBG_COLORS.darkText,
  margin: 0,  // Zero margins on all sides
};

// Title style
const titleStyle = {
  fontFace: 'Aptos',
  fontSize: 44,
  color: NBG_COLORS.darkTeal,
  bold: false,
  margin: 0,
};

// Bullet style
const bulletStyle = {
  fontFace: 'Aptos',
  fontSize: 28,
  color: NBG_COLORS.black,
  bullet: { type: 'bullet', characterCode: '2022' },
  margin: 0,
};

// Text box options (apply to all text elements)
const textBoxOptions = {
  margin: 0,           // Zero margin shorthand
  // Or explicitly:
  // margin: [0, 0, 0, 0],  // [top, right, bottom, left]
};

// Helper function to create text with NBG defaults
function addNBGText(slide, text, options = {}) {
  return slide.addText(text, {
    ...defaultTextStyle,
    margin: 0,
    ...options,
  });
}
```

## html2pptx Configuration

When using html2pptx for NBG presentations, ensure proper text box settings:

```javascript
// In html2pptx options
const nbgOptions = {
  slideWidth: 13.33,  // LAYOUT_WIDE
  slideHeight: 7.5,
  defaultTextStyle: {
    fontFace: 'Aptos',
    fontSize: 12,
    color: '202020',
  },
  textBoxMargin: 0,  // Zero margins for all text boxes
};
```

## OOXML Reference

### Text Box with Zero Margins (XML)
```xml
<a:bodyPr lIns="0" tIns="0" rIns="0" bIns="0" anchor="t">
  <a:normAutofit/>
</a:bodyPr>
```

### Default Body Properties
- `lIns="0"` - Left inset: 0
- `tIns="0"` - Top inset: 0
- `rIns="0"` - Right inset: 0
- `bIns="0"` - Bottom inset: 0
- `anchor="t"` - Top anchor (or `anchor="ctr"` for center)

---

## User Preferences

### Background Style
**IMPORTANT: Use WHITE backgrounds for all slides (not dark themes).**
- Slide background: `#FFFFFF` (white) or `#F5F8F6` (off-white)
- Text color: `#202020` (dark text) or `#003841` (dark teal) for titles
- Avoid dark charcoal/black backgrounds unless specifically requested

---

## Chart Specifications

### CRITICAL: Chart Type Selection
**NEVER use pie charts.** Always use **doughnut charts** instead:
- More modern and professional appearance
- Center hole provides space for key metrics
- Better visual hierarchy

### Recommended Chart Types
| Chart Type | Usage | Priority |
|------------|-------|----------|
| **Doughnut** | Proportions, percentages | **ALWAYS prefer over pie** |
| **Bar Chart** | Comparisons, rankings | Primary for categories |
| **Line Chart** | Trends, time series | Primary for time data |
| **Waterfall** | Financial flows | Budget/flow analysis |
| **Area Chart** | Cumulative trends | Stacked time data |

### Chart Color Sequence (use NBG theme colors)
Charts should use colors in this order for data series:
1. **Series 1**: `#00ADBF` (Accent 3 - Cyan)
2. **Series 2**: `#003841` (Accent 1 - Dark Teal)
3. **Series 3**: `#007B85` (Accent 2 - NBG Teal)
4. **Series 4**: `#939793` (Accent 6 - Medium Gray)
5. **Series 5**: `#BEC1BE` (Accent 5 - Light Gray)
6. **Series 6**: `#00DFF8` (Bright Cyan)

### Chart Colors Frequently Used
| Hex Code | Usage |
|----------|-------|
| `#00ADBF` | Primary chart color (16 occurrences) |
| `#003841` | Secondary chart color (14 occurrences) |
| `#939793` | Tertiary/gray series (13 occurrences) |
| `#B5B7B5` | Light gray series (9 occurrences) |
| `#F5F9F6` | Chart backgrounds (8 occurrences) |
| `#007B85` | Accent series (8 occurrences) |
| `#D9D9D9` | Neutral gray (5 occurrences) |
| `#00E2FC` | Highlight accent (4 occurrences) |

### Chart Style Settings
- **Style ID**: 102 (most common) or 2 (fallback)
- **Rounded Corners**: Off (`roundedCorners val="0"`)
- **Auto Title Deleted**: Yes (titles handled separately)
- **Data Labels**: Bold, 65% luminance text

### Doughnut/Pie Chart Settings
- Use scheme colors: accent1, accent2, accent3, accent4, accent5, accent6
- `varyColors="1"` for multi-colored segments
- No 3D effects (`bubble3D val="0"`)

### Bar Chart Settings
- **Direction**: Column (`barDir val="col"`) or Bar (`barDir val="bar"`)
- **Grouping**: Clustered (`grouping val="clustered"`)
- **Data Labels**: Show values, bold text

### Line Chart Settings (Enhanced)
- **Grouping**: Standard (`grouping val="standard"`)
- **Line Width**: 3pt (thicker for visibility)
- **Line Style**: Solid, smooth curves (`lineSmooth: true`)
- **Markers**: Show with size 10pt for emphasis
- **Data Labels**: Position above markers
- **Grid Lines**: Dotted gray (subtle reference)
- **Category Axis**: Visible with 1pt line

### Waterfall Chart Settings
- **Layout ID**: `waterfall`
- **Data Label Position**: Outside end (`pos="outEnd"`)
- **Font**: Aptos, 10pt for labels, 12pt bold for title
- **Title Color**: Accent 1 (Dark Teal)

### Chart Design Best Practices

**Clean, Minimal Charts:**
1. **Remove clutter**: Hide gridlines where possible, use minimal axis labels
2. **Single focus**: Each chart should communicate ONE key message
3. **Data labels**: Only show if they add value; use `outEnd` position
4. **Legend**: Position at top (`t`) or right (`r`), never obscuring data
5. **Colors**: Use max 3-4 colors per chart; single series = single color

**Supporting Key Messages:**
- Add callout boxes next to charts for insights (e.g., "+113% increase")
- Use annotations (lines, text) to highlight policy changes or events
- Keep subtitle/description below title explaining the data context

**Layout Tips:**
- Two-column layout: Chart on left, insight callout on right
- Full-width for single, important chart with annotations
- Bar charts: Use `barGapWidthPct: 30` for clean spacing

### PptxGenJS Chart Configuration
```javascript
// NBG Chart color array (NO # prefix!)
const NBG_CHART_COLORS = [
  '00ADBF',  // Cyan (primary)
  '003841',  // Dark Teal
  '007B85',  // NBG Teal
  '939793',  // Medium Gray
  'BEC1BE',  // Light Gray
  '00DFF8',  // Bright Cyan
];

// Bar chart example
slide.addChart(pptx.charts.BAR, chartData, {
  x: 1, y: 1.5, w: 10, h: 4.5,
  chartColors: NBG_CHART_COLORS,
  showValue: true,
  valueFontFace: 'Aptos',
  valueFontSize: 10,
  valueFontBold: true,
  catAxisLabelFontFace: 'Aptos',
  catAxisLabelFontSize: 10,
  valAxisLabelFontFace: 'Aptos',
  valAxisLabelFontSize: 10,
});

// Doughnut chart example
slide.addChart(pptx.charts.DOUGHNUT, chartData, {
  x: 1, y: 1.5, w: 5, h: 4.5,
  chartColors: NBG_CHART_COLORS,
  holeSize: 50,
  showLabel: true,
  showPercent: true,
});

// Line chart example
slide.addChart(pptx.charts.LINE, chartData, {
  x: 1, y: 1.5, w: 10, h: 4.5,
  chartColors: NBG_CHART_COLORS,
  lineSize: 2,
  lineSmooth: false,
  showMarker: false,
});
```

---

## Table Specifications

### Default Table Style
- **Style ID**: `{5C22544A-7EE6-4342-B048-85BDC9FD1C3A}`
- **Style Name**: "Medium Style 2 - Accent 1"
- **Border Width**: 12700 EMUs (1pt)
- **Border Color**: Light 1 (white)
- **Cell Fill**: Accent 1 with 20% tint (light teal)
- **Banded Rows**: Accent 1 with 40% tint

### Table Color Scheme
| Element | Color |
|---------|-------|
| Header Row | Dark Teal `#003841` with white text |
| Body Cells | 20% tint of `#003841` (very light teal) |
| Alternating Rows | 40% tint of `#003841` |
| Borders | White `#FFFFFF` |
| Text | Dark 1 (black) |

### PptxGenJS Table Configuration
```javascript
// NBG Table style
const nbgTableStyle = {
  fontFace: 'Aptos',
  fontSize: 10,
  color: '202020',
  margin: 0,
  border: { pt: 1, color: 'FFFFFF' },
  fill: { color: 'E6F0F1' },  // Light teal tint
};

// Header row style
const nbgTableHeaderStyle = {
  fontFace: 'Aptos',
  fontSize: 11,
  bold: true,
  color: 'FFFFFF',
  fill: { color: '003841' },
};
```

---

## Icon Specifications

### Icon Style
- **Format**: SVG (20 icons in template)
- **Primary Fill Color**: `#003841` (Dark Teal) - 515 occurrences
- **Secondary Fill Colors**:
  - `#F5F8F6` (Off-white) - 20 occurrences
  - `#00DEF8` (Bright Cyan) - 4 occurrences
  - `#007B85` (NBG Teal) - 2 occurrences
  - `#73AF3C` (Success Green) - 2 occurrences

### Icon Design Guidelines
- Solid fill, no strokes (stroke-width="0")
- Single color per icon (monochrome)
- Use theme color classes: `MsftOfcThm_Accent1_Fill_v2`, `MsftOfcThm_Text2_Fill_v2`
- Simple geometric shapes

### Icon Color Mapping
| Use Case | Hex Color |
|----------|-----------|
| Standard icons | `#003841` (Dark Teal) |
| Icons on dark backgrounds | `#F5F8F6` (Off-white) |
| Accent/highlight icons | `#00DEF8` (Bright Cyan) |
| Success indicators | `#73AF3C` (Green) |
| Alert indicators | `#AA0028` (Red) |

---

## Slide Layout Catalog

### Layout Categories

#### Cover Slides (30 variants)
- `1_Cover` through `30_Cover`
- Full-page imagery with overlay text
- Large typography for titles

#### Section Dividers (6 variants)
- `1_Divider` through `6_Divider`, `15_Divider`
- Section number + title format
- Clean, minimal design

#### Content Layouts
| Layout Name | Description |
|-------------|-------------|
| `Page 1/2 _Image Right` | Half text, half image (right) |
| `Page 1/2 _Image Left` | Half text, half image (left) |
| `Page 1/4 _Image Right` | Quarter image placement |
| `Page 1/4 _Image Left` | Quarter image placement |
| `Page Cut Edges _Image Right` | Edge-to-edge image right |
| `Page Cut Edges _Image Left` | Edge-to-edge image left |
| `2/3 _Image Right` | Two-thirds image |
| `Full Page` | Full bleed content |
| `Blank Page` | Empty layout |
| `Contact` | Contact information slide |
| `Charts & Infographics` | Data visualization layouts |

### Layout Placeholder Types
| Type | Count | Usage |
|------|-------|-------|
| `body` | 328 | Main content areas |
| `sldNum` / `slidenum` | 116 | Slide numbers |
| `ctrTitle` | 33 | Centered titles |
| `pic` | 11 | Image placeholders |
| `title` | 3 | Standard titles |
| `tbl` | 3 | Table placeholders |

---

## White Background Slide Template

### Recommended White Slide Structure
```javascript
// Create white background slide
const slide = pptx.addSlide();

// White background (default, but explicit)
slide.background = { color: 'FFFFFF' };

// Title (Dark Teal)
slide.addText('Slide Title', {
  x: 0.34, y: 0.36,
  w: 11.5, h: 1.3,
  fontSize: 44,
  fontFace: 'Aptos',
  color: '003841',
  margin: 0,
});

// Body content (Dark text)
slide.addText('Content here', {
  x: 0.34, y: 1.7,
  w: 11.5, h: 4.5,
  fontSize: 12,
  fontFace: 'Aptos',
  color: '202020',
  margin: 0,
});

// Logo (bottom-left)
slide.addImage({
  path: 'nbg-logo.svg',
  x: 0.34, y: 5.45,
  w: 4.01, h: 0.84,
});
```

### Light Theme Color Guidelines
For white/light background slides:
- **Titles**: `#003841` (Dark Teal)
- **Body Text**: `#202020` (Dark text)
- **Accents**: `#007B85` (NBG Teal) or `#00DFF8` (Bright Cyan)
- **Subtle Elements**: `#939793` (Medium Gray)
- **Backgrounds**: `#FFFFFF` (White) or `#F5F8F6` (Off-white)
- **Section Numbers**: `#007B85` (NBG Teal)

---

## Quick Reference Card

### Essential Colors (White Background Theme)
```
Background:    #FFFFFF or #F5F8F6
Title Text:    #003841
Body Text:     #202020
Primary Accent: #007B85
Bright Accent:  #00DFF8
Success:       #73AF3C
Alert:         #AA0028
```

### Essential Fonts
```
Primary:       Aptos (12pt body, 44pt title)
Bullets:       Arial
Fallback:      Calibri
```

### Essential Measurements
```
Slide:         13.33" x 7.5" (LAYOUT_WIDE)
Text Margins:  0 (all sides)
Logo Position: x=0.34", y=5.45"
Logo Size:     4.01" x 0.84"
```

---

## Complete Template Catalog

### Template Section Index
| Section | Slides | Description |
|---------|--------|-------------|
| 01 Instructions | 2-12 | Color palette, fonts, bullets, icons usage |
| 02 Covers | 13-59 | Title/cover slides (47 variants) |
| 03 Contents | 60-63 | Table of contents layouts |
| 04 Dividers | 64-88 | Section dividers (25 variants) |
| 05 Page Layouts | 89-114 | Content page templates |
| 06 Page Layout Examples | 115-136 | Real-world content examples |
| 07 Charts & Infographics | 137-180 | All data visualization types |
| 08 Tables | 181-184 | Table layouts |
| 09 Contact Page | 185-187 | Contact information slides |
| 10 Back Covers | 188-195 | Thank you/closing slides |
| 11 Segment Logos | 196+ | Brand segment logos |

---

## Complete Color Palette

### Primary Brand Colors (from template instructions)
| Name | Hex | Usage |
|------|-----|-------|
| Dark Teal | `#003841` | Primary titles, headings |
| Teal | `#007B85` | Brand color, headers |
| Aqua | `#00ADBF` | Accents, secondary |

### Secondary Colors (for charts & diagrams)
| Name | Hex | Usage |
|------|-----|-------|
| Black | `#212121` | Text (alternative to pure black) |
| Aqua Light | `#3EDEF8` | Light accent |
| Light Grey | `#BEC1BE` | Subtle elements |
| Grey | `#595959` | Secondary text |
| Pale Grey | `#F5F8F6` | Light backgrounds |
| White | `#FFFFFF` | Backgrounds |

### Segment/Division Colors
| Name | Hex | Usage |
|------|-----|-------|
| Business Blue | `#0D90FF` | Business banking segment |
| Corporate Green | `#73AF3C` | Corporate segment |
| Premium Gold | `#D9A757` | Premium/private banking |
| Private Red | `#AA0028` | Private banking segment |

### Status Colors (tables and charts only)
| Name | Hex | Usage |
|------|-----|-------|
| Deep Red | `#CB0030` | Critical/negative |
| Red | `#F60037` | Alert/warning |
| Orange | `#FF7F1A` | Caution |
| Yellow | `#FFDC00` | Attention |
| Green | `#5D8D2F` | Success/positive |
| Bright Green | `#90DC48` | Strong positive |

### Bullet Point Color
| Element | Hex |
|---------|-----|
| Bullet character | `#00DFF8` (Bright Cyan) |

---

## Shape Presets Used

| Shape | Count | Usage |
|-------|-------|-------|
| Rectangle (`rect`) | 649 | Backgrounds, containers, cards |
| Triangle (`triangle`) | 75 | Arrows, indicators, infographics |
| Rounded Rectangle (`roundRect`) | 75 | Buttons, cards, callouts |
| Ellipse (`ellipse`) | 56 | Icons, bullets, highlights |
| Flow Connector (`flowChartConnector`) | 50 | Process flows, connections |
| Line (`line`) | 43 | Dividers, timelines |
| Chevron (`chevron`) | 14 | Process steps, arrows |
| Arc (`arc`) | 11 | Progress indicators, charts |
| Right Arrow (`rightArrow`) | 4 | Direction indicators |
| Callout shapes | 3 | Speech bubbles, annotations |

---

## Cover Slide Specifications

### Cover Elements
| Element | Font | Size | Position (x, y) |
|---------|------|------|-----------------|
| Title | Aptos Regular | 48pt | 0.37", 1.39" |
| Subtitle | Aptos Regular | 48pt | 0.37", 2.90" |
| Location/Description | Aptos Regular | - | 0.37", 4.58" |
| Date (DD/MM/YYYY) | Aptos Regular | - | 0.37", 4.97" |

### Cover Layout Dimensions
- Title text box: 7.86" wide × 1.56" tall
- Subtitle text box: 7.86" wide × 1.44" tall
- Title can continue on two lines

---

## Section Divider Specifications

### Divider Elements
| Element | Font | Size | Position |
|---------|------|------|----------|
| Section Number | Aptos | 60pt | 0.37", 2.84" |
| Section Title | Aptos | 60pt | 1.86", 2.84" |
| Placeholder text | - | - | Below title |

### Number Format
- Two-digit format: "01", "02", "03", etc.
- Color: NBG Teal (`#007B85`)
- Tab-separated from title text

---

## Content Slide Specifications

### Standard Content Layout
| Element | Font | Size | Line Spacing | Space Before |
|---------|------|------|--------------|--------------|
| Title | Aptos | 18-24pt | 0.9 | - |
| Body text | Aptos | 11pt | 1.1 | 9pt |
| Bullet L1 | Aptos | 24pt | 1.0 | 10pt |
| Bullet L2 | Aptos | 20pt | 1.0 | 5pt |
| Bullet L3 | Aptos | 18pt | 1.0 | 5pt |
| Footnotes | Aptos | 8pt | 1.1 | - |

### Page Layout Variants
| Layout | Description | Image Position |
|--------|-------------|----------------|
| Page 1/2 _Image Right | Half text, half image | Right side |
| Page 1/2 _Image Left | Half text, half image | Left side |
| Page 1/4 _Image Right | Quarter image | Right side |
| Page 1/4 _Image Left | Quarter image | Left side |
| Page Cut Edges | Edge-to-edge image | Right or Left |
| 2/3 _Image Right | Two-thirds image | Right side |
| Full Page | Full bleed content | Full slide |

---

## Infographic Patterns

### Numbered List (slide-163 style)
- 3x3 grid of numbered items (1-9)
- Each item has: Number + Title + Description
- Numbers: Large, teal colored
- Spacing: Even grid distribution

### Sequential Steps (slide-164 style)
- 2x3 grid with "01", "02", "03", etc.
- Two-digit numbering
- Compact paragraph descriptions

### Vertical List (slide-165 style)
- Left-aligned items with teal indicator bars
- Icon/bullet on left, text on right
- Stacked vertical layout

### Funnel/Process (slide-169 style)
- Stages: Awareness → Knowledge → Desire → Reinforcement
- Converging visual shape
- Stage labels with descriptions

### Calendar/Timeline (slide-175 style)
- Month headers (January, February, etc.)
- Date markers with numbered indicators
- Event descriptions below dates

### Horizontal Process (slide-176 style)
- Sequential stages: Awareness → Performance → Considerations → Pre-Order → Order
- Horizontal flow with stage labels
- Descriptions below each stage

### Numbered Steps with Icons (slide-174 style)
- Large "01", "02", "03", "04" markers
- Connecting lines between steps
- Title and description for each step

---

## Timeline & Project Slides

### Project Timeline (slide-160 style)
#### Structure:
- Horizontal timeline with month labels
- Multiple workstream rows
- Milestone markers
- "Today" indicator

#### Workstream Rows:
- Research, Content, Design, Design System, Info Arch, Front-End, Development

#### Visual Elements:
- Horizontal bars for duration
- Diamond shapes for milestones
- Vacation periods marked

### Project Status (slide-161 style)
#### Structure:
- Timeline header with "Today" marker
- Key deliverable milestones
- Workstream cards (4-column layout)

#### Workstream Cards:
- Title in bold
- Description paragraphs
- Status indicators

---

## Chart Combination Patterns

### Bar Chart + Pie Chart (slide-146)
- Side-by-side layout
- Shared color palette

### Multiple Bar Charts (slide-143, 144, 145)
- 2x or 4x grid layouts
- Consistent axis scaling

### Line Chart + Data (slide-155)
- Chart with supporting metrics
- Text annotations

### Infographic + Chart (slide-158)
- Mixed visualization types
- Supporting data tables
- Text annotations

### Text + Charts (slide-159)
- Two-column layout
- Text explanation on left/right
- Chart/data visualization opposite

---

## Table Specifications

### Table Layouts
| Layout | Width | Description |
|--------|-------|-------------|
| Table 1/2 page | 50% | Half-width table with text |
| Table 3/4 page | 75% | Larger table area |
| Table full width | 100% | Full-width table |

### Table Typography
| Element | Font | Size |
|---------|------|------|
| Header | Aptos | 11pt |
| Cell text | Aptos Regular | 10-11pt |
| Footnotes | Aptos | 8pt |

---

## Contact Page Specifications

### Contact Layout 1 (slide-186)
- Full-width contact list
- Tab-separated: Name, Phone, Email
- Title below name
- Address at bottom

### Contact Layout 2 (slide-187)
- 2-column card layout
- Photo/icon placeholder
- Name, title, phone, email per card
- Division info at bottom

### Contact Typography
| Element | Font | Size |
|---------|------|------|
| Page title | Aptos | 24pt |
| Contact name | Aptos | 14pt |
| Contact details | Aptos Regular | 11-12pt |

---

## Back Cover Slides (Closing)

**IMPORTANT**: NBG presentations should NOT use "Thank You" or "Questions" text on closing slides. Instead, use a **plain back cover** with the centered NBG building oval logo.

### Plain Back Cover (PREFERRED)
The standard NBG back cover is a white slide with only the centered oval NBG building logo.

| Element | Position (x, y) | Size (w × h) | Description |
|---------|-----------------|--------------|-------------|
| Centered Oval Logo | 5.44", 2.98" | 2.45" × 1.54" | NBG building in cyan oval |

### Back Cover Logo Asset
**File**: `~/.claude/plugins/marketplaces/comms-marketplace/assets/nbg-back-cover-logo.png`
- **Description**: Bright cyan oval with dark teal NBG building illustration
- **Format**: PNG with transparency
- **Usage**: Center of slide for back cover only

### PptxGenJS Back Cover Implementation
```javascript
// Plain back cover with centered oval logo
const slide = pptx.addSlide();
slide.background = { color: 'FFFFFF' };

// Add centered oval NBG building logo
slide.addImage({
  path: '~/.claude/plugins/marketplaces/comms-marketplace/assets/nbg-back-cover-logo.png',
  x: 5.44,  // Centered: (13.33 - 2.45) / 2
  y: 2.98,  // Centered: (7.5 - 1.54) / 2
  w: 2.45,
  h: 1.54,
});
```

### What NOT to Include on Back Covers
- "Thank You" text
- "Questions?" text
- "Q&A" labels
- Contact information (use dedicated contact slides instead)
- Any decorative elements

### Variants (from Template)
| Slide Index | Description | Use Case |
|-------------|-------------|----------|
| 190 | Plain white with centered oval logo | **Default/Preferred** |
| 191 | Minimal back cover | Alternative |
| 192 | Plain white | Simple variant |
| 193 | Dark background | Dark theme presentations |

---

## Callout Specifications (slide-180)

### Callout Shapes
- Rounded rectangle containers
- White or light background
- Teal accent border or no border

### Callout Typography
| Element | Font | Size |
|---------|------|------|
| Callout text | Aptos | 11pt |
| Line spacing | - | 1.1 |

---

## Communication Use Case Guide

### For Executive Summaries
Use: Cover → Divider → Key Metrics → Charts → Thank You

### For Project Updates
Use: Cover → Contents → Dividers → Timeline → Status → Charts → Next Steps

### For Data Presentations
Use: Cover → Contents → Charts (bar, line, pie) → Tables → Key Takeaways

### For Strategy Decks
Use: Cover → Dividers → Infographics → Process Flows → Timeline → Contact

### For Training/Educational
Use: Cover → Contents → Page Layouts (with images) → Infographics → Summary

### For Financial Reports
Use: Cover → Contents → KPI Metrics → Charts → Tables → Disclaimers → Contact

---

## PptxGenJS Complete Configuration

```javascript
// ============================================
// NBG PowerPoint Generation - Complete Config
// ============================================

const PptxGenJS = require('pptxgenjs');
const pptx = new PptxGenJS();

// === SLIDE DIMENSIONS ===
// Use LAYOUT_WIDE (13.33" x 7.5") to match NBG template EMU values
pptx.layout = 'LAYOUT_WIDE';

// === COMPLETE COLOR PALETTE ===
const NBG = {
  colors: {
    // Primary Brand
    darkTeal: '003841',
    teal: '007B85',
    aqua: '00ADBF',
    brightCyan: '00DFF8',
    
    // Secondary
    black: '212121',
    aquaLight: '3EDEF8',
    lightGrey: 'BEC1BE',
    grey: '595959',
    paleGrey: 'F5F8F6',
    white: 'FFFFFF',
    
    // Segment Colors
    businessBlue: '0D90FF',
    corporateGreen: '73AF3C',
    premiumGold: 'D9A757',
    privateRed: 'AA0028',
    
    // Status Colors
    deepRed: 'CB0030',
    red: 'F60037',
    orange: 'FF7F1A',
    yellow: 'FFDC00',
    green: '5D8D2F',
    brightGreen: '90DC48',
  },
  
  // Chart color sequence
  chartColors: ['00ADBF', '003841', '007B85', '939793', 'BEC1BE', '00DFF8'],
  
  // Fonts
  fonts: {
    primary: 'Aptos',
    bullet: 'Arial',
    fallback: 'Calibri',
  },
  
  // Font sizes (in points)
  sizes: {
    coverTitle: 48,
    dividerNumber: 60,
    pageTitle: 24,
    heading: 18,
    body: 11,
    bullet1: 24,
    bullet2: 20,
    bullet3: 18,
    footnote: 8,
    default: 12,
  },
  
  // Spacing
  spacing: {
    lineSpacing: 1.1,
    titleLineSpacing: 0.9,
    paragraphBefore: 9,  // points
    bulletL1Before: 10,
    bulletL2Before: 5,
  },
};

// === SLIDE TEMPLATES ===

// Cover slide
function addCoverSlide(title, subtitle, location, date) {
  const slide = pptx.addSlide();
  slide.background = { color: NBG.colors.white };
  
  slide.addText(title, {
    x: 0.37, y: 1.39, w: 7.86, h: 1.56,
    fontSize: NBG.sizes.coverTitle,
    fontFace: NBG.fonts.primary,
    color: NBG.colors.darkTeal,
    margin: 0,
  });
  
  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.37, y: 2.9, w: 7.86, h: 1.44,
      fontSize: NBG.sizes.coverTitle,
      fontFace: NBG.fonts.primary,
      color: NBG.colors.teal,
      margin: 0,
    });
  }
  
  if (location) {
    slide.addText(location, {
      x: 0.37, y: 4.58, w: 7.86, h: 0.34,
      fontSize: 14,
      fontFace: NBG.fonts.primary,
      color: NBG.colors.grey,
      margin: 0,
    });
  }
  
  if (date) {
    slide.addText(date, {
      x: 0.37, y: 4.97, w: 7.86, h: 0.34,
      fontSize: 14,
      fontFace: NBG.fonts.primary,
      color: NBG.colors.grey,
      margin: 0,
    });
  }
  
  return slide;
}

// Section divider
function addDividerSlide(number, title) {
  const slide = pptx.addSlide();
  slide.background = { color: NBG.colors.white };
  
  // Section number
  slide.addText(String(number).padStart(2, '0'), {
    x: 0.37, y: 2.84, w: 1.16, h: 1.02,
    fontSize: NBG.sizes.dividerNumber,
    fontFace: NBG.fonts.primary,
    color: NBG.colors.teal,
    margin: 0,
  });
  
  // Section title
  slide.addText(title, {
    x: 1.86, y: 2.84, w: 9, h: 1.02,
    fontSize: NBG.sizes.dividerNumber,
    fontFace: NBG.fonts.primary,
    color: NBG.colors.darkTeal,
    margin: 0,
  });
  
  return slide;
}

// Content slide with title and bullets
function addContentSlide(title, bullets) {
  const slide = pptx.addSlide();
  slide.background = { color: NBG.colors.white };
  
  // Title
  slide.addText(title, {
    x: 0.36, y: 0.6, w: 11.5, h: 0.5,
    fontSize: NBG.sizes.pageTitle,
    fontFace: NBG.fonts.primary,
    color: NBG.colors.darkTeal,
    margin: 0,
  });
  
  // Bullets
  const bulletText = bullets.map(b => ({
    text: b,
    options: {
      bullet: { type: 'bullet', characterCode: '2022', color: NBG.colors.brightCyan },
      fontSize: NBG.sizes.body,
      fontFace: NBG.fonts.primary,
      color: NBG.colors.black,
    }
  }));
  
  slide.addText(bulletText, {
    x: 0.37, y: 1.33, w: 11.5, h: 5,
    margin: 0,
    paraSpaceBefore: NBG.spacing.bulletL1Before,
    lineSpacing: NBG.spacing.lineSpacing * 100,
  });
  
  return slide;
}

// Infographic slide with numbered items
function addInfographicSlide(title, items) {
  const slide = pptx.addSlide();
  slide.background = { color: NBG.colors.white };
  
  // Title
  slide.addText(title, {
    x: 0.36, y: 0.6, w: 11.5, h: 0.5,
    fontSize: NBG.sizes.pageTitle,
    fontFace: NBG.fonts.primary,
    color: NBG.colors.darkTeal,
    margin: 0,
  });
  
  // Content area with pale grey background
  slide.addShape(pptx.ShapeType.rect, {
    x: 0.37, y: 1.5, w: 11.5, h: 4.8,
    fill: { color: NBG.colors.paleGrey },
    line: { color: NBG.colors.paleGrey },
  });
  
  // Add numbered items in grid
  const cols = 3;
  const itemWidth = 3.5;
  const itemHeight = 1.4;
  
  items.forEach((item, i) => {
    const col = i % cols;
    const row = Math.floor(i / cols);
    const x = 0.6 + (col * (itemWidth + 0.3));
    const y = 1.7 + (row * itemHeight);
    
    // Number
    slide.addText(String(i + 1), {
      x, y, w: 0.5, h: 0.5,
      fontSize: 24,
      fontFace: NBG.fonts.primary,
      color: NBG.colors.teal,
      bold: true,
      margin: 0,
    });
    
    // Title and description
    slide.addText([
      { text: item.title, options: { bold: true, fontSize: 12 } },
      { text: '\n' + item.description, options: { fontSize: 10 } }
    ], {
      x: x + 0.5, y, w: itemWidth - 0.5, h: itemHeight,
      fontFace: NBG.fonts.primary,
      color: NBG.colors.black,
      margin: 0,
      valign: 'top',
    });
  });
  
  return slide;
}

// Thank you slide
function addThankYouSlide() {
  const slide = pptx.addSlide();
  slide.background = { color: NBG.colors.white };
  
  slide.addText('Thank You', {
    x: 0.37, y: 2.5, w: 11.5, h: 1.5,
    fontSize: 60,
    fontFace: NBG.fonts.primary,
    color: NBG.colors.darkTeal,
    margin: 0,
  });
  
  return slide;
}

// Export configuration
module.exports = { pptx, NBG, addCoverSlide, addDividerSlide, addContentSlide, addInfographicSlide, addThankYouSlide };
```

---

## Quick Reference: Slide Types Cheat Sheet

| Slide Type | When to Use | Key Elements |
|------------|-------------|--------------|
| **Cover** | Opening slide | Title (48pt), Subtitle, Date |
| **Contents** | Agenda/TOC | Numbered list with tabs |
| **Divider** | Section break | Large number + title (60pt) |
| **Content** | Main slides | Title (24pt) + body (11pt) |
| **Chart** | Data viz | Bar, Line, Pie, Doughnut |
| **Infographic** | Process/concepts | Numbers, icons, shapes |
| **Timeline** | Project schedule | Horizontal bars, milestones |
| **Table** | Tabular data | Headers, rows, alternating colors |
| **Contact** | Team info | Names, titles, phone, email |
| **Thank You** | Closing | Large text, minimal design |

---

## Element Positioning Reference

### Standard Margins
| Edge | Value |
|------|-------|
| Left margin | 0.36-0.38" |
| Top margin (title) | 0.6" |
| Top margin (content) | 1.33" |
| Right margin | 0.36" |
| Bottom (logo area) | 5.45" from top |

### Common Widths
| Element | Width |
|---------|-------|
| Full-width content | 11.5" |
| Half-page content | 5.5-6" |
| Two-column (each) | ~5.5" |
| Three-column (each) | ~3.5" |
| Logo | 4.01" |

---
