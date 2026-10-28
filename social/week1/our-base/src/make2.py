"""'Boarding soon.' Dubai post: the website's dawn identity, a drawn Dubai skyline in the glyph palette, the Galley pin on the Burj."""
import math, pathlib, random, sys
INK, AMB, CREAM = '#13213A', '#F2A93B', '#F4EFE6'
W, H, G = 1080, 1440, 1150   # G = shoreline
OUT = []
def add(s): OUT.append(s)
DIM = f'fill="{INK}" fill-opacity=".22"'
INKF = f'fill="{INK}"'

def burj_khalifa(cx, h):
    lv = [(0, 56), (.17, 49), (.32, 42), (.46, 35), (.58, 28), (.68, 21), (.77, 15), (.84, 10), (.9, 6)]
    left, right = [], []
    for i, (f, w) in enumerate(lv):
        y0 = G - f * h; y1 = G - (lv[i + 1][0] if i + 1 < len(lv) else .9) * h
        left += [(cx - w, y0), (cx - w, y1)]
        right += [(cx + w, y0), (cx + w, y1)]
    top = G - .9 * h
    pts = left + [(cx - 2.5, top), (cx - 1.6, G - h), (cx + 1.6, G - h), (cx + 2.5, top)] + right[::-1]
    add(f'<path d="M{" L".join(f"{x:.1f} {y:.1f}" for x, y in pts)}Z" {INKF}/>')
    # the core, a cream seam up the middle
    add(f'<path d="M{cx} {G} L{cx} {G - .84 * h}" stroke="{CREAM}" stroke-opacity=".35" stroke-width="3"/>')
    for f in (.17, .32, .46, .58, .68, .77):
        y = G - f * h
        add(f'<path d="M{cx - 30} {y + 14} h60" stroke="{CREAM}" stroke-opacity=".18" stroke-width="2"/>')
    return (cx, G - h)

def burj_al_arab(x0, h):
    add(f'<path d="M{x0 - 26} {G} L{x0 - 12} {G - 22} L{x0 + 96} {G - 22} L{x0 + 110} {G}Z" {DIM}/>')       # island
    add(f'<path d="M{x0} {G - 22} L{x0} {G - h} C{x0 + 70} {G - h * .9} {x0 + 112} {G - h * .5} {x0 + 84} {G - 22}Z" {INKF}/>')   # sail
    for k in range(1, 7):
        y = G - 22 - k * (h - 30) / 7
        t = (G - y) / h
        xr = x0 + 84 + 28 * math.sin(math.pi * min(1, t * 1.05)) - 8
        add(f'<path d="M{x0 + 8} {y:.0f} L{xr - 12:.0f} {y:.0f}" stroke="{CREAM}" stroke-opacity=".26" stroke-width="3"/>')
    add(f'<path d="M{x0 - 12} {G - 22} L{x0 - 12} {G - h - 40}" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>')  # mast
    add(f'<path d="M{x0 - 12} {G - h + 6} L{x0} {G - h + 6} M{x0 - 12} {G - h * .5} L{x0} {G - h * .5}" stroke="{INK}" stroke-width="5"/>')
    add(f'<path d="M{x0 - 12} {G - 10} L{x0 - 140} {G - 4}" stroke="{INK}" stroke-opacity=".3" stroke-width="5"/>')  # causeway

