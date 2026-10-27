"""Render the artboards to JPEG: python3 render.py [stem ...]  (default: every *.dc.html here)

A .dc.html is static markup: drop the support.js line, unwrap <x-dc> and <helmet>,
and load Inter (variable, opsz + wght) from the site's own font file instead of
Google Fonts. Output goes one folder up, as <stem>.jpg at quality 92.
"""
import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent
FONT = (HERE / '../../../../fonts/inter-latin.woff2').resolve()
FACE = f"<style>@font-face{{font-family:Inter;src:url('{FONT.as_uri()}') format('woff2');font-weight:100 900;font-style:normal}}</style>"


def static_html(src: str) -> str:
    s = src.replace('<script src="./support.js"></script>', '')
    s = re.sub(r'<link href="https://fonts.googleapis.com[^>]*>', FACE, s)
    for tag in ('x-dc', 'helmet'):
        s = s.replace(f'<{tag}>', '').replace(f'</{tag}>', '')
    return s


def main():
    stems = sys.argv[1:] or sorted(p.name[:-len('.dc.html')] for p in HERE.glob('*.dc.html'))
    tmp = HERE / '.render'
    tmp.mkdir(exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        for stem in stems:
            src = (HERE / f'{stem}.dc.html').read_text()
            m = re.search(r'"\$preview":\{"width":(\d+),"height":(\d+)\}', src)
            w, h = int(m.group(1)), int(m.group(2))
            f = tmp / f'{stem}.html'
            f.write_text(static_html(src))
            pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
            pg.goto(f.as_uri())
            pg.evaluate('document.fonts.ready')
            pg.wait_for_timeout(150)
            pg.screenshot(path=str(OUT / f'{stem}.jpg'), type='jpeg', quality=92)
            pg.close()
            print('rendered', stem)
        b.close()
    for f in tmp.glob('*.html'):
        f.unlink()
    tmp.rmdir()


if __name__ == '__main__':
    main()
