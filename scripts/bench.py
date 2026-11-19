"""Draw the profile as panels of one logic analyzer. The alt texts of the panels in the README are generated."""

import argparse
import datetime
import html
import json
import math
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path

import flag
import kit
import themes
import uart
from themes import Theme

NAME = "omer"
DATA = Path(__file__).resolve().parent.parent / "data"
EDGE = 16
MONO_ADVANCE = 0.6
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
PANELS = ("capture", "readouts", "year", "bus")
CHANNELS = (
    ("commits", "commits"),
    ("pull_requests", "PRs opened"),
    ("issues", "issues"),
    ("private", "private repos"),
)
READOUTS = (
    ("pull_requests", "pull requests", "merged, {weeks} weeks"),
    ("flake_commits", "flake commits", "{machines} machines"),
    ("skills", "agent skills", "in my flake"),
    ("upstream_prs", "upstream PRs", "merged"),
    ("agent_clis", "agent CLIs", "one rule set"),
)

CAPTURE_FOOT = 8
PIN_SIZE = 18

READOUT_TOP = 28
READOUT_BOTTOM = 28
READOUT_GUTTER = 16
DIGIT_HEIGHT = 56
LABEL_GAP = 34
SUBLABEL_GAP = 22
LABEL_SIZE = 15
SUBLABEL_SIZE = 13.5

LANES_TOP = 46
LANE_FOOT = 12
TRACE_RISE = 42
TRACE_STROKE = 2
FILL_SHARE = 0.24
CHANNEL_SIZE = 15
CHANNEL_LABEL_INDENT = 34
CHANNEL_LABEL_SIZE = 14
TOTAL_SIZE = 16
AXIS_HEIGHT = 38
TICK_DROP = 34
TICK_LENGTH = 6
TICK_SIZE = 12.5
TICK_GAP = 6
TICK_LABEL_INDENT = 5

BUS_ROW = 142
YEAR_BASELINE = 31
YEAR_SIZE = 14
CELL_TOP = 46
CELL_BOTTOM = 90
CELL_STROKE = 1.8
CURRENT_SHARE = 0.16
NOTCH = 9
NAME_SIZE = 14
CAPTION_BASELINE = 112
CAPTION_LINE = 17
CAPTION_LINES = 2
CAPTION_SIZE = 12.5

COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
IMAGE = re.compile(r"<img\b[^>]*>")
SOURCE = re.compile(r'\bsrc="assets/([a-z]+)-light\.svg"')
ALT = re.compile(r'\balt="[^"]*"')


@dataclass(frozen=True)
class Format:
    suffix: str
    width: int
    capture_left: int
    frames_per_row: int
    idle_cells: int
    readout_columns: int
    plot_left: int
    plot_right_inset: int
    lane: int
    label_lift: int
    bus_columns: int

    @property
    def capture(self) -> uart.Layout:
        return uart.Layout(self.width, self.capture_left, self.frames_per_row, self.idle_cells)

    @property
    def bus_cell(self) -> float:
        return (self.width - 2 * EDGE) / self.bus_columns


FORMATS = (
    Format(
        suffix="",
        width=846,
        capture_left=60,
        frames_per_row=4,
        idle_cells=3,
        readout_columns=5,
        plot_left=176,
        plot_right_inset=112,
        lane=58,
        label_lift=12,
        bus_columns=7,
    ),
    Format(
        suffix="-narrow",
        width=360,
        capture_left=48,
        frames_per_row=2,
        idle_cells=2,
        readout_columns=2,
        plot_left=EDGE,
        plot_right_inset=EDGE,
        lane=88,
        label_lift=56,
        bus_columns=2,
    ),
)


@dataclass(frozen=True)
class Stop:
    year: str
    name: str
    caption: tuple[str, ...]


@dataclass(frozen=True)
class Data:
    numbers: dict[str, int]
    weeks: tuple[dict, ...]
    timeline: tuple[Stop, ...]


def text_width(content: str, size: float) -> float:
    columns = sum(
        0 if unicodedata.combining(char) else 2 if unicodedata.east_asian_width(char) in "WF" else 1
        for char in content
    )
    return columns * size * MONO_ADVANCE


def whole(value: object, where: str) -> int:
    if type(value) is not int or value < 0:
        sys.exit(f"{where} must be a whole number of 0 or more, found {value!r}")
    return value


