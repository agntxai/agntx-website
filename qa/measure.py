import asyncio, json, sys
from playwright.async_api import async_playwright
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8765"
PAGES = []
for v in ["v1-institutional","v2-dark","v3-editorial"]:
    PAGES += [f"/{v}/", f"/{v}/insights/", f"/{v}/insights/ai-governance-gap/"]
VIEWS = [(1440,900),(1280,720),(1024,768),(390,844)]
JS = r"""
() => {
  const nav = document.querySelector('.nav'); const nr = nav.getBoundingClientRect();
  const firstText = document.querySelector('.hero .eyebrow, .ins-hero .kicker, .art-hero .back');
  const h1 = document.querySelector('h1');
  const fr = firstText ? firstText.getBoundingClientRect() : null;
  const hr = h1.getBoundingClientRect();
  const fonts = {};
  for (const sel of ['h1','h2','p','.btn','.brand span','.links a','.kicker']) {
    const el = document.querySelector(sel); if (!el) continue;
    const cs = getComputedStyle(el);
    fonts[sel] = {family: cs.fontFamily.split(',')[0], size: cs.fontSize, weight: cs.fontWeight, lh: cs.lineHeight};
  }
  const loaded = [...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family+' '+f.weight+(f.style==='italic'?'i':''));
  const failed = [...document.fonts].filter(f=>f.status==='error').map(f=>f.family+' '+f.weight);
  const linksVisible = getComputedStyle(document.querySelector('.links')).display !== 'none';
  const links = document.querySelector('.links').getBoundingClientRect();
  const btn = document.querySelector('.nav .btn').getBoundingClientRect();
  return {navBottom: Math.round(nr.bottom), firstTextTop: fr?Math.round(fr.top):null, h1Top: Math.round(hr.top), h1Bottom: Math.round(hr.bottom),
          overlapPx: fr? Math.round(nr.bottom - fr.top) : null, navHeight: Math.round(nr.height),
          linksVisible, linksRight: Math.round(links.right), btnLeft: Math.round(btn.left), navCrowded: linksVisible && links.right > btn.left - 16,
          fonts, loaded: [...new Set(loaded)], failed: [...new Set(failed)], docW: document.documentElement.scrollWidth, vw: innerWidth};
}
"""
async def main():
    out = {}
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for (w,h) in VIEWS:
            ctx = await b.new_context(viewport={"width":w,"height":h})
            pg = await ctx.new_page()
            for path in PAGES:
                await pg.goto(BASE+path+"?static", wait_until="networkidle")
                await pg.evaluate("document.fonts.ready")
                r = await pg.evaluate(JS)
                out[f"{w}x{h} {path}"] = r
                name = (path.strip('/').replace('/','_') or 'root') + f"_{w}.png"
                await pg.screenshot(path=f"/tmp/lapis-qa/{name}", full_page=False)
            await ctx.close()
        await b.close()
    print(json.dumps(out, indent=1))
asyncio.run(main())
