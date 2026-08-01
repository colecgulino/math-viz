#!/usr/bin/env python3
"""Generate the index-card thumbnails in assets/thumbs/.

Each thumbnail is a small, static, self-contained SVG drawn in the same warm
earth palette as assets/theme.css. Re-run after changing the palette:

    python3 tools/gen_thumbs.py
"""

import math
import random
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


# --------------------------------------------------------------- lissajous
def lissajous():
    def curve(a, b, phase, rx, ry, n=260):
        return [
            (
                160 + rx * math.sin(a * (2 * math.pi * i / n) + phase),
                80 - ry * math.sin(b * (2 * math.pi * i / n)),
            )
            for i in range(n + 1)
        ]

    body = [
        polyline(curve(5, 4, math.pi / 2, 116, 54), P["umber"], 1.4, 0.45),
        polyline(curve(3, 4, math.pi / 2, 116, 54), P["clay"], 2.2),
    ]
    write("lissajous.svg", "Interlocking Lissajous curves", body)


# ----------------------------------------------------------------- fourier
def fourier():
    def partial(nterms, n=320):
        out = []
        for i in range(n + 1):
            t = 2 * math.pi * i / n
            v = (4 / math.pi) * sum(
                math.sin((2 * k + 1) * t) / (2 * k + 1) for k in range(nterms)
            )
            out.append((20 + 280 * i / n, 80 - 40 * v))
        return out

    # Ideal square wave the partial sums are converging to.
    square = [
        (20, 80),
        (20, 40),
        (160, 40),
        (160, 120),
        (300, 120),
        (300, 80),
    ]
    body = [
        f'<line x1="12" y1="80" x2="308" y2="80" stroke="{P["axis"]}" stroke-width="1"/>',
        polyline(square, P["faint"], 1.6, 1.0, "4 4"),
        polyline(partial(1), P["ochre"], 1.5, 0.7),
        polyline(partial(3), P["umber"], 1.7, 0.8),
        polyline(partial(11), P["clay"], 2.2),
    ]
    write("fourier.svg", "Square wave built from sine harmonics", body)


# --------------------------------------------------------------- conformal
def conformal():
    ox, oy, sx, sy = 96.0, 80.0, 74.0, 58.0

    def z2(u, v):
        return (ox + sx * (u * u - v * v), oy - sy * (2 * u * v))

    body = []
    for u in [0.35, 0.6, 0.85, 1.1, 1.35]:
        body.append(
            polyline(
                [z2(u, -0.95 + 1.9 * i / 48) for i in range(49)],
                P["umber"],
                1.3,
                0.75,
            )
        )
    for v in [-0.9, -0.6, -0.3, 0.0, 0.3, 0.6, 0.9]:
        body.append(
            polyline(
                [z2(0.3 + 1.1 * i / 48, v) for i in range(49)],
                P["clay"],
                1.3,
                0.75,
            )
        )
    write("conformal.svg", "Cartesian grid warped by a complex map", body)


# ------------------------------------------------------------------- eigen
def eigen():
    a, b, c, d = 1.30, 0.50, 0.35, 1.10
    ox, oy, s = 160.0, 84.0, 30.0

    def T(x, y):
        return (ox + s * (a * x + b * y), oy - s * (c * x + d * y))

    body = []
    for k in [-2, -1, 0, 1, 2]:  # transformed grid
        body.append(polyline([T(k, -2), T(k, 2)], P["faint"], 1.3))
        body.append(polyline([T(-2, k), T(2, k)], P["faint"], 1.3))

    # Eigen-directions of [[a,b],[c,d]] (real, distinct for these values).
    tr, det = a + d, a * d - b * c
    disc = math.sqrt(tr * tr - 4 * det)
    for lam, colour, wdt in (
        ((tr + disc) / 2, P["clay"], 2.4),
        ((tr - disc) / 2, P["olive"], 2.4),
    ):
        vx, vy = b, lam - a  # (A - lam I) v = 0
        norm = math.hypot(vx, vy)
        vx, vy = vx / norm * 1.85, vy / norm * 1.85
        body.append(
            polyline([(ox, oy), (ox + s * vx, oy - s * vy)], colour, wdt)
        )
        body.append(
            f'<circle cx="{ox + s * vx:.1f}" cy="{oy - s * vy:.1f}" r="3.6" fill="{colour}"/>'
        )
        body.append(
            polyline([(ox, oy), (ox - s * vx, oy + s * vy)], colour, wdt, 0.35)
        )
    write("eigen.svg", "Grid under a linear map with its eigen-directions", body)


# ------------------------------------------------------------------ taylor
def taylor():
    x0, x1 = -4.3, 4.3
    sx, sy, oy = 300.0 / (x1 - x0), 30.0, 80.0

    def series(order, n=300):
        out = []
        for i in range(n + 1):
            x = x0 + (x1 - x0) * i / n
            if order is None:
                y = math.sin(x)
            else:
                y = sum(
                    (-1) ** k * x ** (2 * k + 1) / math.factorial(2 * k + 1)
                    for k in range(order)
                )
            # Let divergent tails run past the plate; the clipPath cuts them.
            if abs(y) > 3.2:
                y = math.copysign(3.2, y)
            out.append((10 + sx * (x - x0), oy - sy * y))
        return out

    body = [
        f'<line x1="10" y1="80" x2="310" y2="80" stroke="{P["axis"]}" stroke-width="1"/>',
        polyline(series(1), P["ochre"], 1.5, 0.75),
        polyline(series(2), P["olive"], 1.5, 0.8),
        polyline(series(3), P["umber"], 1.7, 0.85),
        polyline(series(None), P["clay"], 2.3),
    ]
    write(
        "taylor.svg",
        "Sine curve with successive Taylor approximations",
        body,
        clip=True,
    )


# -------------------------------------------------------------- randomwalk
def randomwalk():
    rng = random.Random(11)
    body = [
        f'<line x1="14" y1="86" x2="306" y2="86" stroke="{P["axis"]}" stroke-width="1"/>'
    ]
    for colour, opacity, width in (
        (P["sage"], 0.55, 1.4),
        (P["umber"], 0.7, 1.6),
        (P["clay"], 1.0, 2.1),
    ):
        y, n, pts = 0.0, 88, []
        for i in range(n + 1):
            pts.append((14 + 292 * i / n, 86 - max(-14, min(14, y)) * 5.2))
            y += rng.gauss(0, 1)
        body.append(polyline(pts, colour, width, opacity))
    write("randomwalk.svg", "Three random walks diverging from zero", body)


if __name__ == "__main__":
    lissajous()
    fourier()
    conformal()
    eigen()
    taylor()
    randomwalk()
