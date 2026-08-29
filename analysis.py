#!/usr/bin/env python3
"""Reproduce TSA queue-time lifetime-equivalent comparisons.

The output is a numerical comparison of elapsed human time with historical
terrorism fatalities. It is not a causal estimate of deaths caused or prevented.
"""

from __future__ import annotations

import csv
from pathlib import Path

INPUTS = Path(__file__).parent / "data" / "inputs.csv"
DAYS_PER_YEAR = 365.2425


def load_inputs() -> dict[str, float]:
    with INPUTS.open(newline="", encoding="utf-8") as handle:
        return {row["key"]: float(row["value"]) for row in csv.DictReader(handle)}


def lifetime_equivalents(screenings: float, wait_minutes: float, life_years: float) -> tuple[float, float, float]:
    hours = screenings * wait_minutes / 60.0
    person_years = hours / (24.0 * DAYS_PER_YEAR)
    equivalents = person_years / life_years
    return hours, person_years, equivalents


def main() -> None:
    d = load_inputs()

    screenings = d["tsa_screenings_2024"]
    life_years = d["life_expectancy_us_2024"]

    pre_9_11_deaths_per_year = d["fbi_deaths_1980_1999"] / 20.0
    incl_9_11_deaths_per_year = (
        d["fbi_deaths_1980_1999"] + d["fbi_deaths_2000"] + d["fbi_deaths_2001"]
    ) / 22.0

    pre_9_11_incidents_per_year = d["fbi_incidents_1980_1999"] / 20.0
    incl_9_11_incidents_per_year = (
        d["fbi_incidents_1980_1999"] + d["fbi_incidents_2000"] + d["fbi_incidents_2001"]
    ) / 22.0

    scenarios = [
        ("GAO FY2006 average peak", d["wait_gao_fy2006"]),
        ("GAO FY2005 average peak", d["wait_gao_fy2005"]),
        ("GAO FY2004 average peak", d["wait_gao_fy2004"]),
        ("TSA Dec 2003-Nov 2004 average peak", d["wait_tsa_2003_2004"]),
        ("BTS traveler-reported Dec 2003-Nov 2004", d["wait_bts_perceived_2003_2004"]),
    ]

    print(f"2024 TSA screenings: {screenings:,.0f}")
    print(f"U.S. life expectancy: {life_years:.1f} years")
    print()
    print("Historical-continuation baselines:")
    print(f"  1980-1999: {pre_9_11_incidents_per_year:.2f} incidents/suspected incidents/year; "
          f"{pre_9_11_deaths_per_year:.2f} deaths/year")
    print(f"  1980-2001: {incl_9_11_incidents_per_year:.2f} incidents/year; "
          f"{incl_9_11_deaths_per_year:.2f} deaths/year")
    print()

    header = (
        "scenario",
        "wait_min",
        "wait_hours",
        "person_years",
        "79y_lifetime_equiv",
        "ratio_vs_1980_1999_deaths",
        "ratio_vs_1980_2001_deaths",
    )
    print(",".join(header))

    for label, wait_minutes in scenarios:
        hours, years, equivalents = lifetime_equivalents(screenings, wait_minutes, life_years)
        print(
            f'"{label}",{wait_minutes:.1f},{hours:.1f},{years:.2f},{equivalents:.2f},'
            f"{equivalents / pre_9_11_deaths_per_year:.3f},"
            f"{equivalents / incl_9_11_deaths_per_year:.3f}"
        )


if __name__ == "__main__":
    main()
