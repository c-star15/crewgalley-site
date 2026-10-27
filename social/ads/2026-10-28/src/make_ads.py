"""Galley ads, activities series (28 Oct 2026): writes the 14 editable artboards.

python3 make_ads.py            -> ../src/*.dc.html (the canvas sources)
Each ad is one plan from the app: a big headline, a top-down sketch of the plan
(a dot is a person, a dashed ring is an open spot) and the app's light-mode
ActivityCard (app/src/components/activity-card.tsx, light palette in theme.ts),
scaled up. Icons are the app's Ionicons, from the npm package `ionicons`.
Every card carries an "Illustration" label just above it, right-aligned (Victor,
28 Oct: app mocks never suggest activity that hasn't happened); it is the site's
.mock-label (style.css) scaled for 1080 wide.
"""
import json
import math
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
ICONS = json.loads((HERE / 'ionicons.json').read_text())

INK, AMBER, CREAM, PAGE_INK = '#13213A', '#F2A93B', '#F4EFE6', '#0B1424'
# App light palette (theme.ts ink.light)
APP = dict(surface='#FFFFFF', text='#0B1430', muted='#4A5470', border='#D9DEE8',
           accent='#FFB800', accentText='#0B1430', link='#8A5E00', signalSoft='#FFF3CC')

HEAD_PX = 124   # one headline size for the whole series
S = 2.4         # card scale: app points -> px
# The site's .mock-label colour (--hero-soon), light and dark
LABEL_FG = dict(cream='#4A5468', ink='#B7C0D1')

ADS = [
    dict(n=1, key='yoga', bg='ink', head=['Stretch out', 'the night flight.'], title='Sunrise yoga',
         when='Sat', time='06:30', where='Kite Beach', icon='body-outline', rule='up_to', n_in=5, max=8,
         caption='Sunrise yoga with crew who are off when you are.', tag='#yogadubai',
         alt_card='Sunrise yoga, Sat 06:30 at Kite Beach, 5 of 8 in', alt_sketch='eight yoga mats by the sea, five taken'),
    dict(n=2, key='run', bg='cream', head=['5 km before', 'the heat.'], title='Morning run',
         when='Tue', time='06:00', where='Dubai Marina', icon='footsteps-outline', rule='up_to', n_in=4, max=6,
         caption='Off on a Tuesday? So is your running crew.', tag='#runningdubai',
         alt_card='Morning run, Tue 06:00 at Dubai Marina, 4 of 6 in', alt_sketch='four runners on a loop by the water, two spots open'),
    dict(n=3, key='live-music', bg='ink', head=['Off tonight?', "There's a band."], title='Live music',
         when='Thu', time='21:00', where='Al Quoz', icon='musical-notes-outline', rule='min', n_in=3, max=3,
         caption='Live music, a good table and crew who get your hours.', tag='#livemusicdubai',
         alt_card='Live music, Thu 21:00 in Al Quoz, open to anyone, 3 going', alt_sketch='a stage and a table for six, three seats taken'),
    dict(n=4, key='coffee', bg='cream', head=['Red-eye in.', 'Flat white out.'], title='Coffee',
         when='Today', time='10:30', where='Jumeirah', icon='cafe-outline', rule='up_to', n_in=2, max=4,
         caption='Coffee after a red-eye hits different with company.', tag='#coffeedubai',
         alt_card='Coffee, today 10:30 in Jumeirah, 2 of 4 in', alt_sketch='a café table for four, two people with cups'),
    dict(n=5, key='beach', bg='ink', head=['Beach day.', 'Bring crew.'], title='Beach & swim',
         when='Fri', time='16:00', where='Kite Beach', icon='sunny-outline', rule='min', n_in=6, max=6,
         caption="Sea, sun and a plan that's already made.", tag='#dubaibeach',
         alt_card='Beach & swim, Fri 16:00 at Kite Beach, open to anyone, 6 going', alt_sketch='six people round a parasol by the waves'),
    dict(n=6, key='day-trip', bg='cream', head=['Two days off.', 'One road trip.'], title='Day trip',
         when='Sun', time='07:00', where='Hatta', icon='trail-sign-outline', rule='up_to', n_in=4, max=5,
         caption='Mountains, kayaks and a car full of crew.', tag='#hatta',
         alt_card='Day trip, Sun 07:00 to Hatta, 4 of 5 in', alt_sketch='a car on the road to the mountains, four seats taken'),
    dict(n=7, key='study', bg='ink', head=['Recurrent', 'next week?', 'Study together.'], title='Study session',
         when='Wed', time='14:00', where='Al Quoz', icon='book-outline', rule='up_to', n_in=3, max=4,
         caption="Recurrent's easier with a study buddy. Pilots and cabin crew.", tag='#crewtraining',
         alt_card='Study session, Wed 14:00 in Al Quoz, 3 of 4 in', alt_sketch='a study table for four, three with open books'),
]


