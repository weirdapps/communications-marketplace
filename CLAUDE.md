# Communications Marketplace

Plugin marketplace for Claude Code providing communication and productivity workflows.

## Structure

```
plugins/
├── presentation-maker/      # Multi-agent presentation system (v3.2)
│   ├── orchestrator/        # Master workflow orchestrator
│   ├── agents/              # Storyline, Storyboard, Graphics agents
│   ├── shared/nbg-brand-system/  # Brand source of truth
│   ├── commands/            # /create-presentation, /redesign-deck, /polish-slides
│   └── depends on: creative-toolkit
├── creative-toolkit/        # Reusable creative agents (v1.0)
│   ├── agents/              # Icon Designer, Infographic Specialist, Device Mockup
│   └── commands/            # /create-icon, /create-infographic
├── email-handler/           # Email command center with self-learning (v2.0)
│   ├── agents/email-handler/  # 10-phase workflow agent
│   ├── commands/            # /mail-review, /draft-review, /send-mail
│   └── shared/              # Style guide, recipient profiles
└── _template/               # Template for new plugins
```

## Plugins

### Presentation Maker
Multi-agent presentation system for NBG. Orchestrates storyline, storyboard, and rendering agents.
- Entry point: `/create-presentation` or `plugins/presentation-maker/orchestrator/nbg-presenter/SKILL.md`
- Depends on: `creative-toolkit` (for icons, infographics, device mockups)

### Creative Toolkit
Reusable creative agents for icon design, data visualization, and device mockups. Brand-configurable with NBG defaults.
- Entry points: `/create-icon`, `/create-infographic`
- Used by: `presentation-maker`

### Email Handler
Email command center. Reviews inbox with briefings and insights, recommends actions, drafts replies matching your style, sends via Outlook, and self-improves by comparing drafts to actual responses.
- Entry points: `/mail-review`, `/draft-review`, `/send-mail`
- Persistent state: `~/.claude/drafts/` (pending drafts, reviewed drafts, inbox state, learnings)

## File Naming Convention

All output files (presentations, icons, infographics, mockups, exports) MUST use this naming format:

```
YYYYMMDDHHMM_descriptive_name.ext
```

- **Timezone**: Europe/Athens (`TZ='Europe/Athens' date '+%Y%m%d%H%M'`)
- **Case**: all lowercase
- **Separators**: spaces and hyphens → underscores (`_`)
- **Timestamp**: always the save/export time (updates on re-save)
- **Examples**: `202603150208_quarterly_results.pptx`, `202603141030_payment_icon.svg`

## Install / Test

```bash
./install.sh          # Interactive plugin installer
./uninstall.sh        # Remove installed plugins
```
