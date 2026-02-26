# Contributing to Communications Marketplace

Thank you for your interest in contributing to the Communications Marketplace.

## Table of Contents

- [Getting Started](#getting-started)
- [Creating a New Plugin](#creating-a-new-plugin)
- [Plugin Architecture](#plugin-architecture)
- [Quality Standards](#quality-standards)
- [Submitting Changes](#submitting-changes)

## Getting Started

### Prerequisites

- Git
- Claude Code CLI installed
- Basic understanding of YAML and JSON

### Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/weirdapps/communications-marketplace.git
cd communications-marketplace
```

2. Create a branch for your changes:
```bash
git checkout -b feature/my-new-plugin
```

## Creating a New Plugin

### 1. Copy the Template

```bash
cp -r plugins/_template plugins/my-plugin
```

### 2. Update Plugin Manifest

Edit `plugins/my-plugin/plugin.json`:

```json
{
  "name": "my-plugin",
  "description": "What your plugin does",
  "version": "1.0.0",
  "author": {
    "name": "Your Name"
  },
  "commands": "./commands",
  "agents": {
    "my-agent": {
      "path": "./agents/my-agent/SKILL.md",
      "description": "What this agent does"
    }
  }
}
```

### 3. Create Your Agents

Create `agents/my-agent/SKILL.md` following the template structure.

### 4. Create Your Commands

Create `commands/my-command.md` following the command template.

### 5. Register in Marketplace

Add your plugin to `.claude-plugin/marketplace.json`:

```json
{
  "name": "my-plugin",
  "description": "Brief description",
  "version": "1.0.0",
  "author": { "name": "Your Name" },
  "source": "./plugins/my-plugin",
  "category": "productivity"
}
```

## Plugin Architecture

### Standard Directory Structure

```
my-plugin/
├── plugin.json          # Manifest (required)
├── README.md            # Documentation (required)
│
├── agents/              # AI agents (if any)
│   └── my-agent/
│       └── SKILL.md     # Agent instructions
│
├── commands/            # Slash commands (if any)
│   └── my-command.md
│
├── orchestrator/        # Master orchestrator (optional)
│   └── main/
│       └── SKILL.md
│
├── shared/              # Common specs (optional)
│   └── specs.md
│
└── assets/              # Static assets (optional)
```

### Required Files

| File | Purpose |
|------|---------|
| `plugin.json` | Plugin manifest with metadata |
| `README.md` | User-facing documentation |

### Optional Components

| Component | When to Include |
|-----------|-----------------|
| `agents/` | When you need AI-powered capabilities |
| `commands/` | When exposing slash commands |
| `orchestrator/` | When coordinating multiple agents |
| `shared/` | When multiple agents share specifications |
| `assets/` | When including static files (images, templates) |

## Quality Standards

### Code Quality

- All JSON files must be valid (validated by CI)
- All SKILL.md files must follow template structure
- README must document all features

### Documentation Quality

- Clear, concise descriptions
- Working examples
- Troubleshooting section

### Plugin Naming

- Use kebab-case: `my-plugin`
- Be descriptive but concise
- Avoid generic names

### Version Numbers

Follow semantic versioning:
- `1.0.0` - Initial release
- `1.1.0` - New features (backward compatible)
- `1.0.1` - Bug fixes
- `2.0.0` - Breaking changes

## Submitting Changes

### Before Submitting

1. **Test your changes locally**:
```bash
# Validate JSON files
cat .claude-plugin/marketplace.json | python3 -m json.tool
cat plugins/my-plugin/plugin.json | python3 -m json.tool
```

2. **Update documentation** if needed

3. **Add CHANGELOG entry** if adding new features

### Pull Request Process

1. Push your branch:
```bash
git add .
git commit -m "Add my-plugin: brief description"
git push origin feature/my-new-plugin
```

2. Open a Pull Request on GitHub

3. Fill in the PR template:
   - Describe what the plugin does
   - List the commands/agents included
   - Note any dependencies

4. Wait for CI validation to pass

5. Address any review feedback

### PR Title Convention

```
[plugin-name] Brief description

Examples:
[nbg-presentations] Fix Thank You slide contradiction
[my-plugin] Add new feature X
[docs] Update contributing guide
```

## Questions?

- Open an issue for questions
- Check existing plugins for examples
- Review the `_template` plugin structure

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.
