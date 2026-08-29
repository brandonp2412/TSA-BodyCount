#!/usr/bin/env python3
"""Reproduce the normalized annual results from checked-in source inputs."""

from __future__ import annotations

import csv
from pathlib import Path

from model import ROOT, baselines, load_inputs, scenarios

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
                "ratio_vs_1980_1999_deaths_per_year",
                "ratio_vs_1980_2001_deaths_per_year",
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
                    f"{row.ratio_pre_9_11:.3f}",
                    f"{row.ratio_incl_9_11:.3f}",
                ]
            )


def main() -> None:
    d = load_inputs()
    pre_deaths, incl_deaths, pre_incidents, incl_incidents = baselines(d)
    write_results()
    print(f"2024 TSA screenings: {d['tsa_screenings_2024']:,.0f}")
    print(f"U.S. life expectancy: {d['life_expectancy_us_2024']:.1f} years")
    print(
        f"1980–1999 baseline: {pre_incidents:.2f} incidents/year; "
        f"{pre_deaths:.2f} deaths/year"
    )
    print(
        f"1980–2001 baseline: {incl_incidents:.2f} incidents/year; "
        f"{incl_deaths:.2f} deaths/year"
    )
    try:
        shown = OUTPUT.relative_to(Path.cwd())
    except ValueError:
        shown = OUTPUT
    print(f"Wrote {shown}")


if __name__ == "__main__":
    main()
