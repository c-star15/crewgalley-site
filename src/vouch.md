---
title: Vouch for crew · Galley
description: A colleague asked you to vouch for them on Galley. Open it in the app.
robots: noindex
---
<div class="join" id="vouch">
<p class="eyebrow">Vouch for crew</p>
<div class="plan">
<h1 class="plan-title">A colleague asked you to vouch for them.</h1>
<p>They can't get a code at their airline email, so two crew from the same airline can let them in instead. You'll see their name, role and airline in the app before you decide.</p>
<p class="code-big" id="code" hidden></p>
<div class="actions"><a class="btn" id="open" href="galley://vouch">Open in Galley</a></div>
<p class="plan-note">Only vouch for someone you know flies for your airline now. If they turn out not to be crew, your vouching and invite link switch off.</p>
</div>
<section class="join-new">
<h2>Link didn't open the app?</h2>
<p>In Galley, tap your photo at the top right, then <strong>Vouch for crew</strong>, and enter the code above.</p>
<p>Only verified crew at the same airline who joined with a work email can vouch.</p>
<div class="actions"><a class="btn secondary" href="/verification/">How we check crew</a></div>
</section>
</div>
<script>
(function(){
  var c = (new URLSearchParams(location.search).get('c') || '').toUpperCase();
  if (!/^[A-Z2-9]{8}$/.test(c)) return;
  var code = document.getElementById('code');
  code.textContent = c;
  code.hidden = false;
  document.getElementById('open').href = 'galley://vouch?c=' + encodeURIComponent(c);
})();
</script>
