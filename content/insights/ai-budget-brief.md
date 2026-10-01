---
title: Your AI Bill Should Scale With Output, Not Conversation
type: Brief
date: 2026-07-28
author: Lapis Research
read: 4 min
image: ai_budget.jpg
summary: A one-page brief for CFOs and operating partners on why AI costs balloon, and the architectural choice that keeps them in line.
---
## The problem in one line

Most AI tools bill for every step of their thinking: every re-read file, every retry, every "let me reconsider." **Cost scales with how long the AI talks, not with what it produces.**

## Why costs balloon

In a typical unmanaged AI workflow, the premium model is used for *everything*:

- routine lookups a database could answer instantly
- status checks and file reads
- re-reading the same context over and over
- long loops of trial and error

All of it is billed at full rate.

## The two-zone model

A well-architected AI system splits work into two zones:

| | Zone 1: Thinking & orchestration | Zone 2: Producing the work |
|---|---|---|
| **What happens** | Planning, reasoning with company knowledge, routing routine steps to ordinary software | The model writes the actual code, document, or analysis |
| **How it's billed** | Mostly cached or deterministic, often around a tenth of list price, and **zero** for steps that don't need AI at all | Full rate, but only for bounded, clearly specified work |

The result: **cost tracks output, not session length.** A session that looks like 100,000 tokens of activity can bill like a fraction of that.

## Receipts from practice

- Long working sessions compressed by about **74%** without losing what matters
- Around **90%** of follow-on context served from cache
- Routine workflow steps run on ordinary software, with **no AI cost at all**

## Questions for your team or your portfolio companies

1. What share of our AI spend goes to producing output, versus the AI re-reading and retrying?
2. Are routine, mechanical steps being sent to expensive models?
3. Does our AI remember what it learned last week, or do we pay to re-teach it?
4. If usage doubled, would cost double, or more than double?

## The takeaway

The cheapest AI token is the one you never needed to spend. Governance isn't just a risk control. **It's a cost control.**
