#!/usr/bin/env python3
"""Build the agntx.ai site into dist/.

  src/index.html          homepage template (<!-- INSIGHTS_TEASER --> is filled in)
  src/css/*.css           base -> insights -> refinements -> theme, concatenated to dist/style.css
  src/assets/             copied as-is to dist/assets/
  content/insights/*.md   one file per post, front-matter + markdown

Usage:  python3 scripts/build.py            (production, indexable)
        SITE_ENV=preview python3 scripts/build.py   (adds noindex)
"""
import os, re, glob, html, shutil, hashlib, datetime
import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, CONTENT, DIST = (os.path.join(ROOT, p) for p in ("src", "content/insights", "dist"))
PREVIEW = os.environ.get("SITE_ENV", "").lower() == "preview" or os.environ.get("CF_PAGES_BRANCH", "main") != "main"
SITE_URL = "https://agntx.ai"
e = html.escape

def parse(path):
    raw = open(path, encoding="utf-8").read()
    _, fm, body = raw.split("---", 2)
    meta = {}
    for line in fm.strip().splitlines():
        if ":" not in line: continue
        k, v = line.split(":", 1); v = v.strip()
        if len(v) > 1 and v[0] == v[-1] and v[0] in "'\"": v = v[1:-1]
        meta[k.strip()] = v
    for req in ("title", "type", "date", "author", "read", "image", "summary"):
        if req not in meta: raise SystemExit(f"{os.path.basename(path)}: missing front-matter field '{req}'")
    meta["slug"] = os.path.basename(path)[:-3]
    meta["html"] = markdown.markdown(body, extensions=["tables"])
    meta["dt"] = datetime.date.fromisoformat(meta["date"])
    if not os.path.exists(os.path.join(SRC, "assets/insights", meta["image"])):
        raise SystemExit(f"{meta['slug']}: image assets/insights/{meta['image']} not found")
    return meta

def fmt(d): return d.strftime("%B %-d, %Y")
def plural(t): return {"All": "All", "Case Study": "Case Studies"}.get(t, t + "s")

def card(p, href):
    return (f'<a class="ins-card reveal" href="{href}" data-type="{e(p["type"])}"><div class="ins-img" style="background-image:url(/assets/insights/{p["image"]})"></div>'
            f'<div class="ins-body"><p class="ins-meta"><span class="ins-type">{e(p["type"])}</span> · {fmt(p["dt"])} · {e(p["read"])}</p>'
            f'<h3>{e(p["title"])}</h3><p>{e(p["summary"])}</p><span class="ins-more">Read →</span></div></a>')

