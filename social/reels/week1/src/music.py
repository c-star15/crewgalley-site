"""Original soundtrack for each week 1 Reel, synthesised in numpy (no samples).

python3 music.py <reel> <timing.json|-> <out.wav>
A warm, minimal pluck / pad / kick groove (120-126 BPM), one variation per Reel,
with light effects on the page's events (pop as crew dots appear, chime on
joining, whoosh on a scene change, ticks for the roster slot machine). The
timing JSON is what render.py dumps from the page (bpm, dur, cues, events); the
two art Reels (horizon, departures) have their timing here instead.
Output: 48 kHz stereo float WAV, peak-normalised; loudness (-14 LUFS) is set at the mux.
"""
import json
import sys

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 48000


def mhz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


QUAL = {'maj7': [0, 4, 7, 11], 'maj9': [0, 4, 7, 11, 14], 'm7': [0, 3, 7, 10], 'm9': [0, 3, 7, 10, 14], '6': [0, 4, 7, 9],
        'add9': [0, 4, 7, 14], 'sus2': [0, 2, 7, 12], 'maj': [0, 4, 7, 12], 'min': [0, 3, 7, 12], '7sus': [0, 5, 7, 10]}
DEG = {'I': 0, 'ii': 2, 'iii': 4, 'IV': 5, 'V': 7, 'vi': 9, 'bVII': 10}

# one variation per Reel: key (MIDI of the root, octave 3), progression (one chord a bar), arpeggio, bass rhythm, colour
PRESETS = {
    'horizon': dict(key=50, prog=[('I', 'maj9'), ('vi', 'm7'), ('IV', 'maj7'), ('V', '7sus')], arp=[0, 2, 1, 3, 2, 4, 1, 3], step=0.5,
                    bass=[0, 2.5], bright=0.8, kick='half', seed=1),
    'off-today': dict(key=53, prog=[('I', 'maj9'), ('vi', 'm7'), ('IV', 'maj7'), ('V', '6')], arp=[0, 2, 3, 1, 2, 3, 4, 2], step=0.5,
                      bass=[0, 1.5, 2.5, 3.5], bright=1.0, kick='four', seed=2),
    '47-messages': dict(key=57, prog=[('I', 'm7'), ('I', 'm9'), ('bVII', '6'), ('I', 'm7')], post_key=48,
                        post_prog=[('I', 'add9'), ('V', 'maj'), ('vi', 'm7'), ('IV', 'maj7')], arp=[0, 3, 1, 2, 0, 3, 2, 1], step=0.25,
                        bass=[0, 0.75, 2, 2.75], bright=1.1, kick='four', seed=3),
    'departures': dict(key=51, prog=[('I', 'maj7'), ('vi', 'm9'), ('IV', 'maj7'), ('V', 'add9')], arp=[0, 1, 2, 3, 4, 3, 2, 1], step=0.5,
                       bass=[0, 2, 3.5], bright=0.85, kick='four', seed=4),
    'off-tuesday': dict(key=55, prog=[('I', 'maj7'), ('iii', 'm7'), ('IV', 'maj9'), ('V', '6')], arp=[0, 2, 1, 3, 0, 2, 4, 3], step=0.5,
                        bass=[0, 1.5, 3], bright=0.95, kick='four', seed=5),
    'roster-roulette': dict(key=50, prog=[('vi', 'm7'), ('IV', 'maj7'), ('I', 'add9'), ('V', '6')], arp=[0, 1, 2, 3, 1, 2, 3, 4], step=0.25,
                            bass=[0, 0.5, 2, 2.5, 3.5], bright=1.05, kick='four', seed=6),
    'clubs': dict(key=58, prog=[('I', 'maj7'), ('vi', 'm9'), ('ii', 'm7'), ('V', '6')], arp=[0, 2, 4, 2, 1, 3, 2, 3], step=0.5,
                  bass=[0, 1.5, 2.5], bright=1.0, kick='four', seed=7),
}


# ---------------------------------------------------------------------------
# instruments (mono numpy arrays at SR)
# ---------------------------------------------------------------------------
def t_axis(d):
    return np.arange(int(d * SR)) / SR


def pluck(f, d=0.9, bright=1.0, rng=None):
    t = t_axis(d)
    y = np.zeros_like(t)
    for k in range(1, 11):
        fk = f * k * (1 + 0.0007 * k * k)
        if fk > 12000:
            break
        y += (1 / k ** 1.25) * np.exp(-t * (2.2 + 2.0 * k / bright)) * np.sin(2 * np.pi * fk * t + (rng.random() * 0.3 if rng is not None else 0))
    att = np.minimum(1, t / 0.003)
    return y * att * 0.5