def stop(entry: object, index: int) -> Stop:
    where = f"data/profile.json: timeline entry {index + 1}"
    if not isinstance(entry, dict) or not all(isinstance(entry.get(key), str) for key in ("year", "name")):
        sys.exit(f"{where} needs a text year and a text name")
    caption = entry.get("caption")
    if not isinstance(caption, list) or not 1 <= len(caption) <= CAPTION_LINES or not all(isinstance(line, str) for line in caption):
        sys.exit(f"{where} needs a caption of 1 to {CAPTION_LINES} text lines")
    for page in FORMATS:
        if text_width(entry["name"], NAME_SIZE) > page.bus_cell - 2 * NOTCH:
            sys.exit(f"{where}: the name {entry['name']!r} does not fit a {page.bus_cell:.0f} px cell")
        if any(text_width(line, CAPTION_SIZE) > page.bus_cell for line in caption):
            sys.exit(f"{where}: a caption line of {entry['name']!r} does not fit a {page.bus_cell:.0f} px cell")
    return Stop(entry["year"], entry["name"], tuple(caption))


def week(entry: object, index: int) -> dict:
    where = f"data/activity.json: week {index + 1}"
    if not isinstance(entry, dict) or not isinstance(entry.get("week"), str):
        sys.exit(f"{where} needs a week date")
    try:
        datetime.date.fromisoformat(entry["week"])
    except ValueError:
        sys.exit(f"{where} has the date {entry['week']!r}, which is not YYYY-MM-DD")
    return {"week": entry["week"]} | {key: whole(entry.get(key), f"{where}: {key}") for key, _ in CHANNELS}


def load() -> Data:
    written = json.loads((DATA / "profile.json").read_text(encoding="utf-8"))
    fetched = json.loads((DATA / "activity.json").read_text(encoding="utf-8"))
    shared = written["numbers"].keys() & fetched["numbers"].keys()
    if shared:
        sys.exit(f"data/profile.json and data/activity.json both set {sorted(shared)}")
    numbers = {key: whole(value, f"the count {key!r}") for key, value in (written["numbers"] | fetched["numbers"]).items()}
    missing = [key for key, _, _ in READOUTS if key not in numbers]
    if missing:
        sys.exit(f"the data files set no count for {missing}")
    if not fetched["weeks"] or not written["timeline"]:
        sys.exit("the data files need at least one week and one timeline entry")
    return Data(
        numbers=numbers,
        weeks=tuple(week(entry, index) for index, entry in enumerate(fetched["weeks"])),
        timeline=tuple(stop(entry, index) for index, entry in enumerate(written["timeline"])),
    )


def readout_labels(data: Data) -> list[tuple[int, str, str]]:
    return [
        (data.numbers[key], label, note.format(weeks=len(data.weeks), **data.numbers))
        for key, label, note in READOUTS
    ]


def capture(page: Format, theme: Theme) -> str:
    layout = page.capture
    lines = uart.rows(NAME, layout)
    height = uart.HEADER_HEIGHT + len(lines) * uart.ROW_HEIGHT + CAPTURE_FOOT
    span = layout.x(layout.row_cells) - layout.x(0) + 4
    style = kit.sweep_style(span)
    parts = [kit.panel(page.width, height, theme), *uart.legend(layout, theme)]
    for row, line in enumerate(lines):
        parts.append(f'<g transform="translate(0 {uart.HEADER_HEIGHT + row * uart.ROW_HEIGHT})">')
        parts.append(uart.trace(line.levels, layout, theme))
        parts.append(kit.sweep_cover(f"row-{row}", layout.x(0), 4, span, uart.LOW_Y + 6, theme))
        for column, (start, char) in enumerate(zip(line.frame_starts, line.text)):
            name = f"frame-{row}-{column}"
            style += kit.appear(name, (start + uart.FRAME_CELLS) / layout.row_cells * kit.SWEEP_PERCENT)
            parts.append(f'<g class="{name}">')
            parts += uart.frame_marks(line.levels, start, char, layout, theme)
            parts.append("</g>")
        parts.append(kit.text(EDGE, (uart.HIGH_Y + uart.LOW_Y) / 2 + 6, "TX", PIN_SIZE, theme.ink, weight=600))
        parts.append("</g>")
    return kit.svg(page.width, height, f"UART capture at {uart.BAUD} baud, 8N1, that decodes to {NAME}", style, parts)


