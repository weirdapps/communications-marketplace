---
description: "Read inbox and present a briefing with summaries, action recommendations, and insights — no drafting or replying"
argument-hint: "[inbox|archive|both] [--count N] [--unread]"
allowed-tools: Read, Write, Edit, Glob, Grep, mcp__plugin_playwright_playwright__browser_navigate, mcp__plugin_playwright_playwright__browser_snapshot, mcp__plugin_playwright_playwright__browser_click, mcp__plugin_playwright_playwright__browser_press_key, mcp__plugin_playwright_playwright__browser_evaluate
---

<objective>
Read Outlook emails via Outlook Web and present a concise inbox briefing with summaries, action recommendations, and strategic insights. This command is read-only — it never drafts, replies, or modifies any email.

User request: $ARGUMENTS
</objective>

<process>
## Workflow

### 1. Load Previous State
- Read `~/.claude/drafts/inbox-state.json` (if exists) to know which emails were seen before

### 2. Navigate to Outlook Web
Open https://outlook.office.com/mail/inbox in the browser.

### 3. Read Emails
Scan the inbox by taking snapshots of the message list:
- **Inbox**: Read ALL visible emails — the inbox is a to-do list of unprocessed items
- **Archive** (if requested): Navigate to archive, read last N emails (default 20)
- Scroll down and take additional snapshots if needed to capture all emails
- For important/complex emails, click to open and read the full body

For each email, extract: From, To/Cc, Subject, Preview/Body, Timestamp

### 4. Classify New vs Previously Seen
Compare current inbox against `inbox-state.json`:
- **NEW**: Emails not in the previous state
- **PREVIOUSLY SEEN**: Emails present in a prior run
  - Note if user appears to have acted (email moved to archive, reply sent, etc.)

### 5. Analyze & Recommend Actions
For each email, determine one or more actions:

| Action | When | Symbol |
|--------|------|--------|
| **REPLY** | Needs your direct response (decision, approval, input) | ↩️ |
| **DELEGATE** | Someone on your team should handle this | 👉 |
| **FORWARD** | Needs to be sent to someone outside the thread | ➡️ |
| **MONITOR** | You're CC'd or FYI — no action now but keep an eye | 👀 |
| **URGENT** | Time-sensitive, needs immediate attention | ⚡ |
| **SKIP** | No action needed (newsletter, notification, auto-email) | ⏭️ |
| **FOLLOW-UP** | You already replied but thread needs follow-up check | 🔄 |

### 6. Generate Gist
For each email, write a 1-2 sentence gist:
- What is this about? (substance, not just subject line)
- What does the sender want from you specifically?
- Any context that matters (deadline, escalation, repeat request)

### 7. Present Briefing

```
═══════════════════════════════════════════════
INBOX BRIEFING — [date], [time]
[count] emails in inbox
═══════════════════════════════════════════════

NEW SINCE LAST RUN ([count])
───────────────────────────────────────────────
1. [SENDER] — [Subject]
   GIST: [1-2 sentence summary]
   ACTION: [symbol] [ACTION] — [brief reason]

2. ...

PREVIOUSLY SEEN ([count])
───────────────────────────────────────────────
N. [SENDER] — [Subject]
   GIST: [1-2 sentence summary]
   STATUS: [still in inbox / user replied / updated]
   ACTION: [symbol] [ACTION] — [brief reason]

═══════════════════════════════════════════════
INSIGHTS
═══════════════════════════════════════════════
- [X] emails need your decision/reply
- [Patterns observed, e.g., "3 emails from Cards team about same POS issue"]
- [Urgency flags, e.g., "ΥΦΑΝΤΙΔΗΣ waiting 2 days — no response yet"]
- [Delegation opportunities, e.g., "4 emails could be handled by sector heads"]
- [Thread connections between emails]
- [Suggested priorities for the day]
═══════════════════════════════════════════════
```

### 8. Save Inbox State
Write `~/.claude/drafts/inbox-state.json`:
```json
{
  "last_run": "ISO-8601 timestamp",
  "run_count": N,
  "seen_emails": [
    {
      "from": "sender name",
      "subject": "subject line",
      "timestamp": "email timestamp",
      "action_recommended": "REPLY|DELEGATE|FWD|MONITOR|SKIP|URGENT|FOLLOW-UP",
      "action_taken": "PENDING",
      "gist": "1-line summary"
    }
  ]
}
```
</process>

<specifications>
## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `folder` | No | `inbox` | Which folder to read: `inbox`, `archive`, or `both` |
| `--count` | No | `20` | Number of emails to process (for archive) |
| `--unread` | No | `false` | Only process unread emails |

## Output
- Inbox briefing with new vs previously seen separation
- 1-2 sentence gist per email
- Action recommendations with symbols
- Strategic insights and patterns
- NO drafting, NO replying, NO Outlook interaction beyond reading
</specifications>

<examples>
## Usage Examples

### Quick inbox scan
```
/inbox-briefing
```

### Include archive context
```
/inbox-briefing both
```

### Only unread
```
/inbox-briefing --unread
```

### Deep archive scan
```
/inbox-briefing archive --count 50
```
</examples>
