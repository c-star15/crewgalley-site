# Working agreement for Claude sessions

Several Claude sessions work on Galley in parallel and push to `main`. The full
agreement is `CLAUDE.md` in the app repo (c-star15/crew-hub). For this site:

- `git pull --rebase origin main` before starting and before every push; never force-push.
- The legal pages here (`src/privacy.md`, `src/terms.md`, `src/guidelines.md`,
  `src/safety.md`) must match the drafts in crew-hub `docs/legal/*.md`. Change
  both in the same sitting.
- Messages are end-to-end encrypted. The privacy policy's section 4a carries the
  detail. `src/private.md` is kept to the minimum (Victor, 27 Oct 20:13): that chats
  are end-to-end encrypted, what we can see (metadata), how reports work, and a link
  to section 4a. Don't add technical detail or extra sections back. Keep every claim
  one the app meets without caveats: no "nobody can get them from us" and no
  "even if our servers are breached", because there are no security codes and no key
  rotation yet.
- Build with `python3 build.py`; check the page at 390 px wide in light and dark
  before pushing.
- Brand line (Victor, 28 Oct 00:17): "Life beyond the roster." The home page is his copy:
  a community for pilots and cabin crew, Your base, Clubs, How Galley works, one short
  When you're away block, Our story, Join us. Base and Clubs are one story (Base says when
  and where; clubs give people and interests worth going for), relaxed, not luxurious or
  exclusive. No safety or verification section on the home page (the nav pages carry it),
  no layover feature explainer, and no app mock that shows activity that hasn't happened
  (counts, other people, plans); mocks are labelled "Illustration". Don't bring back
  "by crew, for crew", "connect with verified crew", "make the most of every layover" or
  "Find your people. At base and away."
