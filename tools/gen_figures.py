#!/usr/bin/env python3
"""Generate the in-page explanatory figures in assets/figures/.

    python3 tools/gen_figures.py

Each panel is written as its own SVG rather than one wide multi-panel file, so
the page can lay them side by side on a desktop and stack them on a phone. A
single wide SVG would shrink to fit a narrow screen and take its labels down to
a few pixels with it.
"""

from svgkit import (
    P, arrow, halo, line, right_angle, svg_doc, text, unit, write_svg,
)

PW, PH = 364, 306  # panel box
U = 40  # world unit in px
OX, OY = 68, 222  # origin within the panel
BG = P["sand100"]  # label backing, matches the panel plate


def plate(cells_x=(-1, 7), cells_y=(-2, 5)):
    """Panel background, grid and axes."""
    out = [
        f'<rect x="0.5" y="0.5" width="{PW - 1}" height="{PH - 1}" rx="10" '
        f'fill="{P["sand100"]}" stroke="{P["sand400"]}" stroke-width="1"/>'
    ]
    for i in range(cells_x[0], cells_x[1] + 1):
        x = OX + i * U
        if 0 < x < PW:
            out.append(line((x, 6), (x, PH - 6), P["grid"], 1.0))
    for j in range(cells_y[0], cells_y[1] + 1):
        y = OY - j * U
        if 6 < y < PH - 6:
            out.append(line((6, y), (PW - 6, y), P["grid"], 1.0))
    out.append(line((6, OY), (PW - 6, OY), P["axis"], 1.3))
    out.append(line((OX, 6), (OX, PH - 6), P["axis"], 1.3))
    return out


def resultant(body, w):
    body.append(arrow((OX, OY), w, P["ink900"], 3.0, head_max=13))
    body.append(
        text(w[0] + 20, w[1] - 12, "w", P["ink900"], 17, "serif",
             italic=True, boxed=BG)
    )


W_TIP = (OX + 3 * U, OY - 2 * U)  # both panels land on w = (3, 2)


def standard_basis():
    body = plate()
    corner = (OX + 3 * U, OY)

    # the walk: 3 along i, then 2 along j
    body.append(halo((OX, OY), corner, P["clay"]))
    body.append(halo(corner, W_TIP, P["olive"]))
    body.append(arrow((OX, OY), corner, P["clay"], 1.8, 0.95, dash="6 5"))
    body.append(arrow(corner, W_TIP, P["olive"], 1.8, 0.95, dash="6 5"))

    # the basis vectors themselves, bold over the walk
    body.append(arrow((OX, OY), (OX + U, OY), P["clay"], 3.4, head_max=11))
    body.append(arrow((OX, OY), (OX, OY - U), P["olive"], 3.4, head_max=11))

    body.append(text(OX + 22, OY - 17, "î", P["clay"], 16, "serif", italic=True, boxed=BG))
    body.append(text(OX - 19, OY - 24, "ĵ", P["olive"], 16, "serif", italic=True, boxed=BG))
    body.append(text(OX + 78, OY + 18, "3î", P["clay"], 12, boxed=BG))
    body.append(text(OX + 142, OY - 40, "2ĵ", P["olive"], 12, boxed=BG))
    resultant(body, W_TIP)

    write_svg(
        "assets/figures/basis-standard.svg",
        svg_doc(PW, PH, body, "w reached as three steps along i-hat then two along j-hat"),
    )


def custom_basis():
    # a and b straddle w rather than running alongside it, so the walk stays
    # clear of the resultant: step down along 0.5a first, then climb 2.5b.
    body = plate()
    mid = (OX + 0.5 * U, OY + 0.5 * U)

    body.append(halo((OX, OY), mid, P["sage"]))
    body.append(halo(mid, W_TIP, P["umber"]))
    body.append(arrow((OX, OY), mid, P["sage"], 1.8, 0.95, dash="6 5"))
    body.append(arrow(mid, W_TIP, P["umber"], 1.8, 0.95, dash="6 5"))

    body.append(arrow((OX, OY), (OX + U, OY + U), P["sage"], 3.4, head_max=11))
    body.append(arrow((OX, OY), (OX + U, OY - U), P["umber"], 3.4, head_max=11))

    body.append(text(OX + 27, OY + 53, "a", P["sage"], 15, "serif", italic=True, boxed=BG))
    body.append(text(OX + 27, OY - 53, "b", P["umber"], 15, "serif", italic=True, boxed=BG))
    body.append(text(OX - 6, OY + 28, "0.5a", P["sage"], 12, boxed=BG))
    body.append(text(OX + 88, OY - 10, "2.5b", P["umber"], 12, boxed=BG))
    resultant(body, W_TIP)

    write_svg(
        "assets/figures/basis-custom.svg",
        svg_doc(PW, PH, body, "The same w reached as half a step along a then two and a half along b"),
    )


