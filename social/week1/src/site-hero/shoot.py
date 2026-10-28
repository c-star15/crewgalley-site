import sys, pathlib
from playwright.sync_api import sync_playwright
here = pathlib.Path(__file__).resolve().parent
def shoot(out, **kw):
    s = (here / 'post.html').read_text()
    for k, v in kw.items(): s = s.replace(f'__{k}__', str(v))
    p2 = here / 'post.tmp.html'; p2.write_text(s)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1080, 'height': 1440}, device_scale_factor=1, reduced_motion='reduce', color_scheme='light')
        pg.goto(p2.as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_function("document.fonts.check('900 50px Inter')"); pg.wait_for_timeout(600)
        pg.screenshot(path=out, type='jpeg', quality=93); b.close()
if __name__ == '__main__':
    import json; shoot(sys.argv[1], **json.loads(sys.argv[2]))
