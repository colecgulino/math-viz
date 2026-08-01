# math-viz

Small, self-contained web pages that visualize mathematical concepts. No build
step, no dependencies, no tracking — plain HTML, CSS and SVG.

**Live site:** https://colecgulino.github.io/math-viz/

## Layout

```
index.html            landing page + index of visualizations
assets/theme.css      shared design tokens (colors, type, layout)
assets/thumbs/*.svg   index-card thumbnails, generated
tools/gen_thumbs.py   regenerates the thumbnails
<topic>/index.html    one directory per visualization
```

## Design

Warm earth tones throughout: sand backgrounds, warm grey text, burnt orange as
the single accent. Drawings use an ochre/olive/umber/brick palette that sits in
the same family. Motion is kept to a minimum — transitions on hover and focus
only, and `prefers-reduced-motion` is respected.

All values live in [`assets/theme.css`](assets/theme.css) as CSS custom
properties. Pages should reference the tokens rather than hard-coding hex
values, so the whole collection can be retuned from one file.

## Adding a visualization

1. Create `<topic>/index.html` and link `../assets/theme.css`.
2. Add a thumbnail routine to `tools/gen_thumbs.py`, then run
   `python3 tools/gen_thumbs.py`.
3. Add a card to the index grid in `index.html`.

## Local preview

Any static server works:

```bash
python3 -m http.server 8000
```

## License

MIT