def px(v):
    v = round(v, 1)
    return f'{int(v)}px' if v == int(v) else f'{v}px'


# ---------------------------------------------------------------------------
# The app's ActivityCard, light mode, scaled by S
# ---------------------------------------------------------------------------
def card(a, width=888):
    meta = ' · '.join(x for x in [a['when'], a['time'], a['where'], 'Anyone' if a['rule'] == 'min' else None] if x)
    icon = ICONS[a['icon']].replace('currentColor', APP['link'])
    dots = []
    for i in range(a['max']):
        if i < a['n_in']:
            dots.append(f'<span style="width: {px(7*S)}; height: {px(7*S)}; border-radius: {px(4*S)}; background: {APP["link"]}"></span>')
        else:
            dots.append(f'<span style="width: {px(7*S)}; height: {px(7*S)}; box-sizing: border-box; border-radius: {px(4*S)}; border: {px(1.5*S)} solid {APP["border"]}"></span>')
    spots = f'{a["n_in"]} going' if a['rule'] == 'min' else f'{a["n_in"]} of {a["max"]}'
    return f'''<div style="width: {px(width)}; box-sizing: border-box; display: flex; align-items: center; gap: {px(16*S)}; padding: {px(14*S)} {px(16*S)}; border-radius: {px(16*S)}; background: {APP['surface']}; color: {APP['text']}">
      <div style="flex: 0 0 auto; width: {px(44*S)}; height: {px(44*S)}; border-radius: {px(22*S)}; background: {APP['signalSoft']}; display: flex; align-items: center; justify-content: center"><svg width="{round(22*S,1)}" height="{round(22*S,1)}" viewBox="0 0 512 512" aria-hidden="true">{icon}</svg></div>
      <div style="flex: 1 1 auto; min-width: 0; display: flex; flex-direction: column; gap: {px(3*S)}">
        <span style="font-size: {px(17*S)}; line-height: 1.2; font-weight: 700; color: {APP['text']}">{a['title'].replace('&', '&amp;')}</span>
        <span style="font-size: {px(14*S)}; line-height: 1.25; font-weight: 400; color: {APP['muted']}">{meta}</span>
      </div>
      <div style="flex: 0 0 auto; min-width: {px(64*S)}; display: flex; flex-direction: column; align-items: flex-end; gap: {px(8*S)}">
        <button type="button" style="min-width: {px(64*S)}; height: {px(32*S)}; box-sizing: border-box; margin: 0; padding: 0 {px(14*S)}; border: 0; border-radius: 999px; background: {APP['accent']}; color: {APP['accentText']}; font-family: inherit; font-size: {px(15*S)}; font-weight: 800; display: flex; align-items: center; justify-content: center">Join</button>
        <span style="display: flex; gap: {px(3*S)}" role="img" aria-label="{spots}">{''.join(dots)}</span>
      </div>
    </div>'''


def mock_label(bg):
    """The site's .mock-label at 1080 wide: sits 20 px above its (positioned) parent, right-aligned."""
    return (f'<span style="position: absolute; right: 0; bottom: 100%; margin-bottom: 20px; padding: 8px 20px 8px 22px; '
            f'border: 2px solid currentColor; border-radius: 999px; font-size: 24px; font-weight: 700; line-height: 1.1; '
            f'letter-spacing: 0.08em; text-transform: uppercase; white-space: nowrap; color: {LABEL_FG[bg]}; opacity: 0.75">Illustration</span>')


