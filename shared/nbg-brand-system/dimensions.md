# NBG Slide Dimensions & Positioning

## Slide Dimensions

**IMPORTANT**: The NBG template uses 12,192,000 x 6,858,000 EMU which equals **13.33" x 7.5"** in standard units (914,400 EMU = 1 inch). Use `LAYOUT_WIDE` in PptxGenJS.

```yaml
slide:
  width: 13.33"      # Standard widescreen (LAYOUT_WIDE)
  height: 7.5"       # Standard widescreen
  emu_width: 12192000
  emu_height: 6858000
  aspect_ratio: "16:9"
  format: "LAYOUT_WIDE"
```

**Note**: The spec document mentions "12.192 inches" but this is a labeling convention based on dividing EMU by 1,000,000. Always use LAYOUT_WIDE (13.33" x 7.5") for correct output.

## Margins & Safe Zones

```yaml
margins:
  left: 0.37"
  right: 0.37"
  top_title: 0.6"
  top_content: 1.5"
  bottom: 0.5"
```

## Logo Placement

```yaml
logo:
  greek:
    path: "assets/nbg-logo-gr.svg"
    x: 0.34"
    y: 6.6"         # Adjusted for 7.5" height
    width: 2.14"
    height: 0.62"

  english:
    path: "assets/nbg-logo.svg"
    x: 0.34"
    y: 6.6"
    width: 2.94"
    height: 0.62"
```

## Content Areas

### Full Width Content
```yaml
full_width:
  x: 0.37"
  y: 1.5"
  width: 12.5"
  height: 5.0"
```

### Two Column (50/50)
```yaml
two_column_even:
  left:
    x: 0.37"
    y: 1.5"
    width: 6.0"
  right:
    x: 6.7"
    y: 1.5"
    width: 6.0"
```

### Two Column (40/60 - Text/Chart)
```yaml
two_column_text_chart:
  text:
    x: 0.37"
    y: 1.5"
    width: 5.0"
  chart:
    x: 5.7"
    y: 1.3"
    width: 7.0"
```

### Three Column
```yaml
three_column:
  col1:
    x: 0.37"
    width: 3.8"
  col2:
    x: 4.5"
    width: 3.8"
  col3:
    x: 8.6"
    width: 3.8"
```

## Element Positions

### Cover Slide
```yaml
cover:
  title:
    x: 0.37"
    y: 1.5"
    width: 8.0"
    height: 1.6"

  subtitle:
    x: 0.37"
    y: 3.2"
    width: 8.0"
    height: 1.5"

  location:
    x: 0.37"
    y: 5.2"

  date:
    x: 0.37"
    y: 5.6"
```

### Divider Slide
```yaml
divider:
  number:
    x: 0.37"
    y: 3.0"
    width: 1.2"

  title:
    x: 1.9"
    y: 3.0"
    width: 10.5"
```

### Content Slide
```yaml
content:
  title:
    x: 0.37"
    y: 0.6"
    width: 12.5"
    height: 0.8"

  body:
    x: 0.37"
    y: 1.5"
    width: 12.5"
    height: 5.0"
```

## Slide Number Position

```yaml
slide_number:
  x: 12.5"
  y: 7.1"
  size: 10pt
  color: "#939793"
```

## PptxGenJS Configuration

```javascript
const pptx = new PptxGenJS();

// Use LAYOUT_WIDE for NBG presentations (13.33" x 7.5")
pptx.layout = 'LAYOUT_WIDE';

// This matches the NBG template EMU values: 12192000 x 6858000
```