def pad_note(f, d, bright=1.0):
    t = t_axis(d)
    y = np.zeros_like(t)
    for det in (-0.006, 0.0, 0.0065):
        for k in range(1, 9):
            fk = f * (1 + det) * k
            if fk > 5000:
                break
            y += (1 / k) * np.exp(-0.35 * k / bright) * np.sin(2 * np.pi * fk * t + k * 1.3 + det * 900)
    a, r = min(0.35, d * 0.4), min(0.5, d * 0.4)
    env = np.minimum(1, t / a) * np.minimum(1, (d - t) / r)
    trem = 1 + 0.06 * np.sin(2 * np.pi * 0.3 * t)
    return y * env * trem / 6


def bass_note(f, d):
    t = t_axis(d)
    y = np.sin(2 * np.pi * f * t) + 0.28 * np.sin(4 * np.pi * f * t) + 0.08 * np.sin(6 * np.pi * f * t)
    env = np.minimum(1, t / 0.006) * (0.55 + 0.45 * np.exp(-t / 0.18)) * np.minimum(1, (d - t) / 0.04)
    return np.tanh(1.4 * y * env) * 0.55


def kick(level=1.0):
    t = t_axis(0.42)
    f = 46 + 88 * np.exp(-t / 0.028)
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) * np.exp(-t / 0.16)
    click = np.exp(-t / 0.002) * 0.25
    return (y + click) * level


def noise(d, seed):
    return np.random.default_rng(seed).standard_normal(int(d * SR))


SOS_HP = butter(4, 7000, 'hp', fs=SR, output='sos')
SOS_CLAP = butter(2, [900, 2800], 'bandpass', fs=SR, output='sos')
SOS_TICK = butter(2, [2500, 6500], 'bandpass', fs=SR, output='sos')
SOS_LP = butter(2, 5000, 'lp', fs=SR, output='sos')


def hat(seed, d=0.05, tau=0.014):
    t = t_axis(d)
    return sosfilt(SOS_HP, noise(d, seed)) * np.exp(-t / tau) * 0.5


def clap(seed):
    t = t_axis(0.25)
    n = sosfilt(SOS_CLAP, noise(0.25, seed))
    env = np.zeros_like(t)
    for o in (0.0, 0.011, 0.022):
        env += (t >= o) * np.exp(-np.maximum(0, t - o) / (0.008 if o < 0.02 else 0.07))
    return n * env * 0.5


def pop_sfx(f):
    t = t_axis(0.12)
    fr = f * (1 + 0.9 * np.exp(-t / 0.012))
    ph = 2 * np.pi * np.cumsum(fr) / SR
    return np.sin(ph) * np.exp(-t / 0.035) * np.minimum(1, t / 0.0015) * 0.8


def tap_sfx(seed):
    t = t_axis(0.03)
    return sosfilt(SOS_TICK, noise(0.03, seed)) * np.exp(-t / 0.004) * 0.6


def blip_sfx(f):
    t = t_axis(0.07)
    return np.sin(2 * np.pi * f * t) * np.exp(-t / 0.018) * np.minimum(1, t / 0.002) * 0.5


def chime_sfx(f):
    t = t_axis(2.2)
    y = np.zeros_like(t)
    for ratio, amp, tau in ((1, 1, 0.9), (2.0, 0.45, 0.6), (2.76, 0.3, 0.35), (5.4, 0.14, 0.18), (8.93, 0.06, 0.1)):
        if f * ratio > 16000:
            continue
        y += amp * np.sin(2 * np.pi * f * ratio * t) * np.exp(-t / tau)
    return y * np.minimum(1, t / 0.002) * 0.45


def whoosh_sfx(seed, d=0.42):
    n = noise(d, seed)
    t = t_axis(d)
    out = np.zeros_like(n)
    blocks = 12
    L = len(n) // blocks
    for b in range(blocks):
        fc = 400 * (12 ** (b / (blocks - 1)))
        sos = butter(2, [fc * 0.6, min(fc * 1.6, 20000)], 'bandpass', fs=SR, output='sos')
        seg = sosfilt(sos, n[b * L:(b + 1) * L + 512])[:L]
        out[b * L:(b + 1) * L] = seg
    env = np.sin(np.pi * np.minimum(1, t / d)) ** 2
    return out * env * 0.35


