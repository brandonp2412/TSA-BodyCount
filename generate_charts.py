#!/usr/bin/env python3
"""Generate deterministic, dependency-free SVG charts from data/inputs.csv."""

from __future__ import annotations

from html import escape

from model import ROOT, baselines, lifetime_equivalents, load_inputs, scenarios

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
FONT = "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"


def svg_open(title: str, subtitle: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(title)}</title>',
        f'<desc id="desc">{escape(subtitle)}</desc>',
        f'<rect width="{W}" height="{H}" rx="24" fill="{BG}"/>',
        '<defs><linearGradient id="panel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#102236"/><stop offset="1" stop-color="#091522"/></linearGradient></defs>',
        f'<text x="60" y="68" fill="{TEXT}" font-family="{FONT}" font-size="38" font-weight="800">{escape(title)}</text>',
        f'<text x="60" y="102" fill="{MUTED}" font-family="{FONT}" font-size="18">{escape(subtitle)}</text>',
        f'<line x1="60" y1="126" x2="1140" y2="126" stroke="{GRID}"/>',
    ]


def text(x: float, y: float, value: str, size: int = 16, color: str = TEXT, anchor: str = "start", weight: int = 500) -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" fill="{color}" text-anchor="{anchor}" font-family="{FONT}" font-size="{size}" font-weight="{weight}">{escape(value)}</text>'


def footer(lines: list[str]) -> list[str]:
    y = 674
    out = [f'<line x1="60" y1="640" x2="1140" y2="640" stroke="{GRID}"/>']
    for line in lines[:2]:
        out.append(text(60, y, line, 14, MUTED))
        y += 22
    out.append("</svg>")
    return out


def queue_cost_chart() -> str:
    d = load_inputs()
    rows = scenarios(d)
    s = svg_open(
        "Annual TSA Queue Cost",
        f"2024 volume: {d['tsa_screenings_2024']/1e6:.0f}M screenings · life expectancy: {d['life_expectancy_us_2024']:.1f} years",
    )
    left, top, right, bottom = 100, 165, 1140, 535
    max_y = 500
    for tick in range(0, 501, 100):
        y = bottom - (tick / max_y) * (bottom - top)
        s += [f'<line x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}" stroke="{GRID}" stroke-dasharray="5 7"/>', text(left - 18, y + 6, str(tick), 14, MUTED, "end")]
    s.append(text(28, 355, "79-year lifetime-equivalents / year", 15, MUTED))
    colors = [BLUE, "#4899e8", CYAN, GOLD, RED]
    plot_w = right - left
    slot = plot_w / len(rows)
    bar_w = 118
    for i, (row, color) in enumerate(zip(rows, colors)):
        cx = left + slot * (i + 0.5)
        h = (row.lifetime_equivalents / max_y) * (bottom - top)
        x, y = cx - bar_w / 2, bottom - h
        s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w}" height="{h:.1f}" rx="9" fill="{color}" opacity="0.92"/>')
        s.append(text(cx, y - 14, f"{row.lifetime_equivalents:.1f}", 22, TEXT, "middle", 800))
        s.append(text(cx, bottom + 32, f"{row.wait_minutes:.1f} min", 17, TEXT, "middle", 750))
        s.append(text(cx, bottom + 55, row.short_label, 13, MUTED, "middle"))
    s += [
        f'<rect x="760" y="148" width="380" height="58" rx="12" fill="{PANEL}" stroke="{GRID}"/>',
        text(780, 173, "Gross elapsed queue time, not lives literally lost", 14, GOLD, "start", 700),
        text(780, 194, "Sensitivity scenarios using historical federal wait data", 13, MUTED),
    ]
    s += footer(["Formula: screenings × wait minutes ÷ minutes/year ÷ 79.0", "Sources: TSA, CDC/NCHS, BTS, GAO · generated from data/inputs.csv"])
    return "\n".join(s)


def baseline_chart() -> str:
    d = load_inputs()
    pre, incl, _, _ = baselines(d)
    s = svg_open("Counterfactual Terrorism Baselines", "Naive annualized U.S. terrorism deaths if historical averages simply continued")
    left, top, right, bottom = 150, 165, 1080, 525
    max_y = 150
    for tick in range(0, 151, 25):
        y = bottom - (tick / max_y) * (bottom - top)
        s += [f'<line x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}" stroke="{GRID}" stroke-dasharray="5 7"/>', text(left - 18, y + 6, str(tick), 14, MUTED, "end")]
    vals = [("1980–1999", "205 deaths / 20 years", pre, BLUE), ("1980–2001 incl. 9/11", "2,993 deaths / 22 years", incl, RED)]
    xs = [390, 820]
    for (label, note, value, color), cx in zip(vals, xs):
        h = (value / max_y) * (bottom - top)
        y = bottom - h
        s.append(f'<rect x="{cx-95}" y="{y:.1f}" width="190" height="{h:.1f}" rx="12" fill="{color}" opacity="0.92"/>')
        s.append(text(cx, y - 18, f"{value:.2f}", 28, TEXT, "middle", 800))
        s.append(text(cx, bottom + 36, label, 17, TEXT, "middle", 750))
        s.append(text(cx, bottom + 60, note, 14, MUTED, "middle"))
    s += [
        f'<rect x="150" y="590" width="930" height="42" rx="10" fill="{PANEL}" stroke="{GOLD}"/>',
        text(175, 617, "9/11 dominates the inclusive average: START reports 85% of U.S. terrorism deaths (1970–2013) occurred that day.", 15, GOLD, "start", 650),
    ]
    s += footer(["Historical continuation benchmark only — not an estimate of TSA-prevented deaths", "Sources: FBI Terrorism in the United States; START Global Terrorism Database analysis"])
    return "\n".join(s)


