---
description: "Review inbox with briefing, insights, action recommendations, and draft replies"
argument-hint: "[inbox|archive|both] [--count N] [--briefing-only]"
allowed-tools: Agent, Read, Write, Edit, Bash, Glob, Grep
---

<objective>
Read emails via Apple Mail, provide a comprehensive briefing with insights, recommend actions, and draft replies matching the user's communication style (defined in `shared/style-guide.md`).

**Architecture**: Hybrid approach — Apple Mail for reading (full AppleScript access), Outlook for reply/forward drafts (UI scripting for proper signatures, threading, formatting).

User request: $ARGUMENTS
</objective>

<process>
## Workflow

### 0. Learn from Previous Drafts (AUTOMATIC — runs silently every time)
**First run**: If `~/.claude/drafts/` directory structure doesn't exist, create it automatically. If no `inbox-state.json` exists, treat all emails as NEW. Skip learning if no pending drafts.

Check `~/.claude/drafts/pending/` for unprocessed draft files.
If pending drafts exist:
1. Read Sent Items via Apple Mail AppleScript to find matching sent emails:
   ```applescript
   tell application "Mail"
       set sentBox to mailbox "Sent Items" of account "Exchange"
       set msgs to messages 1 thru 30 of sentBox
       -- search by subject keywords and date
   end tell
   ```
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

### 2. Read Emails via Apple Mail AppleScript

Use the Bash tool to run AppleScript against Apple Mail. The NBG Exchange account is available as `account "Exchange"`.

**Reading inbox messages:**
```applescript
tell application "Mail"
    set msgCount to count messages of inbox
    -- Read all inbox messages (or cap at a reasonable number)
    set maxMsgs to msgCount
    if maxMsgs > 50 then set maxMsgs to 50
    set msgs to messages 1 thru maxMsgs of inbox

    set output to ""
    repeat with m in msgs
        set output to output & "===" & linefeed
        set output to output & "FROM: " & sender of m & linefeed
        set output to output & "SUBJECT: " & subject of m & linefeed
        set output to output & "DATE: " & (date received of m as string) & linefeed
        set output to output & "READ: " & read status of m & linefeed
        set output to output & "TO: " & (address of every to recipient of m) & linefeed
        set output to output & "CC: " & (address of every cc recipient of m) & linefeed
        -- Read first 500 chars of body
        set bodyText to content of m
        if length of bodyText > 500 then
            set bodyText to text 1 thru 500 of bodyText
        end if
        set output to output & "BODY: " & bodyText & linefeed
    end repeat
    return output
end tell
```

**Reading archive:**
```applescript
tell application "Mail"
    set archiveBox to mailbox "Archive" of account "Exchange"
    set msgs to messages 1 thru N of archiveBox
    -- same extraction loop
end tell
```

**Reading full message body** (for important/complex emails that need deeper analysis):
```applescript
tell application "Mail"
    set msg to message N of inbox
    return content of msg
end tell
```

**Key points:**
- Process messages in batches (5-10 at a time) to avoid AppleScript timeouts
- Use `content of m` for plain text body (reliable, fast)
- For `--unread` flag: filter with `whose read status is false`
- `message id of m` provides a unique identifier for each message

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

### 10. Create Reply Drafts via Outlook UI Scripting

For each approved draft, create a Reply All draft using the Mac Outlook client. This produces proper formatting: reply text, signature, HR separator, and full quoted thread — all natively handled by Outlook.

**Method**: Use AppleScript UI scripting with clipboard paste (NOT keystroke typing, which loses focus).

**Step 1: Find the target email row in Outlook's message list.**

Before creating drafts, scan the message list to find each email's row number by matching sender/subject in `description of UI element 1 of row N of tbl`. The row numbers in Outlook match the order seen during the Apple Mail reading phase, but offset by +1 because row 1 is a date header (e.g., "Today, Expanded").

```bash
# Read Outlook message list to find target row
osascript <<'SCRIPT'
tell application "Microsoft Outlook" to activate
delay 0.5
tell application "System Events"
  tell process "Microsoft Outlook"
    set w to window "Inbox • All Accounts"
    set sg to UI element 2 of w
    set spg to splitter group 1 of sg
    set spg2 to splitter group 1 of spg
    set msgList to group 1 of spg2
    set sa to scroll area 1 of msgList
    set tbl to table 1 of sa

    set output to ""
    repeat with i from 1 to 10
      try
        set desc to description of UI element 1 of row i of tbl
        set output to output & "ROW " & i & ": " & desc & linefeed
      end try
    end repeat
    return output
  end tell
end tell
SCRIPT
```

**Step 2: For each approved draft, set clipboard and create the reply.**

```bash
# Set clipboard with reply text
printf '%s' "reply text here" | pbcopy

# AppleScript to select email, Reply All, paste, save
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

**For forwarding**: Use `click menu item "Forward" of menu "Message" of menu bar 1` instead of Reply All, then add the recipient in the To field before pasting.

**For multi-line reply text**: Use `printf '%s' "line1\n\nline2" | pbcopy` to preserve newlines.

**Key points:**
- Outlook UI scripting produces proper: signature, HR separator, quoted thread, conversation threading
- `keystroke` for typing text does NOT work (focus escapes to other apps) — always use clipboard + paste
- Date header rows (e.g., "Today, Expanded") occupy row positions — account for them when targeting
- Always return to the Inbox folder after all drafts are created

**Fallback**: If Mac Outlook client is unavailable, use `/send-mail` to create new emails via AppleScript (does not include original thread).
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
- Option to create reply drafts via Apple Mail
</specifications>

<examples>
## Usage Examples

### Full workflow — briefing + drafts (auto-learns first)
```
/mail-review
```

### Just the briefing, no drafts
```
/mail-review --briefing-only
```

### Read last 50 from archive
```
/mail-review archive --count 50
```

### Only unread emails
```
/mail-review --unread
```

### Learning mode only — process pending drafts
```
/mail-review --learn
```
</examples>
