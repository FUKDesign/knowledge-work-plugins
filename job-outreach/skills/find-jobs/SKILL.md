---
name: find-jobs
description: Find and score remote design job leads for Aidan McFarlane from Upwork, remote and Japan-focused job boards, agency careers pages and Gmail job alerts, de-duplicated against past outreach in Gmail. Trigger with "find jobs", "find me design jobs", "search for leads", "what's new on Upwork", "build this week's shortlist", "any new remote design roles".
---

# Find Jobs

Search every connected source for design leads, score each one against the candidate profile, remove anything already contacted or declined, and present a ranked shortlist for the user to approve. This skill only reads and saves; it never contacts anyone.

Read first:
- `../../references/candidate-profile.md` (target roles, sectors, proof points, TODOs)

## Connectors

| Connector | Used for | Required |
|-----------|----------|----------|
| **Upwork** | `find_jobs` to search, `save_job` to bookmark approved leads | Recommended |
| **Web search** | Job boards, careers pages, LinkedIn via search | Yes |
| **Gmail** | Job-alert emails; history check so nothing is re-pitched | Yes |

> **No Upwork?** Skip that source and say so in the summary. **No Gmail?** Stop and ask the user to connect it: the history check is mandatory.

---

## Workflow

```
1. LOAD     profile + any criteria the user adds this run
2. SEARCH   Upwork → web/job boards → Gmail job alerts
3. NORMALISE one row per lead: org, role, type, location/remote, link, source, date
4. DEDUPE   merge duplicates across sources
5. HISTORY  check Gmail; drop anything already contacted or declined
6. SCORE    0–100 with the rubric below
7. PRESENT  ranked shortlist table; wait for approval
8. SAVE     on approval, save Upwork jobs with save_job
```

### Step 1: Load criteria

Use the target roles in `candidate-profile.md`. Ask once, briefly, only if the user wants to narrow this run (e.g. "freelance only this week", "Japan-market only"). Default lookback: 7 days.

### Step 2: Search sources

**Upwork (`find_jobs`):** run several queries, e.g. "brand designer", "graphic designer", "campaign design", "social media designer", "Japanese localization design", "Japanese English bilingual designer", "AI ad creative", "Figma UX audit", "Rakuten banner". Prefer jobs posted in the last 7 days, verified payment and a clear brief.

**Web search:** use `site:` queries and careers pages. Sources to cover:

| Source | Focus |
|--------|-------|
| Japan Dev (japan-dev.com) | Japan-based, English-friendly roles |
| TokyoDev (tokyodev.com) | Japan-based and remote roles |
| Wantedly (wantedly.com) | Japanese startups, design roles (search in Japanese too: デザイナー, ブランドデザイナー, リモート) |
| Daijob (daijob.com) | Bilingual roles in Japan |
| CareerCross (careercross.com) | Bilingual JP/EN roles |
| Working Nomads | Remote design |
| Dribbble Jobs | Design-specific, freelance and full-time |
| We Work Remotely | Remote design |
| Remotive | Remote design |
| LinkedIn (via search only: `site:linkedin.com/jobs`) | Remote brand/graphic/UX roles |
| Agency and studio careers pages | Creative agencies, studios and brands in his sectors, especially those with Japan or APAC work |

Read each posting before scoring. Capture: organisation, role title, contract type (freelance / contract / fractional / full-time), location and remote policy (and whether time zones or Japan are allowed), seniority, languages, posting date, link, and any application route or contact named.

**Gmail job alerts:** search recent alert emails, e.g.
`newer_than:7d (from:linkedin.com OR from:indeed.com OR from:glassdoor.com OR from:wantedly.com OR from:dribbble.com OR subject:"job alert")`.
Extract the individual roles and open the linked posting where possible.

### Step 3–4: Normalise and de-duplicate

One row per (organisation, role). Keep the best source link and note other sources.

### Step 5: Gmail history check (mandatory before shortlisting)

For every organisation on the list, search Gmail for any past contact:

- Labels: `label:"Job Outreach/Sent" OR label:"Job Outreach/Replied" OR label:"Job Outreach/Interview" OR label:"Job Outreach/Declined" OR label:"Job Outreach/Won" OR label:"Job Outreach/Drafted"`, combined with the organisation name or domain
- Sent mail: `in:sent ("[Org name]" OR [domain])`, no date limit
- Replies: `from:[domain]` and `"[Org name]" (unfortunately OR "not hiring" OR "position has been filled" OR "not moving forward" OR "keep your details on file")`

Rules:
- **Declined or "not hiring" at any time:** drop. Do not re-pitch.
- **Contacted in the last 6 months with no reply:** drop (follow-ups are handled by `track-pipeline`).
- **Active conversation or work in progress:** drop from the shortlist and note "already in pipeline".
- **Contacted more than 6 months ago, no decline, and a genuinely new role:** keep, but mark `Previously contacted (date)` so the user decides.
- **Already drafted:** drop and note "draft exists".

Report how many leads were removed by the history check, but do not print the details of past correspondence beyond the organisation name and status.

### Step 6: Score (0–100)

| Criterion | Points | What earns full marks |
|-----------|--------|-----------------------|
| Role fit | 0–30 | Brand, graphic, campaign, social, content or UX design that matches his disciplines and portfolio |
| Remote / Japan compatibility | 0–25 | Fully remote with no country restriction, or Japan-based remote, or explicitly async; Fukuoka on-site also counts. Zero if restricted to a region that excludes Japan |
| Seniority match | 0–15 | Mid-weight to senior, or lead on a small team. Junior or head-of roles score low |
| Language advantage | 0–15 | Japanese or Korean required or a bonus; Japan/APAC market focus; localisation |
| Client/industry overlap | 0–15 | Sector or client type he already has named proof for (agency, consumer health, e-commerce, NGO, hospitality, camera/photo, travel, education, AI ad production) |

Adjustments:
- −10 if the posting is older than 21 days or the brief is vague
- −15 if the role requires on-site work outside Fukuoka (until the relocation TODO in the profile is resolved)
- −20 and flag for Upwork jobs with unverified payment or obvious spec-work requests

Bands: **80+** strong, pitch this week · **60–79** good · **40–59** maybe, only if the week is thin · **<40** drop.

### Step 7: Present the shortlist

```markdown
# Job Shortlist: [date range]

**Sources searched:** Upwork ([n]), web/job boards ([n]), Gmail alerts ([n])
**Removed by history check:** [n] (declined [n], recently contacted [n], in pipeline [n], draft exists [n])

| # | Score | Organisation | Role | Type | Remote / location | Why it fits | Source |
|---|-------|--------------|------|------|-------------------|-------------|--------|
| 1 | 88 | [Org] | [Role] | Freelance | Remote, any TZ | [1-line reason + best proof point] | [link] |

**Maybe (40–59):** [short list with links]
**Flags:** [unverified payment, on-site, previously contacted, etc.]

Reply with the numbers to approve (e.g. "1, 2, 5"), and I'll draft outreach for them.
```

Every row must include a working source link.

### Step 8: On approval

- For approved Upwork jobs, call `save_job` so they are bookmarked.
- Hand the approved rows (with links, application route and any contact found) to `draft-outreach`.

## Rules

- Never contact anyone from this skill. No emails, no Upwork proposals, no drafts.
- Never write lead or pipeline details into the repo or plugin files. Results live in the conversation and, once drafted, in Gmail labels.
- Never invent postings. If a link cannot be opened, mark the row "unverified".