# ---------------------------------------------------------------------------
# Wordmark: lowercase galley, Inter Black, the pin as its full stop
# ---------------------------------------------------------------------------
def wordmark(fg, size=64):
    return (f'<span style="font-size: {px(size)}; font-weight: 900; letter-spacing: -0.065em; line-height: 1; '
            f'white-space: nowrap; color: {fg}; font-variation-settings: \'opsz\' 32">galley'
            f'<svg viewBox="-60.7 -92.1 61.7 92.1" aria-hidden="true" style="display: inline-block; vertical-align: -0.2em; '
            f'height: 0.5em; width: 0.335em; margin-left: 0.08em; overflow: visible">'
            f'<path d="M-33.25 -68.40 L-38.11 -65.81 L0 0Z" fill="{fg}"></path>'
            f'<circle cx="-35.68" cy="-67.1" r="24" fill="{AMBER}"></circle></svg></span>')


# ---------------------------------------------------------------------------
# Plan sketches, seen from above, in an 888 x 400 box
# person = solid dot, open spot = dashed ring, lines faint
# ---------------------------------------------------------------------------
R = 24  # person dot radius


def person(x, y, fg):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{R}" fill="{fg}"></circle>'


def open_spot(x, y, fg):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{R-2}" fill="none" stroke="{fg}" stroke-opacity="0.55" '
            f'stroke-width="4" stroke-dasharray="7 7.5"></circle>')


def lines(fg, op=0.32, w=4):
    return f'fill="none" stroke="{fg}" stroke-opacity="{op}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'


def wave(y, x0, x1, amp, period, phase=0.0):
    pts = []
    n = int((x1 - x0) / 6)
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        pts.append(f'{x:.1f} {y + amp * math.sin((x - x0) / period * 2 * math.pi + phase):.1f}')
    return 'M' + ' L'.join(pts)


def sk_yoga(fg):
    out = [f'<path d="{wave(26, 20, 868, 9, 148)}" {lines(fg, 0.3)}></path>',
           f'<path d="{wave(62, 20, 868, 9, 148, 1.2)}" {lines(fg, 0.18)}></path>']
    mw, mh, gap = 78, 236, 30
    x0 = (888 - (8 * mw + 7 * gap)) / 2
    open_at = {2, 6, 7}
    for i in range(8):
        x = x0 + i * (mw + gap)
        out.append(f'<rect x="{x:.1f}" y="128" width="{mw}" height="{mh}" rx="14" fill="{fg}" fill-opacity="0.06" stroke="{fg}" stroke-opacity="0.32" stroke-width="4"></rect>')
        cx, cy = x + mw / 2, 128 + 54
        out.append(open_spot(cx, cy, fg) if i in open_at else person(cx, cy, fg))
    return out


def sk_run(fg):
    # a loop round the water; four running single file, two spots open behind them
    x0, x1, cy, r = 214, 674, 200, 128
    loop = f'M {x0} {cy - r} H {x1} A {r} {r} 0 0 1 {x1} {cy + r} H {x0} A {r} {r} 0 0 1 {x0} {cy - r} Z'
    out = [f'<path d="{loop}" {lines(fg, 0.3, 6)}></path>',
           f'<path d="{wave(176, 250, 638, 7, 96)}" {lines(fg, 0.16)}></path>',
           f'<path d="{wave(220, 290, 598, 7, 96, 1.6)}" {lines(fg, 0.1)}></path>']
    # start and finish
    out.append(f'<line x1="704" y1="{cy + r - 34}" x2="704" y2="{cy + r + 34}" {lines(fg, 0.5, 6)}></line>')
    for x, kind in [(296, 'o'), (366, 'o'), (436, 'p'), (506, 'p'), (576, 'p'), (646, 'p')]:
        out.append(person(x, cy + r, fg) if kind == 'p' else open_spot(x, cy + r, fg))
    return out