# --------------------------------------------------------------- dot products
def V(x, y, u=U, ox=OX, oy=OY):
    return (ox + u * x, oy - u * y)


def dot_projection():
    """a, b, and the shadow a casts on b."""
    body = plate()
    a, b = (2, 3), (5, 1)
    d = a[0] * b[0] + a[1] * b[1]  # 13
    bb = b[0] ** 2 + b[1] ** 2  # 26
    p = (d / bb * b[0], d / bb * b[1])  # (2.5, 0.5)

    o, at, bt, pt = V(0, 0), V(*a), V(*b), V(*p)

    # b's line, extended, is the axis a is measured against
    body.append(line(V(-1, -0.2), V(7, 1.4), P["sand400"], 1.2, dash="4 5"))
    body.append(line(at, pt, P["ink400"], 1.3, 0.8, dash="4 4"))  # the drop
    body.append(right_angle(pt, unit(pt, at), unit(pt, o), 9, P["ink400"]))

    body.append(arrow(o, bt, P["sage"], 2.8))
    body.append(arrow(o, pt, P["ochre"], 4.0, head_max=13))
    body.append(arrow(o, at, P["clay"], 2.8))

    body.append(text(at[0] - 16, at[1] - 8, "a", P["clay"], 15, "serif", italic=True, boxed=BG))
    body.append(text(bt[0] + 15, bt[1] - 10, "b", P["sage"], 15, "serif", italic=True, boxed=BG))
    body.append(text(pt[0] - 6, pt[1] + 20, "p", P["ochre"], 15, "serif", italic=True, boxed=BG))

    write_svg(
        "assets/figures/dot-projection.svg",
        svg_doc(PW, PH, body, "Vector a projected onto vector b, giving the shadow p"),
    )


def dot_perpendicular():
    """The same construction when the shadow vanishes."""
    body = plate()
    a, b = (1, 3), (3, -1)  # a . b = 3 - 3 = 0
    o, at, bt = V(0, 0), V(*a), V(*b)

    body.append(line(V(-1.33, 0.44), V(7, -2.33), P["sand400"], 1.2, dash="4 5"))
    body.append(right_angle(o, unit(o, at), unit(o, bt), 11, P["ink400"]))

    body.append(arrow(o, bt, P["sage"], 2.8))
    body.append(arrow(o, at, P["clay"], 2.8))
    body.append(f'<circle cx="{o[0]}" cy="{o[1]}" r="4.5" fill="{P["ochre"]}"/>')

    body.append(text(at[0] - 16, at[1] - 8, "a", P["clay"], 15, "serif", italic=True, boxed=BG))
    body.append(text(bt[0] + 16, bt[1] + 6, "b", P["sage"], 15, "serif", italic=True, boxed=BG))
    body.append(text(o[0] - 30, o[1] + 22, "p = 0", P["ochre"], 12, boxed=BG))

    write_svg(
        "assets/figures/dot-perpendicular.svg",
        svg_doc(PW, PH, body, "Perpendicular vectors, where the projection collapses to a point"),
    )


def length_pythagoras():
    """v = (3, 4) as the hypotenuse of a right triangle."""
    body = plate()
    o, vt, corner = V(0, 0), V(3, 4), V(3, 0)

    # Clay marks the x-component and sage the y-component in both length
    # figures, with v itself in ink, so the pair reads as one diagram.
    body.append(line(o, corner, P["clay"], 1.8, 0.9, dash="5 4"))
    body.append(line(corner, vt, P["sage"], 1.8, 0.9, dash="5 4"))
    body.append(right_angle(corner, unit(corner, o), unit(corner, vt), 10, P["ink400"]))
    body.append(arrow(o, vt, P["ink900"], 3.0))

    body.append(text(V(1.5, 0)[0], V(1.5, 0)[1] + 18, "3", P["clay"], 13, boxed=BG))
    body.append(text(V(3, 2)[0] + 18, V(3, 2)[1], "4", P["sage"], 13, boxed=BG))
    body.append(text(V(0.7, 2.7)[0], V(0.7, 2.7)[1], "|v| = 5", P["ink900"], 13, boxed=BG))
    body.append(text(vt[0] + 20, vt[1] - 10, "v", P["ink900"], 16, "serif", italic=True, boxed=BG))

    write_svg(
        "assets/figures/length-pythagoras.svg",
        svg_doc(PW, PH, body, "The vector (3, 4) as the hypotenuse of a 3-4-5 right triangle"),
    )