def thunk_sfx(seed):
    t = t_axis(0.2)
    f = 70 + 120 * np.exp(-t / 0.02)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.06)
    y += sosfilt(SOS_CLAP, noise(0.2, seed)) * np.exp(-t / 0.006) * 0.3
    return y * 0.8


def tick_sfx(seed):
    t = t_axis(0.02)
    return sosfilt(SOS_TICK, noise(0.02, seed)) * np.exp(-t / 0.0025) * 0.5


def flap_sfx(seed):
    t = t_axis(0.05)
    y = sosfilt(SOS_CLAP, noise(0.05, seed)) * np.exp(-t / 0.006)
    y += np.sin(2 * np.pi * 420 * t) * np.exp(-t / 0.01) * 0.3
    return y * 0.5


# ---------------------------------------------------------------------------
class Bus:
    def __init__(self, dur):
        self.n = int(dur * SR) + SR * 3
        self.l = np.zeros(self.n)
        self.r = np.zeros(self.n)

    def add(self, sig, t, gain=1.0, pan=0.0):
        i = int(round(t * SR))
        if i >= self.n or i + len(sig) <= 0:
            return
        if i < 0:
            sig, i = sig[-i:], 0
        j = min(self.n, i + len(sig))
        s = sig[: j - i] * gain
        self.l[i:j] += s * np.sqrt(0.5 * (1 - pan))
        self.r[i:j] += s * np.sqrt(0.5 * (1 + pan))


def reverb_ir(seconds=1.6, seed=9):
    t = t_axis(seconds)
    rng = np.random.default_rng(seed)
    env = np.exp(-t * 6.9 / seconds)
    l = sosfilt(SOS_LP, rng.standard_normal(len(t))) * env
    r = sosfilt(SOS_LP, rng.standard_normal(len(t))) * env
    l[: int(0.012 * SR)] = 0
    r[: int(0.017 * SR)] = 0
    return l / np.sqrt((l ** 2).sum()), r / np.sqrt((r ** 2).sum())


def chord_notes(key, deg, qual, octave=0):
    root = key + DEG[deg] + 12 * octave
    return [root + q for q in QUAL[qual]]


def art_timing(name):
    if name == 'horizon':
        bpm, dur = 125, 14.0
        B = 60 / bpm
        ev = [{'t': 9.6, 'kind': 'chime'}]
        return dict(bpm=bpm, dur=dur, cues={'lift': 4 * B * 2, 'end': 4 * B * 6, 'nodrums': 4 * B * 5}, events=ev, key='D')
    if name == 'departures':
        bpm, dur = 120, 14.0
        ev = []
        t = 0.5
        while t < 10.4:
            ev.append({'t': t + 0.17, 'kind': 'flap', 'n': len(ev)})
            t += 0.34
        for tc in (2.3, 9.0):
            for r in range(8):
                ev.append({'t': tc + r * 0.09 + 0.17, 'kind': 'flap', 'n': r})
        for c in range(5):
            for r in range(8):
                if r == 3 and c <= 3:
                    continue
                ev.append({'t': 11.0 + c * 0.07 + r * 0.085 + 0.17, 'kind': 'flap', 'n': c * 8 + r, 'soft': 1})
        ev.append({'t': 12.0, 'kind': 'chime'})
        return dict(bpm=bpm, dur=dur, cues={'lift': 2.0 * 2, 'end': 12.0, 'nodrums': 11.0}, events=ev, key='Eb')
    raise SystemExit(f'no timing for {name}')


