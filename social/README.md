# Instagram media

Rendered posts for @crewgalley, hosted here so the scheduler (Metricool) can fetch them by URL.
Not part of the website build (`build.py` doesn't copy this folder). Sources: the design canvas
"Galley Instagram starter kit".

- `ads/2026-10-28/`: ads, activities series (7 plans other than padel: yoga, run, live music, coffee, beach, Hatta day trip, study), each as a 3:4 post (`ad-N-*-post.jpg`, Metricool drafts) and a 9:16 story (`ad-N-*-story.jpg`). Sources in `src/`: `make_ads.py` writes the canvas artboards (captions and alt text are in its table; `--posts` prints them), `render.py` renders the JPEGs.
- `week1/`: week 1 feed and stories (28 Oct to 4 Nov) after Victor's 28 Oct decisions: post 1 reworked to "Life beyond the roster." (`p1-life-beyond-the-roster.jpg`), and every app card or screen labelled "Illustration" (`p2b-brunch-illustration.jpg`, `p3c-base-illustration.jpg`, `ad-N-*-{post,story}-illustration.jpg`). Ads render with `ads/2026-10-28/src/render.py --out ../../../week1 --suffix=-illustration`; posts 1 to 3 come from the canvas artboards `v2-1-find`, `v2-4b-chat`, `v2-3c-tuesday` (static HTML, system Inter).
- `art/`: city mosaic art, Horizon and Departures (3:4 post stills, 14 s 9:16 Reels and their covers; art and wordmark only, no copy). Re-render with `art/src/` (`shoot.py` for a still, `render.py` for a Reel).
