# Creating Plugins for Communications Marketplace

This guide explains how to create a new plugin for the Communications Marketplace.

## Plugin Structure

Every plugin must follow this structure:

```
plugins/my-plugin/
├── plugin.json          # Required: Plugin manifest
├── README.md            # Required: Plugin documentation
├── agents/              # Optional: AI agents
│   └── my-agent/
│       └── SKILL.md
├── commands/            # Optional: Slash commands
│   └── my-command.md
├── shared/              # Optional: Shared configurations
├── assets/              # Optional: Static assets
└── tools/               # Optional: Build tools/scripts
```

## Step 1: Create Plugin Directory

```bash
# Copy the template
cp -r plugins/_template plugins/my-plugin
```

## Step 2: Configure plugin.json

The `plugin.json` file is the manifest for your plugin:

```json
{
  "name": "my-plugin",
  "description": "Brief description of what this plugin does",
  "version": "1.0.0",
  "type": "plugin",
  "author": {
    "name": "Your Name"
  },
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "commands": "./commands",
  "agents": {
    "my-agent": {
      "path": "./agents/my-agent/SKILL.md",
      "description": "What this agent does",
      "triggers": [
        "trigger phrase 1",
        "trigger phrase 2"
      ]
    }
  }
}
```

### Required Fields

| Field | Description |
|-------|-------------|
| `name` | Unique plugin identifier (lowercase, hyphens) |
| `description` | Brief description (shown in marketplace) |
| `version` | Semantic version (e.g., "1.0.0") |
| `type` | Must be "plugin" |

### Optional Fields

| Field | Description |
|-------|-------------|
| `author` | Plugin author information |
| `license` | License type |
| `keywords` | Search keywords |
| `commands` | Path to commands directory |
| `agents` | Agent definitions |

## Step 3: Create Agents

Agents are AI assistants with specific skills. Create a `SKILL.md` file for each agent:

```markdown
# My Agent

## Role
Brief description of this agent's role.

## Capabilities
- Capability 1
- Capability 2

## Inputs
What this agent expects as input.

## Outputs
What this agent produces.

## Workflow
1. Step 1
2. Step 2
3. Step 3

## Guidelines
- Important rules to follow
```

### Agent Triggers

Triggers are phrases that automatically activate an agent:

```json
{
  "agents": {
    "my-agent": {
      "triggers": [
        "create a report",
        "generate report",
        "make report"
      ]
    }
  }
}
```

## Step 4: Create Commands

Commands are slash commands users can invoke. Create a `.md` file for each command:

```markdown
# /my-command

Brief description.

## Usage
\`\`\`
/my-command [arg1] [arg2]
\`\`\`

## Arguments
| Argument | Required | Description |
|----------|----------|-------------|
| arg1 | Yes | Description |

## Examples
\`\`\`
/my-command value1 value2
\`\`\`
```

## Step 5: Register in Marketplace

Add your plugin to `.claude-plugin/marketplace.json`:

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "communications-marketplace",
  "description": "Your marketplace description",
  "owner": {
    "name": "your-username"
  },
  "plugins": [
    {
      "name": "my-plugin",
      "description": "What it does",
      "version": "1.0.0",
      "author": {
        "name": "Your Name"
      },
      "source": "./plugins/my-plugin",
      "category": "category-id",
      "homepage": "https://github.com/username/repo/tree/main/plugins/my-plugin"
    }
  ]
}
```

**Note:** The `plugins` field is an **array**, not an object. Each plugin entry includes:
- `name`: Unique identifier
- `description`: Brief description (shown in marketplace)
- `version`: Semantic version
- `source`: Path to plugin directory
- `category`: Plugin category ID

### Available Categories

| Category ID | Description |
|-------------|-------------|
| `presentations` | Presentation creation tools |
| `documents` | Document generation |
| `communications` | Email, messaging tools |
| `data-viz` | Data visualization |

## Step 6: Update CLAUDE.md Configuration

If your plugin needs specific CLAUDE.md instructions, add them to `install.sh`:

```bash
generate_myplugin_config() {
    cat << 'CLAUDE_CONTENT'
---

## MY-PLUGIN Configuration

Instructions for Claude...

---
CLAUDE_CONTENT
}
```

Then update the `generate_plugin_config` function:

```bash
generate_plugin_config() {
    local plugin_name=$1
    case "$plugin_name" in
        "my-plugin")
            generate_myplugin_config
            ;;
        # ... other plugins
    esac
}
```

## Best Practices

### Naming
- Use lowercase with hyphens for plugin names
- Use descriptive, action-oriented command names
- Use clear, role-based agent names

### Documentation
- Include a comprehensive README.md
- Document all commands and their arguments
- Provide usage examples

### Organization
- Keep related functionality together
- Use `shared/` for common configurations
- Use `assets/` for logos, templates, etc.

### Versioning
- Follow semantic versioning (MAJOR.MINOR.PATCH)
- Update version when making changes
- Document changes in a CHANGELOG if needed

## Testing Your Plugin

1. Install the marketplace locally
2. Run the installer and select your plugin
3. Test all commands and triggers
4. Verify CLAUDE.md configuration works

## Submitting Your Plugin

1. Fork the repository
2. Create your plugin following this guide
3. Test thoroughly
4. Submit a pull request with:
   - Description of the plugin
   - Usage examples
   - Any special requirements

## Example Plugins

See `plugins/nbg-presentations/` for a complete example of a production plugin with:
- Multiple agents in a pipeline
- Multiple commands
- Brand system in `shared/`
- Assets and templates
- Build tools
