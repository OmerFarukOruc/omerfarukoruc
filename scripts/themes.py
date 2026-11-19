from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    surface: str
    edge: str
    ink: str
    muted: str
    accent: str
    channels: tuple[str, str, str, str]

    @property
    def faint(self) -> str:
        return mix(self.surface, self.ink, 0.2)

    @property
    def ghost(self) -> str:
        return mix(self.surface, self.ink, 0.1)


def rgb(color: str) -> tuple[int, int, int]:
    return int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)


def mix(base: str, other: str, share: float) -> str:
    return "#" + "".join(f"{round(a + (b - a) * share):02x}" for a, b in zip(rgb(base), rgb(other)))


def luminance(color: str) -> float:
    linear = [c / 3294.6 if c <= 10 else ((c / 255 + 0.055) / 1.055) ** 2.4 for c in rgb(color)]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(first: str, second: str) -> float:
    lighter, darker = sorted((luminance(first), luminance(second)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


THEMES = {
    "dark": Theme(
        surface="#161b22",
        edge="#3d444d",
        ink="#f0f6fc",
        muted="#b7c0ca",
        accent="#79c0ff",
        channels=("#ff7b72", "#ffa657", "#d2a8ff", "#56d4dd"),
    ),
    "light": Theme(
        surface="#f6f8fa",
        edge="#d1d9e0",
        ink="#1f2328",
        muted="#4b535d",
        accent="#0969da",
        channels=("#cf222e", "#bc4c00", "#8250df", "#1b7c83"),
    ),
}


def main() -> None:
    print(f"{'theme':<8}{'ink':>6}{'muted':>7}{'accent':>8}  channels")
    for name, theme in THEMES.items():
        ratios = " ".join(f"{contrast(color, theme.surface):5.1f}" for color in theme.channels)
        print(
            f"{name:<8}{contrast(theme.ink, theme.surface):6.1f}{contrast(theme.muted, theme.surface):7.1f}"
            f"{contrast(theme.accent, theme.surface):8.1f}  {ratios}"
        )


if __name__ == "__main__":
    main()
