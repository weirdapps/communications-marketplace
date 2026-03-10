# Email Drafter

AI-powered email reply drafting that mimics your exact communication style.

## What It Does

1. **Reads** your Outlook 365 inbox/archive via browser automation
2. **Triages** emails — identifies which ones need a reply
3. **Drafts** replies matching your communication style per recipient
4. **Learns** by comparing drafts to your actual responses

## Commands

| Command | Description |
|---------|-------------|
| `/draft` | Read emails and draft replies |
| `/draft-review` | Compare drafts to actual responses and improve |

## How It Works

The plugin maintains a **style guide** (`shared/style-guide.md`) that captures:
- Your reply patterns (brevity, tone, language)
- Per-recipient tone profiles
- Anti-patterns (things you never do)
- Decision flow for triaging emails

The `/draft-review` command creates a feedback loop:
1. You run `/draft` → agent creates draft replies
2. You send your actual replies (modified or original)
3. You run `/draft-review` → agent compares drafts to actual responses
4. Agent updates the style guide with learned patterns
5. Next `/draft` run is more accurate

## Setup

Requires:
- Outlook Web access (logged into https://outlook.office.com)
- Playwright MCP server (for browser automation)
- `outlook-mailer` plugin (for sending drafts to Outlook)

## Style Guide

The style guide was built by analyzing 150+ emails (sent items, inbox CC'd copies, and archived emails). Key characteristics:

- **Ultra-brief**: 60%+ of replies are 1-10 words
- **No greetings/closings**: Straight to the point
- **Lowercase**: Almost always starts lowercase in Greek
- **Recipient-aware**: Different tone for boss vs. direct reports vs. PA
- **Greek internal**: Always Greek for NBG, English only for internationals
