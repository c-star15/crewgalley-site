"""Render a page's render(t) frame by frame into an H.264 MP4 (deterministic).
usage: render.py <page?query> <out.mp4> <W> <H> <seconds> [fps]"""
import pathlib, subprocess, sys, time
from playwright.sync_api import sync_playwright
page, out, W, H, dur = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5])
fps = int(sys.argv[6]) if len(sys.argv) > 6 else 30
n = int(round(dur * fps))
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(fps), '-c:v', 'png', '-i', '-',
                       '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p',
                       '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
                       '-r', str(fps), '-movflags', '+faststart', '-an', out], stdin=subprocess.PIPE)
t0 = time.time()
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=1)
    pg.goto((pathlib.Path(__file__).resolve().parent / page.split('?')[0]).as_uri() + ('?' + page.split('?', 1)[1] if '?' in page else ''))
    pg.wait_for_function('window.READY === true')
    for i in range(n):
        pg.evaluate('t => render(t)', i / fps)
        ff.stdin.write(pg.screenshot(type='png', animations='disabled'))
        if i % 60 == 0: print(f'{i}/{n} {time.time()-t0:.0f}s', flush=True)
    b.close()
ff.stdin.close(); ff.wait()
print('done', out, n, 'frames', f'{time.time()-t0:.0f}s')
