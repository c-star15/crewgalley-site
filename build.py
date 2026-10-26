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
<p class="eyebrow">By crew, for crew · any airline</p>
<h1>Find your people.<br><em>At base and away.</em></h1>
<p class="lead">Off on a Tuesday? So are plenty of crew at your base. Mark your free days and join padel, coffee, a run or a study session with pilots and cabin crew. On a layover, find crew in town too.</p>
<ul class="trust"><li><strong>Verified crew only.</strong> Every account is checked before it can see anyone.</li></ul>
<div class="actions"><a class="btn" href="#how">See how it works</a><a class="btn secondary" href="/verification/">How we check crew</a></div>
<p class="soon">Coming to the App Store and Google Play in December 2026.</p>
</div><svg class="skyline" viewBox="0 0 1440 340" preserveAspectRatio="xMidYMax slice" aria-hidden="true"><g class="far"><rect x="-20" y="120" width="90" height="230"/><rect x="70" y="120" width="90" height="230"/><rect x="190" y="170" width="90" height="180"/><rect x="310" y="170" width="120" height="180"/><rect x="430" y="170" width="90" height="180"/><rect x="530" y="80" width="90" height="270"/><rect x="630" y="200" width="90" height="150"/><rect x="720" y="80" width="60" height="270"/><rect x="810" y="80" width="90" height="270"/><rect x="900" y="80" width="60" height="270"/><rect x="990" y="80" width="90" height="270"/><rect x="1080" y="170" width="60" height="180"/><rect x="1140" y="200" width="60" height="150"/><rect x="1230" y="80" width="120" height="270"/><rect x="1350" y="200" width="120" height="150"/></g><g class="near"><rect x="0" y="244" width="66" height="106" rx="3"/><rect x="72" y="60" width="98" height="290" rx="3"/><rect x="176" y="220" width="98" height="130" rx="3"/><rect x="280" y="190" width="58" height="160" rx="3"/><rect x="344" y="20" width="42" height="330" rx="3"/><rect x="392" y="160" width="58" height="190" rx="3"/><rect x="456" y="100" width="42" height="250" rx="3"/><rect x="504" y="130" width="82" height="220" rx="3"/><rect x="592" y="20" width="42" height="330" rx="3"/><rect x="640" y="130" width="58" height="220" rx="3"/><rect x="704" y="270" width="42" height="80" rx="3"/><rect x="752" y="100" width="82" height="250" rx="3"/><rect x="840" y="160" width="82" height="190" rx="3"/><rect x="928" y="244" width="58" height="106" rx="3"/><rect x="992" y="190" width="98" height="160" rx="3"/><rect x="1096" y="130" width="42" height="220" rx="3"/><rect x="1144" y="160" width="66" height="190" rx="3"/><rect x="1216" y="160" width="58" height="190" rx="3"/><rect x="1280" y="220" width="66" height="130" rx="3"/><rect x="1352" y="160" width="98" height="190" rx="3"/></g><g class="lights"><rect class="lit" x="10" y="260" width="6" height="9" rx="1"/><rect class="lit" x="38" y="282" width="6" height="9" rx="1"/><rect class="lit" x="38" y="304" width="6" height="9" rx="1"/><rect class="lit" x="52" y="326" width="6" height="9" rx="1"/><rect class="lit" x="82" y="76" width="6" height="9" rx="1"/><rect class="lit" x="82" y="120" width="6" height="9" rx="1"/><rect class="lit" x="96" y="120" width="6" height="9" rx="1"/><rect class="lit" x="152" y="186" width="6" height="9" rx="1"/><rect class="lit" x="96" y="252" width="6" height="9" rx="1"/><rect class="lit" x="124" y="274" width="6" height="9" rx="1"/><rect class="lit" x="96" y="296" width="6" height="9" rx="1"/><rect class="lit" x="96" y="318" width="6" height="9" rx="1"/><rect class="lit" x="242" y="236" width="6" height="9" rx="1"/><rect class="lit" x="200" y="258" width="6" height="9" rx="1"/><rect class="lit" x="304" y="206" width="6" height="9" rx="1"/><rect class="lit" x="318" y="206" width="6" height="9" rx="1"/><rect class="lit" x="290" y="250" width="6" height="9" rx="1"/><rect class="lit" x="430" y="242" width="6" height="9" rx="1"/><rect class="lit" x="402" y="308" width="6" height="9" rx="1"/><rect class="lit" x="542" y="146" width="6" height="9" rx="1"/><rect class="lit" x="528" y="190" width="6" height="9" rx="1"/><rect class="lit" x="556" y="212" width="6" height="9" rx="1"/><rect class="lit" x="542" y="300" width="6" height="9" rx="1"/><rect class="lit" x="556" y="322" width="6" height="9" rx="1"/><rect class="lit" x="602" y="278" width="6" height="9" rx="1"/><rect class="lit" x="602" y="300" width="6" height="9" rx="1"/><rect class="lit" x="714" y="286" width="6" height="9" rx="1"/><rect class="lit" x="776" y="138" width="6" height="9" rx="1"/><rect class="lit" x="790" y="138" width="6" height="9" rx="1"/><rect class="lit" x="762" y="160" width="6" height="9" rx="1"/><rect class="lit" x="818" y="160" width="6" height="9" rx="1"/><rect class="lit" x="776" y="182" width="6" height="9" rx="1"/><rect class="lit" x="804" y="226" width="6" height="9" rx="1"/><rect class="lit" x="790" y="270" width="6" height="9" rx="1"/><rect class="lit" x="818" y="270" width="6" height="9" rx="1"/><rect class="lit" x="906" y="198" width="6" height="9" rx="1"/><rect class="lit" x="892" y="220" width="6" height="9" rx="1"/><rect class="lit" x="850" y="264" width="6" height="9" rx="1"/><rect class="lit" x="892" y="264" width="6" height="9" rx="1"/><rect class="lit" x="892" y="286" width="6" height="9" rx="1"/><rect class="lit" x="892" y="308" width="6" height="9" rx="1"/><rect class="lit" x="938" y="260" width="6" height="9" rx="1"/><rect class="lit" x="966" y="260" width="6" height="9" rx="1"/><rect class="lit" x="952" y="282" width="6" height="9" rx="1"/><rect class="lit" x="966" y="282" width="6" height="9" rx="1"/><rect class="lit" x="1044" y="250" width="6" height="9" rx="1"/><rect class="lit" x="1044" y="272" width="6" height="9" rx="1"/><rect class="lit" x="1058" y="272" width="6" height="9" rx="1"/><rect class="lit" x="1044" y="294" width="6" height="9" rx="1"/><rect class="lit" x="1058" y="294" width="6" height="9" rx="1"/><rect class="lit" x="1044" y="316" width="6" height="9" rx="1"/><rect class="lit" x="1106" y="256" width="6" height="9" rx="1"/><rect class="lit" x="1120" y="278" width="6" height="9" rx="1"/><rect class="lit" x="1154" y="176" width="6" height="9" rx="1"/><rect class="lit" x="1168" y="176" width="6" height="9" rx="1"/><rect class="lit" x="1196" y="242" width="6" height="9" rx="1"/><rect class="lit" x="1226" y="220" width="6" height="9" rx="1"/><rect class="lit" x="1240" y="220" width="6" height="9" rx="1"/><rect class="lit" x="1226" y="286" width="6" height="9" rx="1"/><rect class="lit" x="1318" y="258" width="6" height="9" rx="1"/><rect class="lit" x="1362" y="176" width="6" height="9" rx="1"/><rect class="lit" x="1404" y="242" width="6" height="9" rx="1"/><rect class="lit" x="1376" y="308" width="6" height="9" rx="1"/></g></svg></section>
<main id="content" class="home">
<section class="section how" id="how"><div class="wrap wide">
<p class="eyebrow">How it works</p>
<h2>Plans with crew who are free when you are.</h2>
<ol class="steps">
<li><span class="step-n">01</span><h3>Add free time</h3><p>Only when you feel like doing something. Your free time stays private; you pick who sees what you’re up for.</p></li>
<li><span class="step-n">02</span><h3>Join a club</h3><p>Padel, running, coffee, gym, studying and more. Each base has its own, like Dubai Padel Club. See who’s in and ask anything in its forum.</p></li>
<li><span class="step-n">03</span><h3>Show up</h3><p>Join a plan with a spot left, or start one in four taps: what, when, where, how many.</p></li>
</ol>
</div></section>
<section class="section band"><div class="wrap wide">
<p class="eyebrow">Meeting new people</p>
<h2>Easy to say yes. Easy to say no.</h2>
<p class="intro">Galley is built around plans, not profiles, so meeting someone new feels relaxed for everyone.</p>
<div class="grid">
<div class="card"><span class="num">1</span><strong>Everyone is verified crew</strong>Galley checks every account before it can see anyone else.</div>
<div class="card"><span class="num">2</span><strong>Plans, not profiles</strong>At base you see what’s on, and who’s up for something if they chose to show you. Free time itself is never listed.</div>
<div class="card"><span class="num">3</span><strong>Chat inside the plan</strong>Message the group, or anyone in a plan you’ve both joined. Nobody can message you out of the blue. <a class="quiet" href="/private/">Chats are end-to-end encrypted</a>.</div>
<div class="card"><span class="num">4</span><strong>Women-only plans</strong>Start one or join one. Only women can see them.</div>
</div></div></section>
<section class="section how"><div class="wrap wide">
<p class="eyebrow">On a layover</p>
<h2>Away from base, too.</h2>
<ol class="steps">
<li><span class="step-n">01</span><h3>Add your layover</h3><p>City and dates, two taps. See how many crew will be in town before you land.</p></li>
<li><span class="step-n">02</span><h3>Join the locals</h3><p>Join plans there, from other crew on a layover to a local crew’s morning run.</p></li>
<li><span class="step-n">03</span><h3>You pick who can invite you</h3><p>Invites are off until you turn them on. Then only crew who’ve landed can send one. Their phone checks the city; we never see anyone’s location.</p></li>
</ol>
</div></section>
<section class="section origin"><div class="wrap">
<p class="eyebrow">Made by crew</p>
<h2>Built from the inside.</h2>
<p>Galley was started by a working airline pilot. Crew days off land midweek, rosters change every month, and the group chat never lines up. Galley is the app we wanted: who’s free when you are, what’s on, and good company when you’re away.</p>
</div></section>
<section class="section closing"><div class="wrap">
<h2>See you at base. And away.</h2>
<p>For pilots and cabin crew of any airline, 18+. Coming to the App Store and Google Play in December 2026.</p>
<div class="actions"><a class="btn" href="/verification/">How we check crew</a><a class="btn ghost" href="/safety/">Tips for meeting safely</a></div>
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