def wind_towers(x0):
    """Al Fahidi houses with barjeel wind towers (heritage, no hotels)."""
    for bx, bw, bh, tx, tw, th in ((x0, 150, 120, x0 + 22, 50, 118), (x0 + 128, 128, 92, x0 + 196, 44, 96)):
        add(f'<rect x="{bx}" y="{G - bh}" width="{bw}" height="{bh}" {INKF}/>')
        for k in range(int(bw // 22)):   # parapet
            add(f'<rect x="{bx + 4 + k * 22}" y="{G - bh - 10}" width="12" height="12" {INKF}/>')
        add(f'<rect x="{tx}" y="{G - bh - th}" width="{tw}" height="{th}" {INKF}/>')
        for k in range(3):               # the slots that catch the wind
            add(f'<rect x="{tx + 7 + k * (tw - 14) / 3:.0f}" y="{G - bh - th + 22}" width="{(tw - 14) / 3 - 5:.0f}" height="{th * .52:.0f}" rx="3" fill="{CREAM}" fill-opacity=".55"/>')
        add(f'<path d="M{tx - 6} {G - bh - th} h{tw + 12}" stroke="{INK}" stroke-width="8"/>')
        for k in range(4):
            add(f'<rect x="{tx - 4 + k * (tw + 4) / 4:.0f}" y="{G - bh - th - 14}" width="8" height="12" {INKF}/>')
        add(f'<rect x="{bx + bw * .55:.0f}" y="{G - 52}" width="26" height="52" rx="13" fill="{AMB}" fill-opacity=".9"/>')  # a lit doorway

def ain_dubai(cx, cy, r):
    add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-opacity=".3" stroke-width="7"/>')
    for k in range(16):
        a = k * math.pi / 8
        add(f'<path d="M{cx} {cy} L{cx + r * math.cos(a):.1f} {cy + r * math.sin(a):.1f}" stroke="{INK}" stroke-opacity=".2" stroke-width="2.5"/>')
        add(f'<circle cx="{cx + r * math.cos(a):.1f}" cy="{cy + r * math.sin(a):.1f}" r="7" fill="{INK}" fill-opacity=".3"/>')
    add(f'<circle cx="{cx}" cy="{cy}" r="10" fill="{INK}" fill-opacity=".3"/>')
    add(f'<path d="M{cx} {cy} L{cx - 60} {G} M{cx} {cy} L{cx + 60} {G}" stroke="{INK}" stroke-opacity=".3" stroke-width="10" stroke-linecap="round"/>')

def tower(x, w, h, top='flat', op=None, windows=0):
    f = DIM if op is None else f'fill="{INK}" fill-opacity="{op}"'
    if top == 'flat':
        add(f'<rect x="{x}" y="{G - h}" width="{w}" height="{h}" rx="4" {f}/>')
    elif top == 'slant':
        add(f'<path d="M{x} {G} L{x} {G - h + w * .9} L{x + w} {G - h} L{x + w} {G}Z" {f}/>')
    elif top == 'spire':
        add(f'<path d="M{x} {G} L{x} {G - h} Q{x + w / 2} {G - h - w * .7} {x + w} {G - h} L{x + w} {G}Z" {f}/>')
    random.seed(int(x * 7 + h))
    for _ in range(windows):
        wx = x + 6 + random.random() * (w - 18); wy = G - h + 30 + random.random() * (h - 60)
        add(f'<rect x="{wx:.0f}" y="{wy:.0f}" width="8" height="10" rx="1.5" fill="{AMB}" fill-opacity=".85"/>')

def cayan(x, w, h):
    add(f'<rect x="{x}" y="{G - h}" width="{w}" height="{h}" rx="6" fill="{INK}" fill-opacity=".26"/>')
    for k in range(9):
        y = G - h + 20 + k * (h - 30) / 9
        add(f'<path d="M{x} {y + 18:.0f} Q{x + w / 2} {y:.0f} {x + w} {y + 10:.0f}" stroke="{CREAM}" stroke-opacity=".45" stroke-width="2.5" fill="none"/>')

def museum(cx, h):
    add(f'<ellipse cx="{cx}" cy="{G}" rx="104" ry="30" fill="{INK}" fill-opacity=".22"/>')
    rx, ry = h * .5, h * .42
    cy = G - 22 - ry
    add(f'<ellipse cx="{cx}" cy="{cy:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="none" stroke="{INK}" stroke-width="{h * .13:.0f}"/>')
    for a0, a1 in ((196, 236), (252, 300), (316, 350), (12, 40), (60, 104), (128, 166)):
        p = lambda a: (cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a)))
        (x0, y0), (x1, y1) = p(a0), p(a1)
        add(f'<path d="M{x0:.1f} {y0:.1f} A{rx:.0f} {ry:.0f} 0 0 1 {x1:.1f} {y1:.1f}" stroke="{CREAM}" stroke-opacity=".5" stroke-width="4" fill="none" stroke-linecap="round" stroke-dasharray="10 6 3 6"/>')

def emirates(x, h1, h2):
    tower(x, 36, h1, 'slant', op='.3')
    tower(x + 50, 30, h2, 'slant', op='.3')

