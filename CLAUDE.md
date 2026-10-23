# Working agreement for Claude sessions

Several Claude sessions work on Galley in parallel and push to `main`. The full
agreement is `CLAUDE.md` in the app repo (c-star15/crew-hub). For this site:

- `git pull --rebase origin main` before starting and before every push; never force-push.
- The legal pages here (`src/privacy.md`, `src/terms.md`, `src/guidelines.md`,
  `src/safety.md`) must match the drafts in crew-hub `docs/legal/*.md`. Change
  both in the same sitting.
- Messages are end-to-end encrypted. Keep the privacy policy's encryption section
  and `src/private.md` accurate: what we cannot see, what we can (metadata), how
  reports work, and the stated limits (no security codes yet, no per-message key
  rotation). Do not make claims the app does not meet.
- Build with `python3 build.py`; check the page at 390 px wide in light and dark
  before pushing.
