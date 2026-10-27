#!/usr/bin/env python3
"""Builds the static site into site/dist from site/src/*.md.
Frontmatter: title, description, hero (home page only)."""
import pathlib, re, shutil, markdown

root = pathlib.Path(__file__).parent
src, dist = root / 'src', root / 'dist'
shutil.rmtree(dist, ignore_errors=True)
dist.mkdir()
shutil.copy(root / 'style.css', dist / 'style.css')
for f in ('icon.png', 'apple-touch-icon.png', 'favicon.ico', 'wordmark.png', 'planet.js'):
    shutil.copy(root / f, dist / f)
shutil.copytree(root / 'fonts', dist / 'fonts')
header = (root / '_header.html').read_text()
footer = (root / '_footer.html').read_text()

HERO = '''<section class="hero"><div class="wrap wide hero-grid"><div class="hero-copy">
<p class="eyebrow">A community for pilots and cabin crew</p>
<h1>Life beyond<br><em>the roster.</em></h1>
<p class="tagline">Your time off, your interests, your community.</p>
<p class="lead">Galley brings crew together through local clubs, shared interests and plans that fit around the way we live.</p>
<div class="actions"><a class="btn" href="https://www.instagram.com/crewgalley/" rel="noopener">Follow @crewgalley</a></div>
<p class="soon">Starting in Dubai · December 2026</p>
</div><div class="hero-phone" role="img" aria-label="An illustration of Galley’s Base screen: your days off this week and your clubs in Dubai."><span class="mock-label" aria-hidden="true">Illustration</span><div class="phone" aria-hidden="true"><div class="screen"><div class="a-status"><b>9:41</b><span class="a-batt"></span></div><div class="a-head"><div class="a-head-t"><b>Dubai</b><span>Make the most of your days off.</span></div><span class="a-iconbtn"><svg viewBox="0 0 24 24"><rect x="3.5" y="5" width="17" height="15.5" rx="3"/><path d="M3.5 10h17M8 3v4M16 3v4"/></svg></span><span class="a-me">SK</span></div><div class="a-strip"><div class="a-col"><div class="a-cell "><span class="a-dow">Today</span><span class="a-num">10</span></div><span class="a-bar"></span></div><div class="a-col"><div class="a-cell free on"><span class="a-dow">Thu</span><span class="a-num">11</span></div><span class="a-bar on"></span></div><div class="a-col"><div class="a-cell free"><span class="a-dow">Fri</span><span class="a-num">12</span></div><span class="a-bar on"></span></div><div class="a-col"><div class="a-cell "><span class="a-dow">Sat</span><span class="a-num">13</span></div><span class="a-bar"></span></div><div class="a-col"><div class="a-cell "><span class="a-dow">Sun</span><span class="a-num">14</span></div><span class="a-bar"></span></div><div class="a-col"><div class="a-cell "><span class="a-dow">Mon</span><span class="a-num">15</span></div><span class="a-bar"></span></div><div class="a-col"><div class="a-cell "><span class="a-dow">Tue</span><span class="a-num">16</span></div><span class="a-bar"></span></div></div><div class="a-key"><i class="sw"></i>Your days off</div><div class="a-free"><p><b>Thu 11</b><span> · Free all day</span></p><span class="a-link">Edit</span></div><div class="a-row"><b>Your clubs</b><span class="a-link">See all</span></div><div class="a-clubs"><div class="a-club"><span class="a-ic"><svg viewBox="0 0 24 24"><ellipse cx="11" cy="9.5" rx="6" ry="6.5"/><path d="M14.6 14.6 19.5 20"/><circle cx="18.5" cy="5" r="1.6"/></svg></span><b>Padel</b></div><div class="a-club"><span class="a-ic"><svg viewBox="0 0 24 24"><ellipse cx="8" cy="8" rx="2.6" ry="4.2"/><ellipse cx="16" cy="12.5" rx="2.6" ry="4.2"/><path d="M6.2 15.4h3.6M14.2 19.9h3.6"/></svg></span><b>Running</b></div><div class="a-club"><span class="a-ic"><svg viewBox="0 0 24 24"><path d="M5 9h11v5a5 5 0 0 1-5 5h-1a5 5 0 0 1-5-5Z"/><path d="M16 10.5h1.5a2.5 2.5 0 0 1 0 5H16M9 3.5v2.5M12 3.5v2.5"/></svg></span><b>Coffee</b></div><div class="a-club"><span class="a-ic"><svg viewBox="0 0 24 24"><path d="M4 5.5A1.5 1.5 0 0 1 5.5 4H11v16H5.5A1.5 1.5 0 0 1 4 18.5Z"/><path d="M20 5.5A1.5 1.5 0 0 0 18.5 4H13v16h5.5a1.5 1.5 0 0 0 1.5-1.5Z"/></svg></span><b>Books</b></div><div class="a-club"><span class="a-ic"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M5.6 5.6c3.5 3.5 3.5 9.3 0 12.8M18.4 5.6c-3.5 3.5-3.5 9.3 0 12.8"/></svg></span><b>Tennis</b></div><div class="a-club"><span class="a-ic"><svg viewBox="0 0 24 24"><path d="M2.5 9 12 4.5 21.5 9 12 13.5Z"/><path d="M6.5 11v4.5c1.5 1.5 3.5 2.2 5.5 2.2s4-.7 5.5-2.2V11"/></svg></span><b>Study</b></div></div><div class="a-row"><b>Clubs in Dubai</b><span class="a-link">Explore</span></div><div class="a-more"><span>Beach</span><span>Brunch</span><span>Gym</span><span>Day trips</span></div><div class="a-tabs"><span class="on"><svg viewBox="0 0 24 24" class="fill"><path d="M4 10.5 12 4l8 6.5V20h-5.5v-5.5h-5V20H4Z"/></svg>Base</span><span><svg viewBox="0 0 24 24"><circle cx="9" cy="8.5" r="3.2"/><path d="M3 19c.6-3.4 3-5.2 6-5.2s5.4 1.8 6 5.2"/><path d="M15.5 5.6a3 3 0 0 1 0 5.8M17.6 14.2c1.8.6 3 2.2 3.4 4.8"/></svg>Clubs</span><span><svg viewBox="0 0 24 24"><path d="M10.5 3.6c0-.8.7-1.6 1.5-1.6s1.5.8 1.5 1.6V9l7 4v2l-7-2v5l2 1.5V21L12 20l-3.5 1v-1.5l2-1.5v-5l-7 2v-2l7-4Z"/></svg>Away</span><span><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5-5 2 2-5Z"/></svg>Explore</span><span><svg viewBox="0 0 24 24"><path d="M4 5.5h11A1.5 1.5 0 0 1 16.5 7v6.5A1.5 1.5 0 0 1 15 15H9l-3.5 3v-3H4a1.5 1.5 0 0 1-1.5-1.5V7A1.5 1.5 0 0 1 4 5.5Z"/><path d="M18.5 9H20a1.5 1.5 0 0 1 1.5 1.5V17a1.5 1.5 0 0 1-1.5 1.5h-1.5V21L15 18.5h-4"/></svg>Chats</span></div></div></div></div></div><div class="gm" id="planet" aria-hidden="true"></div><script src="/planet.js" defer></script></section>
<main id="content" class="home">
<section class="section story"><div class="wrap wide">
<p class="eyebrow">Your base</p>
<h2>Same city. Different schedules.</h2>
<div class="story-text">
<p class="first">Sharing a home base doesn’t always mean sharing the same days off.</p>
<p>Galley brings together crew with similar interests, making it easier to find company and make plans whenever you’re free.</p>
<p>Whether it’s tennis, a morning run, a study session before your next simulator, or simply catching up over coffee.</p>
</div>
</div></section>
<section class="section band clubs"><div class="wrap wide clubs-grid"><div>
<p class="eyebrow">Clubs</p>
<h2>A place for shared interests.</h2>
<p class="intro">Join local clubs built around the things you enjoy.</p>
<p class="intro">Discover plans, exchange recommendations and get to know crew at your home base.</p>
</div><div class="orbits" aria-hidden="true"><svg class="orb-lines" viewBox="0 0 400 320" preserveAspectRatio="none">
<g class="orb-spin"><ellipse cx="200" cy="165" rx="185" ry="135"/></g>
<g class="orb-spin rev"><ellipse cx="200" cy="165" rx="120" ry="88"/></g>
<ellipse class="orb-solid" cx="200" cy="165" rx="58" ry="44"/>
<path id="orbA" d="M15 165a185 135 0 1 0 370 0a185 135 0 1 0 -370 0" fill="none" stroke="none"/>
<path id="orbB" d="M320 165a120 88 0 1 0 -240 0a120 88 0 1 0 240 0" fill="none" stroke="none"/>
<circle class="orb-dot" r="3.5"><animateMotion dur="26s" repeatCount="indefinite"><mpath href="#orbA"/></animateMotion></circle>
<circle class="orb-dot b" r="2.5"><animateMotion dur="17s" repeatCount="indefinite" begin="-6s"><mpath href="#orbB"/></animateMotion></circle>
</svg>
<span class="orb-core"><span class="orb-pin"></span>Your base</span><span class="orb-chip" style="left:20%;top:16%;--d:7s;--w:0s"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M5.6 5.6c3.5 3.5 3.5 9.3 0 12.8M18.4 5.6c-3.5 3.5-3.5 9.3 0 12.8"/></svg>Tennis</span><span class="orb-chip" style="left:62%;top:8%;--d:8s;--w:1.2s"><svg viewBox="0 0 24 24" aria-hidden="true"><ellipse cx="11" cy="9.5" rx="6" ry="6.5"/><path d="M14.6 14.6 19.5 20"/><circle cx="18.5" cy="5" r="1.6"/></svg>Padel</span><span class="orb-chip" style="left:82%;top:33%;--d:6.5s;--w:0.6s"><svg viewBox="0 0 24 24" aria-hidden="true"><ellipse cx="8" cy="8" rx="2.6" ry="4.2"/><ellipse cx="16" cy="12.5" rx="2.6" ry="4.2"/><path d="M6.2 15.4h3.6M14.2 19.9h3.6"/></svg>Running</span><span class="orb-chip" style="left:14%;top:50%;--d:7.5s;--w:2s"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 9h11v5a5 5 0 0 1-5 5h-1a5 5 0 0 1-5-5Z"/><path d="M16 10.5h1.5a2.5 2.5 0 0 1 0 5H16M9 3.5v2.5M12 3.5v2.5"/></svg>Coffee</span><span class="orb-chip" style="left:78%;top:66%;--d:8.5s;--w:0.3s"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5.5A1.5 1.5 0 0 1 5.5 4H11v16H5.5A1.5 1.5 0 0 1 4 18.5Z"/><path d="M20 5.5A1.5 1.5 0 0 0 18.5 4H13v16h5.5a1.5 1.5 0 0 0 1.5-1.5Z"/></svg>Books</span><span class="orb-chip" style="left:18%;top:82%;--d:7s;--w:1.6s"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2.5 9 12 4.5 21.5 9 12 13.5Z"/><path d="M6.5 11v4.5c1.5 1.5 3.5 2.2 5.5 2.2s4-.7 5.5-2.2V11"/></svg>Study</span><span class="orb-chip" style="left:52%;top:88%;--d:6s;--w:0.9s"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4a8 8 0 0 1 8 8H4a8 8 0 0 1 8-8Z"/><path d="M12 12v7M4 20c2.7-1.3 5.3-1.3 8 0s5.3 1.3 8 0"/></svg>Beach</span><span class="orb-chip" style="left:40%;top:30%;--d:9s;--w:2.4s"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="13" r="7"/><circle cx="12" cy="13" r="2.5"/><path d="M4 4v4M2.5 4v3.5a1.5 1.5 0 0 0 3 0V4M20 4v16"/></svg>Brunch</span></div></div></section>
<section class="section how" id="how"><div class="wrap wide">
<p class="eyebrow">How Galley works</p>
<h2>Simple from the start.</h2>
<ol class="steps">
<li><span class="step-n">01</span><h3>Find your community</h3><p>Choose your home base and explore local clubs and interests.</p></li>
<li><span class="step-n">02</span><h3>See what’s happening</h3><p>Discover plans that fit your time off. Find crew who are free on the same days as you.</p></li>
<li><span class="step-n">03</span><h3>Join in</h3><p>Meet for something you enjoy, or start a plan of your own.</p></li>
</ol>
</div></section>
<section class="section origin"><div class="wrap">
<p class="eyebrow">When you’re away</p>
<h2>Your community travels with you.</h2>
<p>Explore places recommended by fellow crew and discover plans during your layovers. Wherever work takes you, Galley gives you a connection to the crew community.</p>
</div></section>
<section class="section origin"><div class="wrap">
<p class="eyebrow">Our story</p>
<h2>Made with crew life in mind.</h2>
<p>Galley began with a simple observation: people can share a home base, similar interests and the same unpredictable schedules, yet rarely have their days off together.</p>
<p>Created by an airline pilot, Galley is designed to make those days a little easier to enjoy. It starts with the people and places around us.</p>
</div></section>
<section class="section closing"><div class="wrap">
<p class="eyebrow">Join us</p>
<h2>A little more life off duty.</h2>
<p>A community for verified pilots and cabin crew, beginning in Dubai.</p>
<div class="actions"><a class="btn" href="https://www.instagram.com/crewgalley/" rel="noopener">Follow @crewgalley</a></div>
<p class="small">Launching December 2026.</p>
<p class="small">Galley is an independent community for pilots and cabin crew aged 18+. It is not affiliated with any airline.</p>
</div></section>
</main>'''

