---
name: track-pipeline
description: Track Aidan McFarlane's job-outreach pipeline using Gmail labels (Job Outreach/Drafted, Sent, Replied, Interview, Declined, Won). Reclassifies threads from sent mail and replies, drafts one follow-up for emails with no reply after 7 days, and produces a weekly pipeline summary. Trigger with "track my pipeline", "update the job pipeline", "who hasn't replied", "pipeline summary", "any follow-ups due", "weekly job report".
---

# Track Pipeline

Gmail labels are the pipeline. This skill reads sent mail and replies, moves each thread to the right label, drafts follow-ups where they are due, and reports the week. It never sends anything, and it never stores pipeline data anywhere except Gmail.

## Labels

| Label | Meaning |
|-------|---------|
| `Job Outreach/Drafted` | Draft created by `draft-outreach`, not yet sent |
| `Job Outreach/Sent` | Sent by the user; waiting for a reply |
| `Job Outreach/Replied` | A human replied (not an auto-reply) and the next step is open |
| `Job Outreach/Interview` | A call, interview, test task or meeting is proposed or booked |
| `Job Outreach/Declined` | Rejected, not hiring, role filled, or out of scope |
| `Job Outreach/Won` | Offer, contract or paid project agreed |

Each thread carries exactly one of these labels. When moving a thread, add the new label and remove the old one. Create any missing labels with `create_label` (parent `Job Outreach` first).

## Connectors

| Connector | Used for |
|-----------|----------|
| **Gmail** (required) | `search_threads`, `get_thread`, `label_thread` / `unlabel_thread`, `create_label`, `list_drafts`, `create_draft` |
| **Google Calendar** (optional) | Spot interview events and confirm the Interview stage; never create or accept events without asking |

---

## Workflow

### 1. Drafted → Sent

- Find threads labelled `Job Outreach/Drafted`.
- If the thread now has a message in `in:sent` from aidanrmcfarlane@gmail.com, move it to `Job Outreach/Sent`.
- Also catch outreach the user sent by hand: `in:sent newer_than:14d subject:"| Aidan McFarlane"` without any `Job Outreach/*` label → label `Job Outreach/Sent`.
- Drafts older than 14 days and still unsent: list them as "stale drafts" for the user to send or delete. Do not delete them.

### 2. Sent → Replied / Interview / Declined / Won

For each `Job Outreach/Sent` and `Job Outreach/Replied` thread, read new messages from anyone other than Aidan:

| Signal in the reply | New label |
|---------------------|-----------|
| Auto-reply, "out of office", "we've received your application", no-reply sender | Stay in `Sent` (note "auto-ack") |
| "Unfortunately", "not hiring", "role has been filled", "not moving forward", "only considering candidates in…", "not commissioning" | `Declined` |
| Proposes a call, interview, portfolio review, test task, video interview or calendar invite | `Interview` |
| Offer, contract, SOW, PO, "we'd like to go ahead", agreed fee or start date | `Won` |
| Any other human response (questions, "keep you on file", request for rates or more samples) | `Replied` |

"Kept on file" with no open role counts as `Declined` for re-pitching purposes; mention it in the summary as "on file".

If Google Calendar is connected, a calendar event that names the organisation confirms `Interview`.

When a classification is uncertain, leave the label as is and list the thread under "Needs your review".

### 3. Follow-ups (one maximum)

A thread is due for a follow-up when **all** are true:
- Label is `Job Outreach/Sent`
- The last message is Aidan's and is **7+ days old**
- Aidan has sent only one message in the thread (no follow-up yet)
- There is no existing draft in the thread

For each one, create a **draft reply in the same thread** using the follow-up template in `../../references/writing-style.md`, with one new specific line (a recent piece of their work or one relevant project). Do not send it. Do not apply a new label; it stays in `Sent`.

If a follow-up has already been sent and 7+ more days have passed with no reply, do **not** draft another. Mark it "no response, closed" in the summary and leave it in `Sent`. Never send or draft a third message.

### 4. Weekly summary

```markdown
# Job Pipeline: week of [date]

| Stage | Count | Change this week |
|-------|-------|------------------|
| Drafted | n | +n |
| Sent | n | +n |
| Replied | n | +n |
| Interview | n | +n |
| Declined | n | +n |
| Won | n | +n |

**Response rate (last 30 days):** [replied + interview + declined + won] / [sent] = [x]%

## Action needed
| Organisation | Stage | What to do | Thread |
|--------------|-------|------------|--------|
| [Org] | Interview | Reply with times (state JST) | [Gmail link] |
| [Org] | Sent, day 8 | Follow-up draft ready: review and send | [Gmail link] |
| [Org] | Drafted, 15 days | Stale draft: send or delete | [Gmail link] |

## Moved this week
- [Org]: Sent → Declined ("role filled")
- [Org]: Sent → Interview (call proposed)

## Needs your review
- [Org]: ambiguous reply, left in [stage]

## Closed with no response
- [Org]: one follow-up sent [date], no reply
```

Show the summary in the conversation only. Do not write it to the repo or any file unless the user asks for a file.

## Rules

- Never send, reply-send or forward. Drafts only.
- Never delete threads, drafts or labels.
- When writing the response to a decline, keep it gracious and short ("I completely understand, and thanks for keeping me in mind"). Only draft one if the user asks.
- Organisation names and correspondence stay in Gmail and the conversation; never commit them to the plugin.
