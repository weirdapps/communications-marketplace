# NBG Typography

## Font Family

### Primary Font
- **Name**: Aptos
- **Weights**: Light, Regular, SemiBold
- **Fallback**: Calibri, Tahoma

### Bullet Font
- **Name**: Arial
- **Purpose**: Bullet characters only

## Text Styles

### Cover Slide

| Element | Font | Size | Color | Weight |
|---------|------|------|-------|--------|
| Title | Aptos | 48pt | #003841 | Regular |
| Subtitle | Aptos | 48pt | #007B85 | Regular |
| Location | Aptos | 14pt | #003841 | Regular |
| Date | Aptos | 14pt | #003841 | Regular |

### Divider Slide

| Element | Font | Size | Color | Weight |
|---------|------|------|-------|--------|
| Section Number | Aptos | 60pt | #007B85 | Regular |
| Section Title | Aptos | 60pt | #003841 | Regular |

### Content Slide

| Element | Font | Size | Color | Weight |
|---------|------|------|-------|--------|
| Page Title | Aptos | 24pt | #003841 | Regular |
| Body Text | Aptos | 11pt | #202020 | Regular |
| Bullet L1 | Aptos | 24pt | #202020 | Regular |
| Bullet L2 | Aptos | 20pt | #202020 | Regular |
| Bullet L3 | Aptos | 18pt | #202020 | Regular |
| Footnotes | Aptos | 8pt | #939793 | Regular |

### Charts & Tables

| Element | Font | Size | Color | Weight |
|---------|------|------|-------|--------|
| Chart Labels | Aptos | 10pt | #202020 | Regular |
| Chart Values | Aptos | 10pt | #202020 | Bold |
| Table Header | Aptos | 11pt | #FFFFFF | Bold |
| Table Cell | Aptos | 10pt | #202020 | Regular |

## Line Spacing

| Element | Line Spacing |
|---------|--------------|
| Titles | 0.9 |
| Body Text | 1.1 |
| Bullets | 1.1 |

## Paragraph Spacing

| Element | Space Before |
|---------|--------------|
| Body Text | 9pt |
| Table Cells | 9pt |
| Bullets | 10pt (L1), 5pt (L2, L3) |

## Text Box Settings

**CRITICAL**: All text boxes must use:
```javascript
{
  margin: 0,  // or [0, 0, 0, 0]
  valign: 'top',
  align: 'left'  // unless specified otherwise
}
```

## Bullet Points

```yaml
bullet:
  character: "•"
  unicode: "2022"
  font: "Arial"
  color: "#00DFF8"  # Bright Cyan
```

## Number Formatting

| Type | Format | Example |
|------|--------|---------|
| Section Numbers | Two-digit | "01", "02", "03" |
| Percentages | With symbol | "47%" |
| Currency | With symbol | "€4.2B" |
| Large Numbers | With unit | "2.3M" |
