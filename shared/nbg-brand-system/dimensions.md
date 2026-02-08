# NBG Slide Dimensions & Positioning

## Slide Dimensions

```yaml
slide:
  width: 12.192"   # NOT standard 13.33"
  height: 6.858"   # NOT standard 7.5"
  aspect_ratio: "16:9"
  format: "NBG Custom"
```

## Margins & Safe Zones

```yaml
margins:
  left: 0.37"
  right: 0.37"
  top_title: 0.6"
  top_content: 1.33"
  bottom: 0.4"
```

## Logo Placement

```yaml
logo:
  greek:
    path: "assets/nbg-logo-gr.svg"
    x: 0.34"
    y: 5.9"
    width: 2.14"
    height: 0.62"

  english:
    path: "assets/nbg-logo.svg"
    x: 0.34"
    y: 5.9"
    width: 2.94"
    height: 0.62"
```

## Content Areas

### Full Width Content
```yaml
full_width:
  x: 0.37"
  y: 1.33"
  width: 11.45"
  height: 4.5"
```

### Two Column (50/50)
```yaml
two_column_even:
  left:
    x: 0.37"
    y: 1.33"
    width: 5.5"
  right:
    x: 6.1"
    y: 1.33"
    width: 5.5"
```

### Two Column (40/60 - Text/Chart)
```yaml
two_column_text_chart:
  text:
    x: 0.37"
    y: 1.33"
    width: 4.5"
  chart:
    x: 5.1"
    y: 1.2"
    width: 6.7"
```

### Three Column
```yaml
three_column:
  col1:
    x: 0.37"
    width: 3.6"
  col2:
    x: 4.2"
    width: 3.6"
  col3:
    x: 8.0"
    width: 3.6"
```

## Element Positions

### Cover Slide
```yaml
cover:
  title:
    x: 0.37"
    y: 1.39"
    width: 7.86"
    height: 1.56"

  subtitle:
    x: 0.37"
    y: 2.90"
    width: 7.86"
    height: 1.44"

  location:
    x: 0.37"
    y: 4.58"

  date:
    x: 0.37"
    y: 4.97"
```

### Divider Slide
```yaml
divider:
  number:
    x: 0.37"
    y: 2.84"
    width: 1.2"

  title:
    x: 1.86"
    y: 2.84"
    width: 9.5"
```

### Content Slide
```yaml
content:
  title:
    x: 0.37"
    y: 0.6"
    width: 11.45"
    height: 0.8"

  body:
    x: 0.37"
    y: 1.33"
    width: 11.45"
    height: 4.5"
```

## Slide Number Position

```yaml
slide_number:
  x: 11.4"
  y: 6.3"
  size: 10pt
  color: "#939793"
```
