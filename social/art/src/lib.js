/* Shared helpers for the Galley mosaic art renders (deterministic, no CSS animation). */
(function () {
  'use strict';
  const G = window.GM_GLYPHS, C = window.GM_CITIES;
  const KEYS = Object.keys(G);
  const rng = (seed) => () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const shuffled = (arr, seed) => {
    const r = rng(seed), a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
    return a;
  };
  // CSS cubic-bezier, solved for x
  function bezier(x1, y1, x2, y2) {
    const cx = 3 * x1, bx = 3 * (x2 - x1) - cx, ax = 1 - cx - bx;
    const cy = 3 * y1, by = 3 * (y2 - y1) - cy, ay = 1 - cy - by;
    const sx = (t) => ((ax * t + bx) * t + cx) * t, sy = (t) => ((ay * t + by) * t + cy) * t;
    const dx = (t) => (3 * ax * t + 2 * bx) * t + cx;
    return (x) => {
      if (x <= 0) return 0; if (x >= 1) return 1;
      let t = x;
      for (let i = 0; i < 8; i++) { const e = sx(t) - x; const d = dx(t); if (Math.abs(e) < 1e-7 || Math.abs(d) < 1e-7) break; t -= e / d; }
      t = Math.min(1, Math.max(0, t));
      return sy(t);
    };
  }
  const EASE = { inOut: bezier(.42, 0, .58, 1), in: bezier(.42, 0, 1, 1), out: bezier(0, 0, .58, 1), ease: bezier(.25, .1, .25, 1) };
  const clamp01 = (v) => Math.max(0, Math.min(1, v));
  const ramp = (t, a, b) => clamp01((t - a) / (b - a));

  // A glyph as an <svg> element; colours: f (landmark), d + dOp (behind), a (warm detail).
  const NS = 'http://www.w3.org/2000/svg';
  function glyph(key, size, col) {
    const s = document.createElementNS(NS, 'svg');
    s.setAttribute('viewBox', '0 0 64 64');
    s.setAttribute('width', size); s.setAttribute('height', size);
    s.style.overflow = 'visible'; s.style.display = 'block';
    const acc = [];
    for (const l of G[key].layers) {
      const p = document.createElementNS(NS, 'path');
      p.setAttribute('d', l.d);
      const tone = l.tone || 'fg';
      const c = tone === 'accent' ? col.a : col.f;
      if (l.stroke) { p.setAttribute('fill', 'none'); p.setAttribute('stroke', c); p.setAttribute('stroke-width', l.stroke); p.setAttribute('stroke-linecap', 'round'); }
      else p.setAttribute('fill', c);
      if (l.evenodd) p.setAttribute('fill-rule', 'evenodd');
      if (tone === 'dim') p.setAttribute('opacity', col.dOp);
      if (tone === 'accent') acc.push(p);
      s.appendChild(p);
    }
    s._acc = acc;
    return s;
  }
  // The brand pin as an inline svg string (site header shape).
  const PIN = (needle) => `<svg class="pin" viewBox="-60.7 -92.1 61.7 92.1" aria-hidden="true"><path d="M-33.25 -68.40 L-38.11 -65.81 L0 0Z" fill="${needle}"/><circle cx="-35.68" cy="-67.10" r="24" fill="#F2A93B"/></svg>`;
  function wordmark(px, ink) {
    const d = document.createElement('div');
    d.className = 'wm';
    d.style.fontSize = px + 'px';
    d.style.color = ink;
    d.innerHTML = 'galley' + PIN(ink);
    return d;
  }
  window.ART = { G, C, KEYS, rng, shuffled, EASE, bezier, clamp01, ramp, glyph, wordmark };
})();
