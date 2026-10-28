"""'Our base. Our home.' carousel: photo slides (cropped to 3:4, the first with the title) and an end card in the website identity.
python3 make.py cover <photo> <out.jpg> [focus_y 0-1]
python3 make.py photo <photo> <out.jpg> [focus_y]
python3 make.py end <out.jpg>"""
import base64, pathlib, sys
from playwright.sync_api import sync_playwright
W, H = 1080, 1440
FONT = '/home/claude/crewgalley-site/fonts/inter-latin.woff2'
HEAD = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:"Inter";src:url({FONT}) format("woff2");font-weight:100 900;font-display:block}}
html,body{{margin:0}}body{{width:{W}px;height:{H}px;overflow:hidden;position:relative;font-family:Inter,sans-serif;font-feature-settings:"cv11","ss01";-webkit-font-smoothing:antialiased}}
.ph{{position:absolute;inset:0;background-size:cover;background-repeat:no-repeat}}
.shade{{position:absolute;left:0;right:0;bottom:0;height:62%;background:linear-gradient(180deg,rgba(11,20,36,0) 0%,rgba(11,20,36,.55) 55%,rgba(11,20,36,.82) 100%)}}
.t{{position:absolute;left:84px;right:84px;bottom:110px;color:#F4EFE6}}
.eyebrow{{display:flex;align-items:center;gap:16px;font-size:28px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#F2A93B;margin:0 0 22px}}
.eyebrow::before{{content:"";width:16px;height:16px;border-radius:50%;background:#F2A93B;box-shadow:0 0 0 8px rgba(242,169,59,.25)}}
h1{{font-size:150px;line-height:.96;letter-spacing:-.045em;margin:0;font-weight:900;font-variation-settings:"opsz" 32}}
h1 em{{font-style:normal;color:#F2A93B}}
.brand{{white-space:nowrap;font-weight:900;line-height:1;letter-spacing:-.055em;font-variation-settings:"opsz" 32}}
.brand .pin{{display:inline-block;vertical-align:-.2em;height:.5em;width:auto;margin-left:.07em;overflow:visible}}
.mark{{position:absolute;right:84px;top:80px;font-size:52px;color:#F4EFE6}}
</style></head><body>'''
PIN = '<svg class="pin" viewBox="-60.7 -92.1 61.7 92.1"><path d="M-33.25 -68.40 L-38.11 -65.81 L0 0Z" fill="currentColor"/><circle cx="-35.68" cy="-67.10" r="24" fill="#F2A93B"/></svg>'

def bg(photo, fy):
    data = base64.b64encode(pathlib.Path(photo).read_bytes()).decode()
    mime = 'image/png' if photo.lower().endswith('.png') else 'image/jpeg'
    return f'<div class="ph" style="background-image:url(data:{mime};base64,{data});background-position:50% {fy * 100:.0f}%"></div>'

def cover(photo, fy=.5):
    return HEAD + bg(photo, fy) + '<div class="shade"></div><div class="t"><p class="eyebrow">Dubai</p><h1>Our base.<br><em>Our home.</em></h1></div></body></html>'

def photo(p, fy=.5):
    return HEAD + bg(p, fy) + '</body></html>'

def end():
    return HEAD + '''<div style="position:absolute;inset:0;background:radial-gradient(60% 55% at 85% 12%,rgba(242,169,59,.34),transparent 70%),radial-gradient(80% 60% at 10% 110%,rgba(214,203,184,.5),transparent 70%),linear-gradient(180deg,#FBF7F0,#F4EFE6)"></div>
<div style="position:absolute;left:0;right:0;top:0;bottom:0;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#13213A;text-align:center">
<div class="brand" style="font-size:230px">galley''' + PIN + '''</div>
<p style="margin:56px 0 0;font-size:66px;line-height:1.1;font-weight:800;letter-spacing:-.02em">Coming soon <span style="color:#B86A00">to Dubai.</span></p>
</div></body></html>'''

def shoot(html, out):
    tmp = pathlib.Path(out).with_suffix('.html'); tmp.write_text(html)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': W, 'height': H})
        pg.goto(tmp.as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_function("document.fonts.check('900 50px Inter')"); pg.wait_for_timeout(300)
        pg.screenshot(path=out, type='jpeg', quality=92); b.close()
    tmp.unlink()

if __name__ == '__main__':
    m = sys.argv[1]
    if m == 'end': shoot(end(), sys.argv[2])
    else:
        fy = float(sys.argv[4]) if len(sys.argv) > 4 else .5
        shoot((cover if m == 'cover' else photo)(sys.argv[2], fy), sys.argv[3])
