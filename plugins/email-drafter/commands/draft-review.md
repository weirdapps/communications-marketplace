---
description: "Compare drafted replies with actual responses to improve the style guide"
argument-hint: "[--days N]"
allowed-tools: Agent, Read, Write, Edit, Bash, mcp__plugin_playwright_playwright__browser_navigate, mcp__plugin_playwright_playwright__browser_snapshot, mcp__plugin_playwright_playwright__browser_click, mcp__plugin_playwright_playwright__browser_press_key, mcp__plugin_playwright_playwright__browser_run_code, mcp__plugin_playwright_playwright__browser_take_screenshot, mcp__plugin_playwright_playwright__browser_evaluate
---

<objective>
Compare past email drafts with actual responses sent by Dimitris Plessas, identify style deltas, and update the style guide.

User request: $ARGUMENTS
</objective>

<process>
## Workflow

### 1. Read Actual Responses
Navigate Outlook Web to read emails FROM Dimitris (CC'd copies in inbox/archive).
Since he CC's himself, his replies appear in inbox/archive with him as sender.

### 2. Match Against Previous Drafts
For each actual response, check if the agent previously drafted a reply for the same thread.
If draft-log.json exists in the shared directory, use it for matching.

### 3. Analyze Deltas
For each matched pair (draft vs actual), analyze:

| Dimension | Check |
|-----------|-------|
| **Length** | Was draft longer/shorter than actual? |
| **Tone** | Did tone match? Was draft too formal/informal? |
| **Content** | Did he say the same thing differently? |
| **Words** | Did he use specific words/phrases the draft missed? |
| **Decision** | Did he approve/reject differently than drafted? |
| **Skip/Reply** | Did he reply to something we skipped, or skip what we drafted? |

### 4. Generate Delta Report
Present findings as a table:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STYLE DELTA REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ACCURACY SCORE: X/10

PATTERNS LEARNED:
• [New pattern discovered]
• [Correction to existing pattern]

RECIPIENT UPDATES:
• [Recipient]: [Style adjustment needed]

TRIAGE ACCURACY:
• Correctly skipped: X
• Correctly drafted: X
• False positives (drafted but he skipped): X
• False negatives (skipped but he replied): X
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 5. Update Style Guide
With user approval, update `shared/style-guide.md` with:
- New patterns discovered
- Corrections to existing patterns
- New recipient profiles
- Updated per-recipient tone adjustments
- New example phrases

### 6. Save Learning Log
Append findings to `shared/learning-log.md` for historical tracking.
</process>

<specifications>
## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--days` | No | `1` | How many days back to compare |
| `--recipient` | No | all | Focus on a specific recipient |
| `--update` | No | `false` | Auto-update style guide without asking |

## Output
- Delta report with accuracy score
- Specific style corrections
- Updated style guide (with approval)
</specifications>

<examples>
## Usage Examples

### Review today's emails
```
/draft-review
```

### Review last week
```
/draft-review --days 7
```

### Focus on boss communication
```
/draft-review --recipient ΘΕΟΦΙΛΙΔΗ
```
</examples>
