---
description: "Compare drafted replies with actual responses to improve the style guide"
argument-hint: "[--days N]"
allowed-tools: Agent, Read, Write, Edit, Bash, Glob, Grep, mcp__plugin_playwright_playwright__browser_navigate, mcp__plugin_playwright_playwright__browser_snapshot, mcp__plugin_playwright_playwright__browser_click, mcp__plugin_playwright_playwright__browser_press_key, mcp__plugin_playwright_playwright__browser_run_code, mcp__plugin_playwright_playwright__browser_take_screenshot, mcp__plugin_playwright_playwright__browser_evaluate
---

<objective>
Compare past email drafts with actual responses sent by the user, identify style deltas, and update the style guide.

User request: $ARGUMENTS
</objective>

<process>
## Workflow

### 1. Load Pending Drafts
Read all JSON files from `~/.claude/drafts/pending/`.
Also optionally read `~/.claude/drafts/reviewed/` for historical reference.

### 2. Find Matching Sent Emails
Navigate Outlook Web to find emails FROM the user (CC'd copies in inbox/archive):
- Search by subject keywords from each pending draft
- Match by subject + approximate timestamp (within 72h)
- Read the actual email body

### 3. Analyze Deltas
For each matched pair (draft vs actual), analyze:

| Dimension | Check |
|-----------|-------|
| **Length** | Was draft longer/shorter than actual? |
| **Tone** | Did tone match? Was draft too formal/informal? |
| **Content** | Did they say the same thing differently? |
| **Words** | Did they use specific words/phrases the draft missed? |
| **Decision** | Did they approve/reject differently than drafted? |
| **Skip/Reply** | Did they reply to something we skipped, or skip what we drafted? |

Classify each:
- **SENT_AS_IS**: Draft sent unchanged (score: perfect)
- **MODIFIED**: Altered tone/length/words (score: partial — learn from diff)
- **REWRITTEN**: Substantially different (score: miss — analyze why)
- **NOT_SENT**: No matching email found (score: triage error — should have been SKIP)

### 4. Scan Organic Emails
Also scan last 20 sent items for emails NOT matching any draft.
These reveal patterns the style guide may be missing:
- New recipients not yet profiled
- New reply patterns
- Evolving vocabulary

### 5. Generate Delta Report
```
STYLE DELTA REPORT — [date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ACCURACY SCORE: X/10

DRAFTS PROCESSED: N
  SENT_AS_IS:  X (perfect matches)
  MODIFIED:    X (partial matches — learnings extracted)
  REWRITTEN:   X (misses — significant learnings)
  NOT_SENT:    X (triage errors)

PATTERNS LEARNED:
  [New pattern discovered]
  [Correction to existing pattern]

RECIPIENT UPDATES:
  [Recipient]: [Style adjustment needed]

TRIAGE ACCURACY:
  Correctly skipped: X
  Correctly drafted: X
  False positives: X (drafted but user skipped)
  False negatives: X (skipped but user replied)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 6. Update Style Guide
Update `shared/style-guide.md` with:
- New patterns discovered
- Corrections to existing patterns
- New recipient profiles
- Updated per-recipient tone adjustments
- New example phrases (anonymize sensitive content)

### 7. Archive Processed Drafts
Move processed drafts from `pending/` to `reviewed/` with added fields:
```json
{
  "actual_text": "what the user actually sent",
  "delta_type": "SENT_AS_IS | MODIFIED | REWRITTEN | NOT_SENT",
  "learnings": ["specific observation 1", "specific observation 2"],
  "reviewed_date": "ISO-8601 timestamp"
}
```

### 8. Append to Learning Log
Append the delta report to `~/.claude/drafts/learnings.md` with date header.
This builds a historical record of how drafting accuracy improves over time.
</process>

<specifications>
## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--days` | No | `3` | How many days back to search for sent emails |
| `--recipient` | No | all | Focus on a specific recipient |
| `--update` | No | `true` | Auto-update style guide (set false for dry run) |

## Output
- Delta report with accuracy score
- Specific style corrections
- Updated style guide
</specifications>

<examples>
## Usage Examples

### Review pending drafts (default)
```
/draft-review
```

### Review with wider search window
```
/draft-review --days 7
```

### Focus on specific recipient
```
/draft-review --recipient LASTNAME
```

### Dry run — see report without updating style guide
```
/draft-review --update false
```
</examples>