def sk_live(fg):
    out = []
    # the stage from above: a drum kit and a keyboard
    out.append(f'<rect x="164" y="6" width="560" height="146" rx="20" fill="{fg}" fill-opacity="0.07" stroke="{fg}" stroke-opacity="0.34" stroke-width="4"></rect>')
    kit = [(392, 98, 21), (428, 54, 17), (470, 54, 17), (508, 100, 25)]
    for x, y, rr in kit:
        out.append(f'<circle cx="{x}" cy="{y}" r="{rr}" fill="none" stroke="{fg}" stroke-opacity="0.42" stroke-width="4"></circle>')
    for x, y in [(352, 52), (552, 46)]:
        out.append(f'<circle cx="{x}" cy="{y}" r="28" fill="none" stroke="{fg}" stroke-opacity="0.26" stroke-width="3"></circle>')
        out.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{fg}" fill-opacity="0.42"></circle>')
    out.append(f'<rect x="590" y="70" width="104" height="40" rx="4" fill="none" stroke="{fg}" stroke-opacity="0.42" stroke-width="4"></rect>')
    keys = ' '.join(f'M {602 + 10*i} 72 V 96' for i in range(9))
    out.append(f'<path d="{keys}" {lines(fg, 0.3, 3)}></path>')
    out.append(f'<rect x="200" y="58" width="74" height="52" rx="6" fill="none" stroke="{fg}" stroke-opacity="0.42" stroke-width="4"></rect>')
    out.append(f'<circle cx="237" cy="84" r="15" fill="none" stroke="{fg}" stroke-opacity="0.3" stroke-width="3"></circle>')
    # a table for six in front of it, three in
    cx, cy, tr = 444, 306, 64
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{tr}" fill="{fg}" fill-opacity="0.06" stroke="{fg}" stroke-opacity="0.32" stroke-width="4"></circle>')
    for k in range(6):
        ang = math.radians(-90 + 30 + k * 60)
        x, y = cx + 112 * math.cos(ang), cy + 112 * math.sin(ang)
        out.append(person(x, y, fg) if k in (0, 4, 5) else open_spot(x, y, fg))
    return out


def sk_coffee(fg):
    cx, cy, tr = 444, 200, 128
    out = [f'<circle cx="{cx}" cy="{cy}" r="{tr}" fill="{fg}" fill-opacity="0.06" stroke="{fg}" stroke-opacity="0.32" stroke-width="4"></circle>']
    seats = [(180, 'p'), (-90, 'p'), (0, 'o'), (90, 'o')]
    for ang, kind in seats:
        a = math.radians(ang)
        x, y = cx + 186 * math.cos(a), cy + 186 * math.sin(a)
        if kind == 'p':
            out.append(person(x, y, fg))
            ux, uy = cx + 76 * math.cos(a), cy + 76 * math.sin(a)
            out.append(f'<circle cx="{ux:.1f}" cy="{uy:.1f}" r="24" fill="none" stroke="{fg}" stroke-opacity="0.34" stroke-width="4"></circle>')
            out.append(f'<circle cx="{ux:.1f}" cy="{uy:.1f}" r="12" fill="{fg}" fill-opacity="0.34"></circle>')
        else:
            out.append(open_spot(x, y, fg))
    return out


def sk_beach(fg):
    out = [f'<path d="{wave(22, 0, 888, 10, 160)}" {lines(fg, 0.34)}></path>',
           f'<path d="{wave(58, 0, 888, 10, 160, 1.4)}" {lines(fg, 0.22)}></path>',
           f'<path d="{wave(94, 0, 888, 10, 160, 2.8)}" {lines(fg, 0.12)}></path>']
    # parasol from above
    ux, uy, ur = 444, 262, 74
    poly = ' '.join(f'{ux + ur*math.cos(math.radians(22.5 + 45*k)):.1f},{uy + ur*math.sin(math.radians(22.5 + 45*k)):.1f}' for k in range(8))
    out.append(f'<polygon points="{poly}" fill="{fg}" fill-opacity="0.08" stroke="{fg}" stroke-opacity="0.34" stroke-width="4" stroke-linejoin="round"></polygon>')
    for k in range(8):
        a = math.radians(22.5 + 45 * k)
        out.append(f'<line x1="{ux}" y1="{uy}" x2="{ux + ur*math.cos(a):.1f}" y2="{uy + ur*math.sin(a):.1f}" {lines(fg, 0.24, 3)}></line>')
    spots = [(250, 210, 'p'), (230, 318, 'p'), (330, 372, 'p'), (558, 372, 'p'), (658, 318, 'p'), (638, 210, 'p'), (130, 270, 'o'), (758, 270, 'o')]
    for x, y, k in spots:
        out.append(person(x, y, fg) if k == 'p' else open_spot(x, y, fg))
    return out


