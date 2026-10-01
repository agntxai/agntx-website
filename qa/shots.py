import asyncio, sys, json
from playwright.async_api import async_playwright
import os; BASE=os.environ.get("BASE","http://localhost:8765")
async def main():
    res={}
    async with async_playwright() as p:
        for eng in ["chromium","webkit"]:
            b = await getattr(p,eng).launch()
            for (w,h) in [(1470,760),(1440,600),(1280,640)]:
                ctx = await b.new_context(viewport={"width":w,"height":h}, device_scale_factor=1)
                pg = await ctx.new_page()
                for v in ["v1-institutional","v2-dark","v3-editorial"]:
                    for sub in ["", "insights/", "insights/two-hour-app/"]:
                        await pg.goto(f"{BASE}/{v}/{sub}", wait_until="networkidle"); await pg.wait_for_timeout(600)
                        r = await pg.evaluate("""()=>{const n=document.querySelector('.nav').getBoundingClientRect();
                          const els=[...document.querySelectorAll('main h1, main .eyebrow, main .kicker, main .lede, main .back, main .ins-meta')].filter(e=>e.getBoundingClientRect().top<innerHeight);
                          const hit=els.filter(e=>{const r=e.getBoundingClientRect();return r.top < n.bottom && r.bottom>n.top}).map(e=>e.className||e.tagName);
                          return {navBottom:Math.round(n.bottom), firstTop: els.length?Math.round(Math.min(...els.map(e=>e.getBoundingClientRect().top))):null, hit}}""")
                        res[f"{eng} {w}x{h} {v}/{sub}"]=r
                        if w==1470 or h==600: await pg.screenshot(path=f"{eng}_{w}x{h}_{v}_{sub.strip('/').replace('/','_') or 'home'}.png")
                await ctx.close()
            await b.close()
    for k,r in res.items(): print(f"{k:60s} navBottom={r['navBottom']} firstTop={r['firstTop']} overlapping={r['hit']}")
asyncio.run(main())
