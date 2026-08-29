"""Shared deterministic model for the TSA body-count study."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INPUTS = ROOT / "data" / "inputs.csv"
DAYS_PER_YEAR = 365.2425


@dataclass(frozen=True)
class Scenario:
    key: str
    label: str
    short_label: str
    year_label: str
    wait_minutes: float
    wait_hours: float
    person_years: float
    lifetime_equivalents: float
    ratio_pre_9_11: float
    ratio_incl_9_11: float


def load_inputs() -> dict[str, float]:
    with INPUTS.open(newline="", encoding="utf-8") as handle:
        return {row["key"]: float(row["value"]) for row in csv.DictReader(handle)}


def lifetime_equivalents(screenings: float, wait_minutes: float, life_years: float) -> tuple[float, float, float]:
    hours = screenings * wait_minutes / 60.0
    person_years = hours / (24.0 * DAYS_PER_YEAR)
    equivalents = person_years / life_years
    return hours, person_years, equivalents


def baselines(d: dict[str, float]) -> tuple[float, float, float, float]:
    pre_deaths = d["fbi_deaths_1980_1999"] / 20.0
    incl_deaths = (d["fbi_deaths_1980_1999"] + d["fbi_deaths_2000"] + d["fbi_deaths_2001"]) / 22.0
    pre_incidents = d["fbi_incidents_1980_1999"] / 20.0
    incl_incidents = (d["fbi_incidents_1980_1999"] + d["fbi_incidents_2000"] + d["fbi_incidents_2001"]) / 22.0
    return pre_deaths, incl_deaths, pre_incidents, incl_incidents


def scenarios(d: dict[str, float] | None = None) -> list[Scenario]:
    d = d or load_inputs()
    screenings = d["tsa_screenings_2024"]
    life_years = d["life_expectancy_us_2024"]
    pre_deaths, incl_deaths, _, _ = baselines(d)
    defs = [
        ("wait_gao_fy2006", "GAO FY2006 average peak", "GAO", "2006"),
        ("wait_gao_fy2005", "GAO FY2005 average peak", "GAO", "2005"),
        ("wait_gao_fy2004", "GAO FY2004 average peak", "GAO", "2004"),
        ("wait_tsa_2003_2004", "TSA Dec 2003–Nov 2004 average peak", "TSA", "2003–04"),
        ("wait_bts_perceived_2003_2004", "BTS traveler-reported Dec 2003–Nov 2004", "PASSENGERS", "2003–04"),
    ]
    rows: list[Scenario] = []
    for key, label, short_label, year_label in defs:
        wait = d[key]
        hours, years, equiv = lifetime_equivalents(screenings, wait, life_years)
        rows.append(Scenario(
            key=key,
            label=label,
            short_label=short_label,
            year_label=year_label,
            wait_minutes=wait,
            wait_hours=hours,
            person_years=years,
            lifetime_equivalents=equiv,
            ratio_pre_9_11=equiv / pre_deaths,
            ratio_incl_9_11=equiv / incl_deaths,
        ))
    return rows