def readouts(data: Data, page: Format, theme: Theme) -> str:
    entries = [(str(value), label, note) for value, label, note in readout_labels(data)]
    rows = [entries[first : first + page.readout_columns] for first in range(0, len(entries), page.readout_columns)]
    column = (page.width - 2 * EDGE) / page.readout_columns
    longest = max(len(value) for value, _, _ in entries)
    digit_height = min(DIGIT_HEIGHT, (column - READOUT_GUTTER) / kit.readout_span(longest))
    slant_shift = math.tan(math.radians(kit.SLANT_DEGREES)) * digit_height / 2
    row_height = digit_height + LABEL_GAP + SUBLABEL_GAP + READOUT_BOTTOM
    height = READOUT_TOP + len(rows) * row_height
    parts = [kit.panel(page.width, height, theme)]
    for row, group in enumerate(rows):
        top = READOUT_TOP + row * row_height
        indent = EDGE + (page.readout_columns - len(group)) * column / 2
        for index, (value, label, note) in enumerate(group):
            center = indent + column * (index + 0.5)
            left = center - kit.readout_span(len(value)) * digit_height / 2 + slant_shift
            parts.append(f'<g transform="translate({left:.1f} {top})">')
            parts += kit.readout(digit_height, value, theme)
            parts.append("</g>")
            label_y = top + digit_height + LABEL_GAP
            parts.append(kit.text(center, label_y, label, LABEL_SIZE, theme.ink, anchor="middle", weight=600))
            parts.append(kit.text(center, label_y + SUBLABEL_GAP, note, SUBLABEL_SIZE, theme.muted, anchor="middle"))
    return kit.svg(page.width, height, "Counts shown as seven-segment readouts", kit.lamp_test(theme), parts)


def month_ticks(weeks: tuple[dict, ...], left: float, step: float, y: float, limit: float, theme: Theme) -> list[str]:
    parts = []
    free_from = left
    for index, entry in enumerate(weeks):
        day = datetime.date.fromisoformat(entry["week"])
        name = MONTHS[day.month - 1]
        x = left + index * step
        end = x + TICK_LABEL_INDENT + text_width(name, TICK_SIZE)
        if day.day <= 7 and x >= free_from and end <= limit:
            parts.append(f'<line x1="{x:.1f}" y1="{y}" x2="{x:.1f}" y2="{y + TICK_LENGTH}" stroke="{theme.muted}"/>')
            parts.append(kit.text(x + TICK_LABEL_INDENT, y + TICK_LENGTH + 10, name, TICK_SIZE, theme.muted))
            free_from = end + TICK_GAP
    return parts


def year(weeks: tuple[dict, ...], page: Format, theme: Theme) -> str:
    left, right = page.plot_left, page.width - page.plot_right_inset
    height = LANES_TOP + page.lane * len(CHANNELS) + AXIS_HEIGHT
    step = (right - left) / len(weeks)
    header = f"{len(weeks)} weeks · sqrt, per-lane peak"
    parts = [
        kit.panel(page.width, height, theme),
        kit.text(EDGE, kit.HEADER_BASELINE, header, kit.HEADER_SIZE, theme.muted),
        kit.text(page.width - EDGE, kit.HEADER_BASELINE, "total", kit.HEADER_SIZE, theme.muted, anchor="end"),
    ]
    labels = []
    for row, ((key, label), color) in enumerate(zip(CHANNELS, theme.channels)):
        values = [entry[key] for entry in weeks]
        peak = max(values) or 1
        base = LANES_TOP + page.lane * (row + 1) - LANE_FOOT
        label_y = base - page.label_lift
        points = [
            (left + index * step, base - TRACE_RISE * math.sqrt(value / peak)) for index, value in enumerate(values)
        ]
        path = kit.steps(points, right)
        parts.append(f'<line x1="{left}" y1="{base + 0.5:.1f}" x2="{right}" y2="{base + 0.5:.1f}" stroke="{theme.faint}"/>')
        parts.append(f'<path d="{path}V{base:.1f}H{left:.1f}Z" fill="{themes.mix(theme.surface, color, FILL_SHARE)}"/>')
        parts.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="{TRACE_STROKE}" stroke-linejoin="round"/>')
        labels.append(kit.text(EDGE, label_y, f"D{row}", CHANNEL_SIZE, color, weight=600))
        labels.append(kit.text(EDGE + CHANNEL_LABEL_INDENT, label_y, label, CHANNEL_LABEL_SIZE, theme.ink))
        labels.append(kit.text(page.width - EDGE, label_y, f"{sum(values):,}", TOTAL_SIZE, theme.ink, anchor="end", weight=600))
    cover_height = height - LANES_TOP - AXIS_HEIGHT + 6
    parts.append(kit.sweep_cover("plot", left - 2, LANES_TOP - 4, right - left + 4, cover_height, theme))
    parts += labels
    parts += month_ticks(weeks, left, step, height - TICK_DROP, page.width - EDGE, theme)
    return kit.svg(
        page.width, height, "A year of work drawn as four logic analyzer channels", kit.sweep_style(right - left + 4), parts
    )


