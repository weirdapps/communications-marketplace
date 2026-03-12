---
description: "Send an email via Microsoft Outlook on macOS"
argument-hint: "[describe what to send, to whom, subject, and optionally attach files]"
allowed-tools: Bash, Read, Glob
---

<objective>
Send an email using Microsoft Outlook via AppleScript on macOS.
The sender account is configured in `shared/style-guide.md` (see Identity section).

User request: $ARGUMENTS
</objective>

<instructions>

## 1. Parse the user's request

Extract the following from the user's request:
- **To**: One or more recipient email addresses (REQUIRED)
- **CC**: Optional CC recipients (the user's own email from `shared/style-guide.md` is ALWAYS added as CC automatically)
- **BCC**: Optional BCC recipients
- **Subject**: Email subject line (REQUIRED)
- **Body**: Email body content - convert to HTML for proper formatting
- **Attachments**: File paths to attach (optional). Use Glob to find files if paths are approximate.
- **Draft mode**: ALWAYS open as draft (`open newMsg`). Direct send via AppleScript skips the Outlook signature. Opening as draft lets Outlook insert the signature, and the user sends manually.

If the user hasn't provided required fields (To, Subject), ask before proceeding.

## 2. Prepare the body

- Always send emails in **HTML format** for Outlook compatibility
- Convert any markdown content to proper HTML with inline CSS
- Font: **Aptos**, size **12pt**, color **#404040** (Black Text 1 Lighter 25%)
- Do NOT manually append a signature - Outlook adds it automatically
- Wrap content in a basic HTML structure:

```html
<html><body style="font-family: Aptos, sans-serif; font-size: 12pt; color: #404040;">
[content here]
</body></html>
```

## 3. Prepare attachments

If attachments are specified:
- Verify each file exists using Glob or Read
- Collect absolute POSIX paths
- If a file doesn't exist, warn the user and ask whether to proceed without it

## 4. Send via AppleScript

Use the Bash tool to run an AppleScript that:
1. Creates an outgoing message with subject and HTML content
2. Adds To, CC, BCC recipients
3. Adds file attachments
4. Opens the message as draft (so Outlook adds the signature)

### AppleScript template

```applescript
tell application "Microsoft Outlook"
    set newMsg to make new outgoing message with properties {subject:"SUBJECT", content:"HTML_BODY"}

    -- Add recipients (repeat for each)
    make new to recipient at newMsg with properties {email address:{address:"recipient@email.com"}}

    -- ALWAYS add self as CC (use email from shared/style-guide.md)
    make new cc recipient at newMsg with properties {email address:{address:"USER_EMAIL"}}

    -- Add additional CC (if any)
    make new cc recipient at newMsg with properties {email address:{address:"cc@email.com"}}

    -- Add BCC (if any)
    make new bcc recipient at newMsg with properties {email address:{address:"bcc@email.com"}}

    -- Add attachments (if any)
    set posixFile to POSIX file "/absolute/path/to/file.xlsx"
    make new attachment at newMsg with properties {file:posixFile}

    -- Always open as draft to preserve Outlook signature
    open newMsg
end tell
```

### Important AppleScript notes
- Escape double quotes in the HTML body with `\"` or use single quotes in HTML attributes
- Use `&` for `&` in HTML within AppleScript strings
- For multi-line content, concatenate with `& return &`
- Use inline CSS (style attributes) rather than `<style>` blocks

### Outlook AppleScript capabilities and limitations
- `make new outgoing message` works for **new emails only**
- Exchange/O365 mailbox messages are NOT accessible via Outlook AppleScript — `messages of inbox` returns 0
- For **reading emails**: use Apple Mail AppleScript instead (see `inbox-briefing.md`)
- For **reply/reply-all drafts**: use Outlook UI scripting (see `mail-review.md` Step 10)
- This command (`/send-mail`) is for **new emails only**, not replies

## 5. Confirm result

After execution:
- Confirm "Draft created and opened in Outlook for [recipients] with subject [subject] — please review and send"
- If error: report the error and suggest fixes

</instructions>
