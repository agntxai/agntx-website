---
title: "WMSone: When a Great AI Practice Hits Its Ceiling"
type: Case Study
date: 2026-09-29
author: Lapis Research
read: 9 min
image: wmsone_case_study.jpg
summary: A top-tier engineering team had already invested heavily in AI coding tools, and still wasn't moving the needle. What we found in three days, and what we shipped in nine.
---
*WMSone is a pseudonym for a real warehouse-management software company we worked with in mid-2026. Names and identifying details have been changed; the numbers have not.*

## The company

WMSone builds warehouse-management software for third-party logistics providers (3PLs) and the brands they serve: a mature web platform, a newer front end in the middle of a migration, a separate integration engine, and a roadmap full of new builds. It was backed by a private-equity sponsor, and its own roadmap named "internal AI capacity" as a primary lever for delivering more with a lean team.

This wasn't a team that needed convincing about AI.

## The practice: genuinely excellent

Before we wrote a word of recommendation, we read what the team had built. It was one of the most sophisticated AI-assisted engineering practices we'd seen at a company of any size:

- **19 custom AI skills**, including a 13-step merge-request review that establishes intent from the ticket before reading the code, and fails any bug fix that doesn't come with a failing test first
- **4 isolated "publisher" agents**, the only components allowed to write to their systems; everything else is read-only
- A written doctrine: no production changes without human confirmation, design proposals scored before approval, one hypothesis at a time when debugging
- Rules earned the hard way, each tied to a dated incident that had cost them real time

We said so, plainly. Calling any of this "brittle" would have been wrong, and it would have cost us credibility with people who had built sound rails.

## The ceiling

And yet the CTO's own verdict, unprompted, was: **"It's just not moving the needle enough."** Releases were still hard. Things were still breaking. Only two people could really see what the tooling was doing.

He was right, and the reason wasn't a lack of discipline. It was the lack of anywhere for that discipline to *live*.

1. **A knowledge graph written by hand, with nothing behind it.** Their doctrine file was the hub, the skills were spokes, and cross-references pointed to documents that didn't exist anywhere a machine could follow.
2. **Outputs evaporated.** Review findings and debugging notes landed as loose files and were never seen again. Nothing accumulated.
3. **Learning depended on heroics.** A lesson became a rule only when someone noticed a costly failure and wrote it down.
4. **The tooling concentrated risk instead of spreading it.** The engineer who authored the AI practice personally triggered **about 93% of all release pipelines.**
5. **Copies drifted.** When they tried to share their skills with a second AI assistant, the copy had silently lost two skills and several safety checks before anyone noticed.
6. **The documentation disagreed with reality.** The main branch had failed **67 of 67** deployment runs over 90 days on the same error. An entire unit-test suite existed but was never run. A pipeline file described itself as "experimental, never blocks" while it was in fact the only thing blocking merges.

On the operations side, a production outage had lasted roughly three and a half hours. The cause: the live infrastructure had drifted from its own configuration (scaling capped at 2 servers where the specification allowed 5). Monitoring had fired alerts for about three hours before anyone was paged.

## What we did in three working days

With read-only access and no changes to how their team worked, we built a connected knowledge base of their engineering estate:

| What we connected | Scale |
|---|---|
| Work items, full history across both main codebases | **6,866** tickets, searchable |
| Build and deployment history (90 days, refreshed every 6 hours) | **3,560** pipeline runs, **5,915** jobs |
| Release history | rebuilt from their *own* AI-generated release notes |
| People, capabilities, infrastructure configuration | linked to the work they touch |

Three working days from access to a leadership demo. In that demo we traced a single change end to end, from ticket to failed build to fix to green to released, as a single query. We surfaced the outage's root cause as a live mismatch between configuration and reality. And we showed the review step their team did from memory on every merge ("what does this change touch?") answered by the system in seconds.

We were also able to give credit where due. Their test gate had caught a problem in **39%** of merge-request pipelines, roughly twelve times a day. It was doing its job; nobody could see that it was.

## Then we built something

Their roadmap's first major build was a QuickBooks Online accounting integration. **Their own estimate was 8–10 weeks.**

| Phase | What happened |
|---|---|
| **Discover** | The knowledge base above, plus a business-capability map validated with their technical leadership and the QuickBooks API's constraints researched before any design |
| **Discuss** | Four short "thin-slice" walkthroughs that settled what the integration owns: eligibility, the sync ledger, duplicate protection, failure handling |
| **Define** | **31 acceptance scenarios** written first and approved by the client, and **6 architecture decision records**, each stating what it would cost to change the decision later |
| **Deploy** | Built in one working day: **40 automated tests green**, plus **3 live tests against a real QuickBooks sandbox** (the same invoice synced twice produces exactly one document), CI pipeline, and documentation for three audiences |

**Delivered and shared nine working days after access was granted.**

The one-day build wasn't a stunt. It was possible *because* the earlier phases lived in the knowledge base: the specification made the work unambiguous, the constraints research meant no mid-build surprises, and every "what should happen when…" question had already been answered. People made every decision that was a choice; the AI executed everything that was a consequence.

## What this means for you

If you're a private-equity sponsor or an operating leader, three lessons carry over:

- **Sophistication isn't the same as leverage.** A team can be doing everything right with AI and still be bottlenecked, because its knowledge lives in files and in two people's heads.
- **The risk is usually invisible from the outside.** A 93% dependency on one engineer, a main branch that hasn't deployed cleanly in a quarter, monitoring nobody is paged by: none of these show up in a board deck.
- **You don't have to replace what works.** We didn't ask WMSone's team to change a single workflow. Their practice kept running; it just stopped forgetting.

> Their AI investment wasn't wasted. It was stranded.
