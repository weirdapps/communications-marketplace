---
description: "Review inbox with briefing, insights, action recommendations, and draft replies"
argument-hint: "[inbox|archive|both] [--count N] [--briefing-only]"
allowed-tools: Agent, Read, Write, Edit, Bash, Glob, Grep, mcp__plugin_playwright_playwright__browser_navigate, mcp__plugin_playwright_playwright__browser_snapshot, mcp__plugin_playwright_playwright__browser_click, mcp__plugin_playwright_playwright__browser_press_key, mcp__plugin_playwright_playwright__browser_run_code, mcp__plugin_playwright_playwright__browser_take_screenshot, mcp__plugin_playwright_playwright__browser_evaluate
---

<objective>
Read Outlook emails, provide a comprehensive briefing with insights, recommend actions, and draft replies matching the user's communication style (defined in `shared/style-guide.md`).

User request: $ARGUMENTS
</objective>

<process>
## Workflow

### 0. Learn from Previous Drafts (AUTOMATIC — runs silently every time)
Check `~/.claude/drafts/pending/` for unprocessed draft files.
If pending drafts exist:
1. Navigate to Outlook Web and search for matching sent emails (CC'd copies in inbox/archive)
   - Match by subject keywords and approximate date (within 72h of draft creation)
2. For each matched draft:
   - Extract the ACTUAL reply text the user sent (strip signature and quoted text)
   - Compare against the `draft_text` from the pending JSON
   - Classify: SENT_AS_IS | MODIFIED | REWRITTEN | NOT_SENT
   - Note specific differences (words, tone, length, structure)
3. Also scan the last 10 sent items for organic emails not matching any draft
4. If any learnings found:
   - Update `shared/style-guide.md` in the email-handler plugin directory
   - Append a dated entry to `~/.claude/drafts/learnings.md`
   - Move processed drafts from `pending/` to `reviewed/` with added fields
5. Show a brief learning summary:
   ```
   LEARNING: Processed N drafts — X/N sent as-is, Y modified
   Style guide updated: [changes]
   ```

### 1. Load Context
- Read the communication style guide from `shared/style-guide.md`
- Read `~/.claude/drafts/inbox-state.json` to know which emails were seen in the previous run

### 2. Read Emails
Navigate to Outlook Web (https://outlook.office.com/mail/inbox or /mail/archive):
- **Inbox**: Read ALL emails — the inbox is a to-do list of unprocessed items
- **Archive**: Read last N emails (default 20) — for reference only
For each email, extract: From, To/Cc, Subject, Body, Thread context, Timestamp

### 3. Classify New vs Previously Seen
Compare current inbox against `inbox-state.json`:
- **NEW**: Emails not in the previous state (arrived since last run)
- **PREVIOUSLY SEEN**: Emails that were in inbox during a prior run
  - If previously seen with an action recommendation, note if the user acted on it or not

### 4. Analyze & Recommend Actions
For each email, determine:

| Action | When | Symbol |
|--------|------|--------|
| **REPLY** | Needs your direct response (decision, approval, input) | ↩️ |
| **DELEGATE** | Someone on your team should handle this | 👉 |
| **FORWARD** | Needs to be sent to someone outside the thread | ➡️ |
| **MONITOR** | You're CC'd or FYI — no action now but keep an eye | 👀 |
| **URGENT** | Time-sensitive, needs immediate attention | ⚡ |
| **SKIP** | No action needed (newsletter, notification, auto-email) | ⏭️ |
| **FOLLOW-UP** | You already replied but thread needs follow-up check | 🔄 |

Multiple actions can apply (e.g., URGENT + REPLY).

### 5. Generate Gist
For each email, write a 1-2 sentence gist:
- What is this about? (substance, not just subject)
- What does the sender want from you specifically?
- Any context that matters (deadline, escalation, repeat request)

### 6. Present Inbox Briefing
Present the briefing in this format:

```
═══════════════════════════════════════════════
INBOX BRIEFING — [date], [time]
═══════════════════════════════════════════════

NEW SINCE LAST RUN ([count] emails)
───────────────────────────────────────────────
1. [SENDER] — [Subject]
   GIST: [1-2 sentence summary]
   ACTION: [symbol] [ACTION] — [brief reason]

2. [SENDER] — [Subject]
   GIST: [1-2 sentence summary]
   ACTION: [symbol] [ACTION] — [brief reason]

PREVIOUSLY SEEN ([count] emails)
───────────────────────────────────────────────
3. [SENDER] — [Subject]
   GIST: [1-2 sentence summary]
   STATUS: [still waiting / user replied / updated since last run]
   ACTION: [symbol] [ACTION] — [brief reason]

INSIGHTS
───────────────────────────────────────────────
- [X] emails need your decision/reply
- [Pattern/theme observed, e.g., "Boss escalated same issue twice this week"]
- [Urgency note, e.g., "Sender X waiting since 20:57 — no response yet"]
- [Delegation opportunity, e.g., "3 emails could be handled by your team"]
- [Any thread connections between emails]
═══════════════════════════════════════════════
```

### 7. Draft Replies
For each email marked REPLY or DELEGATE:
- Generate a reply following the style guide exactly
- Adapt tone per recipient using per-recipient profiles
- For DELEGATE: draft a forwarding message or a reply that assigns ownership

For each email marked FORWARD:
- Suggest who to forward to and draft forwarding text (if any)

### 8. Present Drafts & Confirm
Show all drafts for user review.
Ask which to send, modify, or discard.

### 9. Save State
**Save drafts**: For each draft created, save a JSON file to `~/.claude/drafts/pending/`:
```json
{
  "id": "YYYY-MM-DD-NNN",
  "created": "ISO-8601 timestamp",
  "subject": "email subject",
  "subject_keywords": ["key", "words"],
  "original_from": "sender name",
  "recipients_to": ["names"],
  "recipients_cc": ["names"],
  "reply_type": "reply | reply_all | forward",
  "draft_text": "exact draft text",
  "draft_style": "BRIEF | FULL",
  "draft_pattern": "Type N (pattern name)",
  "status": "pending"
}
```

**Update inbox state**: Write `~/.claude/drafts/inbox-state.json`:
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
      "action_taken": "DRAFTED|SKIPPED|PENDING",
      "gist": "1-line summary"
    }
  ]
}
```

### 10. Create Drafts via Mac Outlook Reply All

For each approved draft, create a Reply All draft using the Mac Outlook client. This produces proper formatting: reply text, signature, HR separator, and full quoted thread — all natively handled by Outlook.

**Method**: Use AppleScript UI scripting with clipboard paste (NOT keystroke typing, which loses focus).

```bash
# Step 1: Set clipboard with reply text
echo -n "reply text here" | pbcopy

