"""Release gate: header clearance >= 80px, fonts load, no horizontal scroll, no broken links/images, no confidential names.
Usage: BASE=http://localhost:8777 python3 qa/check.py"""
import asyncio, os, re, sys
from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright
BASE = os.environ.get("BASE", "http://localhost:8777")
FORBIDDEN = re.compile(r"packiyo|phillip|\bjavi\b|darius|preston|\bprem\b|\bxavi\b|\braj\b|dorian|palletline", re.I)
VIEWS = [(1440, 900), (1440, 600), (1280, 640), (390, 844)]
async def main():
    fails = []; seen = set(); pages = ["/", "/insights/"]
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await (await b.new_context(viewport={"width": 1440, "height": 900})).new_page()
        await pg.goto(BASE + "/insights/", wait_until="networkidle")
        pages += sorted({urlparse(h).path for h in await pg.eval_on_selector_all("a[href^='/insights/']", "els=>els.map(e=>e.getAttribute('href'))") if h.count('/') == 3})
        await b.close()
        for eng in ("chromium", "webkit"):
            b = await getattr(p, eng).launch()
            for w, h in VIEWS:
                pg = await (await b.new_context(viewport={"width": w, "height": h})).new_page()
                bad = []
                pg.on("response", lambda r: bad.append(f"{r.status} {r.url}") if r.status >= 400 else None)
                for path in pages:
                    await pg.goto(BASE + path + "?static", wait_until="networkidle"); await pg.evaluate("document.fonts.ready")
                    r = await pg.evaluate("""()=>{const n=document.querySelector('.nav').getBoundingClientRect();
                      const f=document.querySelector('.hero .eyebrow, .ins-hero .kicker, .art-hero .back').getBoundingClientRect();
                      return {gap:Math.round(f.top-n.bottom), hs:document.documentElement.scrollWidth>innerWidth+1,
                        fontFail:[...document.fonts].filter(x=>x.status==='error').length,
                        imgFail:[...document.images].filter(i=>i.complete&&!i.naturalWidth).map(i=>i.src), text:document.body.innerText}}""")
                    tag = f"{eng} {w}x{h} {path}"
                    if r["gap"] < 50 if w < 600 else r["gap"] < 80: fails.append(f"{tag}: header gap {r['gap']}px")
                    if r["hs"]: fails.append(f"{tag}: horizontal scroll")
                    if r["fontFail"]: fails.append(f"{tag}: {r['fontFail']} font(s) failed")
                    if r["imgFail"]: fails.append(f"{tag}: broken images {r['imgFail']}")
                    if FORBIDDEN.search(r["text"]): fails.append(f"{tag}: forbidden term '{FORBIDDEN.search(r['text']).group(0)}'")
                    if eng == "chromium" and (w, h) == (1440, 900):
                        for href in await pg.eval_on_selector_all("a[href^='/']", "els=>els.map(e=>e.getAttribute('href'))"):
                            u = urljoin(BASE, href.split('#')[0]); 
                            if u in seen: continue
                            seen.add(u); resp = await pg.request.get(u)
                            if resp.status >= 400: fails.append(f"broken link {href} on {path} -> {resp.status}")
                fails += [f"{eng} {w}x{h}: {x}" for x in set(bad) if "favicon" not in x]
            await b.close()
    print(f"checked {len(pages)} pages x {len(VIEWS)} viewports x 2 engines, {len(seen)} links")
    print("PASS" if not fails else "FAIL\n" + "\n".join(sorted(set(fails))))
    sys.exit(1 if fails else 0)
asyncio.run(main())