def bus(timeline: tuple[Stop, ...], page: Format, theme: Theme) -> str:
    middle = (CELL_TOP + CELL_BOTTOM) / 2
    columns = page.bus_columns
    rows = math.ceil(len(timeline) / columns)
    height = EDGE + rows * BUS_ROW
    cell = page.bus_cell
    parts = [kit.panel(page.width, height, theme)]
    style = ""
    for index, entry in enumerate(timeline):
        row = index // columns
        in_row = min(columns, len(timeline) - row * columns)
        x0 = EDGE + (columns - in_row) * cell / 2 + index % columns * cell
        x1 = x0 + cell
        center = (x0 + x1) / 2
        current = index == len(timeline) - 1
        style += kit.appear(f"cell-{index}", (index + 1) / len(timeline) * kit.SWEEP_PERCENT)
        parts.append(f'<g class="cell-{index}" transform="translate(0 {row * BUS_ROW})">')
        parts.append(
            f'<polygon points="{x0:.1f},{middle} {x0 + NOTCH:.1f},{CELL_TOP} {x1 - NOTCH:.1f},{CELL_TOP} {x1:.1f},{middle} '
            f'{x1 - NOTCH:.1f},{CELL_BOTTOM} {x0 + NOTCH:.1f},{CELL_BOTTOM}" '
            f'fill="{themes.mix(theme.surface, theme.accent, CURRENT_SHARE) if current else "none"}" '
            f'stroke="{theme.accent if current else theme.ink}" stroke-width="{CELL_STROKE}" stroke-linejoin="round"/>'
        )
        year_fill = theme.accent if current else theme.muted
        parts.append(kit.text(x0 + NOTCH, YEAR_BASELINE, entry.year, YEAR_SIZE, year_fill, weight=600))
        parts.append(kit.text(center, middle + 5, entry.name, NAME_SIZE, theme.ink, anchor="middle", weight=600))
        for line, caption in enumerate(entry.caption):
            y = CAPTION_BASELINE + line * CAPTION_LINE
            parts.append(kit.text(center, y, caption, CAPTION_SIZE, theme.muted, anchor="middle"))
        parts.append("</g>")
    return kit.svg(page.width, height, "Timeline drawn as a decoded bus", style, parts)


def alts(data: Data) -> dict[str, str]:
    counts = ", ".join(f"{value:,} {label} ({note})" for value, label, note in readout_labels(data))
    totals = ", ".join(f"{label} {sum(entry[key] for entry in data.weeks):,}" for key, label in CHANNELS)
    stops = "; ".join(f"{entry.year} {entry.name}, {' '.join(entry.caption)}" for entry in data.timeline)
    return {
        "capture": f"A logic analyzer view of a UART line at {uart.BAUD} baud, 8N1. "
        f"Its {len(NAME)} frames decode to the letters {', '.join(NAME)}.",
        "readouts": f"Seven-segment readouts: {counts}.",
        "year": f"Four logic analyzer channels over {len(data.weeks)} weeks, with totals: {totals}.",
        "bus": f"A timeline drawn as a decoded bus: {stops}.",
    }


def with_alts(page: str, texts: dict[str, str], readme: Path) -> str:
    commented = [match.span() for match in COMMENT.finditer(page)]
    found = []

    def rewrite(match: re.Match) -> str:
        tag = match.group(0)
        source = SOURCE.search(tag)
        if not source or source.group(1) not in texts or any(first <= match.start() < last for first, last in commented):
            return tag
        found.append(source.group(1))
        alt = f'alt="{html.escape(texts[source.group(1)])}"'
        return ALT.sub(lambda _: alt, tag) if ALT.search(tag) else f"{tag[:-1].rstrip(' /')} {alt}>"

    rewritten = IMAGE.sub(rewrite, page)
    if sorted(found) != sorted(texts):
        sys.exit(f"{readme} needs exactly one <img> of assets/<panel>-light.svg for each of {sorted(texts)}, found {sorted(found)}")
    return rewritten


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out_dir", type=Path, help="folder that receives <panel>-<theme><format>.svg and flag-tr.svg")
    parser.add_argument("readme", type=Path, help="README whose panel alt texts are rewritten")
    args = parser.parse_args()
    data = load()
    renderers = {
        "capture": capture,
        "readouts": lambda page, theme: readouts(data, page, theme),
        "year": lambda page, theme: year(data.weeks, page, theme),
        "bus": lambda page, theme: bus(data.timeline, page, theme),
    }
    files = {
        args.out_dir / f"{name}-{variant}{page.suffix}.svg": renderers[name](page, theme)
        for page in FORMATS
        for variant, theme in themes.THEMES.items()
        for name in PANELS
    }
    files[args.out_dir / "flag-tr.svg"] = flag.draw()
    files[args.readme] = with_alts(args.readme.read_text(encoding="utf-8"), alts(data), args.readme)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for path, content in files.items():
        path.write_text(content, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
