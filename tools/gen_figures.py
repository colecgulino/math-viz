#!/usr/bin/env python3
"""Generate the in-page explanatory figures in assets/figures/.

    python3 tools/gen_figures.py

Each panel is written as its own SVG rather than one wide multi-panel file, so
the page can lay them side by side on a desktop and stack them on a phone. A
single wide SVG would shrink to fit a narrow screen and take its labels down to
a few pixels with it.
"""

from svgkit import P, arrow, halo, line, svg_doc, text, write_svg

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


if __name__ == "__main__":
    standard_basis()
    custom_basis()
