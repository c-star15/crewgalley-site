"""Screenshot one frame: shoot.py 'horizon.html?mode=still' out.png 1080 1440 (add &t=14 for a reel frame)."""
import pathlib, sys
from playwright.sync_api import sync_playwright
page, out, w, h = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
    pg.goto((pathlib.Path(__file__).resolve().parent / page.split('?')[0]).as_uri() + ('?' + page.split('?', 1)[1] if '?' in page else ''))
    pg.wait_for_function('window.READY === true')
    pg.wait_for_timeout(200)
    pg.screenshot(path=out, type='png')
    b.close()
