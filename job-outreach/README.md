# Job Outreach Plugin

A personal job-search plugin for **Aidan McFarlane**, a British brand, digital and UX designer based in Fukuoka, Japan (EN/JP/KR). Each week it finds remote design leads, scores them against his profile, drafts personalised outreach as Gmail drafts, and keeps the pipeline up to date with Gmail labels.

Works in [Cowork](https://claude.com/product/cowork) and Claude Code.

## Installation

```bash
claude plugins add knowledge-work-plugins/job-outreach
```

## Safety rule: drafts only, a human sends

This plugin **never sends an email and never submits an Upwork proposal.** Every email is created as a Gmail draft labelled `Job Outreach/Drafted`, and every Upwork proposal is output as text to paste. You review, attach your CV and press send yourself. Follow-ups are drafts too, with a maximum of one per thread.

## What it does

| Component | Type | What it does |
|-----------|------|--------------|
| `find-jobs` | Skill | Searches Upwork, remote and Japan-focused job boards (Japan Dev, TokyoDev, Wantedly, Daijob, CareerCross, Working Nomads, Dribbble, We Work Remotely, Remotive, LinkedIn via search), agency careers pages and Gmail job alerts. Checks Gmail so it never re-pitches a company already contacted or declined. Scores each lead 0–100 and returns a ranked shortlist with links. |
| `draft-outreach` | Skill | For each approved lead: researches the company's recent work, finds a published contact or application route, writes a personalised email in Aidan's style, saves it as a Gmail draft and labels it. Upwork proposals are output as text. |
| `track-pipeline` | Skill | Moves threads between `Job Outreach/Drafted`, `/Sent`, `/Replied`, `/Interview`, `/Declined` and `/Won` by reading sent mail and replies. Drafts one follow-up for emails with no reply after 7 days, then stops. Produces a weekly summary table. |
| `job-scout` | Agent | Runs the weekly cycle: track-pipeline → find-jobs → **you approve the shortlist** → draft-outreach → summary. |

Reference files:
- [`references/candidate-profile.md`](references/candidate-profile.md): public profile, target roles, projects, proof points, links
- [`references/writing-style.md`](references/writing-style.md): tone, subject format, template variants, follow-up template, banned phrases

## Connectors

| Connector | Needed for | Required |
|-----------|-----------|----------|
| **Gmail** | Job alerts, history check, drafts, pipeline labels | Yes |
| **Web search** | Job boards, careers pages, company research | Yes |
| **Upwork** | Job search and saving jobs | Recommended |
| **Google Calendar** | Confirming interviews (read-only) | Optional |

See [CONNECTORS.md](CONNECTORS.md) for the exact tools used and the tools the plugin must never call.

## How to run it

Run the whole weekly cycle:

```
Run my weekly job search.
```

Or run one step at a time:

```
Find me design jobs from the last 7 days.
Draft outreach for 1, 3 and 4.
Update my job pipeline and show who needs a follow-up.
```

Typical flow:
1. The agent updates the pipeline and drafts any follow-ups that are due.
2. It shows a ranked shortlist. Reply with the numbers you want to pursue.
3. It drafts emails into Gmail and lists them in a summary table.
4. Open Gmail, attach `Aidan_McFarlane_CV_English.pdf`, check the first line, and send.
5. Next week's run moves sent emails to `Job Outreach/Sent` and tracks replies.

## Making it weekly

- **Claude Code (cloud or desktop):** ask Claude to "create a scheduled task every Monday at 8:47 JST that runs the job-scout weekly run". The run stops at the approval gate, so you approve the shortlist when you next open the session.
- **Cowork:** create a recurring task with the prompt `Weekly job-outreach run` and pick a weekly schedule.
- **Manual:** say "Run my weekly job search" each Monday.

Scheduled runs never send anything; at most they create follow-up drafts and a shortlist for you to approve.

## Privacy

This plugin is safe to keep in a public repo. It contains only public, portfolio-level information. The live pipeline (organisations contacted, replies, outcomes, contacts) exists only in Gmail labels and in the conversation, and the skills are instructed never to write it to files.

## TODO for Aidan

Open items are marked `TODO:` in `references/candidate-profile.md`:
- Preferred full-time salary and minimum day / project rate
- Openness to relocation or on-site / hybrid work
