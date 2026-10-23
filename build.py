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
header = (root / '_header.html').read_text()
footer = (root / '_footer.html').read_text()

HERO = '''<section class="hero"><div class="wrap">
<h1>New city. Free day.<br>Find your people.</h1>
<p>Your crew has other plans? Galley shows pilots and cabin crew from any airline on a layover in the same city, up for the same thing. One tap to meet up. Every account is checked by a person before it can see anyone, and every message is end-to-end encrypted.</p>
<a class="btn" href="/verification/">How verification works</a><a class="btn secondary" href="/private/">Private by design</a>
</div></section>
<main><div class="wrap">
<div class="grid">
<div class="card"><strong>Now and Later</strong>Add a stay: city, arrival, departure. See every verified crew member whose dates overlap yours, and nobody else.</div>
<div class="card"><strong>Up for today</strong>Coffee, a run, dinner, a night out. Say it once; it shows on your row until midnight.</div>
<div class="card"><strong>Meetups and events</strong>Post one, join one, chat with the group. Women-only, your airline only, pilots or cabin crew only: your call.</div>
<div class="card"><strong>Crew tips</strong>Per city, from crew who have been there. The run route, the 24-hour place, the thing only crew know.</div>
<div class="card"><strong>Chats only you can read</strong>Every message is end-to-end encrypted on your phone. We can't read them. <a href="/private/">How it works</a></div>
<div class="card"><strong>Nothing public</strong>No search, no directory, no map. Your stay is visible only to verified crew in the same city, on the same dates, from 2 days out.</div>
</div>
<h2>Plans, not pickup lines.</h2>
<div class="grid">
<div class="card"><strong>Everyone here is verified crew</strong>A person checks every account before it can see anyone.</div>
<div class="card"><strong>Invites are plans, not messages</strong>Dinner, a run, coffee, and a time. No text. They tap yes or not now, and nobody hears about a not now.</div>
<div class="card"><strong>Only crew who've landed can invite you</strong>Invites start off. Switch them on and, by default, only crew in your city can send one. Their phone checks the city; we never get anyone's location.</div>
<div class="card"><strong>Women-only events, one tap</strong>Post one or join one. Only women see it.</div>
</div>
<p class="meta">Pilots and cabin crew of any airline, 18+. Coming to the App Store and Google Play in December 2026.</p>
</div></main>'''

def page(md_text, meta):
    body = markdown.markdown(md_text, extensions=['tables'])
    if meta.get('hero'):
        content = HERO
    else:
        content = f'<main><div class="wrap">{body}</div></main>'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{meta["title"]}</title><meta name="description" content="{meta.get("description","")}">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" href="/icon.png" type="image/png"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><meta name="theme-color" content="#0B1424"><link rel="stylesheet" href="/style.css"></head><body>
{header}{content}{footer}</body></html>'''

for f in sorted(src.glob('*.md')):
    text = f.read_text()
    m = re.match(r'---\n(.*?)\n---\n?(.*)', text, re.S)
    meta = dict(line.split(': ', 1) for line in m.group(1).splitlines() if ': ' in line)
    meta['hero'] = meta.get('hero') == 'true'
    html = page(m.group(2), meta)
    out = dist / 'index.html' if f.stem == 'index' else dist / f.stem / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print('built', out.relative_to(dist))

(dist / 'CNAME').write_text('crewgalley.app\n')
(dist / '.nojekyll').write_text('')
# .well-known for later universal links; harmless now
wk = dist / '.well-known'; wk.mkdir()
(wk / 'apple-app-site-association').write_text('{"applinks":{"apps":[],"details":[]}}')
