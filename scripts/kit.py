from xml.sax.saxutils import escape

from themes import Theme

FONT = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
CYCLE_SECONDS = 30
SWEEP_PERCENT = 10
STILL = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
HEADER_BASELINE = 28
HEADER_SIZE = 14
APPEAR_FADE_PERCENT = 0.6
LAMP_HOLD_PERCENT = 1.5
LAMP_END_PERCENT = 3
SLANT_DEGREES = 6
DIGIT_ASPECT = 0.52
DIGIT_PITCH = 0.82
SEGMENT_THICKNESS = 0.12

SEGMENTS = {
    "0": "abcdef",
    "1": "bc",
    "2": "abged",
    "3": "abgcd",
    "4": "fgbc",
    "5": "afgcd",
    "6": "afgedc",
    "7": "abc",
    "8": "abcdefg",
    "9": "abcdfg",
}


def svg(width: int, height: int, title: str, style: str, parts: list[str]) -> str:
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" role="img" font-family="{FONT}">',
            f"<title>{escape(title)}</title>",
            f"<style>{style}{STILL}</style>",
            *parts,
            "</svg>",
        ]
    ) + "\n"


def panel(width: int, height: int, theme: Theme) -> str:
    return (
        f'<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="10" '
        f'fill="{theme.surface}" stroke="{theme.edge}" stroke-width="1.5"/>'
    )


def text(
    x: float, y: float, content: str, size: float, fill: str, anchor: str = "start", weight: int = 400
) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" '
        f'text-anchor="{anchor}" fill="{fill}">{escape(content)}</text>'
    )


def horizontal(x: float, y: float, length: float, thick: float) -> str:
    half = thick / 2
    return (
        f"{x + half:.1f},{y:.1f} {x + thick:.1f},{y - half:.1f} {x + length - thick:.1f},{y - half:.1f} "
        f"{x + length - half:.1f},{y:.1f} {x + length - thick:.1f},{y + half:.1f} {x + thick:.1f},{y + half:.1f}"
    )


def vertical(x: float, y: float, length: float, thick: float) -> str:
    half = thick / 2
    return (
        f"{x:.1f},{y + half:.1f} {x + half:.1f},{y + thick:.1f} {x + half:.1f},{y + length - thick:.1f} "
        f"{x:.1f},{y + length - half:.1f} {x - half:.1f},{y + length - thick:.1f} {x - half:.1f},{y + thick:.1f}"
    )


def digit(x: float, y: float, height: float, char: str, theme: Theme) -> list[str]:
    width = height * DIGIT_ASPECT
    thick = height * SEGMENT_THICKNESS
    half = height / 2
    shapes = {
        "a": horizontal(x, y, width, thick),
        "g": horizontal(x, y + half, width, thick),
        "d": horizontal(x, y + height, width, thick),
        "f": vertical(x, y, half, thick),
        "b": vertical(x + width, y, half, thick),
        "e": vertical(x, y + half, half, thick),
        "c": vertical(x + width, y + half, half, thick),
    }
    return [
        f'<polygon points="{points}" fill="{theme.accent}"/>'
        if name in SEGMENTS[char]
        else f'<polygon class="unlit" points="{points}" fill="{theme.ghost}"/>'
        for name, points in shapes.items()
    ]


def readout_span(digits: int) -> float:
    return (digits - 1) * DIGIT_PITCH + DIGIT_ASPECT


def readout(height: float, value: str, theme: Theme) -> list[str]:
    parts = [f'<g transform="skewX(-{SLANT_DEGREES})">']
    for index, char in enumerate(value):
        parts += digit(index * DIGIT_PITCH * height, 0, height, char, theme)
    parts.append("</g>")
    return parts


def steps(points: list[tuple[float, float]], end: float) -> str:
    commands = [f"M{points[0][0]:.1f} {points[0][1]:.1f}"]
    for (_, before), (x, y) in zip(points, points[1:]):
        if y != before:
            commands.append(f"H{x:.1f}V{y:.1f}")
    commands.append(f"H{end:.1f}")
    return "".join(commands)


def lamp_test(theme: Theme) -> str:
    return (
        f"@keyframes lamp{{0%,{LAMP_HOLD_PERCENT}%{{fill:{theme.accent}}}{LAMP_END_PERCENT}%,100%{{fill:{theme.ghost}}}}}"
        f".unlit{{animation:lamp {CYCLE_SECONDS}s linear infinite}}"
    )


def sweep_style(width: float) -> str:
    return (
        f"@keyframes sweep{{0%{{transform:translateX(0)}}{SWEEP_PERCENT}%,100%{{transform:translateX({width:.0f}px)}}}}"
        f"@keyframes head{{0%,{SWEEP_PERCENT - 1}%{{opacity:1}}{SWEEP_PERCENT}%,100%{{opacity:0}}}}"
        f".sweep{{animation:sweep {CYCLE_SECONDS}s linear infinite}}"
        f".head{{animation:head {CYCLE_SECONDS}s linear infinite;opacity:0}}"
    )


def sweep_cover(name: str, x: float, y: float, width: float, height: float, theme: Theme) -> str:
    return (
        f'<clipPath id="{name}"><rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}"/></clipPath>'
        f'<g clip-path="url(#{name})"><g class="sweep" transform="translate({width:.0f} 0)">'
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" fill="{theme.surface}"/>'
        f'<line class="head" x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y + height:.1f}" '
        f'stroke="{theme.accent}" stroke-width="2"/></g></g>'
    )


def appear(name: str, at_percent: float) -> str:
    return (
        f"@keyframes {name}{{0%,{at_percent:.2f}%{{opacity:0}}{at_percent + APPEAR_FADE_PERCENT:.2f}%,100%{{opacity:1}}}}"
        f".{name}{{animation:{name} {CYCLE_SECONDS}s linear infinite}}"
    )
