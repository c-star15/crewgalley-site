// Shared pieces for the week 1 Reels: palette, easing, the wordmark, the app's
// light-mode components (rebuilt from crew-hub app/src/components, scaled up),
// the Illustration label, headlines and the end card.
(function () {
  const C = { ink: '#13213A', amber: '#F2A93B', cream: '#F4EFE6', page: '#0B1424', softOnInk: '#B7C0D1', softOnCream: '#4A5468' };
  // crew-hub app/src/theme.ts, ink.light
  const APP = {
    bg: '#F3F5F9', surface: '#FFFFFF', surface2: '#E9EDF4', border: '#D9DEE8', text: '#0B1430', muted: '#4A5470',
    faint: '#6B7590', accent: '#FFB800', accentText: '#0B1430', link: '#8A5E00', signalSoft: '#FFF3CC',
    success: '#1E8E5A', successSoft: '#E3F3EB',
  };

  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const ramp = (t, a, b) => clamp((t - a) / (b - a));
  const EASE = {
    out: (k) => 1 - Math.pow(1 - k, 3),
    in: (k) => k * k * k,
    inOut: (k) => (k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2),
    back: (k) => { const c = 1.6; return 1 + (c + 1) * Math.pow(k - 1, 3) + c * Math.pow(k - 1, 2); },
  };
  // a pop: 0 -> overshoot -> 1 over d seconds
  const pop = (t, t0, d = 0.28) => (t < t0 ? 0 : EASE.back(ramp(t, t0, t0 + d)));
  function rng(seed) { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }

  function h(tag, style, inner) {
    const e = document.createElement(tag);
    if (style) Object.assign(e.style, style);
    if (inner != null) {
      if (Array.isArray(inner)) inner.forEach((c) => c && e.appendChild(c));
      else if (inner instanceof Node) e.appendChild(inner);
      else e.innerHTML = inner;
    }
    return e;
  }
  const px = (v) => `${Math.round(v * 10) / 10}px`;
  function icon(name, size, color) {
    const s = `<svg viewBox="0 0 512 512" width="${size}" height="${size}" aria-hidden="true" style="display:block;color:${color}">${window.IONICONS[name]}</svg>`;
    return h('span', { display: 'inline-flex', width: px(size), height: px(size), flex: '0 0 auto' }, s);
  }

  // lowercase galley, Inter Black, the pin as its full stop
  function wordmark(size, fg) {
    return h('span', { fontSize: px(size), color: fg, display: 'inline-block' },
      `galley<svg viewBox="-60.7 -92.1 61.7 92.1" aria-hidden="true"><path d="M-33.25 -68.40 L-38.11 -65.81 L0 0Z" fill="${fg}"></path><circle cx="-35.68" cy="-67.1" r="24" fill="${C.amber}"></circle></svg>`);
  }

  // Illustration label, as crewgalley.app's .mock-label: right-aligned above the mock, like the week 1 posts
  function illus(stage, right, top, onInk) {
    const e = h('div', { right: px(1080 - right), top: px(top), color: onInk ? C.softOnInk : C.softOnCream }, 'Illustration');
    e.className = 'ill';
    stage.appendChild(e);
    return e;
  }

  // ---------------------------------------------------------------------------
  // Headlines: Inter Black, word by word in, out together
  // ---------------------------------------------------------------------------
  function Headlines(stage, list, opts) {
    const o = Object.assign({ top: 300, size: 124, color: C.cream, max: 888, stagger: 0.07 }, opts);
    const items = list.map((it) => {
      const p = h('p', { top: px(it.top ?? o.top), color: it.color || o.color, opacity: 0 });
      p.className = 'head';
      const words = [];
      it.lines.forEach((line, li) => {
        if (li) p.appendChild(document.createElement('br'));
        line.split(' ').forEach((w, wi) => {
          if (wi) p.appendChild(document.createTextNode(' '));
          const s = h('span', null, w); s.className = 'w';
          if (it.style && it.style[`${li}`]) Object.assign(s.style, it.style[`${li}`]);
          p.appendChild(s); words.push({ s, li, at: it.at ? it.at[words.length] : null });
        });
      });
      stage.appendChild(p);
      return { ...it, p, words };
    });
    function fit() {
      for (const it of items) {
        let size = it.size || o.size;
        it.p.style.fontSize = px(size);
        it.p.style.opacity = 1;
        while (it.p.offsetWidth > o.max && size > 60) { size -= 2; it.p.style.fontSize = px(size); }
        it.p.style.opacity = 0;
      }
    }
    function render(t) {
      for (const it of items) {
        const tOut = it.t1 ?? 1e9;
        if (t < it.t0 - 0.01 || t > tOut + 0.4) { it.p.style.opacity = 0; continue; }
        it.p.style.opacity = 1;
        const ko = EASE.in(ramp(t, tOut, tOut + 0.26));
        it.words.forEach((w, i) => {
          const start = w.at != null ? w.at : it.t0 + i * (it.stagger ?? o.stagger);
          const k = EASE.out(ramp(t, start, start + 0.34));
          w.s.style.opacity = (k * (1 - ko)).toFixed(3);
          w.s.style.transform = `translateY(${((1 - k) * 56 - ko * 40).toFixed(1)}px)`;
        });
      }
    }
    return { items, fit, render };
  }

  // ---------------------------------------------------------------------------
  // ActivityCard (app/src/components/activity-card.tsx), light mode, scale S
  // a = { title, meta, icon, max, label? } ; state per frame: n (dots in), joined, press, dotPop[i]
  // ---------------------------------------------------------------------------
  function ActivityCard(a, S, width) {
    const iconEl = h('div', { flex: '0 0 auto', width: px(44 * S), height: px(44 * S), borderRadius: px(22 * S), background: APP.signalSoft, display: 'flex', alignItems: 'center', justifyContent: 'center' }, icon(a.icon, 22 * S, APP.link));
    const mid = h('div', { flex: '1 1 auto', minWidth: 0, display: 'flex', flexDirection: 'column', gap: px(3 * S) });
    if (a.label) mid.appendChild(h('span', { fontSize: px(12 * S), fontWeight: 800, color: APP.link, letterSpacing: px(0.2 * S), whiteSpace: 'nowrap' }, a.label));
    mid.appendChild(h('span', { fontSize: px(17 * S), lineHeight: 1.2, fontWeight: 700, color: APP.text, whiteSpace: 'nowrap' }, a.title));
    mid.appendChild(h('span', { fontSize: px(14 * S), lineHeight: 1.25, color: APP.muted, whiteSpace: 'nowrap' }, a.meta));
    const pillBox = h('div', { position: 'relative', width: px(64 * S), height: px(32 * S) });
    const join = h('div', { position: 'absolute', inset: 0, borderRadius: '999px', background: APP.accent, color: APP.accentText, fontSize: px(15 * S), fontWeight: 800, display: 'flex', alignItems: 'center', justifyContent: 'center' }, 'Join');
    const inPill = h('div', { position: 'absolute', inset: 0, borderRadius: '999px', background: APP.successSoft, color: APP.success, fontSize: px(15 * S), fontWeight: 800, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: px(3 * S), opacity: 0 },
      [icon('checkmark', 14 * S, APP.success), h('span', null, 'In')]);
    pillBox.appendChild(join); pillBox.appendChild(inPill);
    const dotsRow = h('div', { display: 'flex', gap: px(3 * S) });
    const dots = [];
    for (let i = 0; i < a.max; i++) {
      const d = h('span', { position: 'relative', width: px(7 * S), height: px(7 * S), borderRadius: px(4 * S), border: `${px(1.5 * S)} solid ${APP.border}` });
      const fill = h('span', { position: 'absolute', left: px(-1.5 * S), top: px(-1.5 * S), width: px(7 * S), height: px(7 * S), borderRadius: px(4 * S), background: APP.link, transform: 'scale(0)' });
      d.appendChild(fill); dotsRow.appendChild(d); dots.push({ d, fill });
    }
    const right = h('div', { flex: '0 0 auto', minWidth: px(64 * S), display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: px(8 * S) }, [pillBox, dotsRow]);
    const el = h('div', { width: px(width), display: 'flex', alignItems: 'center', gap: px(16 * S), padding: `${px(14 * S)} ${px(16 * S)}`, borderRadius: px(16 * S), background: APP.surface, color: APP.text }, [iconEl, mid, right]);
    el.className = 'app';
    // state: dotK[i] in 0..1 (fill scale), joinK 0..1 (Join -> In), press 0..1
    function set({ dotK, joinK = 0, press = 0 }) {
      dots.forEach((x, i) => { const k = dotK[i] ?? 0; x.fill.style.transform = `scale(${k.toFixed(3)})`; x.d.style.borderColor = k > 0.5 ? 'transparent' : APP.border; });
      join.style.opacity = (1 - joinK).toFixed(3);
      inPill.style.opacity = joinK.toFixed(3);
      pillBox.style.transform = `scale(${(1 - 0.08 * press).toFixed(3)})`;
    }
    return { el, set, dots };
  }

  // ---------------------------------------------------------------------------
  // DayStrip cell (app/src/components/day-strip.tsx): selected = dark fill,
  // free = soft amber fill with an amber weekday, plans = dots
  // ---------------------------------------------------------------------------
  function DayCell(c, S) {
    const dow = h('span', { fontSize: px(11 * S), fontWeight: 600, color: APP.muted, whiteSpace: 'nowrap' }, c.dow);
    const num = h('span', { fontSize: px(20 * S), fontWeight: 800, color: APP.text, letterSpacing: px(-0.4 * S), lineHeight: 1.15 }, String(c.num));
    const dots = h('div', { display: 'flex', gap: px(3 * S), height: px(6 * S), marginTop: px(3 * S) });
    const dl = [];
    for (let i = 0; i < (c.dots || 0); i++) { const d = h('span', { width: px(5 * S), height: px(5 * S), borderRadius: px(3 * S), background: APP.link }); dots.appendChild(d); dl.push(d); }
    const el = h('div', { width: px(50 * S), height: px(66 * S), borderRadius: px(12 * S), background: APP.surface, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }, [dow, num, dots]);
    el.className = 'app';
    function set({ free = 0, sel = 0 }) {
      // free: blend surface -> signalSoft; sel: -> text (dark)
      el.style.background = sel > 0.5 ? APP.text : free > 0.5 ? APP.signalSoft : APP.surface;
      dow.style.color = sel > 0.5 ? APP.bg : free > 0.5 ? APP.link : APP.muted;
      dow.style.fontWeight = free > 0.5 && sel <= 0.5 ? 700 : 600;
      num.style.color = sel > 0.5 ? APP.bg : APP.text;
      dl.forEach((d) => (d.style.background = sel > 0.5 ? APP.accent : APP.link));
    }
    set({});
    return { el, set };
  }

  // a light app screen inside a phone outline that runs off the bottom of the frame
  function Phone(stage, top, onInk, opts = {}) {
    const left = opts.left ?? 60, w = opts.w ?? 960;
    const frame = h('div', {
      position: 'absolute', left: px(left), top: px(top), width: px(w), height: px(1920 - top + 200), borderRadius: '96px',
      background: APP.bg, border: onInk ? '12px solid #2A3A5C' : `12px solid ${APP.text}`, overflow: 'hidden',
    });
    const inner = h('div', { position: 'absolute', left: 0, top: 0, width: '100%', height: '100%' });
    frame.appendChild(inner);
    stage.appendChild(frame);
    return { frame, inner, left, w, top };
  }

  // ---------------------------------------------------------------------------
  // End card: wordmark, "Life beyond the roster.", then "Opening soon"
  // ---------------------------------------------------------------------------
  function EndCard(stage, bg, fg, soft, soonText) {
    const box = h('div', { position: 'absolute', inset: 0, background: bg, opacity: 0 });
    const wm = wordmark(196, fg); wm.className = 'wm';
    const wmBox = h('div', { position: 'absolute', left: 0, right: 0, top: '640px', textAlign: 'center' }, wm);
    const line = h('p', { position: 'absolute', left: 0, right: 0, top: '930px', margin: 0, textAlign: 'center', fontSize: '76px', fontWeight: 900, letterSpacing: '-.04em', color: fg, lineHeight: 1, fontVariationSettings: '"opsz" 32' });
    const words = 'Life beyond the roster.'.split(' ').map((w) => { const s = h('span', { display: 'inline-block' }, w); return s; });
    words.forEach((s, i) => { if (i) line.appendChild(document.createTextNode(' ')); line.appendChild(s); });
    const soon = h('p', { position: 'absolute', left: 0, right: 0, top: '1060px', margin: 0, textAlign: 'center', fontSize: '42px', fontWeight: 600, letterSpacing: '-.01em', color: soft }, soonText || 'Opening soon');
    box.appendChild(wmBox); box.appendChild(line); box.appendChild(soon);
    stage.appendChild(box);
    // t0: card in; t1: Opening soon
    function render(t, t0, t1) {
      const k = EASE.out(ramp(t, t0, t0 + 0.35));
      box.style.opacity = k.toFixed(3);
      box.style.visibility = k > 0 ? 'visible' : 'hidden';
      const kw = EASE.out(ramp(t, t0 + 0.05, t0 + 0.6));
      wmBox.style.opacity = kw.toFixed(3);
      wmBox.style.transform = `translateY(${((1 - kw) * 30).toFixed(1)}px) scale(${(0.94 + 0.06 * kw).toFixed(4)})`;
      words.forEach((s, i) => {
        const a = t0 + 0.35 + i * 0.09, kk = EASE.out(ramp(t, a, a + 0.34));
        s.style.opacity = kk.toFixed(3); s.style.transform = `translateY(${((1 - kk) * 40).toFixed(1)}px)`;
      });
      const ks = EASE.out(ramp(t, t1, t1 + 0.4));
      soon.style.opacity = ks.toFixed(3); soon.style.transform = `translateY(${((1 - ks) * 20).toFixed(1)}px)`;
    }
    return { render };
  }

  window.LIB = { C, APP, clamp, ramp, EASE, pop, rng, h, px, icon, wordmark, illus, Headlines, ActivityCard, DayCell, Phone, EndCard };
})();