def ratio_heatmap() -> str:
    d = load_inputs()
    rows = scenarios(d)
    pre, incl, _, _ = baselines(d)
    s = svg_open("Queue Cost vs. Counterfactual Deaths", "Lifetime-equivalents consumed in line per projected terrorism death")
    x0, y0 = 80, 165
    label_w, col_w, row_h = 390, 310, 76
    headers = [
        (x0 + label_w, "vs. 1980–1999", f"{pre:.2f} deaths/year", CYAN),
        (x0 + label_w + col_w, "vs. 1980–2001 incl. 9/11", f"{incl:.2f} deaths/year", GOLD),
    ]
    s.append(f'<rect x="{x0}" y="{y0}" width="{label_w + 2*col_w}" height="{row_h*6}" rx="16" fill="url(#panel)" stroke="{GRID}"/>')
    s.append(text(x0 + 24, y0 + 34, "Wait-time scenario", 16, MUTED, "start", 700))
    for x, h1, h2, color in headers:
        s.append(text(x + col_w/2, y0 + 30, h1, 15, color, "middle", 750))
        s.append(text(x + col_w/2, y0 + 53, h2, 13, MUTED, "middle"))
    for i, row in enumerate(rows):
        y = y0 + row_h * (i + 1)
        if i:
            s.append(f'<line x1="{x0}" y1="{y}" x2="{x0+label_w+2*col_w}" y2="{y}" stroke="{GRID}"/>')
        s.append(text(x0 + 24, y + 31, f"{row.wait_minutes:.1f} min · {row.short_label}", 16, TEXT, "start", 650))
        for j, (value, color) in enumerate([(row.ratio_pre_9_11, CYAN), (row.ratio_incl_9_11, GOLD)]):
            x = x0 + label_w + j * col_w
            opacity = min(0.78, 0.18 + value / (45 if j == 0 else 3.5) * 0.55)
            s.append(f'<rect x="{x+1}" y="{y+1}" width="{col_w-2}" height="{row_h-2}" fill="{color}" opacity="{opacity:.3f}"/>')
            s.append(text(x + col_w/2, y + 45, f"{value:.2f}×", 26, TEXT, "middle", 850))
    s += footer(["Each cell = queue-time lifetime-equivalents ÷ historical deaths/year", "Illustrative numerical comparison · generated from the same checked-in source inputs"])
    return "\n".join(s)


def sensitivity_chart() -> str:
    d = load_inputs()
    rows = scenarios(d)
    screenings = d["tsa_screenings_2024"]
    life = d["life_expectancy_us_2024"]
    s = svg_open("Sensitivity: Every Extra Minute Scales Linearly", "2024 screening volume held fixed at 904 million")
    left, top, right, bottom = 100, 165, 1125, 535
    x_max, y_max = 25.0, 550.0
    for tick in range(0, 551, 100):
        y = bottom - (tick / y_max) * (bottom - top)
        s += [f'<line x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}" stroke="{GRID}" stroke-dasharray="5 7"/>', text(left - 18, y + 6, str(tick), 14, MUTED, "end")]
    for tick in range(0, 26, 5):
        x = left + (tick / x_max) * (right - left)
        s.append(text(x, bottom + 32, str(tick), 14, MUTED, "middle"))
    points = []
    for minute in range(0, 26):
        equiv = lifetime_equivalents(screenings, float(minute), life)[2]
        x = left + minute / x_max * (right - left)
        y = bottom - equiv / y_max * (bottom - top)
        points.append(f"{x:.1f},{y:.1f}")
    s.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="{BLUE}" stroke-width="5" stroke-linecap="round"/>')
    for i, row in enumerate(rows):
        x = left + row.wait_minutes / x_max * (right - left)
        y = bottom - row.lifetime_equivalents / y_max * (bottom - top)
        color = [BLUE, "#4899e8", CYAN, GOLD, RED][i]
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="{color}" stroke="{TEXT}" stroke-width="2"/>')
        dy = -16 if i % 2 == 0 else 27
        s.append(text(x, y + dy, f"{row.wait_minutes:.1f}m → {row.lifetime_equivalents:.0f}", 13, TEXT, "middle", 700))
    s += [text((left+right)/2, bottom + 62, "Average checkpoint wait (minutes)", 15, MUTED, "middle"), text(25, 360, "79-year lifetime-equivalents/year", 14, MUTED)]
    s += footer(["This chart is arithmetic sensitivity, not a causal claim about TSA", "Inputs: 904M annual screenings; 79.0-year U.S. life expectancy"])
    return "\n".join(s)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    charts = {
        "queue_lifetime_equivalents.svg": queue_cost_chart(),
        "counterfactual_baselines.svg": baseline_chart(),
        "ratio_heatmap.svg": ratio_heatmap(),
        "wait_time_sensitivity.svg": sensitivity_chart(),
    }
    for name, content in charts.items():
        path = OUT / name
        path.write_text(content + "\n", encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
