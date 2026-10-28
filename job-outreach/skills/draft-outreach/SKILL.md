---
name: draft-outreach
description: Research each approved job lead, find a contact email or application route, and write a personalised outreach email for Aidan McFarlane as a Gmail draft (never sent), labelled "Job Outreach/Drafted". Upwork proposals are drafted as text to paste. Trigger with "draft outreach", "write the emails for these leads", "draft applications for 1, 3 and 4", "write a pitch to [company]", "draft an Upwork proposal".
---

# Draft Outreach (Job Search)

Research first, then draft. Every email is personalised to the company's own work and saved as a **Gmail draft only**. The user reviews, attaches the CV and sends it themselves.

Read first:
- `../../references/candidate-profile.md` (proof points, links, TODOs)
- `../../references/writing-style.md` (structure, templates, banned phrases)

## Safety rules (non-negotiable)

1. **Never send.** Use Gmail `create_draft` only. Never call `send_message`, `reply` or `forward`, even if asked to "just send it"; tell the user to send from Gmail.
2. **Never submit on Upwork.** Do not call `manage_proposals` or `send_message`. Output the proposal text for the user to paste.
3. **Never state a rate, salary or start date** unless the user gives it in this conversation.
4. **Re-check history before each draft:** search Gmail for the organisation's name and domain. If they have declined, or there is a draft or a sent email in the last 6 months, skip the lead and say why.
5. **Do not write lead details into the repo.** Drafts and labels in Gmail are the record.

## Connectors

| Connector | Used for |
|-----------|----------|
| **Gmail** | History check, `create_draft`, `create_label`, `list_labels`, labelling the draft |
| **Web search / fetch** | Company research, contact and application route |
| **Upwork** (optional) | Reading the full job post for proposal drafting |

> **No Gmail?** Output each email as text with its To and Subject lines, and say that no draft was created.

---

## Workflow (per approved lead)

### 1. Research the company (always first)

Look at, in this order:
- Their website: work / case studies / projects page, about page, news or blog
- Their most recent visible work: a campaign, launch, rebrand, report, product, social series (last 6–12 months)
- The job posting itself: responsibilities, tools, languages, time zones
- Japan or APAC activity, if any

Record **one specific hook**: the named piece of work and why it is relevant to Aidan. If you cannot find one, say so and ask the user whether to skip the lead; never fall back to a generic opener.

### 2. Find the contact route

Prefer, in order:
1. The application route named in the posting (email address, form, ATS link). If it's a form or ATS, **do not draft an email**; prepare the cover note text and the link instead.
2. A named hiring manager, creative director or studio lead with a published work email
3. A general studio or careers address on their site (e.g. hello@, careers@, jobs@, work@)

Only use addresses published by the company itself. Never guess an address pattern. If nothing is published, report "no email found" and give the application link or LinkedIn route.

### 3. Choose angle and proof points

Pick the template variant from `writing-style.md` (agency, in-house brand, NGO / mission-driven, Japan-market). Choose **2–3 named clients** from the proof-points table in `candidate-profile.md` that match this lead's sector and work type.

### 4. Write the email

Follow `writing-style.md` exactly:
- Subject: `[Offer] | Aidan McFarlane`
- Personalised first line about their work (mandatory)
- Short pitch with 2–3 named clients
- CV attached + portfolio (https://aidanmdesign.xyz/) + LinkedIn links
- Soft closing question
- British English, 90–150 words, no banned phrases, no leftover brackets

Self-check before saving: Is the first line specific to this company only? Would it make sense sent to anyone else? If yes, rewrite it.

### 5. Create the Gmail draft

1. Make sure the label exists: `list_labels`; if `Job Outreach/Drafted` is missing, `create_label` (create the parent `Job Outreach` first if needed).
2. `create_draft` with To, Subject and the plain-text body. Send from aidanrmcfarlane@gmail.com.
3. Apply the label `Job Outreach/Drafted` to the draft's message.
4. The CV cannot be attached automatically: remind the user to attach `Aidan_McFarlane_CV_English.pdf` before sending.

### 6. Upwork proposals

For Upwork leads, do not create a Gmail draft. Write the proposal per the "Upwork proposals" section of `writing-style.md` and output it in a code block with the job link, for the user to paste and submit.

---

## Output: summary for the user

```markdown
# Outreach Drafts: [date]

| # | Organisation | Role / offer | To / route | Subject | Hook used | Proof points | Status |
|---|--------------|--------------|------------|---------|-----------|--------------|--------|
| 1 | [Org] | [Role] | [email] | [subject] | [their work] | [Client A, Client B] | Gmail draft created, labelled |
| 2 | [Org] | [Role] | [ATS link] | n/a | [their work] | [..] | Cover note below (apply via form) |
| 3 | [Org] | [Upwork job] | Upwork | n/a | [their brief] | [..] | Proposal text below (paste into Upwork) |

**Skipped:** [Org]: [reason: declined before / no specific hook / no contact route]

**Before sending:** attach your CV to each draft, read the first line once more, and send from Gmail. Once sent, `track-pipeline` will move them to "Job Outreach/Sent".
```

Then list the full text of each email, cover note and proposal below the table.