def compose(name, tm, only=None, norm=True):
    """only='music' leaves out the effects, only='sfx' keeps just them; norm=False skips the peak normalise (for checks)."""
    P = PRESETS[name]
    rng = np.random.default_rng(P['seed'])
    bpm, dur, cues = tm['bpm'], tm['dur'], tm['cues']
    B = 60 / bpm
    bar = 4 * B
    lift = cues.get('lift', cues.get('drop', 0))
    end = cues['end']
    stall = cues.get('stall')
    drop = cues.get('drop')
    nodrums = cues.get('nodrums', end)
    dry, wet = Bus(dur), Bus(dur)
    sfx_dry, sfx_wet = (Bus(dur), Bus(dur)) if only == 'sfx' else (dry, wet)

    def harmony(t):
        """chord notes and key for time t (47 messages switches key at the drop)."""
        if 'post_prog' in P and drop is not None and t >= drop - 1e-6:
            k, prog, t0 = P['post_key'], P['post_prog'], drop
        else:
            k, prog, t0 = P['key'], P['prog'], 0.0
        i = int(np.floor((t - t0) / bar + 1e-6)) % len(prog)
        return k, prog[i]

    def silent(t):
        return stall is not None and stall <= t < drop

    # drums and bass, beat by beat
    nb = int(np.ceil(dur / B)) + 1
    kick_times = []
    for b in range(nb):
        t = b * B
        if t >= nodrums - 1e-6 or silent(t):
            continue
        full = t >= lift - 1e-6
        if drop is not None and drop - B <= t < drop and not silent(t):
            continue  # one beat of air before the drop
        k_on = P['kick'] == 'four' or b % 2 == 0
        if k_on and (full or b % 2 == 0):
            lvl = 1.0 if full else 0.7
            dry.add(kick(lvl), t, 0.55)
            kick_times.append(t)
        # hats on the off-beats, shaker on 16ths once full
        dry.add(hat(b * 7 + 1), t + B / 2, 0.32 if full else 0.22, 0.25)
        if full:
            for s16 in (1, 3):
                dry.add(hat(b * 11 + s16, 0.03, 0.008), t + s16 * B / 4 + 0.012, 0.12, -0.3)
            if b % 4 in (1, 3):
                dry.add(clap(b), t, 0.42, 0.05)
                wet.add(clap(b), t, 0.12)
    # bass
    nbar = int(np.ceil(dur / bar)) + 1
    for i in range(nbar):
        t0 = i * bar
        for j, off in enumerate(P['bass']):
            t = t0 + off * B
            if t < lift - 1e-6 or t >= nodrums - 1e-6 or silent(t):
                continue
            if drop is not None and drop - B <= t < drop:
                continue
            k, (deg, q) = harmony(t)
            root = k - 12 + DEG[deg]
            nxt = P['bass'][j + 1] * B if j + 1 < len(P['bass']) else bar
            d = min(nxt - off * B, B * 1.5) * 0.92
            dry.add(bass_note(mhz(root), d), t, 0.42)
    # pad, a chord a bar (held through the stall), then the final chord on the end card
    for i in range(nbar):
        t0 = i * bar
        if t0 >= end - 1e-6 or ('post_prog' in P and drop is not None and t0 >= drop - 1e-6):
            break
        t1 = min(t0 + bar, end)
        k, (deg, q) = harmony(t0)
        if 'post_prog' in P and drop is not None and t0 < drop < t1:
            t1 = drop
        for m in chord_notes(k, deg, q, 1):
            sig = pad_note(mhz(m), t1 - t0 + 0.25, P['bright'])
            dry.add(sig, t0, 0.15, rng.uniform(-0.4, 0.4))
            wet.add(sig, t0, 0.12)
    if 'post_prog' in P and drop is not None:
        # the drop bar starts on its own downbeat
        tb = drop
        while tb < end - 1e-6:
            k, (deg, q) = harmony(tb)
            t1 = min(tb + bar, end)
            for m in chord_notes(k, deg, q, 1):
                sig = pad_note(mhz(m), t1 - tb + 0.25, P['bright'])
                dry.add(sig, tb, 0.15, rng.uniform(-0.4, 0.4))
                wet.add(sig, tb, 0.12)
            tb += bar
    # pluck arpeggio
    step = P['step'] * B
    ns = int(np.ceil(end / step))
    for s in range(ns):
        t = s * step
        if silent(t) or t >= end - 1e-6:
            continue
        if step < B / 2 and t < lift - 1e-6 and s % 2:
            continue  # sparser before the lift
        k, (deg, q) = harmony(t)
        notes = chord_notes(k, deg, q, 2 if k < 55 else 1)
        m = notes[P['arp'][s % len(P['arp'])] % len(notes)]
        acc = 1.0 if s % int(round(B / step)) == 0 else 0.75
        sig = pluck(mhz(m), 0.8, P['bright'], rng)
        pan = 0.35 * np.sin(s * 0.9)
        dry.add(sig, t, 0.26 * acc, pan)
        wet.add(sig, t, 0.1 * acc)
    # end card: the home chord, rolled, with a soft low root
    k0, prog0 = (P.get('post_key', P['key']), P.get('post_prog', P['prog']))
    deg0, q0 = prog0[0]
    final = chord_notes(k0, deg0, 'maj9' if 'm' not in q0 else q0, 1)
    tail = dur - end + 1.0
    for i, m in enumerate(final):
        sig = pad_note(mhz(m), tail, P['bright'])
        dry.add(sig, end, 0.17, (i - 2) * 0.2)
        wet.add(sig, end, 0.16)
    for i, m in enumerate(chord_notes(k0, deg0, 'add9', 2 if k0 < 55 else 1)):
        sig = pluck(mhz(m), 1.6, P['bright'], rng)
        dry.add(sig, end + i * B / 4, 0.2, (i - 1.5) * 0.25)
        wet.add(sig, end + i * B / 4, 0.16)
    dry.add(bass_note(mhz(k0 - 12 + DEG[deg0]), min(tail, 2.5)), end, 0.5)
    dry.add(kick(0.9), end, 0.8)
    kick_times.append(end)

    # effects on the page's events
    if only == 'sfx':
        dry, wet = sfx_dry, sfx_wet
    if only == 'music':
        tm = dict(tm, events=[])
    scale = [0, 2, 4, 7, 9, 12]
    pop_root = 67 + (k0 - 67) % 12      # G4..F#5
    chime_root = 79 + (k0 - 79) % 12    # G5..F#6
    blip_root = 72 + (k0 - 72) % 12
    for e in tm['events']:
        t, kind, n = e['t'], e['kind'], e.get('n', 0)
        if kind == 'pop':
            f = mhz(pop_root + scale[n % len(scale)])
            dry.add(pop_sfx(f), t, 0.42, 0.15 * ((n % 5) - 2))
            wet.add(pop_sfx(f), t, 0.1)
        elif kind == 'tap':
            dry.add(tap_sfx(int(t * 1000)), t, 0.35)
        elif kind == 'chime':
            for i, iv in enumerate((7, 12)):
                sig = chime_sfx(mhz(chime_root + iv))
                dry.add(sig, t + i * 0.09, 0.3, -0.2 + 0.4 * i)
                wet.add(sig, t + i * 0.09, 0.22)
        elif kind == 'whoosh':
            sig = whoosh_sfx(int(t * 100))
            dry.add(sig, t - 0.3, 0.55)
            wet.add(sig, t - 0.3, 0.2)
        elif kind == 'blip':
            f = mhz(blip_root + scale[(n * 2) % 6])
            dry.add(blip_sfx(f), t, 0.26, 0.3 * (n % 3 - 1))
        elif kind == 'thunk':
            dry.add(thunk_sfx(int(t * 1000)), t, 0.55)
            wet.add(thunk_sfx(int(t * 1000)), t, 0.12)
        elif kind == 'spin':
            # a ratchet that slows as the reels stop
            tt, t1 = t, e['t1']
            i = 0
            while tt < t1:
                k = (tt - t) / (t1 - t)
                dry.add(tick_sfx(i + int(t * 100)), tt, 0.4 * (1 - 0.4 * k), 0.4 * np.sin(i))
                tt += 0.045 + 0.11 * k ** 2
                i += 1
        elif kind == 'flap':
            dry.add(flap_sfx(n * 13 + 5), t, 0.2 if e.get('soft') else 0.32, 0.5 * np.sin(n * 1.7))

    # sidechain: pad and plucks breathe with the kick
    duck = np.ones(dry.n)
    for tk in kick_times:
        i = int(tk * SR)
        L = int(0.3 * SR)
        seg = 1 - 0.3 * np.exp(-np.arange(L) / (0.09 * SR))
        j = min(dry.n, i + L)
        duck[i:j] = np.minimum(duck[i:j], seg[: j - i])
    irl, irr = reverb_ir()
    wl = fftconvolve(wet.l * duck, irl)[: dry.n]
    wr = fftconvolve(wet.r * duck, irr)[: dry.n]
    L = dry.l + wl * 0.9
    R = dry.r + wr * 0.9
    n = int(round(dur * SR))
    out = np.stack([L[:n], R[:n]], 1)
    # fade the last 0.35 s, gentle limiter
    f = int(0.35 * SR)
    out[-f:] *= np.linspace(1, 0, f)[:, None] ** 1.5
    out[: int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))[:, None]
    if not norm:
        return out
    out /= np.max(np.abs(out)) + 1e-9
    out = np.tanh(1.6 * out) / np.tanh(1.6)
    return out * 0.89


def main():
    name, timing, out = sys.argv[1], sys.argv[2], sys.argv[3]
    tm = art_timing(name) if timing == '-' else json.load(open(timing))
    y = compose(name, tm)
    from scipy.io import wavfile
    wavfile.write(out, SR, y.astype(np.float32))
    print('wrote', out, f'{len(y) / SR:.2f}s')


if __name__ == '__main__':
    main()