def main():
    posts = sorted((parse(p) for p in glob.glob(os.path.join(CONTENT, "*.md"))), key=lambda m: m["dt"], reverse=True)
    shutil.rmtree(DIST, ignore_errors=True); os.makedirs(DIST)
    shutil.copytree(os.path.join(SRC, "assets"), os.path.join(DIST, "assets"))
    css = "".join(open(os.path.join(SRC, "css", f), encoding="utf-8").read() + "\n" for f in ("base.css", "insights.css", "refinements.css", "theme.css"))
    open(os.path.join(DIST, "style.css"), "w").write(css)
    ver = hashlib.sha1(css.encode()).hexdigest()[:10]

    home = open(os.path.join(SRC, "index.html"), encoding="utf-8").read()
    home = home.replace('href="/style.css"', f'href="/style.css?v={ver}"')
    robots_meta = '<meta name="robots" content="noindex,nofollow">' if PREVIEW else ""
    home = home.replace('<meta charset="utf-8">', '<meta charset="utf-8">' + robots_meta, 1)
    home = home.replace('href="insights/', 'href="/insights/').replace('href="insights/"', 'href="/insights/"')
    head = re.search(r"<head>(.*?)</head>", home, re.S).group(1)
    header = re.search(r"<header.*?</header>", home, re.S).group(0)
    footer = re.search(r"<footer.*?</footer>", home, re.S).group(0)
    script = re.search(r"<script>.*?</script>", home, re.S).group(0)
    cls = re.search(r'<body class="([^"]+)"', home).group(1)
    to_home = lambda s: re.sub(r'href="#([a-z]+)"', lambda m: 'href="/"' if m.group(1) == "top" else f'href="/#{m.group(1)}"', s)
    sub_header, sub_footer = to_home(header).replace('href="/insights/"', 'href="/insights/" aria-current="page"'), to_home(footer)
    sub_head = re.sub(r"<title>.*?</title>", "", head)
    if not PREVIEW:  # production only: canonical + social share tags for the homepage
        desc = re.search(r'<meta name="description" content="([^"]*)"', home).group(1)
        title = re.search(r"<title>(.*?)</title>", home).group(1)
        home_meta = (f'<link rel="canonical" href="{SITE_URL}/"><meta property="og:type" content="website">'
                     f'<meta property="og:url" content="{SITE_URL}/"><meta property="og:title" content="{title}">'
                     f'<meta property="og:description" content="{desc}"><meta property="og:image" content="{SITE_URL}/assets/hero-v1.jpg">'
                     '<meta name="twitter:card" content="summary_large_image">')
        home = home.replace("</head>", home_meta + "</head>", 1)

    teaser = ('<section class="sec home-ins"><div class="wrap"><p class="kicker center">Insights</p><h2 class="center">Thinking out loud.</h2>'
              '<p class="center sub2">Essays, research and field notes on AI, organizational knowledge, and modernizing without starting over.</p>'
              f'<div class="ins-grid">{"".join(card(p, "/insights/" + p["slug"] + "/") for p in posts[:3])}</div>'
              '<p class="center"><a class="btn btn-ghost" href="/insights/">All insights →</a></p></div></section>')
    open(os.path.join(DIST, "index.html"), "w").write(home.replace("<!-- INSIGHTS_TEASER -->", teaser))

    types = ["All"] + sorted({p["type"] for p in posts})
    chips = "".join(f'<button class="chip{" on" if t == "All" else ""}" data-f="{e(t)}">{e(plural(t))}</button>' for t in types)
    feat, rest = posts[0], posts[1:]
    listing = f'''<!doctype html><html lang="en"><head>{sub_head}<title>Insights | Lapis by Agentic Technologies</title></head><body class="{cls} insights-page">{sub_header}<main>
<section class="ins-hero"><div class="wrap"><p class="kicker">Insights</p><h1>Essays, research and field notes.</h1><p class="lede">What we're learning about AI, organizational knowledge, and modernizing without starting over.</p></div></section>
<section class="wrap"><a class="ins-feature reveal" href="/insights/{feat['slug']}/"><div class="ins-img" style="background-image:url(/assets/insights/{feat['image']})"></div>
<div class="ins-body"><p class="ins-meta"><span class="ins-type">Featured {e(feat['type'])}</span> · {fmt(feat['dt'])} · {e(feat['read'])}</p><h2>{e(feat['title'])}</h2><p>{e(feat['summary'])}</p><span class="ins-more">Read the {e(feat['type'].lower())} →</span></div></a>
<div class="chips">{chips}</div><div class="ins-grid">{"".join(card(p, "/insights/" + p["slug"] + "/") for p in rest)}</div></section>
<section class="cta"><div class="wrap cta-in"><h2>Get new insights by email.</h2><p>A short note when we publish something worth your time. No spam.</p><a class="btn btn-lg" href="mailto:hello@agntx.ai?subject=Subscribe%20to%20Lapis%20Insights">Subscribe →</a></div></section>
</main>{sub_footer}{script}
<script>document.querySelectorAll('.chip').forEach(c=>c.onclick=()=>{{document.querySelectorAll('.chip').forEach(x=>x.classList.remove('on'));c.classList.add('on');const f=c.dataset.f;document.querySelectorAll('.ins-grid .ins-card').forEach(k=>k.style.display=(f==='All'||k.dataset.type===f)?'':'none')}})</script></body></html>'''
    os.makedirs(os.path.join(DIST, "insights"))
    open(os.path.join(DIST, "insights/index.html"), "w").write(listing)

    for p in posts:
        related = [q for q in posts if q["slug"] != p["slug"]][:3]
        dl = '<a class="btn btn-ghost btn-sm" href="javascript:window.print()">Download PDF</a>' if p["type"] in ("Whitepaper", "Brief") else ""
        subj = re.sub(r"\s", "%20", e(p["title"]))
        page = f'''<!doctype html><html lang="en"><head>{sub_head}<title>{e(p['title'])} | Lapis Insights</title><meta name="description" content="{e(p['summary'])}">
<meta property="og:title" content="{e(p['title'])}"><meta property="og:description" content="{e(p['summary'])}"><meta property="og:image" content="{SITE_URL}/assets/insights/{p['image']}"><meta property="og:type" content="article"><link rel="canonical" href="{SITE_URL}/insights/{p['slug']}/"></head>
<body class="{cls} insights-page article-page">{sub_header}<main><article>
<header class="art-hero"><div class="wrap art-narrow"><a class="back" href="/insights/">← All insights</a><p class="ins-meta"><span class="ins-type">{e(p['type'])}</span> · {fmt(p['dt'])} · {e(p['read'])}</p>
<h1>{e(p['title'])}</h1><p class="lede">{e(p['summary'])}</p><div class="byline"><span>By {e(p['author'])}</span>{dl}</div></div></header>
<div class="wrap"><div class="art-img" style="background-image:url(/assets/insights/{p['image']})"></div></div>
<div class="wrap art-narrow prose-art">{p['html']}</div></article>
<section class="art-cta"><div class="wrap art-narrow"><h3>Want to see what this looks like in your organization?</h3><p>Bring a real problem. In 90 minutes we'll show you what Lapis does with it.</p><a class="btn" href="mailto:hello@agntx.ai?subject=Re%3A%20{subj}">Talk to us →</a></div></section>
<section class="wrap related"><p class="kicker">Keep reading</p><div class="ins-grid">{"".join(card(q, "/insights/" + q["slug"] + "/") for q in related)}</div></section>
</main>{sub_footer}{script}</body></html>'''
        os.makedirs(os.path.join(DIST, "insights", p["slug"]))
        open(os.path.join(DIST, "insights", p["slug"], "index.html"), "w").write(page)

    urls = [SITE_URL + "/", SITE_URL + "/insights/"] + [f"{SITE_URL}/insights/{p['slug']}/" for p in posts]
    open(os.path.join(DIST, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{u}</loc></url>" for u in urls) + "</urlset>\n")
    open(os.path.join(DIST, "robots.txt"), "w").write("User-agent: *\nDisallow: /\n" if PREVIEW else f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    headers = "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n"
    if PREVIEW: headers += "  X-Robots-Tag: noindex, nofollow\n"
    headers += "/assets/*\n  Cache-Control: public, max-age=86400\n/style.css\n  Cache-Control: public, max-age=31536000, immutable\n"
    open(os.path.join(DIST, "_headers"), "w").write(headers)
    if os.path.exists(os.path.join(ROOT, "_redirects")): shutil.copy(os.path.join(ROOT, "_redirects"), DIST)
    print(f"built {len(posts)} posts -> dist/ ({'preview' if PREVIEW else 'production'})")

if __name__ == "__main__":
    main()
