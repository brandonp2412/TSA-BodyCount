#!/usr/bin/env python3
"""Generate deterministic SVG charts from checked-in data."""

from __future__ import annotations

from html import escape

from model import ROOT, aviation_baselines, lifetime_equivalents, load_inputs, scenarios

OUT = ROOT / "charts"
W, H = 1200, 720
BG = "#07111f"
PANEL = "#0d1b2b"
GRID = "#24364a"
TEXT = "#f8fafc"
MUTED = "#9fb3c8"
BLUE = "#53a7ff"
CYAN = "#2dd4bf"
GOLD = "#f5b942"
RED = "#f05252"
WHITE = "#ffffff"
FONT = "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"


def text(x, y, value, size=16, color=TEXT, anchor="start", weight=500):
    return f'<text x="{x:.1f}" y="{y:.1f}" fill="{color}" text-anchor="{anchor}" font-family="{FONT}" font-size="{size}" font-weight="{weight}">{escape(value)}</text>'


def svg_open(title, subtitle):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(title)}</title>',
        f'<desc id="desc">{escape(subtitle)}</desc>',
        f'<rect width="{W}" height="{H}" rx="24" fill="{BG}"/>',
        f'<text x="60" y="70" fill="{TEXT}" font-family="{FONT}" font-size="40" font-weight="900">{escape(title)}</text>',
        f'<text x="60" y="106" fill="{MUTED}" font-family="{FONT}" font-size="18" font-weight="600">{escape(subtitle)}</text>',
        f'<line x1="60" y1="130" x2="1140" y2="130" stroke="{GRID}"/>',
    ]


def footer(source):
    return [
        f'<line x1="60" y1="654" x2="1140" y2="654" stroke="{GRID}"/>',
        text(60, 684, source, 13, MUTED),
        "</svg>",
    ]


def chart1():
    d = load_inputs()
    rows = scenarios(d)
    s = svg_open(
        "TSA LIVES BURNED EACH YEAR",
        "Each bar uses one federal wait-time measurement · 1 life = 79 years",
    )
    left, top, right, bottom = 95, 165, 1140, 535
    max_y = 500
    for tick in range(0, 501, 100):
        y = bottom - tick / max_y * (bottom - top)
        s += [
            f'<line x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}" stroke="{GRID}" stroke-dasharray="5 7"/>',
            text(left - 15, y + 5, str(tick), 13, MUTED, "end"),
        ]
    colors = [BLUE, BLUE, CYAN, GOLD, RED]
    slot = (right - left) / len(rows)
    for i, row in enumerate(rows):
        cx = left + slot * (i + 0.5)
        h = row.lifetime_equivalents / max_y * (bottom - top)
        y = bottom - h
        s.append(
            f'<rect x="{cx-62:.1f}" y="{y:.1f}" width="124" height="{h:.1f}" rx="10" fill="{colors[i]}"/>'
        )
        s.append(text(cx, y - 15, f"{row.lifetime_equivalents:.0f}", 28, WHITE, "middle", 900))
        s.append(text(cx, bottom + 38, row.year_label, 27, WHITE, "middle", 900))
        s.append(text(cx, bottom + 64, f"{row.wait_minutes:.1f} min · {row.short_label}", 13, MUTED, "middle", 700))
    s += footer("Sources: TSA 2024 volume · CDC 79-year lifespan · GAO/BTS wait times")
    return "\n".join(s)


def chart2():
    d = load_inputs()
    rows = scenarios(d)
    baseline = aviation_baselines(d)
    tsa = next(row for row in rows if row.key == "wait_tsa_2003_2004")
    s = svg_open(
        "TSA VS. AVIATION TERRORISTS",
        "Annual human lives · U.S. airport/aircraft attacks and aviation hijackings only",
    )
    s += [
        f'<rect x="70" y="170" width="500" height="390" rx="22" fill="{PANEL}" stroke="{BLUE}" stroke-width="3"/>',
        f'<rect x="630" y="170" width="500" height="390" rx="22" fill="{PANEL}" stroke="{RED}" stroke-width="3"/>',
        text(320, 225, "WAITING IN TSA", 23, BLUE, "middle", 900),
        text(880, 225, "KILLED BY TERRORISTS", 23, RED, "middle", 900),
        text(320, 360, f"{tsa.lifetime_equivalents:.0f}", 108, WHITE, "middle", 950),
        text(880, 360, f"{baseline.pre_tsa_rate:.2f}", 108, WHITE, "middle", 950),
        text(320, 405, "LIVES BURNED / YEAR", 23, MUTED, "middle", 800),
        text(880, 405, "AVIATION DEATHS / YEAR", 23, MUTED, "middle", 800),
        text(320, 455, "13.0 min TSA-measured wait", 17, MUTED, "middle", 650),
        text(
            880,
            455,
            f"{baseline.pre_tsa_deaths:.0f} deaths · {baseline.pre_tsa_years} pre-TSA GTD years",
            17,
            MUTED,
            "middle",
            650,
        ),
        f'<rect x="365" y="500" width="470" height="82" rx="18" fill="{GOLD}"/>',
        text(600, 552, f"TSA: {tsa.ratio_aviation_pre_tsa:.0f}× MORE", 31, BG, "middle", 950),
        text(600, 620, f"Even averaging in 9/11: TSA = {tsa.ratio_aviation_incl_911:.2f}×", 16, GOLD, "middle", 800),
    ]
    s += footer("Sources: TSA · CDC · BTS · START GTD · U.S. Congress 9/11 victim count")
    return "\n".join(s)


