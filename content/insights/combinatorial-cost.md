---
title: The Exponential Value, Combinatorial Cost Race
type: Essay
date: 2026-09-08
author: Shaun Anderson, Founder
read: 8 min
image: combinatorial_cost.jpg
summary: The AI industry sells exponential value. Nobody has shown that the cost of extracting it safely, at real organizational scale, is anything but combinatorial.
---
*This piece is a diagnosis, not a pitch. It deliberately doesn't mention a product. I'd genuinely like to be told I'm wrong.*

## The claim, in one sentence

**The AI coding industry sells exponential value. Nobody has shown that the cost of extracting that value safely, at real organizational scale, is anything other than combinatorial. If that's true, there's a scale at which the promise inverts.**

## The promise, stated fairly

This isn't a straw man. I have my own receipts: one engineer producing the output of a six-to-eight-person team in a month, and a six-week integration project compressed to six hours. Those numbers are real, and I'm not walking them back. The promise holds *at the scale it was demonstrated at*.

The open question is whether that curve holds as you add the three things every real business eventually adds: more people, more tools, more customers.

## Three axes that compound

Every serious AI-assisted engineering practice I've seen up close eventually layers a governing discipline on top of the raw tool: a way of instructing the model, a set of dos and don'ts, and rules for what the AI shouldn't decide alone.

In almost every implementation, **that discipline lives in prose**: a markdown file, a set of team habits, things a person has to read, remember, and correctly re-apply every time, forever.

- **Add an engineer**, and they must absorb all of it before they're safe to operate unsupervised. The more discipline there is, the more expensive that absorption gets.
- **Add a tool or assistant**, and the discipline is either duplicated (and starts drifting the moment one copy changes) or kept in sync by hand.
- **Add a customer or a new edge case**, and it either becomes a new hand-written rule that everyone must now know, or it's quietly lost.

These don't add. **They compound**, because every person has to stay consistent with every tool, every tool with every person's habits, and every new edge case can touch all of it. What actually grows is the number of relationships that must stay consistent, and they're enforced by nothing but memory.

## The "second expert" problem

A small, disciplined team can absorb this cost because one person can hold the whole system in their head.

The failure isn't when that person leaves. It comes earlier: **the moment the organization needs a second person with equal authority over the same system.** That doesn't double the cost. It adds a cost that didn't exist before, which is keeping two people's judgment consistent with each other.

The cost of this model was never the first expert it required. It's the coordination tax on the second one. Every successful business eventually needs a second one, and a third.

## The data is already showing it

- Experienced developers measured **19% slower** with AI tools while believing they were 20% faster (METR, 2025).
- **91% of organizations** use AI coding tools; only **5% of repositories** have any structured governance (arXiv, 2025).
- A **4× increase in code duplication** in AI-heavy codebases (GitClear, 2026).
- **+91% code review time and +154% pull-request size** under unmanaged adoption (Faros AI / DORA, 2025).
- Developer trust in AI output fell for the first time on record, **from 70% to 60%** (Stack Overflow, 2025).

The standard reading is "the tools have rough edges; prompt better." I think that's the wrong reading. **This is what a coordination cost catching up with a value curve looks like from the inside.**

## The uncomfortable part

If the diagnosis is right, "buy a governance platform" isn't automatically the answer. A badly designed governance layer is just one more tool with its own prose to absorb, and it relocates the cost instead of collapsing it.

The only version that holds is one where the discipline **stops living in prose**: where it's structural, enforced by the system and correct no matter who's operating it. That's a falsifiable claim, and it deserves testing rather than assuming.

## The question I'd like answered

Does the value curve of AI-assisted work stay ahead of the coordination cost of running it safely as an organization scales its people, tools, and customers? Or does the cost curve eventually overtake it, and if so, at what scale?

I don't think anyone has measured that rigorously yet. It may be the most important open question in the industry.
