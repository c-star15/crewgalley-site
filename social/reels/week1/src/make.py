"""Build the week 1 Reels: render (render.py), score (music.py), mux at -14 LUFS.

python3 make.py [--work DIR] [name ...]     (default: all seven)
Writes ../w1-<n>-<name>.mp4 and ../w1-<n>-<name>-cover.jpg. Intermediates go to --work.
The two art Reels reuse social/art/*-reel.mp4 (video copied as is) with their own music.
"""
import argparse
import json
import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent
ART = HERE.parents[2] / 'art'
REELS = [  # day order
    (1, 'horizon', 'art'),
    (2, 'off-today', 'page'),
    (3, '47-messages', 'page'),
    (4, 'departures', 'art'),
    (5, 'off-tuesday', 'page'),
    (6, 'roster-roulette', 'page'),
    (7, 'clubs', 'page'),
]
TARGET = -14.0


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def loudness(path):
    p = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(path), '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                       capture_output=True, text=True)
    s = p.stderr[p.stderr.rfind('Summary:'):]
    i = float(re.search(r'I:\s+(-?[\d.]+) LUFS', s).group(1))
    tp = float(re.search(r'Peak:\s+(-?[\d.]+) dBFS', s).group(1))
    return i, tp


def build(n, name, kind, work):
    stem = f'w1-{n}-{name}'
    wav = work / f'{name}.wav'
    if kind == 'page':
        run([sys.executable, str(HERE / 'render.py'), 'video', name, str(work)])
        video = work / f'{name}.silent.mp4'
        run([sys.executable, str(HERE / 'music.py'), name, str(work / f'{name}.json'), str(wav)])
        shutil.copy(work / f'{name}-cover.jpg', OUT / f'{stem}-cover.jpg')
    else:
        video = ART / f'{name}-reel.mp4'
        run([sys.executable, str(HERE / 'music.py'), name, '-', str(wav)])
        shutil.copy(ART / f'{name}-reel-cover.jpg', OUT / f'{stem}-cover.jpg')
    i, _ = loudness(wav)
    gain = TARGET - i
    out = OUT / f'{stem}.mp4'
    run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(video), '-i', str(wav), '-map', '0:v:0', '-map', '1:a:0',
         '-af', f'volume={gain:.2f}dB', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
         '-movflags', '+faststart', '-shortest', str(out)])
    fi, ftp = loudness(out)
    info = dict(file=out.name, cover=f'{stem}-cover.jpg', gain_db=round(gain, 2), lufs=fi, true_peak_dbfs=ftp,
                mb=round(out.stat().st_size / 1e6, 2))
    print(json.dumps(info), flush=True)
    return info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', default='/tmp/galley-reels-w1')
    ap.add_argument('names', nargs='*')
    a = ap.parse_args()
    work = pathlib.Path(a.work)
    work.mkdir(parents=True, exist_ok=True)
    for n, name, kind in REELS:
        if not a.names or name in a.names:
            build(n, name, kind, work)


if __name__ == '__main__':
    main()
