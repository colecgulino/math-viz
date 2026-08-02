"""Shared SVG drawing helpers for the generators in this directory.

Both gen_thumbs.py (index cards) and gen_figures.py (in-page diagrams) build
static SVG by string concatenation. Everything here is plain geometry; the
palette mirrors the tokens in assets/theme.css and should be kept in sync
with it.
"""

import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SERIF = "Iowan Old Style, Palatino Linotype, Palatino, Georgia, serif"
MONO = "ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, monospace"

P = {
    # surfaces
    "sand100": "#f6efe3",
    "sand200": "#efe5d5",
    "sand300": "#e6d9c4",
    "sand400": "#d9c9ae",
    "plate": "#e6d9c4",  # card thumbnails sit on sand-100, so they go darker
    # structure
    "grid": "#d6c6ac",
    "axis": "#9c8f7c",
    "faint": "#c9b593",
    # ink
    "ink900": "#2f2a25",
    "ink500": "#6f665c",
    "ink400": "#8a8074",
    # warm plot colors
    "clay": "#bf5b2e",
    "umber": "#8c6239",
    "ochre": "#c99a2e",
    "olive": "#7d8447",
    "brick": "#a8553f",
    "sage": "#5f7161",
}


def pts_to_str(pts):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def polyline(pts, stroke, width=2.0, opacity=1.0, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<polyline points="{pts_to_str(pts)}" fill="none" stroke="{stroke}" '
        f'stroke-width="{width}" stroke-opacity="{opacity}" '
        f'stroke-linecap="round" stroke-linejoin="round"{d}/>'
    )


def line(p0, p1, stroke, width=1.0, opacity=1.0, dash=None):
    return polyline([p0, p1], stroke, width, opacity, dash)


def arrow(p0, p1, colour, width, opacity=1.0, dash=None, head_max=12.0):
    """A line from p0 to p1 with a filled triangular head at p1."""
    (x1, y1), (x2, y2) = p0, p1
    dx, dy = x2 - x1, y2 - y1
    ln = math.hypot(dx, dy)
    if ln < 0.5:
        return ""
    ux, uy = dx / ln, dy / ln
    head = min(head_max, ln * 0.42)
    hw = head * 0.44
    bx, by = x2 - ux * head, y2 - uy * head
    px, py = -uy, ux
    return polyline(
        [(x1, y1), (bx + ux, by + uy)], colour, width, opacity, dash
    ) + (
        f'<path d="M{x2:.1f},{y2:.1f} L{bx + px * hw:.1f},{by + py * hw:.1f} '
        f'L{bx - px * hw:.1f},{by - py * hw:.1f} Z" fill="{colour}" '
        f'fill-opacity="{opacity}"/>'
    )


def right_angle(corner, u1, u2, size=9.0, colour=None, width=1.3):
    """The small square that marks a right angle at `corner`, opening along
    the unit vectors u1 and u2."""
    cx, cy = corner
    return polyline(
        [
            (cx + u1[0] * size, cy + u1[1] * size),
            (cx + (u1[0] + u2[0]) * size, cy + (u1[1] + u2[1]) * size),
            (cx + u2[0] * size, cy + u2[1] * size),
        ],
        colour,
        width,
    )


def unit(p0, p1):
    """Unit vector pointing from p0 to p1."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    ln = math.hypot(dx, dy) or 1.0
    return (dx / ln, dy / ln)


def halo(p0, p1, colour, width=9.0, opacity=0.16):
    """A soft band under an arrow, so a step that lands on top of another
    vector still reads as a distinct part of the walk."""
    return line(p0, p1, colour, width, opacity)


def text(
    x, y, s, colour, size=12, family="mono", anchor="middle", italic=False,
    boxed=None,
):
    """A text label. `boxed` fills a plate-colored rect behind it, which is
    what makes labels legible where they have to sit over grid lines or
    crossing arrows — crowded diagrams have nowhere else to put them."""
    fam = MONO if family == "mono" else SERIF
    st = ' font-style="italic"' if italic else ""
    out = ""
    if boxed:
        per_char = 0.62 if family == "mono" else 0.52
        bw = len(s) * size * per_char + 9
        bh = size + 6
        bx = {"middle": x - bw / 2, "start": x - 3, "end": x - bw + 3}[anchor]
        out = (
            f'<rect x="{bx:.1f}" y="{y - bh / 2:.1f}" width="{bw:.1f}" '
            f'height="{bh:.1f}" rx="3" fill="{boxed}" opacity="0.9"/>'
        )
    return out + (
        f'<text x="{x:.1f}" y="{y:.1f}" fill="{colour}" font-family="{fam}" '
        f'font-size="{size}" text-anchor="{anchor}" '
        f'dominant-baseline="middle"{st}>{s}</text>'
    )


def svg_doc(w, h, body, title, background=None, clip_id=None):
    """Wrap body in an SVG root. clip_id clips content to the full canvas so
    anything running out of range is cut cleanly at the edge."""
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" role="img" aria-label="{title}">'
    ]
    if background:
        out.append(f'  <rect width="{w}" height="{h}" fill="{background}"/>')
    if clip_id:
        out.append(
            f'  <defs><clipPath id="{clip_id}">'
            f'<rect width="{w}" height="{h}"/></clipPath></defs>'
        )
        out.append(f'  <g clip-path="url(#{clip_id})">')
    out.append("  " + "\n  ".join(body))
    if clip_id:
        out.append("  </g>")
    out.append("</svg>")
    return "\n".join(out) + "\n"


def write_svg(relpath, markup):
    path = ROOT / relpath
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(markup)
    print(f"wrote {relpath}")
