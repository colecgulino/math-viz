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


# ------------------------------------------------- linear transformations
def transformation():
    """A square lattice with its sheared image laid over the top."""
    u, ox, oy = 22.0, 160.0, 80.0
    M = (1.15, 0.75, -0.5, 0.95)

    def G(x, y):
        return (ox + u * x, oy - u * y)

    def T(x, y):
        return G(M[0] * x + M[1] * y, M[2] * x + M[3] * y)

    body = []
    for i in range(-4, 5):  # the starting grid, pale
        body.append(line(G(i, -4), G(i, 4), P["sand400"], 1.0))
        body.append(line(G(-4, i), G(4, i), P["sand400"], 1.0))
    for i in range(-4, 5):  # and where it ends up
        axis = i == 0
        body.append(
            line(T(i, -4), T(i, 4), P["sage"], 2.0 if axis else 1.1,
                 0.9 if axis else 0.4)
        )
        body.append(
            line(T(-4, i), T(4, i), P["clay"], 2.0 if axis else 1.1,
                 0.9 if axis else 0.4)
        )
    for i in range(-4, 5):
        for j in range(-4, 5):
            x, y = T(i, j)
            if 6 < x < 314 and 4 < y < 156:
                body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.9" fill="{P["umber"]}"/>')
    body.append(arrow(G(0, 0), T(1, 0), P["clay"], 2.4, head_max=9))
    body.append(arrow(G(0, 0), T(0, 1), P["sage"], 2.4, head_max=9))

    write_svg(
        "assets/thumbs/transformation.svg",
        svg_doc(
            W, H, body, "A square grid and its sheared image",
            background=P["plate"], clip_id="plate",
        ),
    )


# ------------------------------------------------------------ vector spaces
def vectorspace():
    """A line through the origin sitting inside the plane: a subspace."""
    u, ox, oy = 26.0, 160.0, 80.0

    def V(x, y):
        return (ox + u * x, oy - u * y)

    body = []
    for gx in range(-6, 7):
        body.append(line(V(gx, -3), V(gx, 3), P["grid"], 1.0))
    for gy in range(-3, 4):
        body.append(line(V(-6, gy), V(6, gy), P["grid"], 1.0))
    body.append(line(V(-6, 0), V(6, 0), P["axis"], 1.2))
    body.append(line(V(0, -3), V(0, 3), P["axis"], 1.2))

    # the subspace, tinted and dashed
    body.append(line(V(-5.4, -2.7), V(5.4, 2.7), P["clay"], 13, 0.16))
    body.append(line(V(-5.4, -2.7), V(5.4, 2.7), P["clay"], 1.4, 0.7, dash="6 5"))
    body.append(arrow(V(0, 0), V(2, 1), P["clay"], 2.4, head_max=10))
    body.append(arrow(V(2, 1), V(4, 2), P["sage"], 2.0, head_max=10))
    body.append(f'<circle cx="{V(0, 0)[0]}" cy="{V(0, 0)[1]}" r="3.4" fill="{P["ink900"]}"/>')

    write_svg(
        "assets/thumbs/vectorspace.svg",
        svg_doc(
            W, H, body, "A line through the origin inside the plane",
            background=P["plate"], clip_id="plate",
        ),
    )


# ------------------------------------------------------------- column spaces
def columnspace():
    """Two columns in 3D and the plane they span, orthographic."""
    import math

    yaw, pitch, k = 0.62, 0.42, 15.0
    ox, oy = 152.0, 82.0
    ct, st = math.cos(yaw), math.sin(yaw)
    cp, sp = math.cos(pitch), math.sin(pitch)
    rgt = (-st, ct, 0.0)
    up = (-sp * ct, -sp * st, cp)

    def pr(v):
        d = lambda a, b: a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
        return (ox + k * d(v, rgt), oy - k * d(v, up))

    a1, a2 = (2, 1, -1), (1, 2, -2)
    e1 = (0.8165, 0.4082, -0.4082)          # a1 normalised
    e2 = (-0.0, 0.7071, -0.7071)            # a2 orthogonalised against a1
    def pt(s_, t_):
        return (e1[0] * s_ + e2[0] * t_, e1[1] * s_ + e2[1] * t_,
                e1[2] * s_ + e2[2] * t_)

    R = 3.1
    body = []
    quad = [pr(pt(-R, -R)), pr(pt(R, -R)), pr(pt(R, R)), pr(pt(-R, R))]
    body.append(
        '<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in quad)
        + f' Z" fill="{P["ochre"]}" fill-opacity="0.17"/>'
    )
    for i in range(-3, 4):
        u = i * R / 3
        body.append(line(pr(pt(u, -R)), pr(pt(u, R)), P["ochre"], 1.0, 0.5))
        body.append(line(pr(pt(-R, u)), pr(pt(R, u)), P["ochre"], 1.0, 0.5))
    for ax in ((4.0, 0, 0), (0, 4.0, 0), (0, 0, 4.0)):
        neg = tuple(-c for c in ax)
        body.append(line(pr(neg), pr((0, 0, 0)), P["sand400"], 1.0, dash="3 4"))
        body.append(line(pr((0, 0, 0)), pr(ax), P["axis"], 1.2))
    body.append(arrow(pr((0, 0, 0)), pr(a1), P["clay"], 2.2, head_max=9))
    body.append(arrow(pr((0, 0, 0)), pr(a2), P["sage"], 2.2, head_max=9))
    b = (a1[0] + a2[0], a1[1] + a2[1], a1[2] + a2[2])
    body.append(arrow(pr((0, 0, 0)), pr(b), P["ink900"], 2.6, head_max=10))

    write_svg(
        "assets/thumbs/columnspace.svg",
        svg_doc(
            W, H, body, "Two columns in three dimensions and the plane they span",
            background=P["plate"], clip_id="plate",
        ),
    )


if __name__ == "__main__":
    lincomb()
    dotproduct()
    transformation()
    vectorspace()
    columnspace()
