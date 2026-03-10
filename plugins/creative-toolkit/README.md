# Creative Toolkit

Reusable creative agents for icon design, data visualization, and device mockups. Brand-configurable with NBG as the default brand system.

## Agents

| Agent | Purpose |
|-------|---------|
| **Icon Designer** | SVG icon generation — solid fill, monochrome, geometric |
| **Infographic Specialist** | Charts, diagrams, KPI dashboards, data visualizations |
| **Device Mockup** | Pixel-perfect iPhone mockups from app screenshots |

## Commands

| Command | Description |
|---------|-------------|
| `/create-icon` | Generate an SVG icon |
| `/create-infographic` | Create a data visualization or infographic |

## Brand Configuration

All agents default to the **NBG brand system** (colors, fonts, specifications). When called from `presentation-maker`, they use the full brand spec at `presentation-maker/shared/nbg-brand-system/README.md`.

When called standalone or from other plugins, agents use the NBG defaults embedded in their SKILL files. To use a different brand, pass brand config as input.

### Default Colors (NBG)

| Name | Hex | Usage |
|------|-----|-------|
| Dark Teal | `#003841` | Standard icon fill, titles |
| NBG Teal | `#007B85` | Brand emphasis |
| Cyan | `#00ADBF` | Primary chart color |
| Bright Cyan | `#00DFF8` | Accents |
| Dark Text | `#202020` | Body text |

### Default Font
- Primary: Aptos
- Fallback: Arial

## Used By

- `presentation-maker` — calls these agents during the presentation pipeline
- Can be used standalone via `/create-icon` and `/create-infographic`
