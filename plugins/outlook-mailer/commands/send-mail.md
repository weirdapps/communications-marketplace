---
description: "Send an email via Microsoft Outlook on macOS"
argument-hint: "[describe what to send, to whom, subject, and optionally attach files]"
allowed-tools: Bash, Read, Glob
---

<objective>
Send an email using Microsoft Outlook via AppleScript on macOS.
The default sender account is dimitrios.plessas@nbg.gr.

User request: $ARGUMENTS
</objective>

<instructions>

## 1. Parse the user's request

Extract the following from the user's request:
- **To**: One or more recipient email addresses (REQUIRED)
- **CC**: Optional CC recipients (dimitrios.plessas@nbg.gr is ALWAYS added as CC automatically)
- **BCC**: Optional BCC recipients
- **Subject**: Email subject line (REQUIRED)
- **Body**: Email body content - convert to HTML for proper formatting
- **Attachments**: File paths to attach (optional). Use Glob to find files if paths are approximate.
- **Draft mode**: If the user says "draft" or "save as draft", do NOT send - just create and open. Otherwise, send immediately.

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
4. Either opens (draft) or sends the message

### AppleScript template

```applescript
tell application "Microsoft Outlook"
    set newMsg to make new outgoing message with properties {subject:"SUBJECT", content:"HTML_BODY"}

    -- Add recipients (repeat for each)
    make new to recipient at newMsg with properties {email address:{address:"recipient@email.com"}}

    -- ALWAYS add self as CC
    make new cc recipient at newMsg with properties {email address:{address:"dimitrios.plessas@nbg.gr"}}

    -- Add additional CC (if any)
    make new cc recipient at newMsg with properties {email address:{address:"cc@email.com"}}

    -- Add BCC (if any)
    make new bcc recipient at newMsg with properties {email address:{address:"bcc@email.com"}}

    -- Add attachments (if any)
    set posixFile to POSIX file "/absolute/path/to/file.xlsx"
    make new attachment at newMsg with properties {file:posixFile}

    -- Either send or open as draft
    send newMsg
    -- OR for draft: open newMsg
end tell
```

### Important AppleScript notes
- Escape double quotes in the HTML body with `\"` or use single quotes in HTML attributes
- Use `&` for `&` in HTML within AppleScript strings
- For multi-line content, concatenate with `& return &`
- Use inline CSS (style attributes) rather than `<style>` blocks

## 5. Confirm result

After execution:
- If sent: confirm "Email sent to [recipients] with subject [subject]"
- If draft: confirm "Draft created and opened in Outlook"
- If error: report the error and suggest fixes

</instructions>
