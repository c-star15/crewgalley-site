#!/usr/bin/env python3
"""Builds the static site into site/dist from site/src/*.md.
Frontmatter: title, description, hero (home page only)."""
import pathlib, re, shutil, markdown

root = pathlib.Path(__file__).parent
src, dist = root / 'src', root / 'dist'
shutil.rmtree(dist, ignore_errors=True)
dist.mkdir()
shutil.copy(root / 'style.css', dist / 'style.css')
for f in ('icon.png', 'apple-touch-icon.png', 'favicon.ico', 'wordmark.png'):
    shutil.copy(root / f, dist / f)
shutil.copytree(root / 'fonts', dist / 'fonts')
header = (root / '_header.html').read_text()
footer = (root / '_footer.html').read_text()

HERO = '''<section class="hero"><div class="wrap wide">
<p class="eyebrow">Pilots and cabin crew · any airline</p>
<h1>New city. Free day.<br><em>Find your people.</em></h1>
<p class="lead">Your crew has other plans? Galley shows pilots and cabin crew from any airline on a layover in the same city, up for the same thing. One tap to meet up. Every account is checked by a person before it can see anyone, and every message is end-to-end encrypted.</p>
<div class="actions"><a class="btn" href="/verification/">How verification works</a><a class="btn secondary" href="/private/">Private by design</a></div>
<p class="soon">Coming to the App Store and Google Play in December 2026.</p>
</div><svg class="skyline" viewBox="0 0 1440 340" preserveAspectRatio="xMidYMax slice" aria-hidden="true"><g class="far"><rect x="-20" y="120" width="90" height="230"/><rect x="70" y="120" width="90" height="230"/><rect x="190" y="170" width="90" height="180"/><rect x="310" y="170" width="120" height="180"/><rect x="430" y="170" width="90" height="180"/><rect x="530" y="80" width="90" height="270"/><rect x="630" y="200" width="90" height="150"/><rect x="720" y="80" width="60" height="270"/><rect x="810" y="80" width="90" height="270"/><rect x="900" y="80" width="60" height="270"/><rect x="990" y="80" width="90" height="270"/><rect x="1080" y="170" width="60" height="180"/><rect x="1140" y="200" width="60" height="150"/><rect x="1230" y="80" width="120" height="270"/><rect x="1350" y="200" width="120" height="150"/></g><g class="near"><rect x="0" y="244" width="66" height="106" rx="3"/><rect x="72" y="60" width="98" height="290" rx="3"/><rect x="176" y="220" width="98" height="130" rx="3"/><rect x="280" y="190" width="58" height="160" rx="3"/><rect x="344" y="20" width="42" height="330" rx="3"/><rect x="392" y="160" width="58" height="190" rx="3"/><rect x="456" y="100" width="42" height="250" rx="3"/><rect x="504" y="130" width="82" height="220" rx="3"/><rect x="592" y="20" width="42" height="330" rx="3"/><rect x="640" y="130" width="58" height="220" rx="3"/><rect x="704" y="270" width="42" height="80" rx="3"/><rect x="752" y="100" width="82" height="250" rx="3"/><rect x="840" y="160" width="82" height="190" rx="3"/><rect x="928" y="244" width="58" height="106" rx="3"/><rect x="992" y="190" width="98" height="160" rx="3"/><rect x="1096" y="130" width="42" height="220" rx="3"/><rect x="1144" y="160" width="66" height="190" rx="3"/><rect x="1216" y="160" width="58" height="190" rx="3"/><rect x="1280" y="220" width="66" height="130" rx="3"/><rect x="1352" y="160" width="98" height="190" rx="3"/></g><g class="lights"><rect class="lit" x="10" y="260" width="6" height="9" rx="1"/><rect class="lit" x="38" y="282" width="6" height="9" rx="1"/><rect class="lit" x="38" y="304" width="6" height="9" rx="1"/><rect class="lit" x="52" y="326" width="6" height="9" rx="1"/><rect class="lit" x="82" y="76" width="6" height="9" rx="1"/><rect class="lit" x="82" y="120" width="6" height="9" rx="1"/><rect class="lit" x="96" y="120" width="6" height="9" rx="1"/><rect class="lit" x="152" y="186" width="6" height="9" rx="1"/><rect class="lit" x="96" y="252" width="6" height="9" rx="1"/><rect class="lit" x="124" y="274" width="6" height="9" rx="1"/><rect class="lit" x="96" y="296" width="6" height="9" rx="1"/><rect class="lit" x="96" y="318" width="6" height="9" rx="1"/><rect class="lit" x="242" y="236" width="6" height="9" rx="1"/><rect class="lit" x="200" y="258" width="6" height="9" rx="1"/><rect class="lit" x="304" y="206" width="6" height="9" rx="1"/><rect class="lit" x="318" y="206" width="6" height="9" rx="1"/><rect class="lit" x="290" y="250" width="6" height="9" rx="1"/><rect class="lit" x="430" y="242" width="6" height="9" rx="1"/><rect class="lit" x="402" y="308" width="6" height="9" rx="1"/><rect class="lit" x="542" y="146" width="6" height="9" rx="1"/><rect class="lit" x="528" y="190" width="6" height="9" rx="1"/><rect class="lit" x="556" y="212" width="6" height="9" rx="1"/><rect class="lit" x="542" y="300" width="6" height="9" rx="1"/><rect class="lit" x="556" y="322" width="6" height="9" rx="1"/><rect class="lit" x="602" y="278" width="6" height="9" rx="1"/><rect class="lit" x="602" y="300" width="6" height="9" rx="1"/><rect class="lit" x="714" y="286" width="6" height="9" rx="1"/><rect class="lit" x="776" y="138" width="6" height="9" rx="1"/><rect class="lit" x="790" y="138" width="6" height="9" rx="1"/><rect class="lit" x="762" y="160" width="6" height="9" rx="1"/><rect class="lit" x="818" y="160" width="6" height="9" rx="1"/><rect class="lit" x="776" y="182" width="6" height="9" rx="1"/><rect class="lit" x="804" y="226" width="6" height="9" rx="1"/><rect class="lit" x="790" y="270" width="6" height="9" rx="1"/><rect class="lit" x="818" y="270" width="6" height="9" rx="1"/><rect class="lit" x="906" y="198" width="6" height="9" rx="1"/><rect class="lit" x="892" y="220" width="6" height="9" rx="1"/><rect class="lit" x="850" y="264" width="6" height="9" rx="1"/><rect class="lit" x="892" y="264" width="6" height="9" rx="1"/><rect class="lit" x="892" y="286" width="6" height="9" rx="1"/><rect class="lit" x="892" y="308" width="6" height="9" rx="1"/><rect class="lit" x="938" y="260" width="6" height="9" rx="1"/><rect class="lit" x="966" y="260" width="6" height="9" rx="1"/><rect class="lit" x="952" y="282" width="6" height="9" rx="1"/><rect class="lit" x="966" y="282" width="6" height="9" rx="1"/><rect class="lit" x="1044" y="250" width="6" height="9" rx="1"/><rect class="lit" x="1044" y="272" width="6" height="9" rx="1"/><rect class="lit" x="1058" y="272" width="6" height="9" rx="1"/><rect class="lit" x="1044" y="294" width="6" height="9" rx="1"/><rect class="lit" x="1058" y="294" width="6" height="9" rx="1"/><rect class="lit" x="1044" y="316" width="6" height="9" rx="1"/><rect class="lit" x="1106" y="256" width="6" height="9" rx="1"/><rect class="lit" x="1120" y="278" width="6" height="9" rx="1"/><rect class="lit" x="1154" y="176" width="6" height="9" rx="1"/><rect class="lit" x="1168" y="176" width="6" height="9" rx="1"/><rect class="lit" x="1196" y="242" width="6" height="9" rx="1"/><rect class="lit" x="1226" y="220" width="6" height="9" rx="1"/><rect class="lit" x="1240" y="220" width="6" height="9" rx="1"/><rect class="lit" x="1226" y="286" width="6" height="9" rx="1"/><rect class="lit" x="1318" y="258" width="6" height="9" rx="1"/><rect class="lit" x="1362" y="176" width="6" height="9" rx="1"/><rect class="lit" x="1404" y="242" width="6" height="9" rx="1"/><rect class="lit" x="1376" y="308" width="6" height="9" rx="1"/></g></svg></section>
<main id="content" class="home">
<section class="section"><div class="wrap wide">
<p class="eyebrow">What’s in it</p>
<h2>One layover, a few taps.</h2>
<p class="intro">Add where you are. See who else is there and what they’re up for. Go.</p>
<div class="grid three">
<div class="card"><span class="ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3.5" y="5" width="17" height="15" rx="3"/><path d="M3.5 10h17M8 3v4M16 3v4"/></svg></span><strong>Meet</strong>Add a layover: city and dates. See how many crew overlap you, then who, from 2 days out. Today and every trip ahead in one place.</div>
<div class="card"><span class="ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.3 5.3l1.4 1.4M17.3 17.3l1.4 1.4M5.3 18.7l1.4-1.4M17.3 6.7l1.4-1.4"/></svg></span><strong>Up for today</strong>Coffee, a run, dinner, a night out. Say it once; it shows on your row until midnight.</div>
<div class="card"><span class="ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8.5" r="3.2"/><path d="M3 19.5c.6-3.3 3-5 6-5s5.4 1.7 6 5"/><circle cx="17" cy="9.5" r="2.6"/><path d="M16.5 14.6c2.4.2 4 1.8 4.5 4.4"/></svg></span><strong>Meetups and events</strong>Post one, join one, chat with the group. Women-only, your airline only, pilots or cabin crew only: your call.</div>
<div class="card"><span class="ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11Z"/><circle cx="12" cy="10" r="2.3"/></svg></span><strong>Crew tips</strong>Per city, from crew who have been there. The run route, the 24-hour place, the thing only crew know.</div>
<div class="card"><span class="ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4.5" y="10.5" width="15" height="10" rx="2.5"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5"/></svg></span><strong>Chats only you can read</strong>Every message is end-to-end encrypted on your phone. We can’t read them. <a href="/private/">How it works</a></div>
<div class="card"><span class="ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3l18 18M10.6 5.1A9.6 9.6 0 0 1 12 5c5 0 8.5 4.2 9.5 7-.4 1.1-1.2 2.4-2.3 3.6M6.4 6.5C4.4 7.8 3 9.8 2.5 12c1 2.8 4.5 7 9.5 7 1.7 0 3.2-.5 4.5-1.2"/><path d="M9.9 9.9a3 3 0 0 0 4.2 4.2"/></svg></span><strong>Nothing public</strong>No search, no directory, no map. Your stay is visible only to verified crew in the same city, on the same dates, from 2 days out.</div>
</div></div></section>
<section class="section band"><div class="wrap wide">
<p class="eyebrow">How invites work</p>
<h2>Plans, not pickup lines.</h2>
<p class="intro">A private chat comes out of a shared plan, never out of a photo.</p>
<div class="grid">
<div class="card"><span class="num">1</span><strong>Everyone here is verified crew</strong>A person checks every account before it can see anyone.</div>
<div class="card"><span class="num">2</span><strong>Invites are plans, not messages</strong>Dinner, a run, coffee, and a time. No text. They tap yes or not now, and nobody hears about a not now.</div>
<div class="card"><span class="num">3</span><strong>Only crew who’ve landed can invite you</strong>Invites start off. Switch them on and, by default, only crew in your city can send one. Their phone checks the city; we never get anyone’s location.</div>
<div class="card"><span class="num">4</span><strong>Women-only events, one tap</strong>Post one or join one. Only women see it.</div>
</div></div></section>
<section class="section closing"><div class="wrap">
<h2>See you on the layover.</h2>
<p>Pilots and cabin crew of any airline, 18+. Coming to the App Store and Google Play in December 2026.</p>
<div class="actions"><a class="btn" href="/verification/">How verification works</a><a class="btn ghost" href="/safety/">Meeting safely</a></div>
</div></section>
</main>'''

def page(md_text, meta):
    body = markdown.markdown(md_text, extensions=['tables'])
    if meta.get('hero'):
        content = HERO
    else:
        content = f'<main id="content"><div class="wrap">{body}</div></main>'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{meta["title"]}</title><meta name="description" content="{meta.get("description","")}">
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
