#!/usr/bin/env python3
"""Regenerate normalized annual results from checked-in source inputs."""

from __future__ import annotations

import csv
from pathlib import Path

from model import ROOT, aviation_baselines, load_inputs, scenarios

OUTPUT = ROOT / "results" / "annualized_2024.csv"


def write_results() -> None:
    d = load_inputs()
    rows = scenarios(d)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(
            [
                "scenario",
                "wait_min",
                "wait_hours",
                "person_years",
                "lifetime_equivalents_79y",
                "ratio_vs_pre_tsa_aviation",
                "ratio_vs_aviation_incl_911",
            ]
        )
        for row in rows:
            writer.writerow(
                [
                    row.label,
                    f"{row.wait_minutes:.1f}",
                    f"{row.wait_hours:.1f}",
                    f"{row.person_years:.2f}",
                    f"{row.lifetime_equivalents:.2f}",
                    f"{row.ratio_aviation_pre_tsa:.3f}",
                    f"{row.ratio_aviation_incl_911:.3f}",
                ]
            )


def main() -> None:
    d = load_inputs()
    baseline = aviation_baselines(d)
    write_results()
    print(f"2024 TSA screenings: {d['tsa_screenings_2024']:,.0f}")
    print(f"U.S. life expectancy: {d['life_expectancy_us_2024']:.1f} years")
    print(
        f"Pre-TSA aviation GTD events: {baseline.pre_tsa_event_count} events; "
        f"{baseline.pre_tsa_deaths:.0f} deaths"
    )
    print(
        f"Pre-TSA aviation rate: {baseline.pre_tsa_rate:.4f} deaths/year "
        f"across {baseline.pre_tsa_years} GTD-covered years"
    )
    print(
        f"Aviation rate including 9/11: {baseline.incl_911_rate:.4f} deaths/year "
        f"across {baseline.incl_911_years} GTD-covered years"
    )
    try:
        shown = OUTPUT.relative_to(Path.cwd())
    except ValueError:
        shown = OUTPUT
    print(f"Wrote {shown}")


if __name__ == "__main__":
    main()
