---
description: "Brief description shown in command list"
argument-hint: "[required-input] [--optional-flag]"
allowed-tools: Task, Read, Write, Bash
---

<objective>
Execute the example command with the user's input.

User request: $ARGUMENTS
</objective>

<process>
## Workflow

### 1. Parse Input
- Extract required arguments
- Parse optional flags
- Validate input format

### 2. Process Request
Based on input type:
- **Type A**: Apply processing strategy A
- **Type B**: Apply processing strategy B
- **Unknown**: Request clarification

### 3. Execute Main Logic
- Invoke relevant agents if needed
- Apply transformations
- Generate output

### 4. Quality Check
- Verify output completeness
- Validate format
- Ensure quality standards met

### 5. Return Results
- Format output appropriately
- Include any warnings or notes
- Suggest next steps if applicable
</process>

<specifications>
## Technical Specifications

### Input Format
```
/example-command [input] [--flag value]
```

### Arguments
| Argument | Required | Description |
|----------|----------|-------------|
| `input` | Yes | The main input to process |
| `--flag` | No | Optional modifier flag |
| `--verbose` | No | Show detailed output |

### Output Format
Describe what the command outputs (file, message, etc.)
</specifications>

<examples>
## Usage Examples

### Basic Usage
```bash
/example-command "Hello world"
```

### With Options
```bash
/example-command "Input text" --flag value
```

### Complex Input
```bash
/example-command "Multi-line
input content" --verbose
```
</examples>

<success_criteria>
## Success Criteria

- [ ] Input parsed correctly
- [ ] Processing completed without errors
- [ ] Output matches expected format
- [ ] Quality standards met
- [ ] User receives actionable result
</success_criteria>

<related_commands>
## Related Commands

| Command | When to Use |
|---------|-------------|
| `/other-command` | When you need different functionality |
| `/helper-command` | For supplementary tasks |
</related_commands>
