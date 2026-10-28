---
title: You're invited · Galley
description: A plan with pilots and cabin crew on Galley. Tap to see it.
robots: noindex
---
<div class="join" id="join" aria-live="polite">
<p class="eyebrow">You’re invited</p>
<div class="plan" id="plan" hidden>
<div class="plan-top"><span class="plan-dot" aria-hidden="true"></span><span class="plan-kind" id="p-kind"></span><span class="plan-tag" id="p-women" hidden>Women only</span></div>
<h1 class="plan-title" id="p-title"></h1>
<ul class="plan-facts">
<li><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="5" width="17" height="15.5" rx="3"/><path d="M3.5 10h17M8 3v4M16 3v4"/></svg><span id="p-when"></span></li>
<li><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-6.5-6.2-6.5-11.2a6.5 6.5 0 0 1 13 0C18.5 14.8 12 21 12 21Z"/><circle cx="12" cy="9.8" r="2.3"/></svg><span id="p-where"></span></li>
<li><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="9" cy="8.5" r="3.2"/><path d="M3 19.5c.6-3.3 3-5.2 6-5.2s5.4 1.9 6 5.2"/><path d="M15.5 5.6a3.2 3.2 0 0 1 0 5.8M17.5 14.6c1.8.7 3 2.4 3.5 4.9"/></svg><span id="p-count"></span></li>
</ul>
<div class="plan-dots" id="p-dots" aria-hidden="true"></div>
<p class="plan-state" id="p-state" hidden></p>
<div class="actions"><a class="btn" id="open" href="galley://join">Open in Galley</a></div>
<p class="plan-note">The exact place shows in the app once you’re in.</p>
</div>
<div class="plan plan-empty" id="gone" hidden>
<h1 class="plan-title">This link has landed.</h1>
<p>Plan links stop working once the plan is over, or when the person who shared it leaves. Ask them for a new one.</p>
</div>
<div class="plan plan-empty" id="loading"><p class="plan-loading">Finding the plan…</p></div>
<section class="join-new">
<h2>New to Galley?</h2>
<p>Galley is where pilots and cabin crew make plans with each other: padel, coffee, a run, dinner. At base on your days off, and on layovers. Join with your name, base and role.</p>
<ul class="trust">
<li><strong>For pilots and cabin crew.</strong> Any airline.</li>
<li><strong>Plans, not profiles.</strong> You join what’s on. Nobody sees where you are.</li>
<li><strong>Starting in Dubai,</strong> December 2026.</li>
</ul>
<p>Once you’ve joined, open this link again and you’ll land on the plan.</p>
<div class="actions"><a class="btn secondary" href="/verification/">How joining works</a><a class="btn ghost" href="/safety/">Meeting safely</a></div>
</section>
</div>
<script>
(function(){
  // Plan previews come from the plan-preview edge function. Staging for now;
  // add the production project here at the first production release.
  var API = 'https://yakmnhpsajekcvbbswqr.supabase.co/functions/v1/plan-preview';
  var t = new URLSearchParams(location.search).get('t') || '';
  var $ = function(id){ return document.getElementById(id); };
  function show(id){ ['plan','gone','loading'].forEach(function(x){ $(x).hidden = x !== id; }); }
  if (!/^[A-Za-z0-9_-]{22}$/.test(t)) { show('gone'); return; }
  $('open').href = 'galley://join?t=' + encodeURIComponent(t);
  function day(s){ var p = s.split('-'); return new Date(+p[0], +p[1]-1, +p[2]).toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short' }); }
  function cap(s){ return s ? s.charAt(0).toUpperCase() + s.slice(1) : ''; }
  function human(s){ return cap((s || '').replace(/_/g, ' ')); }
  function orList(ns){ return ns.length < 2 ? String(ns[0]) : ns.slice(0, -1).join(', ') + ' or ' + ns[ns.length - 1]; }
  function size(p){
    if (p.size_rule === 'min') return p.min_crew + '+';
    if (p.size_rule === 'ideal') return 'Ideal ' + p.ideal_size;
    if (p.size_rule === 'exact') return orList(p.sizes || [p.max_size]);
    return 'Up to ' + p.max_size;
  }
  function target(p){
    if (p.size_rule === 'min') return Math.max(p.min_crew, p.going);
    if (p.size_rule === 'ideal') return Math.max(p.ideal_size || 2, p.going);
    if (p.size_rule === 'exact') { var n = (p.sizes || []).filter(function(s){ return s >= p.going; })[0]; return n || p.max_size; }
    return p.max_size;
  }
  fetch(API + '?t=' + encodeURIComponent(t)).then(function(r){ return r.ok ? r.json() : null; }).then(function(j){
    var p = j && j.plan;
    if (!p) { show('gone'); return; }
    var kind = p.interest ? human(p.interest) : '';
    $('p-kind').textContent = kind && kind.toLowerCase() !== (p.title || '').toLowerCase() ? kind : 'A plan';
    $('p-title').textContent = p.title;
    $('p-women').hidden = !p.women_only;
    $('p-when').textContent = day(p.day) + ' · ' + (p.start_time ? p.start_time.slice(0, 5) : cap(p.slot));
    $('p-where').textContent = [p.neighbourhood, p.city].filter(Boolean).join(', ');
    $('p-count').textContent = p.going + ' in · ' + size(p);
    var n = target(p), dots = '';
    if (n <= 12) for (var i = 0; i < n; i++) dots += '<span class="' + (i < p.going ? 'in' : '') + '"></span>';
    $('p-dots').innerHTML = dots;
    var states = { full: 'It’s full right now.', called_off: 'This one was called off.', past: 'This one already happened.' };
    if (states[p.state]) { $('p-state').textContent = states[p.state]; $('p-state').hidden = false; }
    document.title = p.title + ' · ' + day(p.day) + ' · Galley';
    show('plan');
  }).catch(function(){ show('gone'); });
})();
</script>
