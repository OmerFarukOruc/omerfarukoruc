import math

G = 100
LENGTH = 1.5 * G
HEM_SEAM = G / 30
CRESCENT_CENTRE = G / 2
OUTER_DIAMETER = G / 2
INNER_DIAMETER = 0.4 * G
CENTRE_GAP = G / 16
STAR_GAP = G / 3
STAR_DIAMETER = G / 4
STAR_POINTS = 5
RED = "#e30a17"
WHITE = "#ffffff"


def draw() -> str:
    outer_x = HEM_SEAM + CRESCENT_CENTRE
    inner_x = outer_x + CENTRE_GAP
    star_x = inner_x - INNER_DIAMETER / 2 + STAR_GAP + STAR_DIAMETER / 2
    turn = 360 / STAR_POINTS
    star = " ".join(
        f"{star_x + STAR_DIAMETER / 2 * math.cos(math.radians(180 + turn * point)):.2f},"
        f"{G / 2 + STAR_DIAMETER / 2 * math.sin(math.radians(180 + turn * point)):.2f}"
        for point in (0, 2, 4, 1, 3)
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LENGTH:.0f} {G}" '
        f'width="{LENGTH:.0f}" height="{G}" role="img">\n'
        "<title>Flag of Türkiye</title>\n"
        f'<rect width="{LENGTH:.0f}" height="{G}" fill="{RED}"/>\n'
        f'<circle cx="{outer_x:.2f}" cy="{G / 2}" r="{OUTER_DIAMETER / 2}" fill="{WHITE}"/>\n'
        f'<circle cx="{inner_x:.2f}" cy="{G / 2}" r="{INNER_DIAMETER / 2}" fill="{RED}"/>\n'
        f'<polygon points="{star}" fill="{WHITE}"/>\n'
        "</svg>\n"
    )
