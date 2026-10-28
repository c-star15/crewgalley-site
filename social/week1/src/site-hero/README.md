Post "Life beyond the roster." in the website's hero identity (Victor, 28 Oct 16:33): dawn gradient, eyebrow, headline with "the roster." in the hero accent, the site's tagline, and the hero planet (city landmarks, Dubai pin at the top).

`planet.js` is the site's `planet.js` with three overrides read from `window.PL` (R as a share of the width, apex as a share of the box height, starting offset in degrees). Render:

    python3 shoot.py out.jpg '{"TOP":100,"EYE":96,"H1":170,"GMH":600,"R":1.6,"APEX":0.72,"OFF":0}'

(reduced motion freezes the planet; `post.html` loads Inter from the site's `fonts/`, adjust the path if the repo lives elsewhere).