def frame(x, w, h):
    t = 24
    add(f'<rect x="{x}" y="{G - h}" width="{t}" height="{h}" {INKF}/>')
    add(f'<rect x="{x + w - t}" y="{G - h}" width="{t}" height="{h}" {INKF}/>')
    add(f'<rect x="{x}" y="{G - h}" width="{w}" height="{t + 4}" {INKF}/>')
    add(f'<rect x="{x + t}" y="{G - h + 8}" width="{w - 2 * t}" height="{t - 10}" fill="{AMB}"/>')
    add(f'<rect x="{x - 8}" y="{G - 14}" width="{w + 16}" height="14" {INKF}/>')

def palm(x, h, s=1):
    add(f'<path d="M{x} {G} Q{x + 10 * s} {G - h * .5} {x + 4 * s} {G - h}" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/>')
    tx, ty = x + 4 * s, G - h
    for a, l in ((-160, 46), (-120, 40), (-60, 40), (-20, 46), (-90, 30)):
        r = math.radians(a)
        ex, ey = tx + l * math.cos(r), ty + l * math.sin(r) + 18
        mx, my = tx + l * .5 * math.cos(r), ty + l * .5 * math.sin(r) - 10
        add(f'<path d="M{tx} {ty} Q{mx:.0f} {my:.0f} {ex:.0f} {ey:.0f}" stroke="{INK}" stroke-width="9" fill="none" stroke-linecap="round"/>')

def dhow(x, y, s=1):
    S = lambda a, b: f"{x + a * s:.1f} {y + b * s:.1f}"
    add(f'<path d="M{S(0, -10)} L{S(30, 22)} L{S(150, 26)} L{S(196, -20)} L{S(206, -24)} L{S(198, -2)} L{S(150, 12)}Z" {INKF}/>')
    add(f'<path d="M{S(0, -10)} L{S(196, -20)} L{S(198, -2)} L{S(150, 12)} L{S(30, 14)}Z" {INKF}/>')
    add(f'<path d="M{S(96, -10)} L{S(102, -150)}" stroke="{INK}" stroke-width="{5 * s:.1f}"/>')
    add(f'<path d="M{S(20, -24)} L{S(176, -190)}" stroke="{INK}" stroke-width="{5 * s:.1f}" stroke-linecap="round"/>')
    add(f'<path d="M{S(28, -30)} L{S(170, -184)} L{S(150, -26)}Z" {INKF}/>')
    add(f'<path d="M{S(176, -190)} L{S(204, -182)} L{S(178, -172)}Z" fill="{AMB}"/>')

def water():
    add(f'<rect x="0" y="{G}" width="{W}" height="{H - G}" fill="url(#sea)"/>')
    random.seed(4)
    for i in range(30):
        y = G + 18 + (i % 23) * 12 + random.random() * 6
        x = random.random() * W; w = 30 + random.random() * 90
        add(f'<path d="M{x:.0f} {y:.0f} h{w:.0f}" stroke="{INK}" stroke-opacity=".06" stroke-width="3" stroke-linecap="round"/>')

def sun_glint(cx):
    random.seed(9)
    for i in range(9):
        y = G + 20 + i * 15; w = 120 - i * 9 + random.random() * 20
        add(f'<path d="M{cx - w / 2:.0f} {y:.0f} h{w:.0f}" stroke="{AMB}" stroke-opacity="{.75 - i * .07:.2f}" stroke-width="5" stroke-linecap="round"/>')

def pin(tipx, tipy, height):
    sc = height / 92.1
    add(f'<g transform="translate({tipx:.1f} {tipy:.1f}) scale({sc:.3f})"><path d="M-33.25 -68.40 L-38.11 -65.81 L0 0Z" fill="{INK}"/><circle cx="-35.68" cy="-67.1" r="24" fill="{AMB}"/></g>')

