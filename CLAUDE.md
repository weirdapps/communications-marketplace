# Communications Marketplace

Plugin marketplace for Claude Code providing communication and productivity workflows.

## Structure

```
plugins/
├── nbg-presentations/   # NBG-branded presentation generator (v3.0)
│   ├── shared/nbg-brand-system/README.md  # Brand source of truth
│   ├── orchestrator/    # Master workflow skill
│   ├── agents/          # Storyline, Storyboard, Graphics agents
│   └── skills/          # User-facing slash commands
└── _template/           # Template for new plugins
```

## NBG Presentations

Brand specs and full workflow are defined in the skill files — read them via skills, not from this file.
Entry point: `/create-presentation` skill or `plugins/nbg-presentations/orchestrator/nbg-presenter/SKILL.md`

## Install / Test

```bash
./install.sh          # Interactive plugin installer
./uninstall.sh        # Remove installed plugins
```