# Step 2: AppleScript to select email, Reply All, paste, save
osascript <<'SCRIPT'
tell application "Microsoft Outlook" to activate
delay 0.5
tell application "System Events"
  tell process "Microsoft Outlook"
    perform action "AXRaise" of window "Inbox • All Accounts"
    delay 0.5
    set w to window "Inbox • All Accounts"
    set sg to UI element 2 of w
    set spg to splitter group 1 of sg
    set spg2 to splitter group 1 of spg
    set msgList to group 1 of spg2
    set sa to scroll area 1 of msgList
    set tbl to table 1 of sa

    -- Click on the target email row
    perform action "AXPress" of UI element 1 of row ROW_NUMBER of tbl
    delay 1

    -- Reply All
    click menu item "Reply All" of menu "Message" of menu bar 1
    delay 2

    -- Paste reply text from clipboard
    keystroke "v" using command down
    delay 1

    -- Save as draft
    keystroke "s" using command down
    delay 1

    -- Close compose to go back to reading pane
    key code 53
    delay 0.5
  end tell
end tell
SCRIPT
```

**Finding the right row**: Before creating drafts, scan the message list to find each email's row number by matching sender name in `description of UI element 1 of row N of tbl`.

**For multi-line reply text**: Use `printf '%s' "line1\n\nline2" | pbcopy` to preserve newlines.

**Important**: Always return to the Inbox folder after all drafts are created.

**Fallback**: If Mac client is unavailable, use `/send-mail` to create new emails via AppleScript (does not include original thread).
</process>

<specifications>
## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `folder` | No | `both` | Which folder to read: `inbox`, `archive`, or `both` |
| `--count` | No | `20` | Number of recent emails to process |
| `--unread` | No | `false` | Only process unread emails |
| `--learn` | No | `false` | Run ONLY learning mode (skip reading new emails) |
| `--briefing-only` | No | `false` | Show briefing and insights only, skip drafting |

## Output
- Learning summary (if pending drafts found)
- Inbox briefing with new vs previously seen separation
- Action recommendations with gists
- Insights and patterns
- Draft replies for actionable emails
- Option to send via Outlook
</specifications>

<examples>
## Usage Examples

### Full workflow — briefing + drafts (auto-learns first)
```
/draft
```

### Just the briefing, no drafts
```
/draft --briefing-only
```

### Read last 50 from archive
```
/draft archive --count 50
```

### Only unread emails
```
/draft --unread
```

### Learning mode only — process pending drafts
```
/draft --learn
```
</examples>