def scene(args):
    sunx, suny, sunr = args.get('sun', (330, 930, 118))
    add(f'<circle cx="{sunx}" cy="{suny}" r="{sunr + 70}" fill="url(#sunglow)"/>')
    add(f'<circle cx="{sunx}" cy="{suny}" r="{sunr}" fill="{AMB}"/>')
    # far city
    for x, w, h in ((0, 40, 150), (44, 36, 210), (360, 40, 250), (404, 34, 300), (470, 44, 210), (590, 38, 330), (840, 44, 260), (930, 40, 200), (990, 44, 280), (1040, 40, 180)):
        tower(x, w, h, 'flat')
    ain_dubai(330, G - 150, 128)
    cayan(422, 46, 380)
    tower(372, 40, 290, 'spire', op='.3', windows=2)
    emirates(636, 330, 290)
    museum(552, 150)
    bk = burj_khalifa(args.get('burjx', 790), args.get('burjh', 600))
    wind_towers(40)
    frame(912, 104, 250)
    palm(318, 104); palm(344, 78, -1); palm(1046, 80, -1)
    add(f'<path d="M0 {G} H{W}" stroke="{INK}" stroke-opacity=".25" stroke-width="4"/>')
    water()
    sun_glint(sunx)
    dhow(600, G + 104, .82)
    pin(bk[0], bk[1] - 4, args.get('pinh', 120))

def page(args):
    OUT.clear(); scene(args)
    svg = '\n'.join(OUT)
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:"Inter";src:url(/home/claude/crewgalley-site/fonts/inter-latin.woff2) format("woff2");font-weight:100 900;font-display:block}}
html,body{{margin:0}}
body{{width:{W}px;height:{H}px;overflow:hidden;position:relative;font-family:Inter,sans-serif;font-feature-settings:"cv11","ss01";-webkit-font-smoothing:antialiased;color:{INK};
 background:radial-gradient(60% 55% at 22% 64%,rgba(242,169,59,.38),transparent 70%),radial-gradient(70% 50% at 90% 0%,rgba(214,203,184,.55),transparent 70%),linear-gradient(180deg,#FBF7F0 0%,#F6EBD8 100%)}}
.copy{{position:absolute;left:96px;right:96px;top:{args.get('top', 104)}px}}
.eyebrow{{display:flex;align-items:center;gap:18px;font-size:29px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#8A5200;margin:0 0 30px}}
.eyebrow::before{{content:"";width:17px;height:17px;border-radius:50%;background:{AMB};box-shadow:0 0 0 9px rgba(242,169,59,.2)}}
h1{{font-size:{args.get('h1', 168)}px;line-height:.98;letter-spacing:-.045em;margin:0;font-weight:900;font-variation-settings:"opsz" 32;word-spacing:.06em}}
h1 em{{font-style:normal;color:#B86A00}}
svg{{position:absolute;left:0;top:0}}
.brand{{position:absolute;left:96px;bottom:{args.get('brandb', 78)}px;white-space:nowrap;color:{INK};font-weight:900;font-size:58px;line-height:1;letter-spacing:-.055em;font-variation-settings:"opsz" 32}}
.brand .pin{{display:inline-block;vertical-align:-.2em;height:.5em;width:auto;margin-left:.07em;overflow:visible}}
.soon{{position:absolute;right:96px;bottom:{args.get('brandb', 78) + 8}px;font-size:30px;font-weight:600;color:#4A5468}}
</style></head><body>
<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs>
<radialGradient id="sunglow"><stop offset=".6" stop-color="{AMB}" stop-opacity=".35"/><stop offset="1" stop-color="{AMB}" stop-opacity="0"/></radialGradient>
<linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EADFCB"/><stop offset="1" stop-color="#F4EFE6"/></linearGradient>
</defs>{svg}</svg>
<div class="copy"><h1 style="font-size:230px">Dubai</h1><p style="margin:18px 0 0;font-size:84px;line-height:1.04;font-weight:850;letter-spacing:-.035em;color:#B86A00">Our base.<br>Our home.</p></div>
<div class="brand">galley<svg class="pin" viewBox="-60.7 -92.1 61.7 92.1" aria-hidden="true" style="position:static"><path d="M-33.25 -68.40 L-38.11 -65.81 L0 0Z" fill="currentColor"/><circle cx="-35.68" cy="-67.10" r="24" fill="{AMB}"/></svg></div>

</body></html>'''

def shoot(out, args):
    from playwright.sync_api import sync_playwright
    p2 = pathlib.Path(__file__).with_name('post.tmp.html'); p2.write_text(page(args))
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=1)
        pg.goto(p2.as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_function("document.fonts.check('900 50px Inter')"); pg.wait_for_timeout(300)
        pg.screenshot(path=out, type='jpeg', quality=93); b.close()

if __name__ == '__main__':
    import json
    shoot(sys.argv[1], json.loads(sys.argv[2]) if len(sys.argv) > 2 else {})
