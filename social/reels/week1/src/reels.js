// Week 1 Reels (28 Oct 2026). Each reel builds its DOM once and returns
// { bpm, dur, cues, events, render(t) }. Timing is on the music's beat grid,
// so the soundtrack (music.py) lands on the same frames: events are the
// sounds (pop, tap, chime, whoosh, tick, thunk), cues the music's sections.
(function () {
  const { C, APP, ramp, EASE, pop, rng, h, px, icon, illus, Headlines, ActivityCard, DayCell, Phone, EndCard } = window.LIB;
  const S = 2.4; // app points -> px

  // a dot is a person; you are the amber one
  function personDot(size, fill, ring) {
    return h('div', { position: 'absolute', width: px(size), height: px(size), borderRadius: '50%', background: fill, border: ring ? `${px(size * 0.16)} solid ${ring}` : 'none', transform: 'scale(0)' });
  }

  // ===========================================================================
  // Thu: Off today?
  // ===========================================================================
  function offToday(stage) {
    const bpm = 124, B = 60 / bpm, T = (b) => b * B;
    stage.style.background = C.ink;
    const events = [];
    const heads = Headlines(stage, [
      { lines: ['Off today?'], t0: 0.12, t1: T(6) - 0.28 },
      { lines: ['So are 13 crew.'], t0: T(6), t1: T(14) - 0.28 },
      { lines: ['One spot left', 'at sunrise yoga.'], t0: T(14), t1: T(22) - 0.28 },
    ], { color: C.cream });

    const PT = 720;
    const lab = illus(stage, 984, PT - 64, true);
    const ph = Phone(stage, PT, true);
    const content = h('div', { position: 'absolute', left: 0, top: 0, width: '100%' });
    ph.inner.appendChild(content);
    const P = 16 * S; // side padding
    const add = (e, x, y) => { Object.assign(e.style, { position: 'absolute', left: px(x), top: px(y) }); content.appendChild(e); return e; };

    // header: Dubai / Make the most of your days off.  [calendar] [avatar]
    const hdr = h('div', { width: px(936 - 2 * P), display: 'flex', alignItems: 'center', gap: px(8 * S) }, [
      h('div', { flex: 1, display: 'flex', flexDirection: 'column' }, [
        h('span', { fontSize: px(28 * S), lineHeight: px(34 * S), fontWeight: 800, letterSpacing: px(-0.6 * S), color: APP.text }, 'Dubai'),
        h('span', { fontSize: px(15 * S), color: APP.muted }, 'Make the most of your days off.'),
      ]),
      h('div', { width: px(44 * S), height: px(44 * S), borderRadius: '50%', background: APP.surface, display: 'flex', alignItems: 'center', justifyContent: 'center' }, icon('calendar-outline', 22 * S, APP.text)),
      h('div', { width: px(36 * S), height: px(36 * S), borderRadius: '50%', background: APP.surface2, display: 'flex', alignItems: 'center', justifyContent: 'center' }, icon('person', 18 * S, APP.faint)),
    ]);
    hdr.className = 'app';
    add(hdr, P, 18 * S);

    // day strip
    const days = [['Today', 12, 3], ['Fri', 13, 1], ['Sat', 14, 3], ['Sun', 15, 2], ['Mon', 16, 0], ['Tue', 17, 1], ['Wed', 18, 2]];
    const cells = days.map(([dow, num, dots], i) => { const c = DayCell({ dow, num, dots }, S); add(c.el, P + i * 56 * S, 80 * S); return c; });

    // free line: Today · Not free [I'm free]  ->  Today · Free all day  Edit
    const fy = 80 * S + 66 * S + 16 * S;
    const freeBox = h('div', { width: px(936 - 2 * P), height: px(48 * S), borderRadius: px(12 * S), background: APP.surface, display: 'flex', alignItems: 'center', gap: px(16 * S), padding: `0 ${px(16 * S)}` });
    freeBox.className = 'app';
    const freeText = h('span', { flex: 1, fontSize: px(15 * S), fontWeight: 800, color: APP.text, whiteSpace: 'nowrap' });
    const notFree = h('span', { fontSize: px(14 * S), fontWeight: 400, color: APP.muted }, ' · Not free');
    const isFree = h('span', { fontSize: px(14 * S), fontWeight: 600, color: APP.link }, ' · Free all day');
    freeText.appendChild(document.createTextNode('Today')); freeText.appendChild(notFree); freeText.appendChild(isFree);
    const freeBtn = h('div', { padding: `0 ${px(14 * S)}`, height: px(34 * S), borderRadius: '999px', background: APP.accent, color: APP.accentText, fontSize: px(14 * S), fontWeight: 800, display: 'flex', alignItems: 'center' }, "I'm free");
    const edit = h('span', { fontSize: px(15 * S), fontWeight: 700, color: APP.link }, 'Edit');
    freeBox.appendChild(freeText); freeBox.appendChild(freeBtn); freeBox.appendChild(edit);
    freeBox.appendChild(icon('information-circle-outline', 18 * S, APP.muted));
    add(freeBox, P, fy);

    // counts + who's free
    const cy = fy + 48 * S + 10 * S;
    const counts = add(h('span', { fontSize: px(15 * S), fontWeight: 700, color: APP.text, whiteSpace: 'nowrap' }), P, cy);
    counts.className = 'app';
    const sy = cy + 20 * S + 20 * S;
    const sec = add(h('span', { fontSize: px(20 * S), fontWeight: 800, color: APP.text, letterSpacing: px(-0.3 * S), opacity: 0 }, 'Free today'), P, sy);
    sec.className = 'app';
    const dy = sy + 30 * S + 10 * S, D = 17 * S, G = 6.2 * S;
    const people = [];
    for (let i = 0; i < 14; i++) {
      const d = personDot(D, i === 0 ? APP.surface : APP.text, i === 0 ? APP.accent : null);
      add(d, P + i * (D + G), dy); people.push(d);
    }
    // plans
    const hy = dy + D + 26 * S;
    const happen = h('div', { width: px(936 - 2 * P), display: 'flex', alignItems: 'center', justifyContent: 'space-between' }, [
      h('span', { fontSize: px(20 * S), fontWeight: 800, color: APP.text, letterSpacing: px(-0.3 * S) }, 'Happening in Dubai'),
      h('span', { display: 'flex', alignItems: 'center', gap: px(2 * S), fontSize: px(15 * S), fontWeight: 700, color: APP.link }, [icon('add', 17 * S, APP.link), h('span', null, 'Create plan')]),
    ]);
    happen.className = 'app';
    add(happen, P, hy);
    const card = ActivityCard({ title: 'Sunrise yoga', meta: '06:30 · Kite Beach', icon: 'body-outline', max: 8 }, S, 936 - 2 * P);
    add(card.el, P, hy + 20 * S + 12 * S);
    const ring = h('div', { position: 'absolute', width: px(7 * S), height: px(7 * S), borderRadius: '50%', border: `${px(1.5 * S)} solid ${APP.accent}`, opacity: 0 });
    card.dots[7].d.appendChild(ring);
    Object.assign(ring.style, { left: px(-1.5 * S), top: px(-1.5 * S) });

    // timing
    const tTap = T(3), tPeople = T(6.5), tScroll = T(14), tJoin = T(19), tEnd = T(22), tSoon = T(24);
    events.push({ t: tTap, kind: 'tap' }, { t: tTap + 0.03, kind: 'pop', n: 4 });
    const popAt = (i) => tPeople + (i === 0 ? 0 : B / 2 + (i - 1) * B / 4);
    for (let i = 0; i < 14; i++) events.push({ t: popAt(i), kind: 'pop', n: i === 0 ? 0 : 1 + (i % 7) });
    events.push({ t: tScroll - 0.12, kind: 'whoosh' }, { t: tJoin, kind: 'tap' }, { t: tJoin + 0.06, kind: 'chime' });
    const end = EndCard(stage, C.ink, C.cream, C.softOnInk);

    function render(t) {
      heads.render(t);
      const kIn = EASE.out(ramp(t, 0.15, 0.75));
      ph.frame.style.transform = `translateY(${((1 - kIn) * 140).toFixed(1)}px)`;
      ph.frame.style.opacity = kIn.toFixed(3);
      lab.style.opacity = (0.75 * EASE.out(ramp(t, 0.5, 0.9))).toFixed(3);
      // tap I'm free
      const freeK = t >= tTap + 0.06 ? 1 : 0;
      const press = Math.max(0, 1 - Math.abs(t - tTap) / 0.12);
      freeBtn.style.transform = `scale(${(1 - 0.08 * press).toFixed(3)})`;
      freeBtn.style.display = freeK ? 'none' : 'flex'; edit.style.display = freeK ? 'inline' : 'none';
      notFree.style.display = freeK ? 'none' : 'inline'; isFree.style.display = freeK ? 'inline' : 'none';
      cells.forEach((c, i) => c.set({ sel: i === 0 ? 1 : 0, free: i === 0 && freeK ? 1 : 0 }));
      // who's free
      sec.style.opacity = EASE.out(ramp(t, T(6), T(6) + 0.4)).toFixed(3);
      let n = 0;
      people.forEach((d, i) => { const k = pop(t, popAt(i), 0.3); d.style.transform = `scale(${k.toFixed(3)})`; if (i && t >= popAt(i)) n++; });
      counts.textContent = n ? `${n} crew free` : '';
      // scroll to the plan
      const ks = EASE.inOut(ramp(t, tScroll, tScroll + 0.6));
      content.style.transform = `translateY(${(-ks * 300).toFixed(1)}px)`;
      // the open spot pulses, then you join
      const joined = t >= tJoin + 0.05;
      const dotK = Array.from({ length: 8 }, (_, i) => (i < 7 ? 1 : pop(t, tJoin + 0.05, 0.3)));
      card.set({ dotK, joinK: EASE.out(ramp(t, tJoin + 0.02, tJoin + 0.2)), press: Math.max(0, 1 - Math.abs(t - tJoin) / 0.12) });
      const pulse = t > tScroll + 0.4 && !joined ? 0.5 + 0.5 * Math.sin((t - tScroll) * Math.PI * 2 / (2 * B)) : 0;
      ring.style.opacity = pulse.toFixed(3);
      ring.style.transform = `scale(${(1 + 0.6 * pulse).toFixed(3)})`;
      end.render(t, tEnd, tSoon);
    }
    return { bpm, dur: T(28), cues: { lift: T(6), drop: T(14), end: tEnd }, events, render, cover: T(17.5), key: 'F' };
  }

  // ===========================================================================
  // Fri: 47 messages
  // ===========================================================================
  function messages(stage) {
    const bpm = 126, B = 60 / bpm, T = (b) => b * B;
    stage.style.background = C.cream;
    const events = [];
    const LINES = [
      'brunch saturday?', 'yesss', 'which place', 'the one by the marina?', 'too far for me', 'I land at 11', 'so 1pm?',
      "I'm on standby sat", 'sunday then?', "can't, early report", 'ok saturday it is', 'wait what time', '1pm', 'make it 2?',
      "who's booking", 'not me lol', "I'll check", 'they want a deposit', 'how much', 'per person?', 'is it the pancake one',
      'focus pls', 'ok vote', '1pm or 2pm', '1', '2', 'either', 'roster just changed', 'noooo', 'next weekend?', "I'm away",
      'same', 'ok THIS weekend', 'fine', 'where again', 'scroll up', 'no', 'someone make a plan', 'you make it', "I'm napping",
      'lol', "ok who's in", 'me maybe', 'depends', 'on what', 'the roster', '…',
    ];
    const N = 47;
    const r = rng(47);
    const senders = LINES.map((_, i) => (i === 0 ? 1 : i % 5 === 3 ? 0 : 1 + Math.floor(r() * 5)));
    const arrive = (i) => 0.1 + 4.45 * Math.pow((i + 1) / N, 0.62); // i = 0..46

    const heads = Headlines(stage, [
      { lines: ['47 messages.', '0 plans.'], t0: 0.12, t1: T(12) - 0.28, at: [0.12, 0.19, T(10), T(10) + 0.07] },
      { lines: ['1 plan.', '4 crew.', 'Done.'], t0: T(12), t1: T(17) - 0.28, at: [T(12), T(12) + 0.07, T(13), T(13) + 0.07, T(14)] },
    ], { color: C.ink });
    const countSpan = heads.items[0].words[0].s, wordSpan = heads.items[0].words[1].s;

    const PT = 700;
    const lab = illus(stage, 984, PT - 64, false);
    const ph = Phone(stage, PT, false);
    // chat header
    const SH = ['#13213A', '#4A5470', '#8A93A8', '#2B3A57', '#6B7590', '#B4BCCF'];
    const hdr = h('div', { position: 'absolute', left: 0, top: 0, width: '100%', height: px(56 * S), background: APP.surface, borderBottom: `2px solid ${APP.border}`, display: 'flex', alignItems: 'center', gap: px(10 * S), padding: `0 ${px(16 * S)}` }, [
      icon('chevron-back', 24 * S, APP.text),
      h('div', { display: 'flex', flexDirection: 'column', gap: px(2 * S) }, [
        h('span', { fontSize: px(17 * S), fontWeight: 700, color: APP.text }, 'Saturday brunch?'),
        h('span', { display: 'flex', gap: px(3 * S) }, SH.map((c) => h('span', { width: px(8 * S), height: px(8 * S), borderRadius: '50%', background: c }))),
      ]),
    ]);
    hdr.className = 'app';
    const view = h('div', { position: 'absolute', left: 0, top: px(56 * S), width: '100%', height: px(850 - 56 * S), overflow: 'hidden' });
    const composer = h('div', { position: 'absolute', left: 0, top: px(850), width: '100%', height: '400px', background: APP.surface, borderTop: `2px solid ${APP.border}`, padding: `${px(10 * S)} ${px(14 * S)}` },
      h('div', { height: px(40 * S), borderRadius: '999px', background: APP.bg, display: 'flex', alignItems: 'center', padding: `0 ${px(16 * S)}`, fontSize: px(16 * S), color: APP.faint }, 'Message'));
    composer.className = 'app';
    ph.inner.appendChild(composer);
    const list = h('div', { position: 'absolute', left: 0, top: 0, width: '100%' });
    view.appendChild(list); ph.inner.appendChild(view); ph.inner.appendChild(hdr);
    const bubbles = [];
    let y = 0;
    const GAP = 6 * S;
    for (let i = 0; i < N; i++) {
      const mine = senders[i] === 0;
      const row = h('div', { position: 'absolute', left: px(14 * S), right: px(14 * S), display: 'flex', alignItems: 'flex-end', gap: px(6 * S), justifyContent: mine ? 'flex-end' : 'flex-start' });
      if (!mine) row.appendChild(h('span', { flex: '0 0 auto', width: px(22 * S), height: px(22 * S), borderRadius: '50%', background: SH[senders[i]] }));
      const b = h('div', { maxWidth: '80%', padding: `${px(9 * S)} ${px(14 * S)}`, borderRadius: px(18 * S), fontSize: px(16 * S), lineHeight: px(21 * S), color: APP.text, background: mine ? APP.surface2 : APP.surface, whiteSpace: 'nowrap' }, LINES[i]);
      b.style[mine ? 'borderBottomRightRadius' : 'borderBottomLeftRadius'] = px(6 * S);
      row.appendChild(b); row.className = 'app';
      list.appendChild(row);
      bubbles.push({ row, y: 0, hgt: 0, mine });
    }
    // the plan
    const SK = h('div', { position: 'absolute', left: 0, top: 0, width: '1080px', height: '1920px', opacity: 0 });
    stage.appendChild(SK);
    const tcx = 540, tcy = 930;
    SK.innerHTML = `<svg width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true" style="position:absolute;left:0;top:0">
      <circle cx="${tcx}" cy="${tcy}" r="128" fill="${C.ink}" fill-opacity="0.06" stroke="${C.ink}" stroke-opacity="0.32" stroke-width="4"></circle>
      ${[180, -90, 0, 90].map((a) => { const r2 = a * Math.PI / 180, ux = tcx + 74 * Math.cos(r2), uy = tcy + 74 * Math.sin(r2); return `<circle cx="${ux.toFixed(1)}" cy="${uy.toFixed(1)}" r="26" fill="none" stroke="${C.ink}" stroke-opacity="0.34" stroke-width="4"></circle><circle cx="${ux.toFixed(1)}" cy="${uy.toFixed(1)}" r="11" fill="${C.ink}" fill-opacity="0.3"></circle>`; }).join('')}
    </svg>`;
    const seat = [90, 180, -90, 0].map((a, i) => {
      const r2 = a * Math.PI / 180, d = personDot(48, i === 0 ? C.amber : C.ink);
      Object.assign(d.style, { left: px(tcx + 186 * Math.cos(r2) - 24), top: px(tcy + 186 * Math.sin(r2) - 24) });
      SK.appendChild(d); return d;
    });
    const card = ActivityCard({ title: 'Brunch', meta: 'Sat · 13:00 · JLT', icon: 'egg-outline', max: 4 }, S, 888);
    const cardBox = h('div', { position: 'absolute', left: '96px', top: '1250px', opacity: 0 }, card.el);
    stage.appendChild(cardBox);
    const lab2 = illus(stage, 984, 1250 - 64, false); lab2.style.opacity = 0;

    const tSeat = [T(12.25), T(12.75), T(13), T(13.25)], tDone = T(14), tEnd = T(17), tSoon = T(19);
    for (let i = 0; i < N; i++) events.push({ t: arrive(i), kind: 'blip', n: senders[i] });
    events.push({ t: T(10), kind: 'thunk' }, { t: T(12) - 0.15, kind: 'whoosh' });
    tSeat.forEach((t, i) => events.push({ t, kind: 'pop', n: i * 2 }));
    events.push({ t: tDone, kind: 'chime' });
    const end = EndCard(stage, C.cream, C.ink, C.softOnCream);

    let laid = false;
    function layout() {
      let yy = 0;
      bubbles.forEach((b) => { b.hgt = b.row.offsetHeight; b.y = yy; b.row.style.top = px(yy); yy += b.hgt + GAP; });
      laid = true;
    }
    function render(t) {
      if (!laid) layout();
      heads.render(t);
      // counter
      let n = 0;
      for (let i = 0; i < N; i++) if (t >= arrive(i)) n++;
      n = Math.max(n, 1);
      countSpan.textContent = String(n); wordSpan.textContent = n === 1 ? 'message.' : 'messages.';
      const kIn = EASE.out(ramp(t, 0.1, 0.6)), kOut = EASE.in(ramp(t, T(11.5), T(12.1)));
      ph.frame.style.transform = `translateY(${((1 - kIn) * 140 + kOut * 260).toFixed(1)}px)`;
      ph.frame.style.opacity = (kIn * (1 - kOut)).toFixed(3);
      lab.style.opacity = (0.75 * EASE.out(ramp(t, 0.4, 0.8)) * (1 - kOut)).toFixed(3);
      // scroll: newest at the bottom
      const viewH = view.offsetHeight;
      let off = 0;
      bubbles.forEach((b, i) => {
        const k = EASE.out(ramp(t, arrive(i), arrive(i) + 0.16));
        off += (b.hgt + GAP) * k;
        b.row.style.opacity = k.toFixed(3);
        b.row.style.transform = `translateY(${((1 - k) * 30).toFixed(1)}px)`;
      });
      list.style.transform = `translateY(${(viewH - 10 - off).toFixed(1)}px)`;
      // the plan
      const kp = EASE.out(ramp(t, T(12), T(12) + 0.45));
      SK.style.opacity = kp.toFixed(3);
      SK.style.transform = `translateY(${((1 - kp) * 60).toFixed(1)}px)`;
      seat.forEach((d, i) => (d.style.transform = `scale(${pop(t, tSeat[i], 0.3).toFixed(3)})`));
      const kc = EASE.out(ramp(t, T(12) + 0.1, T(12) + 0.55));
      cardBox.style.opacity = kc.toFixed(3); cardBox.style.transform = `translateY(${((1 - kc) * 60).toFixed(1)}px)`;
      lab2.style.opacity = (0.75 * kc).toFixed(3);
      card.set({ dotK: tSeat.map((ts) => pop(t, ts, 0.3)), joinK: EASE.out(ramp(t, tDone, tDone + 0.18)) });
      end.render(t, tEnd, tSoon);
    }
    return { bpm, dur: T(23), cues: { stall: T(10), drop: T(12), end: tEnd }, events, render, cover: T(10) + 0.5, key: 'A' };
  }

  // ===========================================================================
  // Sun: Off on a Tuesday?
  // ===========================================================================
  function offTuesday(stage) {
    const bpm = 120, B = 60 / bpm, T = (b) => b * B;
    stage.style.background = C.ink;
    const events = [];
    const heads = Headlines(stage, [
      { lines: ['Off on a', 'Tuesday?'], t0: 0.12, t1: T(8) - 0.28 },
      { lines: ['So are 13 crew', 'at your base.'], t0: T(8), t1: T(15) - 0.28 },
    ], { color: C.cream });
    const PT = 720;
    const lab = illus(stage, 984, PT - 64, true);
    const ph = Phone(stage, PT, true);
    const P = 16 * S;
    const add = (e, x, y) => { Object.assign(e.style, { position: 'absolute', left: px(x), top: px(y) }); ph.inner.appendChild(e); return e; };
    const days = [['Today', 9, 1], ['Tue', 10, 2], ['Wed', 11, 1], ['Thu', 12, 3], ['Fri', 13, 0], ['Sat', 14, 3], ['Sun', 15, 2]];
    const cells = days.map(([dow, num, dots], i) => { const c = DayCell({ dow, num, dots }, S); add(c.el, P + i * 56 * S, 20 * S); return c; });
    const fy = 20 * S + 66 * S + 16 * S;
    const freeBox = h('div', { width: px(936 - 2 * P), height: px(48 * S), borderRadius: px(12 * S), background: APP.surface, display: 'flex', alignItems: 'center', gap: px(16 * S), padding: `0 ${px(16 * S)}` });
    freeBox.className = 'app';
    const dayName = h('span', null, 'Today');
    const freeText = h('span', { flex: 1, fontSize: px(15 * S), fontWeight: 800, color: APP.text, whiteSpace: 'nowrap' });
    const notFree = h('span', { fontSize: px(14 * S), fontWeight: 400, color: APP.muted }, ' · Not free');
    const isFree = h('span', { fontSize: px(14 * S), fontWeight: 600, color: APP.link }, ' · Free all day');
    freeText.appendChild(dayName); freeText.appendChild(notFree); freeText.appendChild(isFree);
    const freeBtn = h('div', { padding: `0 ${px(14 * S)}`, height: px(34 * S), borderRadius: '999px', background: APP.accent, color: APP.accentText, fontSize: px(14 * S), fontWeight: 800, display: 'flex', alignItems: 'center' }, "I'm free");
    const edit = h('span', { fontSize: px(15 * S), fontWeight: 700, color: APP.link }, 'Edit');
    freeBox.appendChild(freeText); freeBox.appendChild(freeBtn); freeBox.appendChild(edit);
    freeBox.appendChild(icon('information-circle-outline', 18 * S, APP.muted));
    add(freeBox, P, fy);
    const cy = fy + 48 * S + 10 * S;
    const counts = add(h('span', { fontSize: px(15 * S), fontWeight: 700, color: APP.text, whiteSpace: 'nowrap' }), P, cy);
    counts.className = 'app';
    const sy = cy + 20 * S + 18 * S;
    const sec = add(h('span', { fontSize: px(20 * S), fontWeight: 800, color: APP.text, letterSpacing: px(-0.3 * S), opacity: 0 }, 'Free Tuesday at your base'), P, sy);
    sec.className = 'app';
    // your base, crew around it
    const cx = 936 / 2, ccy = sy + 48 + 300;
    const rings = h('div', { position: 'absolute', left: 0, top: 0, width: '100%', height: '100%', opacity: 0 });
    rings.innerHTML = `<svg width="936" height="1400" style="position:absolute;left:0;top:0" aria-hidden="true">
      <circle cx="${cx}" cy="${ccy}" r="130" fill="none" stroke="${APP.border}" stroke-width="3"></circle>
      <circle cx="${cx}" cy="${ccy}" r="226" fill="none" stroke="${APP.border}" stroke-width="3"></circle></svg>`;
    ph.inner.appendChild(rings);
    const home = add(h('div', { width: '116px', height: '116px', borderRadius: '50%', background: APP.surface, display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: `0 0 0 3px ${APP.border}` }, icon('home', 54, APP.link)), cx - 58, ccy - 58);
    const slots = [];
    for (let i = 0; i < 5; i++) slots.push([130, -90 + 72 * i + 18]);
    for (let i = 0; i < 8; i++) slots.push([226, -90 + 45 * i + 22.5]);
    const order = [0, 6, 3, 10, 1, 8, 12, 4, 7, 2, 11, 5, 9];
    const r = rng(13);
    const crew = slots.map(([rad, ang]) => {
      const a = ang * Math.PI / 180, d = personDot(46, APP.text);
      const fromA = a + (r() - 0.5) * 0.6;
      add(d, cx + rad * Math.cos(a) - 23, ccy + rad * Math.sin(a) - 23);
      return { d, dx: (rad + 420) * Math.cos(fromA) - rad * Math.cos(a), dy: (rad + 420) * Math.sin(fromA) - rad * Math.sin(a) };
    });
    const tSel = T(2), tFree = T(4), tCrew = T(8.5), tEnd = T(15), tSoon = T(17);
    const land = (j) => tCrew + j * B / 4;
    events.push({ t: tSel, kind: 'tap' }, { t: tSel + 0.03, kind: 'pop', n: 2 }, { t: tFree, kind: 'tap' }, { t: tFree + 0.03, kind: 'pop', n: 4 });
    events.push({ t: T(8) - 0.1, kind: 'whoosh' });
    for (let j = 0; j < 13; j++) events.push({ t: land(j), kind: 'pop', n: j % 8 });
    events.push({ t: land(12) + B / 2, kind: 'chime' });
    const end = EndCard(stage, C.ink, C.cream, C.softOnInk);

    function render(t) {
      heads.render(t);
      const kIn = EASE.out(ramp(t, 0.15, 0.75));
      ph.frame.style.transform = `translateY(${((1 - kIn) * 140).toFixed(1)}px)`;
      ph.frame.style.opacity = kIn.toFixed(3);
      lab.style.opacity = (0.75 * EASE.out(ramp(t, 0.5, 0.9))).toFixed(3);
      const onTue = t >= tSel + 0.05, freeK = t >= tFree + 0.06;
      cells.forEach((c, i) => c.set({ sel: (onTue ? i === 1 : i === 0) ? 1 : 0, free: i === 1 && freeK ? 1 : 0 }));
      cells[1].el.style.transform = `scale(${(1 - 0.06 * Math.max(0, 1 - Math.abs(t - tSel) / 0.12)).toFixed(3)})`;
      dayName.textContent = onTue ? 'Tuesday' : 'Today';
      freeBtn.style.transform = `scale(${(1 - 0.08 * Math.max(0, 1 - Math.abs(t - tFree) / 0.12)).toFixed(3)})`;
      freeBtn.style.display = freeK ? 'none' : 'flex'; edit.style.display = freeK ? 'inline' : 'none';
      notFree.style.display = freeK ? 'none' : 'inline'; isFree.style.display = freeK ? 'inline' : 'none';
      const kr = EASE.out(ramp(t, T(8), T(8) + 0.5)), kb = EASE.out(ramp(t, 0.4, 0.9));
      rings.style.opacity = (kb * (0.45 + 0.55 * kr)).toFixed(3); sec.style.opacity = kr.toFixed(3);
      home.style.opacity = kb.toFixed(3); home.style.transform = `scale(${(0.9 + 0.1 * kb + 0.08 * Math.max(0, 1 - Math.abs(t - T(8.25)) / 0.2)).toFixed(3)})`;
      let n = 0;
      order.forEach((si, j) => {
        const c = crew[si], tl = land(j), kf = EASE.out(ramp(t, tl - 0.42, tl));
        const k = t < tl ? 0.7 * kf : pop(t, tl, 0.26) * 0.3 + 0.7;
        c.d.style.transform = `translate(${((1 - kf) * c.dx).toFixed(1)}px, ${((1 - kf) * c.dy).toFixed(1)}px) scale(${k.toFixed(3)})`;
        c.d.style.opacity = kf.toFixed(3);
        if (t >= tl) n++;
      });
      counts.textContent = n ? `${n} crew free` : '';
      end.render(t, tEnd, tSoon);
    }
    return { bpm, dur: T(21), cues: { lift: T(8), end: tEnd }, events, render, cover: T(13), key: 'G' };
  }

  // ===========================================================================
  // Mon: Roster roulette
  // ===========================================================================
  function roster(stage) {
    const bpm = 126, B = 60 / bpm, T = (b) => b * B;
    stage.style.background = C.cream;
    const events = [];
    const heads = Headlines(stage, [
      { lines: ['New roster.', 'Again.'], t0: 0.12, t1: T(8) - 0.28, at: [0.12, 0.19, T(3.5)] },
      { lines: ['Mark your', 'days off.'], t0: T(8), t1: T(14) - 0.28 },
      { lines: ["See who's", 'free too.'], t0: T(14), t1: T(20) - 0.28 },
    ], { color: C.ink });

    // scene 1: the roster as a slot machine, two weeks (an illustration, not the app)
    const DOWS = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];
    const SYM = ['airplane-outline', 'moon-outline', 'OFF'];
    const spin1 = [[0, 0, 2, 0, 1, 2, 0], [1, 0, 0, 2, 0, 0, 2]];
    const spin2 = [[0, 2, 0, 0, 1, 2, 2], [0, 0, 1, 0, 2, 0, 0]];
    const RW = 116, RG = 12, RH = 210, RX = 96, RY = 860, ROWG = 28;
    const board = h('div', { position: 'absolute', left: 0, top: 0, width: '1080px', height: '1920px' });
    stage.appendChild(board);
    DOWS.forEach((d, j) => board.appendChild(h('div', { position: 'absolute', left: px(RX + j * (RW + RG)), top: px(RY - 64), width: px(RW), textAlign: 'center', fontSize: '40px', fontWeight: 800, color: C.ink, opacity: 0.55 }, d)));
    const r = rng(7);
    const reels = [];
    for (let row = 0; row < 2; row++) DOWS.forEach((d, j) => {
      const x = RX + j * (RW + RG), y = RY + row * (RH + ROWG);
      const win = h('div', { position: 'absolute', left: px(x), top: px(y), width: px(RW), height: px(RH), borderRadius: '22px', background: '#FFFFFF', border: `4px solid ${C.ink}`, overflow: 'hidden' });
      const strip = h('div', { position: 'absolute', left: 0, top: 0, width: '100%' });
      const seq = [];
      for (let k = 0; k < 44; k++) seq.push(Math.floor(r() * 3));
      const stop1 = 16 + j + row * 2, stop2 = 36 + j % 3;
      seq[0] = (j + row) % 2; seq[stop1] = spin1[row][j]; seq[stop2] = spin2[row][j];
      seq.forEach((sy) => {
        const cell = h('div', { width: '100%', height: px(RH - 8), display: 'flex', alignItems: 'center', justifyContent: 'center' });
        if (SYM[sy] === 'OFF') cell.appendChild(h('span', { padding: '8px 12px', borderRadius: '14px', background: C.amber, color: C.ink, fontSize: '38px', fontWeight: 900, letterSpacing: '-.02em' }, 'OFF'));
        else cell.appendChild(icon(SYM[sy], 72, C.ink));
        strip.appendChild(cell);
      });
      win.appendChild(strip);
      board.appendChild(win);
      reels.push({ strip, stop1, stop2, j, row });
    });
    const CH = RH - 8;
    // columns stop left to right, both weeks together
    const s1a = T(0.25), s1stop = (j) => T(1.25) + j * B / 4, s2a = T(3.5), s2stop = (j) => T(4.5) + j * B / 4;
    function reelPos(R, t) {
      const seg = (t0, t1, p0, p1) => {
        const k = ramp(t, t0, t1);
        const e = k < 1 ? 1 - Math.pow(1 - k, 2.4) : 1;
        const over = k >= 0.82 ? Math.sin((k - 0.82) / 0.18 * Math.PI) * 0.06 : 0;
        return p0 + (p1 - p0) * e + over;
      };
      if (t < s2a) return seg(s1a, s1stop(R.j), 0, R.stop1);
      return seg(s2a, s2stop(R.j), R.stop1, R.stop2);
    }
    for (let j = 0; j < 7; j++) events.push({ t: s1stop(j), kind: 'thunk', n: j }, { t: s2stop(j), kind: 'thunk', n: j });
    events.push({ t: s1a, kind: 'spin', t1: s1stop(6) }, { t: s2a, kind: 'spin', t1: s2stop(6) });

    // scene 2/3: the app's month grid (app/src/components/month-grid.tsx)
    const PT = 700;
    const lab = illus(stage, 984, PT - 64, false);
    const ph = Phone(stage, PT, false);
    const P = 16 * S, GW = 936 - 2 * P, CW = GW / 7;
    const add = (e, x, y) => { Object.assign(e.style, { position: 'absolute', left: px(x), top: px(y) }); ph.inner.appendChild(e); return e; };
    const title = add(h('span', { fontSize: px(20 * S), fontWeight: 800, color: APP.text, letterSpacing: px(-0.3 * S) }, 'Days off'), P, 16 * S);
    title.className = 'app';
    DOWS.forEach((d, i) => add(h('span', { width: px(CW), textAlign: 'center', fontSize: px(12 * S), fontWeight: 700, color: APP.muted }, d), P + i * CW, 16 * S + 36 * S));
    const lead = 2, len = 30, gy = 16 * S + 36 * S + 24 * S;
    const OFF = [4, 9, 15, 16, 24, 28];
    const COUNT = { 4: 13, 9: 8, 15: 11, 16: 6, 24: 9, 28: 14 };
    const cellEls = {};
    for (let d = 1; d <= len; d++) {
      const idx = lead + d - 1, col = idx % 7, row = Math.floor(idx / 7);
      const c = h('div', { width: px(CW - 6 * S), height: px(CW - 6 * S), borderRadius: px(12 * S), background: APP.surface, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: px(17 * S), fontWeight: 700, color: APP.text }, String(d));
      c.className = 'app';
      add(c, P + col * CW + 3 * S, gy + row * CW + 3 * S);
      cellEls[d] = c;
    }
    // badges: crew free that day
    const badges = OFF.map((d) => {
      const idx = lead + d - 1, col = idx % 7, row = Math.floor(idx / 7);
      const b = h('div', { height: '50px', padding: '0 12px 0 8px', borderRadius: '999px', background: APP.text, color: APP.bg, display: 'flex', alignItems: 'center', gap: '3px', fontSize: '28px', fontWeight: 800, transform: 'scale(0)', boxShadow: `0 0 0 4px ${APP.bg}` }, [icon('person', 24, APP.bg), h('span', null, String(COUNT[d]))]);
      b.className = 'app';
      add(b, P + (col + 1) * CW - 72, gy + row * CW - 16);
      return b;
    });
    const tTap = [T(9.5), T(10), T(10.5), T(11.5), T(12), T(12.5)];
    const tBadge = OFF.map((_, i) => T(14.5) + i * B / 2);
    tTap.forEach((t, i) => events.push({ t, kind: 'tap' }, { t: t + 0.03, kind: 'pop', n: i }));
    tBadge.forEach((t, i) => events.push({ t, kind: 'pop', n: 2 + i }));
    events.push({ t: T(8) - 0.15, kind: 'whoosh' }, { t: tBadge[5] + B, kind: 'chime' });
    const tEnd = T(20), tSoon = T(22);
    const end = EndCard(stage, C.cream, C.ink, C.softOnCream);

    function render(t) {
      heads.render(t);
      // slot board
      const kb = EASE.out(ramp(t, 0.05, 0.5)), kbo = EASE.in(ramp(t, T(7.7), T(8.2)));
      board.style.opacity = (kb * (1 - kbo)).toFixed(3);
      board.style.transform = `translateY(${((1 - kb) * 80 - kbo * 120).toFixed(1)}px)`;
      reels.forEach((R) => { R.strip.style.transform = `translateY(${(-reelPos(R, t) * CH + 4).toFixed(1)}px)`; });
      // phone
      const kIn = EASE.out(ramp(t, T(8), T(8) + 0.55));
      ph.frame.style.transform = `translateY(${((1 - kIn) * 260).toFixed(1)}px)`;
      ph.frame.style.opacity = kIn.toFixed(3);
      lab.style.opacity = (0.75 * kIn).toFixed(3);
      OFF.forEach((d, i) => {
        const on = t >= tTap[i] + 0.04, c = cellEls[d];
        c.style.background = on ? APP.accent : APP.surface;
        c.style.color = on ? APP.accentText : APP.text;
        c.style.fontWeight = on ? 800 : 700;
        const press = Math.max(0, 1 - Math.abs(t - tTap[i]) / 0.12);
        c.style.transform = `scale(${(1 - 0.08 * press + 0.06 * Math.max(0, 1 - Math.abs(t - tTap[i] - 0.14) / 0.14)).toFixed(3)})`;
        badges[i].style.transform = `scale(${pop(t, tBadge[i], 0.3).toFixed(3)})`;
      });
      end.render(t, tEnd, tSoon);
    }
    return { bpm, dur: T(26), cues: { lift: T(8), drop: T(14), end: tEnd }, events, render, cover: T(7), key: 'D' };
  }

  // ===========================================================================
  // Tue: Clubs
  // ===========================================================================
  function clubs(stage) {
    const bpm = 122, B = 60 / bpm, T = (b) => b * B;
    stage.style.background = C.ink;
    const events = [];
    const heads = Headlines(stage, [
      { lines: ['Running.', 'Yoga.', 'Brunch.'], t0: T(0.25), t1: T(6) - 0.28, at: [T(0.25), T(1.25), T(2.25)] },
      { lines: ["There's a club", 'for it at', 'your base.'], t0: T(6), t1: T(13) - 0.28 },
      { lines: ['Join their', 'next plan.'], t0: T(13), t1: T(20) - 0.28 },
    ], { color: C.cream });
    const PT = 770;
    const lab = illus(stage, 984, PT - 62, true);
    const ph = Phone(stage, PT, true);
    const P = 16 * S, IW = 936 - 2 * P;
    const page1 = h('div', { position: 'absolute', left: 0, top: 0, width: '100%', height: '100%' });
    const page2 = h('div', { position: 'absolute', left: 0, top: 0, width: '100%', height: '100%' });
    ph.inner.appendChild(page1); ph.inner.appendChild(page2);
    const add = (pg, e, x, y) => { Object.assign(e.style, { position: 'absolute', left: px(x), top: px(y) }); pg.appendChild(e); return e; };
    // Clubs tab (components/clubs-list.tsx)
    const search = h('div', { width: px(IW), height: px(44 * S), borderRadius: '999px', background: APP.surface, display: 'flex', alignItems: 'center', gap: px(8 * S), padding: `0 ${px(16 * S)}`, fontSize: px(16 * S), color: APP.muted }, [icon('search', 17 * S, APP.muted), h('span', null, 'Search clubs')]);
    search.className = 'app';
    add(page1, search, P, 16 * S);
    const hIn = add(page1, h('span', { fontSize: px(18 * S), fontWeight: 800, color: APP.text }, 'In Dubai'), P, 16 * S + 44 * S + 24 * S);
    hIn.className = 'app';
    const listY = 16 * S + 44 * S + 24 * S + 22 * S + 4 * S;
    const list = add(page1, h('div', { width: px(IW) }), P, listY);
    const CLUBS = [['footsteps-outline', 'Running', '5 free Thu', '2 plans'], ['body-outline', 'Yoga', '4 free Sat', '1 plan'], ['egg-outline', 'Brunch Club', '6 free Fri', '1 plan']];
    const rows = CLUBS.map(([ic, name, pulse, plans], i) => {
      const join = h('div', { height: px(28 * S), minWidth: px(58 * S), padding: `0 ${px(12 * S)}`, borderRadius: '999px', background: APP.accent, color: APP.accentText, fontSize: px(13 * S), fontWeight: 800, display: 'flex', alignItems: 'center', justifyContent: 'center' }, 'Join');
      const joined = h('div', { height: px(28 * S), minWidth: px(58 * S), padding: `0 ${px(12 * S)}`, borderRadius: '999px', border: `${px(1)} solid ${APP.border}`, color: APP.muted, fontSize: px(13 * S), fontWeight: 600, display: 'none', alignItems: 'center', justifyContent: 'center', gap: px(3 * S) }, [icon('checkmark', 13 * S, APP.success), h('span', null, 'Joined')]);
      const row = h('div', { display: 'flex', alignItems: 'center', gap: px(16 * S), padding: `0 ${px(16 * S)}`, minHeight: px(60 * S), background: APP.surface, borderBottom: i < 2 ? `2px solid ${APP.border}` : 'none',
        borderRadius: i === 0 ? `${px(16 * S)} ${px(16 * S)} 0 0` : i === 2 ? `0 0 ${px(16 * S)} ${px(16 * S)}` : '0' }, [
        icon(ic, 20 * S, APP.link),
        h('div', { flex: 1, display: 'flex', flexDirection: 'column' }, [
          h('span', { fontSize: px(16 * S), fontWeight: 700, color: APP.text }, name),
          h('span', { fontSize: px(12 * S), color: APP.muted, marginTop: px(1 * S) }, `<span style="color:${APP.link};font-weight:800">${pulse}</span> · ${plans}`),
        ]),
        join, joined,
      ]);
      row.className = 'app';
      list.appendChild(row);
      return { row, join, joined };
    });
    const note = add(page1, h('div', { width: px(IW), display: 'flex', gap: px(5 * S), fontSize: px(12 * S), color: APP.muted, lineHeight: 1.35 }, [icon('flash-outline', 13 * S, APP.muted), h('span', null, 'Mark your days off and a club pings you when enough of its members are free at the same time.')]), P, listY + 3 * 60 * S + 24 * S);
    note.className = 'app';
    // the club's page, Plans tab (app/club/[id].tsx)
    const head = h('div', { width: px(IW), display: 'flex', alignItems: 'center', gap: px(16 * S) }, [
      h('div', { width: px(48 * S), height: px(48 * S), borderRadius: '50%', background: APP.signalSoft, display: 'flex', alignItems: 'center', justifyContent: 'center' }, icon('footsteps-outline', 24 * S, APP.link)),
      h('div', { flex: 1, display: 'flex', flexDirection: 'column' }, [
        h('span', { fontSize: px(24 * S), lineHeight: px(29 * S), fontWeight: 800, color: APP.text, letterSpacing: px(-0.4 * S) }, 'Dubai Running Club'),
        h('span', { fontSize: px(13 * S), color: APP.muted, marginTop: px(2 * S) }, 'Runs at your base'),
      ]),
    ]);
    head.className = 'app';
    add(page2, head, P, 16 * S);
    const tabs = h('div', { width: px(IW), display: 'flex', gap: px(4 * S) }, ['Free together', 'Plans', 'Tips', 'Members'].map((l) => h('div', { flexGrow: 1, height: px(38 * S), padding: `0 ${px(10 * S)}`, borderRadius: '999px', background: l === 'Plans' ? APP.text : APP.surface, color: l === 'Plans' ? APP.bg : APP.text, fontSize: px(14 * S), fontWeight: 700, display: 'flex', alignItems: 'center', justifyContent: 'center', whiteSpace: 'nowrap' }, l)));
    tabs.className = 'app';
    add(page2, tabs, P, 16 * S + 48 * S + 20 * S);
    const card = ActivityCard({ title: 'Sunrise run', meta: 'Sat · 06:00 · Dubai Marina', icon: 'footsteps-outline', max: 6 }, S, IW);
    add(page2, card.el, P, 16 * S + 48 * S + 20 * S + 38 * S + 20 * S);

    const tRow = [T(0.25), T(1.25), T(2.25)], tJoinClub = T(9), tPage = T(13), tJoin = T(16.5), tEnd = T(20), tSoon = T(22);
    tRow.forEach((t, i) => events.push({ t, kind: 'pop', n: i * 2 }));
    events.push({ t: tJoinClub, kind: 'tap' }, { t: tJoinClub + 0.03, kind: 'pop', n: 4 }, { t: tPage - 0.12, kind: 'whoosh' }, { t: tJoin, kind: 'tap' }, { t: tJoin + 0.06, kind: 'chime' });
    const end = EndCard(stage, C.ink, C.cream, C.softOnInk);

    function render(t) {
      heads.render(t);
      const kIn = EASE.out(ramp(t, 0.1, 0.6));
      ph.frame.style.transform = `translateY(${((1 - kIn) * 140).toFixed(1)}px)`;
      ph.frame.style.opacity = kIn.toFixed(3);
      lab.style.opacity = (0.75 * EASE.out(ramp(t, 0.4, 0.8))).toFixed(3);
      rows.forEach((rw, i) => {
        const k = EASE.out(ramp(t, tRow[i] - 0.05, tRow[i] + 0.3));
        rw.row.style.opacity = k.toFixed(3);
        rw.row.style.transform = `translateX(${((1 - k) * 60).toFixed(1)}px)`;
        const on = i === 0 && t >= tJoinClub + 0.05;
        rw.join.style.display = on ? 'none' : 'flex'; rw.joined.style.display = on ? 'flex' : 'none';
        if (i === 0) rw.join.style.transform = `scale(${(1 - 0.1 * Math.max(0, 1 - Math.abs(t - tJoinClub) / 0.12)).toFixed(3)})`;
      });
      note.style.opacity = EASE.out(ramp(t, tRow[2] + 0.3, tRow[2] + 0.8)).toFixed(3);
      const kp = EASE.inOut(ramp(t, tPage, tPage + 0.5));
      page1.style.transform = `translateX(${(-kp * 936).toFixed(1)}px)`;
      page2.style.transform = `translateX(${((1 - kp) * 936).toFixed(1)}px)`;
      const dotK = Array.from({ length: 6 }, (_, i) => (i < 4 ? 1 : i === 4 ? pop(t, tJoin + 0.05, 0.3) : 0));
      card.set({ dotK, joinK: EASE.out(ramp(t, tJoin + 0.02, tJoin + 0.2)), press: Math.max(0, 1 - Math.abs(t - tJoin) / 0.12) });
      end.render(t, tEnd, tSoon);
    }
    return { bpm, dur: T(26), cues: { lift: T(6), drop: T(13), end: tEnd }, events, render, cover: T(10), key: 'Bb' };
  }

  window.REELS = { 'off-today': offToday, '47-messages': messages, 'off-tuesday': offTuesday, 'roster-roulette': roster, clubs };
})();
