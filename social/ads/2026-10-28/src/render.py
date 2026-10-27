"""Render the artboards to JPEG: python3 render.py [--out DIR] [--suffix S] [stem ...]
(default: every *.dc.html here)

A .dc.html is static markup: drop the support.js line, unwrap <x-dc> and <helmet>,
and load Inter (variable, opsz + wght) from the site's own font file instead of
Google Fonts. Output goes one folder up (or to --out), as <stem><suffix>.jpg at quality 92.
Week 1 (28 Oct, with the Illustration label): --out ../../../week1 --suffix=-illustration
"""
import argparse
import pathlib
import re

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
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=str(OUT))
    ap.add_argument('--suffix', default='')
    ap.add_argument('stems', nargs='*')
    args = ap.parse_args()
    out = (HERE / args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    stems = args.stems or sorted(p.name[:-len('.dc.html')] for p in HERE.glob('*.dc.html'))
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
            pg.screenshot(path=str(out / f'{stem}{args.suffix}.jpg'), type='jpeg', quality=92)
            pg.close()
            print('rendered', stem)
        b.close()
    for f in tmp.glob('*.html'):
        f.unlink()
    tmp.rmdir()


if __name__ == '__main__':
    main()