def length_squares():
    """The same vector with literal squares on its legs: v·v = 9 + 16."""
    u, ox, oy = 30, 56, 176
    body = plate_at(u, ox, oy, cells_x=(-1, 9), cells_y=(-4, 4))

    def W(x, y):
        return (ox + u * x, oy - u * y)

    # square on the horizontal leg, dropped below the axis
    body.append(
        f'<rect x="{W(0, 0)[0]}" y="{W(0, 0)[1]}" width="{3 * u}" height="{3 * u}" '
        f'fill="{P["clay"]}" fill-opacity="0.13" stroke="{P["clay"]}" '
        f'stroke-width="1.4" stroke-opacity="0.55"/>'
    )
    # square on the vertical leg, laid out to its right
    body.append(
        f'<rect x="{W(3, 4)[0]}" y="{W(3, 4)[1]}" width="{4 * u}" height="{4 * u}" '
        f'fill="{P["sage"]}" fill-opacity="0.13" stroke="{P["sage"]}" '
        f'stroke-width="1.4" stroke-opacity="0.55"/>'
    )
    body.append(line(W(0, 0), W(3, 0), P["clay"], 2.2, 0.8))
    body.append(line(W(3, 0), W(3, 4), P["sage"], 2.2, 0.8))
    body.append(arrow(W(0, 0), W(3, 4), P["ink900"], 2.8))

    body.append(text(W(1.5, -1.5)[0], W(1.5, -1.5)[1], "3² = 9", P["clay"], 13, boxed=BG))
    body.append(text(W(5, 2)[0], W(5, 2)[1], "4² = 16", P["sage"], 13, boxed=BG))
    body.append(text(W(1.1, 2.5)[0], W(1.1, 2.5)[1], "v", P["ink900"], 16, "serif", italic=True, boxed=BG))

    write_svg(
        "assets/figures/length-squares.svg",
        svg_doc(PW, PH, body, "Squares built on the components of v, with areas 9 and 16"),
    )


def triangle_strict():
    """a and b tip to tail, with a + b as the direct route."""
    body = plate()
    o, at, sm = V(0, 0), V(3, 1), V(4, 4)

    body.append(arrow(o, at, P["clay"], 2.6))
    body.append(arrow(at, sm, P["sage"], 2.6))
    body.append(arrow(o, sm, P["ink900"], 3.0))

    # All three labels sit outside the triangle, each beside its own edge —
    # the interior is a narrow wedge, and a backing box placed in it punches a
    # gap in whichever arrow it lands on.
    body.append(text(165, 212, "|a|", P["clay"], 13, boxed=BG))
    body.append(text(227, 128, "|b|", P["sage"], 13, boxed=BG))
    body.append(text(120, 120, "|a + b|", P["ink900"], 13, boxed=BG))

    write_svg(
        "assets/figures/triangle-strict.svg",
        svg_doc(PW, PH, body, "Two vectors tip to tail with the shorter direct route between the ends"),
    )


def triangle_equality():
    """The degenerate case: a and b parallel, so the triangle flattens."""
    body = plate()
    o, at, sm = V(0, 0), V(2, 1), V(6, 3)

    # a + b lies exactly under the other two, so it goes down as a band
    body.append(halo(o, sm, P["ink900"], 11, 0.2))
    body.append(arrow(o, at, P["clay"], 2.6))
    body.append(arrow(at, sm, P["sage"], 2.6))

    body.append(text(100, 186, "|a|", P["clay"], 13, boxed=BG))
    body.append(text(220, 126, "|b|", P["sage"], 13, boxed=BG))
    body.append(text(200, 185, "|a + b|", P["ink900"], 13, boxed=BG))

    write_svg(
        "assets/figures/triangle-equality.svg",
        svg_doc(PW, PH, body, "Two parallel vectors, where the triangle collapses onto a line"),
    )


def plate_at(u, ox, oy, cells_x, cells_y):
    """plate() with a custom scale and origin."""
    out = [
        f'<rect x="0.5" y="0.5" width="{PW - 1}" height="{PH - 1}" rx="10" '
        f'fill="{P["sand100"]}" stroke="{P["sand400"]}" stroke-width="1"/>'
    ]
    for i in range(cells_x[0], cells_x[1] + 1):
        x = ox + i * u
        if 0 < x < PW:
            out.append(line((x, 6), (x, PH - 6), P["grid"], 1.0))
    for j in range(cells_y[0], cells_y[1] + 1):
        y = oy - j * u
        if 6 < y < PH - 6:
            out.append(line((6, y), (PW - 6, y), P["grid"], 1.0))
    out.append(line((6, oy), (PW - 6, oy), P["axis"], 1.3))
    out.append(line((ox, 6), (ox, PH - 6), P["axis"], 1.3))
    return out


if __name__ == "__main__":
    standard_basis()
    custom_basis()
    dot_projection()
    dot_perpendicular()
    length_pythagoras()
    length_squares()
    triangle_strict()
    triangle_equality()
