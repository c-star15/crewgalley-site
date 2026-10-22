# crewgalley.app

Public website for Galley: verification page, safety, support, privacy policy, terms, community guidelines, and the password-reset fallback.

`python3 build.py` renders `src/*.md` into `dist/`; GitHub Pages deploys `dist/` on every push to `main`. The custom domain is set in `src`'s `CNAME` output and in the repository's Pages settings.
