---
description: "Read inbox and present a briefing with summaries, action recommendations, and insights — no drafting or replying"
argument-hint: "[inbox|archive|both] [--count N] [--unread]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

<objective>
Read emails via Apple Mail AppleScript and present a concise inbox briefing with summaries, action recommendations, and strategic insights. This command is read-only — it never drafts, replies, or modifies any email.

**Architecture**: This plugin uses a hybrid approach — Apple Mail for reading (full AppleScript access to Exchange mailboxes), Outlook for sending/replying (proper signatures, threading, draft handling).

User request: $ARGUMENTS
</objective>

<process>
## Workflow

### 1. Load Previous State
- Read `~/.claude/drafts/inbox-state.json` (if exists) to know which emails were seen before

### 2. Read Emails via Apple Mail AppleScript

Use the Bash tool to run AppleScript against Apple Mail. The NBG Exchange account is available as `account "Exchange"`.

**Reading the inbox:**
```applescript
tell application "Mail"
    set msgs to messages of inbox
    -- Or for a specific count:
    set msgs to messages 1 thru N of inbox
    repeat with m in msgs
        set output to output & "---" & linefeed
        set output to output & "FROM: " & sender of m & linefeed
        set output to output & "SUBJECT: " & subject of m & linefeed
        set output to output & "DATE: " & (date received of m as string) & linefeed
        set output to output & "READ: " & read status of m & linefeed
        set output to output & "TO: " & (address of every to recipient of m) & linefeed
        set output to output & "CC: " & (address of every cc recipient of m) & linefeed
        set output to output & "BODY: " & text 1 thru 500 of (content of m) & linefeed
    end repeat
    return output
end tell
```

**Reading archive:**
```applescript
tell application "Mail"
    set archiveBox to mailbox "Archive" of account "Exchange"
    set msgs to messages 1 thru N of archiveBox
    -- same loop as above
end tell
```

**Reading full message body** (for important/complex emails):
```applescript
tell application "Mail"
    set msg to message N of inbox
    return content of msg
end tell
```

**Key points:**
- Process messages in batches (e.g., 5-10 at a time) to avoid AppleScript timeouts on large inboxes
- Use `content of msg` for plain text body (reliable, fast)
- `source of msg` gives raw MIME source (may timeout on large messages — avoid unless needed)
- `read status` returns true/false for read/unread
- For `--unread` flag: filter by `read status of m is false`

### 3. Classify New vs Previously Seen
Compare current inbox against `inbox-state.json`:
- **NEW**: Emails not in the previous state
- **PREVIOUSLY SEEN**: Emails present in a prior run
  - Note if user appears to have acted (email moved to archive, reply sent, etc.)

### 4. Analyze & Recommend Actions
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

### 5. Generate Gist
For each email, write a 1-2 sentence gist:
- What is this about? (substance, not just subject line)
- What does the sender want from you specifically?
- Any context that matters (deadline, escalation, repeat request)

### 6. Present Briefing

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

### 7. Save Inbox State
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
- NO drafting, NO replying, NO email modification
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
