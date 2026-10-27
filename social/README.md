# Instagram media

Rendered posts for @crewgalley, hosted here so the scheduler (Metricool) can fetch them by URL.
Not part of the website build (`build.py` doesn't copy this folder). Sources: the design canvas
"Galley Instagram starter kit".

- `ads/2026-10-28/`: ads, activities series (7 plans other than padel: yoga, run, live music, coffee, beach, Hatta day trip, study), each as a 3:4 post (`ad-N-*-post.jpg`, Metricool drafts) and a 9:16 story (`ad-N-*-story.jpg`). Sources in `src/`: `make_ads.py` writes the canvas artboards (captions and alt text are in its table; `--posts` prints them), `render.py` renders the JPEGs.
- `art/`: city mosaic art, Horizon and Departures (3:4 post stills, 14 s 9:16 Reels and their covers; art and wordmark only, no copy). Re-render with `art/src/` (`shoot.py` for a still, `render.py` for a Reel).