def sk_trip(fg):
    out = []
    # contour lines: the mountains (a topo map)
    def blob(cx, cy, r, k, seed):
        pts = []
        for i in range(73):
            t = i / 72 * 2 * math.pi
            rr = r * (1 + 0.12 * math.sin(3 * t + seed) + 0.07 * math.sin(5 * t + seed * 2) * k)
            pts.append(f'{cx + rr * math.cos(t) * 1.5:.1f} {cy + rr * math.sin(t):.1f}')
        return 'M' + ' L'.join(pts) + 'Z'
    for i, r in enumerate([92, 68, 45, 22]):
        out.append(f'<path d="{blob(690 + i*8, 96 - i*4, r, 1 - i*0.2, 0.7)}" {lines(fg, 0.16 + i*0.07, 4)}></path>')
    for i, r in enumerate([54, 32, 12]):
        out.append(f'<path d="{blob(520 + i*4, 40 + i*2, r, 1, 2.1)}" {lines(fg, 0.14 + i*0.08, 4)}></path>')
    # the road, curving up towards the hills
    out.append(f'<path d="M 0 300 C 250 300 420 270 560 196 S 760 120 888 128" {lines(fg, 0.3, 4)}></path>')
    out.append(f'<path d="M 0 364 C 262 364 444 334 592 254 S 782 186 888 192" {lines(fg, 0.3, 4)}></path>')
    out.append(f'<path d="M 0 332 C 256 332 432 302 576 225 S 771 153 888 160" {lines(fg, 0.3, 4)} stroke-dasharray="18 22"></path>')
    # the car, from above: five seats, four in
    car_fill = CREAM if fg == INK else INK
    out.append(f'<g transform="translate(236 330) rotate(-4)">'
               f'<rect x="-168" y="-88" width="336" height="176" rx="54" fill="{car_fill}" stroke="{fg}" stroke-opacity="0.55" stroke-width="5"></rect>'
               f'<path d="M 92 -66 Q 110 0 92 66" {lines(fg, 0.4, 4)}></path>'
               f'<path d="M -138 -58 Q -150 0 -138 58" {lines(fg, 0.3, 4)}></path>'
               + person(46, -36, fg) + person(46, 36, fg)
               + person(-74, -56, fg) + person(-74, 0, fg) + open_spot(-74, 56, fg)
               + '</g>')
    return out


