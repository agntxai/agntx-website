# agntx.ai: Lapis by Agentic Technologies

The marketing site for **Lapis**, built as a plain static site and hosted on **Cloudflare Pages**.

| Branch | Publishes to | Who changes it |
|---|---|---|
| `preview` | **https://preview.lapiscloud.ai** (not indexed by search engines) | Lapis (`agntxai-lapis`) commits here |
| `main` | **https://agntx.ai** (production) | Only by merging an approved pull request `preview → main` |

## How to change the site (no code required)

1. In **Lapis** (lapiscloud.ai), ask for the change, e.g. *"Change the hero subheading to …"* or *"Turn nugget X into a blog post."*
2. Lapis commits to `preview`. About 30 seconds later the change is live at **preview.lapiscloud.ai**.
3. Look at it. Ask for tweaks as often as you like; each one updates the preview.
4. When you're happy, Lapis opens a pull request **preview → main**. **Approve and merge it on GitHub.** agntx.ai updates about 30 seconds later.
5. Something wrong? Cloudflare Pages → Deployments → *Rollback*, or revert the merge commit.

## Where things live

```
content/insights/*.md    Blog posts, essays, whitepapers, briefs, case studies (one file each)
src/index.html           Homepage text and structure
src/css/                 base.css → insights.css → refinements.css → theme.css  (edit these, never dist/)
src/assets/              Images; insights covers go in src/assets/insights/
_redirects               Old URL → new URL (Cloudflare Pages format)
scripts/build.py         Builds everything into dist/
qa/check.py              Release gate (header clearance, fonts, broken links/images, overflow, confidential names)
```

### Adding a post
Create `content/insights/<slug>.md`:
```markdown
---
title: My Post Title
type: Blog            # Blog | Essay | Whitepaper | Brief | Case Study
date: 2026-10-01
author: Shaun Anderson, Founder
read: 5 min
image: my_cover.jpg   # file in src/assets/insights/ (16:9, about 1600px wide)
summary: One or two sentences shown on cards and in link previews.
---
Markdown body. **Bold**, lists, > quotes and | tables | are supported.
```

### Confidentiality rules
Client engagements are published only under pseudonyms (e.g. **WMSone**). No person names, sponsor names or commercial outcomes. `qa/check.py` fails the build if a known real name appears.

## Local build & check

```bash
pip install -r requirements.txt playwright && playwright install chromium webkit
python3 scripts/build.py                  # production build -> dist/
SITE_ENV=preview python3 scripts/build.py # preview build (noindex)
python3 -m http.server 8777 --directory dist &
BASE=http://localhost:8777 python3 qa/check.py
```

## Cloudflare Pages settings
- Build command: `pip install -r requirements.txt && python3 scripts/build.py`
- Build output directory: `dist`
- Production branch: `main` · Preview branch: `preview` → custom domain `preview.lapiscloud.ai`
- Environment variable: `PYTHON_VERSION=3.11`
- Any branch other than `main` automatically builds with `noindex` (via `CF_PAGES_BRANCH`).
