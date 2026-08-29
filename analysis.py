#!/usr/bin/env python3
"""Regenerate normalized annual results from checked-in source inputs."""

from __future__ import annotations

import csv
from pathlib import Path

from model import ROOT, aviation_attack_count, aviation_baselines, load_inputs, scenarios

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
                "ratio_vs_aviation_1970_2000",
                "ratio_vs_aviation_1970_2001_incl_911",
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
                    f"{row.ratio_aviation_pre_911:.3f}",
                    f"{row.ratio_aviation_incl_911:.3f}",
                ]
            )


def main() -> None:
    d = load_inputs()
    deaths, pre_rate, incl_rate = aviation_baselines(d)
    write_results()
    print(f"2024 TSA screenings: {d['tsa_screenings_2024']:,.0f}")
    print(f"U.S. life expectancy: {d['life_expectancy_us_2024']:.1f} years")
    print(f"U.S. airport/aircraft attacks in 1970–1999: {aviation_attack_count(d)}")
    print(f"Aviation terrorism, 1970–2000: {deaths:.0f} deaths; {pre_rate:.4f} deaths/year")
    print(f"Aviation terrorism, 1970–2001 incl. 9/11: {incl_rate:.4f} deaths/year")
    try:
        shown = OUTPUT.relative_to(Path.cwd())
    except ValueError:
        shown = OUTPUT
    print(f"Wrote {shown}")


if __name__ == "__main__":
    main()