def chart3():
    d = load_inputs()
    rows = scenarios(d)
    baseline = aviation_baselines(d)
    s = svg_open(
        "TSA BURNS MORE LIFE AT EVERY WAIT TIME",
        f"TSA lives burned ÷ pre-TSA aviation-terrorist deaths/year ({baseline.pre_tsa_rate:.2f})",
    )
    left, top, right, bottom = 95, 170, 1140, 535
    max_y = 850
    for tick in [0, 200, 400, 600, 800]:
        y = bottom - tick / max_y * (bottom - top)
        s += [
            f'<line x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}" stroke="{GRID}" stroke-dasharray="5 7"/>',
            text(left - 15, y + 5, f"{tick}×", 13, MUTED, "end"),
        ]
    colors = [BLUE, BLUE, CYAN, GOLD, RED]
    slot = (right - left) / len(rows)
    for i, row in enumerate(rows):
        ratio = row.ratio_aviation_pre_tsa
        cx = left + slot * (i + 0.5)
        h = ratio / max_y * (bottom - top)
        y = bottom - h
        s.append(
            f'<rect x="{cx-62:.1f}" y="{y:.1f}" width="124" height="{h:.1f}" rx="10" fill="{colors[i]}"/>'
        )
        s.append(text(cx, y - 14, f"{ratio:.0f}×", 25, WHITE, "middle", 900))
        s.append(text(cx, bottom + 38, row.year_label, 27, WHITE, "middle", 900))
        s.append(text(cx, bottom + 61, f"{row.wait_minutes:.1f} min · {row.short_label}", 12, MUTED, "middle", 700))
    s += footer(
        f"Terrorist baseline: {baseline.pre_tsa_deaths:.0f} GTD-recorded deaths ÷ {baseline.pre_tsa_years} GTD-covered pre-TSA years"
    )
    return "\n".join(s)


def chart4():
    d = load_inputs()
    one = lifetime_equivalents(
        d["tsa_screenings_2024"], 1.0, d["life_expectancy_us_2024"]
    )[2]
    s = svg_open(
        "ONE EXTRA TSA MINUTE = 21.8 LIVES A YEAR",
        "904 million annual screenings turns every added minute into 21.8 full 79-year lives",
    )
    left, top, right, bottom = 110, 205, 1120, 535
    x_max = 25
    y_max = 550
    for tick in range(0, 551, 100):
        y = bottom - tick / y_max * (bottom - top)
        s += [
            f'<line x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}" stroke="{GRID}" stroke-dasharray="5 7"/>',
            text(left - 16, y + 5, str(tick), 13, MUTED, "end"),
        ]
    points = []
    for minute in range(26):
        equivalent = lifetime_equivalents(
            d["tsa_screenings_2024"], float(minute), d["life_expectancy_us_2024"]
        )[2]
        x = left + minute / x_max * (right - left)
        y = bottom - equivalent / y_max * (bottom - top)
        points.append(f"{x:.1f},{y:.1f}")
    s.append(
        f'<polyline points="{" ".join(points)}" fill="none" stroke="{GOLD}" stroke-width="7" stroke-linecap="round"/>'
    )
    for minute in [5, 10, 15, 20, 25]:
        equivalent = one * minute
        x = left + minute / x_max * (right - left)
        y = bottom - equivalent / y_max * (bottom - top)
        s.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="{RED}" stroke="{WHITE}" stroke-width="2"/>'
        )
        s.append(text(x, y - 18, f"{equivalent:.0f} lives", 16, WHITE, "middle", 850))
        s.append(text(x, bottom + 36, f"{minute} min", 15, MUTED, "middle", 750))
    s += footer("Formula: 904M screenings × wait minutes ÷ minutes/year ÷ 79 years")
    return "\n".join(s)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    charts = {
        "tsa_lives_by_year.svg": chart1(),
        "tsa_vs_terrorists.svg": chart2(),
        "how_many_times_worse.svg": chart3(),
        "one_minute_cost.svg": chart4(),
    }
    for old in OUT.glob("*.svg"):
        if old.name not in charts:
            old.unlink()
    for name, content in charts.items():
        (OUT / name).write_text(content + "\n", encoding="utf-8")
        print(f"Wrote charts/{name}")


if __name__ == "__main__":
    main()
