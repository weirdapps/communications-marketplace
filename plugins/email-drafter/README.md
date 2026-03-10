# Email Drafter

Email command center — inbox briefings, action recommendations, style-matched draft replies, and self-learning.

## What It Does

1. **Learns** from previous drafts vs your actual responses (automatic, every run)
2. **Briefs** you on your inbox — gists, insights, new vs previously seen
3. **Recommends** actions — reply, delegate, forward, monitor, skip, urgent, follow-up
4. **Drafts** replies matching your communication style per recipient
5. **Tracks** inbox state across runs to highlight what's changed

## Commands

| Command | Description |
|---------|-------------|
| `/mail-review` | Full inbox briefing + action flags + draft replies |
| `/mail-review --briefing-only` | Quick scan — briefing and insights only, no drafting |
| `/draft-review` | Deep learning pass — compare drafts to actual responses |

## How It Works

### Inbox Briefing
Every run separates emails into **NEW** (since last run) and **PREVIOUSLY SEEN**, with:
- 1-2 sentence gist of each email
- Recommended action (reply, delegate, forward, monitor, skip, urgent, follow-up)
- Insights: who's waiting, cross-thread patterns, urgency flags, delegation opportunities

### Self-Learning Loop
```
/mail-review → drafts saved to ~/.claude/drafts/pending/
    ↓
You edit and send → CC'd copies land in your inbox
    ↓
Next /mail-review → auto-compares drafts vs actual responses
    ↓
Style guide updated → next drafts are more accurate
```

No manual `/draft-review` needed — learning runs automatically at the start of every `/mail-review`. Use `/draft-review` only for deep analysis or focused recipient review.

### Persistent State
| File | Purpose |
|------|---------|
| `~/.claude/drafts/pending/` | Saved drafts awaiting comparison |
| `~/.claude/drafts/reviewed/` | Processed drafts with actual vs draft diffs |
| `~/.claude/drafts/inbox-state.json` | Last-seen emails for new vs seen tracking |
| `~/.claude/drafts/learnings.md` | Historical log of accuracy improvements |
| `shared/style-guide.md` | Communication style guide (updated by learning) |

## Setup

Requires:
- Outlook Web access (logged into https://outlook.office.com)
- Playwright MCP server (for browser automation)
- `outlook-mailer` plugin (for sending drafts to Outlook)

## Style Guide

Built by analyzing 150+ actual emails. Key characteristics:

- **Ultra-brief**: 60%+ of replies are 1-10 words
- **No greetings/closings**: Straight to the point (BRIEF format)
- **Lowercase**: Almost always starts lowercase in Greek
- **Recipient-aware**: Different tone for boss vs direct reports vs PA
- **Greek internal**: Always Greek for NBG, English only for internationals
- **Self-improving**: Automatically updated based on draft-vs-actual comparisons
