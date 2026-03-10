# Communications Marketplace

Plugin marketplace for Claude Code providing communication and productivity workflows.

## Structure

```
plugins/
├── presentation-maker/      # Multi-agent presentation system (v3.1)
│   ├── orchestrator/        # Master workflow orchestrator
│   ├── agents/              # Storyline, Storyboard, Graphics agents
│   ├── shared/nbg-brand-system/  # Brand source of truth
│   ├── commands/            # /create-presentation, /redesign-deck, /polish-slides
│   └── depends on: creative-toolkit
├── creative-toolkit/        # Reusable creative agents (v1.0)
│   ├── agents/              # Icon Designer, Infographic Specialist, Device Mockup
│   └── commands/            # /create-icon, /create-infographic
├── email-drafter/           # AI email drafter with style-matching (v1.0)
│   ├── agents/email-drafter/  # 5-phase workflow agent
│   ├── commands/            # /draft, /draft-review
│   ├── shared/              # Style guide, recipient profiles
│   └── depends on: outlook-mailer
├── outlook-mailer/          # Send emails via macOS Outlook (v1.0)
│   └── commands/            # /send-mail
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

### Email Drafter
Reads Outlook emails via Playwright, drafts replies matching your communication style, and learns from comparing drafts to actual responses.
- Entry point: `/draft` command
- Depends on: `outlook-mailer` (for sending drafts to Outlook)

### Outlook Mailer
Send emails via Microsoft Outlook on macOS using AppleScript.
- Entry point: `/send-mail` command

## Install / Test

```bash
./install.sh          # Interactive plugin installer
./uninstall.sh        # Remove installed plugins
```
