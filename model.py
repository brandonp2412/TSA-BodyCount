"""Shared deterministic model for the TSA body-count study."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INPUTS = ROOT / "data" / "inputs.csv"
AVIATION_EVENTS = ROOT / "data" / "aviation_events.csv"
DAYS_PER_YEAR = 365.2425
PRE_TSA_START_YEAR = 1970
PRE_TSA_END_YEAR = 2000
INCL_911_END_YEAR = 2001


@dataclass(frozen=True)
class AviationBaseline:
    pre_tsa_deaths: float
    pre_tsa_years: int
    pre_tsa_rate: float
    incl_911_deaths: float
    incl_911_years: int
    incl_911_rate: float
    pre_tsa_event_count: int


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
    ratio_aviation_pre_tsa: float
    ratio_aviation_incl_911: float


def load_inputs() -> dict[str, float]:
    with INPUTS.open(newline="", encoding="utf-8") as handle:
        return {row["key"]: float(row["value"]) for row in csv.DictReader(handle)}


def load_aviation_events() -> list[dict[str, str]]:
    with AVIATION_EVENTS.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def lifetime_equivalents(
    screenings: float, wait_minutes: float, life_years: float
) -> tuple[float, float, float]:
    hours = screenings * wait_minutes / 60.0
    person_years = hours / (24.0 * DAYS_PER_YEAR)
    equivalents = person_years / life_years
    return hours, person_years, equivalents


def covered_gtd_years(end_year: int, d: dict[str, float] | None = None) -> list[int]:
    d = d or load_inputs()
    missing_year = int(d["gtd_missing_event_year"])
    return [
        year
        for year in range(PRE_TSA_START_YEAR, end_year + 1)
        if year != missing_year
    ]


def aviation_baselines(d: dict[str, float] | None = None) -> AviationBaseline:
    d = d or load_inputs()
    events = load_aviation_events()
    pre_tsa_events = [
        row
        for row in events
        if PRE_TSA_START_YEAR <= int(row["year"]) <= PRE_TSA_END_YEAR
    ]
    pre_tsa_deaths = sum(
        float(row["gtd_nkill"])
        for row in pre_tsa_events
        if row["gtd_nkill"].strip()
    )
    pre_tsa_years = len(covered_gtd_years(PRE_TSA_END_YEAR, d))
    incl_911_years = len(covered_gtd_years(INCL_911_END_YEAR, d))
    pre_tsa_rate = pre_tsa_deaths / pre_tsa_years
    incl_911_deaths = pre_tsa_deaths + d["sept11_victims_2001"]
    incl_911_rate = incl_911_deaths / incl_911_years
    return AviationBaseline(
        pre_tsa_deaths=pre_tsa_deaths,
        pre_tsa_years=pre_tsa_years,
        pre_tsa_rate=pre_tsa_rate,
        incl_911_deaths=incl_911_deaths,
        incl_911_years=incl_911_years,
        incl_911_rate=incl_911_rate,
        pre_tsa_event_count=len(pre_tsa_events),
    )


def scenarios(d: dict[str, float] | None = None) -> list[Scenario]:
    d = d or load_inputs()
    screenings = d["tsa_screenings_2024"]
    life_years = d["life_expectancy_us_2024"]
    baseline = aviation_baselines(d)
    definitions = [
        ("wait_gao_fy2006", "GAO FY2006 average peak", "GAO", "2006"),
        ("wait_gao_fy2005", "GAO FY2005 average peak", "GAO", "2005"),
        ("wait_gao_fy2004", "GAO FY2004 average peak", "GAO", "2004"),
        ("wait_tsa_2003_2004", "TSA Dec 2003–Nov 2004 average peak", "TSA", "2003–04"),
        ("wait_bts_perceived_2003_2004", "BTS traveler-reported Dec 2003–Nov 2004", "PASSENGERS", "2003–04"),
    ]
    rows: list[Scenario] = []
    for key, label, short_label, year_label in definitions:
        wait = d[key]
        hours, years, equivalents = lifetime_equivalents(screenings, wait, life_years)
        rows.append(
            Scenario(
                key=key,
                label=label,
                short_label=short_label,
                year_label=year_label,
                wait_minutes=wait,
                wait_hours=hours,
                person_years=years,
                lifetime_equivalents=equivalents,
                ratio_aviation_pre_tsa=equivalents / baseline.pre_tsa_rate,
                ratio_aviation_incl_911=equivalents / baseline.incl_911_rate,
            )
        )
    return rows
