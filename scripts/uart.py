from dataclasses import dataclass

import kit
from themes import Theme

BAUD = 115200
DATA_BITS = 8
FRAME_CELLS = DATA_BITS + 2
GAP_CELLS = 2

HEADER_HEIGHT = 48
ROW_HEIGHT = 178
HIGH_Y = 18
LOW_Y = 68
BOX_TOP = 90
BOX_HEIGHT = 54
MARGIN = 14
TRACE_STROKE = 2.4
BOX_STROKE = 1.6
DOT_RADIUS = 2.8
GUIDE_DASH = "3 4"
LETTER_SIZE = 34
LETTER_DROP = 37
HEX_SIZE = 15
HEX_DROP = 20
SCALE_TOP = 18
SCALE_TICK = 10
SCALE_GAP = 10


@dataclass(frozen=True)
class Layout:
    width: int
    left: int
    frames_per_row: int
    idle_cells: int

    @property
    def row_cells(self) -> int:
        return (
            2 * self.idle_cells
            + self.frames_per_row * FRAME_CELLS
            + (self.frames_per_row - 1) * GAP_CELLS
        )

    @property
    def cell(self) -> float:
        return (self.width - self.left - MARGIN) / self.row_cells

    def x(self, cells: float) -> float:
        return self.left + cells * self.cell


@dataclass(frozen=True)
class Row:
    text: str
    levels: tuple[int, ...]
    frame_starts: tuple[int, ...]


def frame_levels(byte: int) -> list[int]:
    return [0, *((byte >> bit) & 1 for bit in range(DATA_BITS)), 1]


def row(text: str, layout: Layout) -> Row:
    levels = [1] * layout.idle_cells
    frame_starts = []
    for index, byte in enumerate(text.encode("ascii")):
        if index:
            levels += [1] * GAP_CELLS
        frame_starts.append(len(levels))
        levels += frame_levels(byte)
    levels += [1] * (layout.row_cells - len(levels))
    return Row(text, tuple(levels), tuple(frame_starts))


def rows(text: str, layout: Layout) -> list[Row]:
    step = layout.frames_per_row
    return [row(text[start : start + step], layout) for start in range(0, len(text), step)]


def level_y(level: int) -> int:
    return HIGH_Y if level else LOW_Y


def trace(levels: tuple[int, ...], layout: Layout, theme: Theme) -> str:
    points = [(layout.x(index), float(level_y(level))) for index, level in enumerate(levels)]
    return (
        f'<path d="{kit.steps(points, layout.x(len(levels)))}" fill="none" stroke="{theme.ink}" '
        f'stroke-width="{TRACE_STROKE}" stroke-linejoin="round" stroke-linecap="round"/>'
    )


def frame_marks(
    levels: tuple[int, ...], start: int, char: str, layout: Layout, theme: Theme
) -> list[str]:
    marks = [
        f'<line x1="{layout.x(edge):.1f}" y1="0" x2="{layout.x(edge):.1f}" y2="{BOX_TOP + BOX_HEIGHT}" '
        f'stroke="{theme.faint}" stroke-dasharray="{GUIDE_DASH}"/>'
        for edge in (start, start + FRAME_CELLS)
    ]
    marks += [
        f'<circle cx="{layout.x(start + bit + 0.5):.1f}" cy="{level_y(levels[start + bit])}" '
        f'r="{DOT_RADIUS}" fill="{theme.accent}"/>'
        for bit in range(1, DATA_BITS + 1)
    ]
    middle = layout.x(start + FRAME_CELLS / 2)
    marks += [
        f'<rect x="{layout.x(start + 1):.1f}" y="{BOX_TOP}" width="{DATA_BITS * layout.cell:.1f}" '
        f'height="{BOX_HEIGHT}" rx="6" fill="none" stroke="{theme.accent}" stroke-width="{BOX_STROKE}"/>',
        kit.text(middle, BOX_TOP + LETTER_DROP, char, LETTER_SIZE, theme.ink, anchor="middle", weight=600),
        kit.text(middle, BOX_TOP + BOX_HEIGHT + HEX_DROP, f"0x{ord(char):02X}", HEX_SIZE, theme.muted, anchor="middle"),
    ]
    return marks


def legend(layout: Layout, theme: Theme) -> list[str]:
    bar_end = layout.width - MARGIN
    bar_start = bar_end - FRAME_CELLS * layout.cell
    frame_microseconds = FRAME_CELLS / BAUD * 1e6
    middle = SCALE_TOP + SCALE_TICK / 2
    return [
        kit.text(MARGIN, kit.HEADER_BASELINE, f"{BAUD} baud, 8N1", kit.HEADER_SIZE, theme.muted),
        f'<path d="M{bar_start:.1f} {SCALE_TOP}v{SCALE_TICK}M{bar_start:.1f} {middle:.0f}H{bar_end:.1f}'
        f'M{bar_end:.1f} {SCALE_TOP}v{SCALE_TICK}" fill="none" stroke="{theme.muted}" stroke-width="1.2"/>',
        kit.text(
            bar_start - SCALE_GAP, kit.HEADER_BASELINE, f"{frame_microseconds:.1f} µs", kit.HEADER_SIZE, theme.muted, anchor="end"
        ),
    ]
