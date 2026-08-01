# math-viz

Small, self-contained web pages that visualize mathematical concepts. No build
step, no dependencies, no tracking — plain HTML, CSS and SVG.

**Live site:** https://colecgulino.github.io/math-viz/

## Layout

```
index.html                  landing page, grouped by area
assets/theme.css            design tokens + shared page furniture
assets/thumbs/*.svg         index-card thumbnails, generated
assets/figures/*.svg        in-page explanatory diagrams, generated
tools/svgkit.py             shared SVG drawing helpers + palette
tools/gen_thumbs.py         regenerates the thumbnails
tools/gen_figures.py        regenerates the figures
<area>/<topic>/index.html   one directory per visualization
```

Pages are grouped on the index by mathematical area — Linear Algebra first —
and each visualization lives at `<area>/<topic>/`.

## Design

Warm earth tones throughout: sand backgrounds, warm grey text, burnt orange as
the single accent. Drawings use an ochre/olive/umber/brick palette that sits in
the same family. Motion is kept to a minimum — transitions on hover and focus
only, and `prefers-reduced-motion` is respected.

All values live in [`assets/theme.css`](assets/theme.css) as CSS custom
properties, alongside the shared page furniture (`.stage`, `.plate`, `.panel`,
`.btn`, form controls). Pages should reference the tokens and reuse those
classes rather than hard-coding hex values, so the whole collection can be
retuned from one file.

Where a page assigns colors at runtime — one per user-created object, say — it
should generate them inside the same warm band rather than picking at random.
See `warmColor()` in the linear-combinations page for the approach: walk an
ordered hue ring so consecutive picks stay distinguishable, and run the olive
end at much lower saturation than the reds.

**Gotcha:** anything that is also `.page` must use `padding-block`, never the
`padding` shorthand — the shorthand silently drops `.page`'s horizontal gutter
and the content ends up flush against the screen edge on narrow viewports.

## Adding a visualization

1. Create `<area>/<topic>/index.html` and link `../../assets/theme.css`.
2. Add a thumbnail routine to `tools/gen_thumbs.py`, then run
   `python3 tools/gen_thumbs.py`.
3. Add a card to the relevant area section in `index.html`, or start a new
   `<section class="topic">` if the area doesn't exist yet.

Static diagrams for a page go in `tools/gen_figures.py`, which shares its
geometry and palette with the thumbnails via `tools/svgkit.py`. Both scripts
must be run from the `tools/` directory. Two conventions worth keeping:

- **Write a multi-panel figure as one SVG per panel**, laid out with CSS grid.
  A single wide SVG shrinks to fit a phone and takes its labels down to a few
  pixels; separate panels can stack and stay readable.
- **Use `boxed=` on labels in crowded diagrams.** It fills a plate-colored rect
  behind the text so it survives sitting over a grid line or a crossing arrow,
  which is usually the only place a label will fit.

## Local preview

Any static server works:

```bash
python3 -m http.server 8000
```

## License

MIT