def sk_study(fg):
    out = []
    tx, ty, tw, th = 234, 120, 420, 176
    out.append(f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="18" fill="{fg}" fill-opacity="0.06" stroke="{fg}" stroke-opacity="0.32" stroke-width="4"></rect>')
    seats = [(339, ty - 52, 'p', 'down'), (549, ty - 52, 'p', 'down'), (339, ty + th + 52, 'p', 'up'), (549, ty + th + 52, 'o', 'up')]
    for x, y, k, face in seats:
        if k == 'p':
            out.append(person(x, y, fg))
            by = ty + 22 if face == 'down' else ty + th - 22 - 52
            # an open book: two pages
            out.append(f'<path d="M {x} {by + 4} L {x} {by + 52} M {x - 46} {by} L {x} {by + 6} L {x + 46} {by} L {x + 46} {by + 48} L {x} {by + 54} L {x - 46} {by + 48} Z" {lines(fg, 0.38, 4)}></path>')
        else:
            out.append(open_spot(x, y, fg))
    return out


SKETCH = {'yoga': sk_yoga, 'run': sk_run, 'live-music': sk_live, 'coffee': sk_coffee,
          'beach': sk_beach, 'day-trip': sk_trip, 'study': sk_study}
SKETCH_ALT = {
    'yoga': 'Eight yoga mats in a row by the sea, five with someone on them, three open',
    'run': 'A running route with five kilometre marks, four runners together and two open spots',
    'live-music': 'A stage and a table for six in front of it, three seats taken and three open',
    'coffee': 'A café table for four from above, two people with cups and two open seats',
    'beach': 'A beach from above: waves, a parasol, six people around it and two open spots',
    'day-trip': 'A car on a road towards the mountains, four seats taken and one open',
    'study': 'A study table for four, three people with open books and one open seat',
}


def sketch(a, fg, x, y, scale=1.0):
    body = '\n      '.join(SKETCH[a['key']](fg))
    tr = f'translate({x} {y})' + (f' scale({scale})' if scale != 1 else '')
    return (f'<svg width="1080" height="{1440 if True else 0}" viewBox="0 0 1080 1440" role="img" aria-label="{SKETCH_ALT[a["key"]]}" '
            f'style="position: absolute; left: 0; top: 0"><g transform="{tr}">\n      {body}\n    </g></svg>')


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def page(a, fmt):
    w, h = (1080, 1440) if fmt == 'post' else (1080, 1920)
    ink = a['bg'] == 'ink'
    bg, fg = (INK, CREAM) if ink else (CREAM, INK)
    lines_n = len(a['head'])
    head = '<br>'.join(a['head'])
    if fmt == 'post':
        head_top = 120
        head_bottom = head_top + lines_n * HEAD_PX * 0.95
        card_top = 990
        sk_top = (head_bottom + card_top) / 2 - 200 + 4
        wm_bottom = 112
    else:
        head_top = 300
        head_bottom = head_top + lines_n * HEAD_PX * 0.95
        card_top = 1236
        sk_top = (head_bottom + card_top) / 2 - 200 + 4
        wm_bottom = 362
    svg = sketch(a, fg, 96, round(sk_top), 1.0).replace('height="1440" viewBox="0 0 1080 1440"', f'height="{h}" viewBox="0 0 1080 {h}"')
    title = f'Ad {a["n"]} · {a["title"]} · {"post 3:4" if fmt == "post" else "story 9:16"}'
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title.replace('&', '&amp;')}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400..900&amp;display=swap" rel="stylesheet">
<style>
body{{margin:0}}
</style>
</helmet>
<div style="position: relative; width: {w}px; height: {h}px; overflow: hidden; background: {bg}; color: {fg}; font-family: Inter, system-ui, sans-serif">
  <p style="position: absolute; left: 96px; top: {head_top}px; margin: 0; font-size: {HEAD_PX}px; font-weight: 900; letter-spacing: -0.045em; word-spacing: 0.04em; line-height: 0.95; white-space: nowrap">{head}</p>
  {svg}
  <div style="position: absolute; left: 96px; top: {card_top}px">
    {mock_label(a['bg'])}
    {card(a)}
  </div>
  <div style="position: absolute; left: 96px; bottom: {wm_bottom}px">{wordmark(fg)}</div>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
class Component extends DCLogic {{
  renderVals() {{
    return {{}};
  }}
}}
</script>
</body>
</html>
'''


HASHTAGS = '#crewlife #cabincrew #pilotlife #dubai'


def caption(a):
    return f"{a['caption']}\n\n{HASHTAGS} {a['tag']}"


def alt_text(a):
    head = ' '.join(a['head'])
    return f"Galley ad: \"{head}\" over an illustration of the app's plan card: {a['alt_card']}, with a Join button. Sketch: {a['alt_sketch']}."


def stem(a, fmt):
    return f'ad-{a["n"]}-{a["key"]}-{fmt}'


if __name__ == '__main__':
    import sys
    if sys.argv[1:] == ['--posts']:  # what goes to the scheduler
        print(json.dumps([dict(file=f'{stem(a, "post")}.jpg', caption=caption(a), alt=alt_text(a)) for a in ADS], indent=1, ensure_ascii=False))
        raise SystemExit
    for a in ADS:
        for fmt in ('post', 'story'):
            (HERE / f'{stem(a, fmt)}.dc.html').write_text(page(a, fmt))
    print('wrote', len(ADS) * 2, 'artboards')
