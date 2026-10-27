"""Render a week 1 Reel frame by frame (deterministic: render(t) per frame, Playwright screenshots).

python3 render.py video <reel> <out_dir>     -> <out_dir>/<reel>.silent.mp4, <reel>.json (timing + sound events), <reel>-cover.jpg
python3 render.py stills <reel> <out_dir> t1 t2 ...   -> PNG stills at those times
python3 render.py cover <reel> <out.jpg>              -> the cover frame only (REEL.cover)
Reels: off-today, 47-messages, off-tuesday, roster-roulette, clubs (see reels.js).
"""
import json
import pathlib
import subprocess
import sys
import time

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
W, H, FPS = 1080, 1920, 30


def open_page(b, reel):
    pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=1)
    pg.goto((HERE / 'reel.html').as_uri() + f'?r={reel}')
    pg.wait_for_function('window.READY === true', timeout=20000)
    return pg


def video(reel, out):
    out.mkdir(parents=True, exist_ok=True)
    mp4 = out / f'{reel}.silent.mp4'
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = open_page(b, reel)
        meta = pg.evaluate('window.REEL')
        (out / f'{reel}.json').write_text(json.dumps(meta, indent=1))
        n = int(round(meta['dur'] * FPS))
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'png', '-i', '-',
                               '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p',
                               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p',
                               '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
                               '-r', str(FPS), '-an', str(mp4)], stdin=subprocess.PIPE)
        t0 = time.time()
        for i in range(n):
            pg.evaluate('t => render(t)', i / FPS)
            ff.stdin.write(pg.screenshot(type='png', animations='disabled'))
            if i % 90 == 0:
                print(f'{reel} {i}/{n} {time.time() - t0:.0f}s', flush=True)
        ff.stdin.close()
        ff.wait()
        pg.evaluate('t => render(t)', meta['cover'])
        pg.screenshot(path=str(out / f'{reel}-cover.jpg'), type='jpeg', quality=90)
        b.close()
    print('done', mp4, n, 'frames', f'{time.time() - t0:.0f}s')


def stills(reel, out, ts):
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = open_page(b, reel)
        for t in ts:
            pg.evaluate('t => render(t)', t)
            pg.screenshot(path=str(out / f'{reel}-{t:05.2f}.png'))
        b.close()


def cover(reel, out):
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = open_page(b, reel)
        pg.evaluate('t => render(t)', pg.evaluate('window.REEL.cover'))
        pg.screenshot(path=str(out), type='jpeg', quality=90)
        b.close()


if __name__ == '__main__':
    mode, reel, out = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3])
    if mode == 'video':
        video(reel, out)
    elif mode == 'cover':
        cover(reel, out)
    else:
        stills(reel, out, [float(x) for x in sys.argv[4:]])
