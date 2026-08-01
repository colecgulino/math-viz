#!/usr/bin/env python3
"""Generate the index-card thumbnails in assets/thumbs/.

Each thumbnail is a small, static, self-contained SVG drawn in the same warm
earth palette as assets/theme.css. Re-run after changing the palette:

    python3 tools/gen_thumbs.py
"""

import math
from pathlib import Path

W, H = 320, 160
OUT = Path(__file__).resolve().parent.parent / "assets" / "thumbs"

# Mirrors the palette in assets/theme.css. Keep the two in sync.
P = {
    "plate": "#e6d9c4",
    "grid": "#d6c6ac",
    "axis": "#b3a389",
    "faint": "#c9b593",
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


def svg(title, body, clip=False):
    """Wrap body in an SVG. With clip=True, drawings are cut at the plate edge
    so curves that run out of range exit cleanly instead of piling up."""
    defs = (
        f'<defs><clipPath id="plate"><rect width="{W}" height="{H}"/></clipPath></defs>\n  '
        if clip
        else ""
    )
    open_g = '<g clip-path="url(#plate)">\n  ' if clip else ""
    close_g = "\n  </g>" if clip else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="img" aria-label="{title}">\n'
        f'  <rect width="{W}" height="{H}" fill="{P["plate"]}"/>\n  '
        + defs
        + open_g
        + "\n  ".join(body)
        + close_g
        + "\n</svg>\n"
    )


def write(name, title, body, clip=False):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(svg(title, body, clip))
    print(f"wrote {name}")


# ------------------------------------------------------- linear combinations
def lincomb():
    """Two vectors and the tip-to-tail walk that builds 2v1 + v2."""
    u, ox, oy = 30.0, 78.0, 140.0

    def W(x, y):
        return (ox + u * x, oy - u * y)

    def arrow(p0, p1, colour, width, opacity=1.0, dash=None):
        (x1, y1), (x2, y2) = p0, p1
        dx, dy = x2 - x1, y2 - y1
        ln = math.hypot(dx, dy)
        ux, uy = dx / ln, dy / ln
        head = min(11.0, ln * 0.4)
        hw = head * 0.42
        bx, by = x2 - ux * head, y2 - uy * head
        px, py = -uy, ux
        out = [polyline([(x1, y1), (bx, by)], colour, width, opacity, dash)]
        out.append(
            f'<path d="M{x2:.1f},{y2:.1f} L{bx + px * hw:.1f},{by + py * hw:.1f} '
            f'L{bx - px * hw:.1f},{by - py * hw:.1f} Z" fill="{colour}" '
            f'fill-opacity="{opacity}"/>'
        )
        return out

    body = []
    for gx in range(0, 9):  # faint grid
        x = ox + u * gx - 60
        body.append(polyline([(x, 8), (x, 152)], P["grid"], 1.0))
    for gy in range(-1, 5):
        y = oy - u * gy
        body.append(polyline([(8, y), (312, y)], P["grid"], 1.0))

    o = W(0, 0)
    body += arrow(o, W(2, 1), P["clay"], 2.2)          # v1
    body += arrow(o, W(1, 2), P["olive"], 2.2)         # v2
    body += arrow(W(2, 1), W(4, 2), P["clay"], 1.7, 0.85, "5 4")   # + v1 again
    body += arrow(W(4, 2), W(5, 4), P["olive"], 1.7, 0.85, "5 4")  # + v2
    body += arrow(o, W(5, 4), "#2f2a25", 2.8)          # the resultant
    write("lincomb.svg", "Two vectors combined tip to tail", body, clip=True)


if __name__ == "__main__":
    lincomb()