def page(md_text, meta):
    body = markdown.markdown(md_text, extensions=['tables'])
    if meta.get('hero'):
        content = HERO
    else:
        content = f'<main id="content"><div class="wrap">{body}</div></main>'
    robots = f'<meta name="robots" content="{meta["robots"]}">' if meta.get('robots') else ''
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{meta["title"]}</title><meta name="description" content="{meta.get("description","")}">{robots}
<meta property="og:title" content="{meta["title"]}"><meta property="og:description" content="{meta.get("description","")}"><meta property="og:image" content="https://crewgalley.app/icon.png"><meta property="og:site_name" content="Galley">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" href="/icon.png" type="image/png"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><meta name="theme-color" content="#0B1424"><script>(function(){{var r=document.documentElement,t=null;try{{t=localStorage.getItem('galley-theme')}}catch(e){{}}if(t==='light'||t==='dark')r.dataset.theme=t;r.dataset.mode=t||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light')}})()</script><link rel="preload" href="/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/style.css"></head><body>
{header}{content}{footer}</body></html>'''

for f in sorted(src.glob('*.md')):
    text = f.read_text()
    m = re.match(r'---\n(.*?)\n---\n?(.*)', text, re.S)
    meta = dict(line.split(': ', 1) for line in m.group(1).splitlines() if ': ' in line)
    meta['hero'] = meta.get('hero') == 'true'
    html = page(m.group(2), meta)
    if f.stem != 'index':
        html = html.replace(f'<a href="/{f.stem}/">', f'<a href="/{f.stem}/" aria-current="page">', 1)
    out = dist / 'index.html' if f.stem == 'index' else dist / f.stem / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print('built', out.relative_to(dist))

(dist / 'CNAME').write_text('crewgalley.app\n')
(dist / '.nojekyll').write_text('')
# .well-known for later universal links; harmless now
wk = dist / '.well-known'; wk.mkdir()
(wk / 'apple-app-site-association').write_text('{"applinks":{"apps":[],"details":[]}}')
