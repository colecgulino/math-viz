#!/usr/bin/env python3
"""Generate the index-card thumbnails in assets/thumbs/.

Each thumbnail is a small, static, self-contained SVG drawn in the same warm
earth palette as assets/theme.css. Re-run after changing the palette:

    python3 tools/gen_thumbs.py
"""

from svgkit import P, arrow, line, right_angle, svg_doc, unit, write_svg

W, H = 320, 160


# ------------------------------------------------------- linear combinations
def lincomb():
    """Two vectors and the tip-to-tail walk that builds 2v1 + v2."""
    u, ox, oy = 30.0, 78.0, 140.0

    def V(x, y):
        return (ox + u * x, oy - u * y)

    body = []
    for gx in range(0, 9):  # faint grid
        x = ox + u * gx - 60
        body.append(line((x, 8), (x, 152), P["grid"], 1.0))
    for gy in range(-1, 5):
        y = oy - u * gy
        body.append(line((8, y), (312, y), P["grid"], 1.0))

    o = V(0, 0)
    body.append(arrow(o, V(2, 1), P["clay"], 2.2))
    body.append(arrow(o, V(1, 2), P["olive"], 2.2))
    body.append(arrow(V(2, 1), V(4, 2), P["clay"], 1.7, 0.85, "5 4"))
    body.append(arrow(V(4, 2), V(5, 4), P["olive"], 1.7, 0.85, "5 4"))
    body.append(arrow(o, V(5, 4), P["ink900"], 2.8))

    write_svg(
        "assets/thumbs/lincomb.svg",
        svg_doc(
            W,
            H,
            body,
            "Two vectors combined tip to tail",
            background=P["plate"],
            clip_id="plate",
        ),
    )


# ------------------------------------------------------------- dot products
def dotproduct():
    """Vector a, vector b, and the shadow a casts on b."""
    u, ox, oy = 26.0, 62.0, 118.0

    def V(x, y):
        return (ox + u * x, oy - u * y)

    a, b = (3, 3), (7, 1)
    d = a[0] * b[0] + a[1] * b[1]
    bb = b[0] ** 2 + b[1] ** 2
    p = (d / bb * b[0], d / bb * b[1])

    body = []
    for gx in range(-2, 10):
        body.append(line((ox + u * gx, 8), (ox + u * gx, 152), P["grid"], 1.0))
    for gy in range(-4, 5):
        body.append(line((8, oy - u * gy), (312, oy - u * gy), P["grid"], 1.0))

    o, at, bt, pt = V(0, 0), V(*a), V(*b), V(*p)
    body.append(line(V(-2, -0.29), V(9, 1.29), P["sand400"], 1.1, dash="4 4"))
    body.append(line(at, pt, P["ink400"], 1.2, 0.8, dash="4 3"))
    body.append(right_angle(pt, unit(pt, at), unit(pt, o), 7, P["ink400"], 1.1))
    body.append(arrow(o, bt, P["sage"], 2.2))
    body.append(arrow(o, pt, P["ochre"], 3.4, head_max=11))
    body.append(arrow(o, at, P["clay"], 2.2))

    write_svg(
        "assets/thumbs/dotproduct.svg",
        svg_doc(
            W,
            H,
            body,
            "One vector projected onto another",
            background=P["plate"],
            clip_id="plate",
        ),
    )


if __name__ == "__main__":
    lincomb()
    dotproduct()
