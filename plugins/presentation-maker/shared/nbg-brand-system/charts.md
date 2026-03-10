# NBG Chart Specifications

## Critical Rules

### NEVER Use Pie Charts
**Pie charts are PROHIBITED.** Always use **doughnut charts** instead:
- More modern and professional appearance
- Center hole provides space for key metrics
- Better visual hierarchy

### Always Specify Explicit Colors
**CRITICAL:** Always specify explicit NBG colors for all chart elements to avoid PptxGenJS defaults (like #333333):
- `catAxisLabelColor`
- `valAxisLabelColor`
- `catAxisLineColor`
- `legendColor`
- `dataLabelColor`

## Chart Type Hierarchy

| Priority | Chart Type | Use For |
|----------|------------|---------|
| 1 | **Doughnut** | Proportions, percentages (ALWAYS instead of pie) |
| 2 | **Bar** | Comparisons, rankings, categories |
| 3 | **Line** | Trends, time series |
| 4 | **Waterfall** | Financial flows, breakdowns |
| 5 | **Area** | Cumulative trends over time |

## Color Sequence

Use these colors in order for data series (no # prefix):

| Order | Hex | Name | RGB |
|-------|-----|------|-----|
| 1 | `00ADBF` | Cyan | 0, 173, 191 |
| 2 | `003841` | Dark Teal | 0, 56, 65 |
| 3 | `007B85` | NBG Teal | 0, 123, 133 |
| 4 | `939793` | Medium Gray | 147, 151, 147 |
| 5 | `BEC1BE` | Light Gray | 190, 193, 190 |
| 6 | `00DFF8` | Bright Cyan | 0, 223, 248 |

```javascript
const NBG_CHART_COLORS = ['00ADBF', '003841', '007B85', '939793', 'BEC1BE', '00DFF8'];
```

## Bar Chart Configuration

```javascript
slide.addChart(pptx.ChartType.bar, chartData, {
  x: 0.37, y: 1.3, w: 8.0, h: 4.8,
  chartColors: ['00ADBF'],

  // Data labels
  showValue: true,
  valueFontFace: 'Aptos',
  valueFontSize: 11,
  valueFontBold: true,
  valueFontColor: '202020',  // Explicit NBG color

  // Bar spacing
  barGapWidthPct: 35,

  // Category axis
  catAxisLabelFontFace: 'Aptos',
  catAxisLabelFontSize: 12,
  catAxisLabelColor: '202020',      // EXPLICIT - avoid defaults
  catAxisLineColor: 'BEC1BE',       // EXPLICIT - avoid defaults
  catAxisLineSize: 0.5,

  // Value axis
  valAxisHidden: true,
  valAxisLabelColor: '202020',      // EXPLICIT - even if hidden

  // Grid lines
  catGridLine: { style: 'none' },
  valGridLine: { style: 'none' },

  // Legend
  showLegend: false,

  // Plot area
  plotArea: { border: { color: 'BEC1BE', pt: 0 } },
});
```

## Doughnut Chart Configuration

**ALWAYS use doughnut instead of pie charts.**

```javascript
slide.addChart(pptx.ChartType.doughnut, chartData, {
  x: 0.37, y: 1.4, w: 5.5, h: 4.5,
  chartColors: ['00ADBF', '003841'],

  // Doughnut settings
  holeSize: 55,
  showLabel: false,
  showPercent: true,

  // Data labels
  dataLabelFontFace: 'Aptos',
  dataLabelFontSize: 12,
  dataLabelColor: '202020',         // EXPLICIT - avoid defaults

  // Legend
  showLegend: true,
  legendPos: 'b',
  legendFontFace: 'Aptos',
  legendFontSize: 12,
  legendColor: '202020',            // EXPLICIT - avoid defaults
});
```

## Line Chart Configuration (Enhanced)

Line charts should have smooth curves, thick lines, and visible markers.

```javascript
slide.addChart(pptx.ChartType.line, chartData, {
  x: 0.37, y: 1.4, w: 7.0, h: 3.8,
  chartColors: ['AA0028'],  // Example: alert color for CMTs

  // Line styling (ENHANCED)
  lineSize: 3,              // Thicker lines
  lineSmooth: true,         // Smooth curves
  lineDash: 'solid',

  // Markers (VISIBLE)
  showMarker: true,
  markerSize: 10,           // Large markers

  // Data labels
  showValue: true,
  valueFontFace: 'Aptos',
  valueFontSize: 11,
  valueFontBold: true,
  valueFontColor: '202020',
  dataLabelPosition: 't',   // Above markers
  dataLabelFontFace: 'Aptos',
  dataLabelColor: '202020', // EXPLICIT

  // Category axis
  catAxisLabelFontFace: 'Aptos',
  catAxisLabelFontSize: 12,
  catAxisLabelColor: '202020',      // EXPLICIT
  catAxisLineShow: true,
  catAxisLineColor: 'BEC1BE',       // EXPLICIT
  catAxisLineSize: 1,

  // Value axis
  valAxisHidden: true,
  valAxisLabelColor: '202020',      // EXPLICIT

  // Grid lines
  catGridLine: { style: 'none' },
  valGridLine: { color: 'BEC1BE', style: 'dot', size: 0.75 },

  // Legend
  showLegend: false,

  // Plot area
  plotArea: {
    fill: { color: 'FFFFFF' },
    border: { color: 'BEC1BE', pt: 0.5 }
  },
});
```

## Status Colors for Charts

| Status | Hex | Use For |
|--------|-----|---------|
| Success/Positive | `73AF3C` | Growth, improvements |
| Alert/Negative | `AA0028` | Declines, issues, CMTs |
| Neutral | `939793` | Baseline, previous period |

## Chart Design Best Practices

### Clean, Minimal Charts
1. **Remove clutter**: Hide gridlines where possible
2. **Single focus**: Each chart = ONE key message
3. **Data labels**: Only show if they add value
4. **Legend**: Position at bottom or right, never obscuring data
5. **Colors**: Max 3-4 colors per chart

### Supporting Key Messages
- Add callout boxes for insights (e.g., "+47%", "-800K")
- Use roundRect shapes for highlight callouts
- Keep subtitle explaining the data context

### Layout Tips
- **Two-column**: Chart on right, text/bullets on left (40/60 split)
- **Full-width**: Single important chart with annotations
- **Bar charts**: Use `barGapWidthPct: 35` for clean spacing

## Complete Chart Colors Reference

```javascript
const NBG = {
  colors: {
    // Chart series (in order)
    cyan: '00ADBF',
    darkTeal: '003841',
    teal: '007B85',
    mediumGray: '939793',
    lightGray: 'BEC1BE',
    brightCyan: '00DFF8',

    // Text/labels
    darkText: '202020',

    // Status
    success: '73AF3C',
    alert: 'AA0028',

    // Backgrounds
    white: 'FFFFFF',
    offWhite: 'F5F8F6',
  },

  chartColors: ['00ADBF', '003841', '007B85', '939793', 'BEC1BE', '00DFF8'],
};
```

## Avoiding Default Colors

PptxGenJS may inject default colors (like #333333) if you don't specify them explicitly. Always include these properties:

```javascript
// ALWAYS INCLUDE THESE to avoid #333333 defaults:
catAxisLabelColor: '202020',
valAxisLabelColor: '202020',
catAxisLineColor: 'BEC1BE',
legendColor: '202020',
dataLabelColor: '202020',
valueFontColor: '202020',
```

## Table Configuration

```javascript
// Header row
const headerStyle = {
  fontFace: 'Aptos',
  fontSize: 11,
  bold: true,
  color: 'FFFFFF',
  fill: { color: '003841' },
};

// Data rows
const cellStyle = {
  fontFace: 'Aptos',
  fontSize: 10,
  color: '202020',
  fill: { color: 'E6F0F1' },  // Light teal tint
};

// Alternating rows
const altCellStyle = {
  ...cellStyle,
  fill: { color: 'F0F5F3' },
};

// Table options
{
  border: { pt: 1, color: 'FFFFFF' },
  align: 'left',
  valign: 'middle',
}
```
