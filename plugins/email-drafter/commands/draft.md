---
description: "Read Outlook emails and draft replies in your communication style"
argument-hint: "[inbox|archive|both] [--count N]"
allowed-tools: Agent, Read, Bash, mcp__plugin_playwright_playwright__browser_navigate, mcp__plugin_playwright_playwright__browser_snapshot, mcp__plugin_playwright_playwright__browser_click, mcp__plugin_playwright_playwright__browser_press_key, mcp__plugin_playwright_playwright__browser_run_code, mcp__plugin_playwright_playwright__browser_take_screenshot, mcp__plugin_playwright_playwright__browser_evaluate
---

<objective>
Read recent Outlook emails and draft replies matching Dimitris Plessas's communication style.

User request: $ARGUMENTS
</objective>

<process>
## Workflow

### 1. Load Style Guide
Read the communication style guide from `shared/style-guide.md` in the email-drafter plugin directory.

### 2. Read Emails
Use the email-drafter agent to:
- Navigate to Outlook Web (https://outlook.office.com/mail/inbox or /mail/archive)
- Read recent unread/unanswered emails
- **Inbox**: Read ALL emails — the inbox is a to-do list of unprocessed items
- **Archive**: Read last N emails (default 20) — for reference only

### 3. Triage
Classify each email as SKIP (no reply needed) or DRAFT (needs reply).
Present the triage summary first.

### 4. Draft Replies
For each DRAFT email, generate a reply following the style guide exactly.
Adapt tone per recipient using the per-recipient profiles.

### 5. Present & Confirm
Show all drafts for user review.
Ask which to send, modify, or discard.

### 6. Send Approved Drafts
Use the outlook-mailer plugin (send-mail command) to create drafts in Outlook.
Always open as draft (`open newMsg`) — never send directly.
Always CC dimitrios.plessas@nbg.gr.
</process>

<specifications>
## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `folder` | No | `both` | Which folder to read: `inbox`, `archive`, or `both` |
| `--count` | No | `20` | Number of recent emails to process |
| `--unread` | No | `false` | Only process unread emails |
| `--learn` | No | `false` | Run in learning mode: compare past drafts to actual replies |

## Output
- Triage summary table
- Draft replies for each email needing response
- Option to send via Outlook
</specifications>

<examples>
## Usage Examples

### Read inbox and draft replies
```
/draft
```

### Read last 50 from archive
```
/draft archive --count 50
```

### Only unread emails
```
/draft --unread
```

### Learning mode — compare drafts to actual responses
```
/draft --learn
```
</examples>
