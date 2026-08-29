"""Shared deterministic model for the TSA body-count study."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INPUTS = ROOT / "data" / "inputs.csv"
AVIATION_DEATHS = ROOT / "data" / "aviation_deaths.csv"
DAYS_PER_YEAR = 365.2425
PRE_911_START_YEAR = 1970
PRE_911_END_YEAR = 2000
INCL_911_END_YEAR = 2001


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
    ratio_aviation_pre_911: float
    ratio_aviation_incl_911: float


def load_inputs() -> dict[str, float]:
    with INPUTS.open(newline="", encoding="utf-8") as handle:
        return {row["key"]: float(row["value"]) for row in csv.DictReader(handle)}


def load_aviation_deaths() -> list[dict[str, str]]:
    with AVIATION_DEATHS.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def lifetime_equivalents(
    screenings: float, wait_minutes: float, life_years: float
) -> tuple[float, float, float]:
    hours = screenings * wait_minutes / 60.0
    person_years = hours / (24.0 * DAYS_PER_YEAR)
    equivalents = person_years / life_years
    return hours, person_years, equivalents


def aviation_baselines(d: dict[str, float] | None = None) -> tuple[float, float, float]:
    d = d or load_inputs()
    pre_911_deaths = sum(int(row["deaths"]) for row in load_aviation_deaths())
    pre_911_years = PRE_911_END_YEAR - PRE_911_START_YEAR + 1
    incl_911_years = INCL_911_END_YEAR - PRE_911_START_YEAR + 1
    pre_911_rate = pre_911_deaths / pre_911_years
    incl_911_rate = (pre_911_deaths + d["sept11_victims_2001"]) / incl_911_years
    return float(pre_911_deaths), pre_911_rate, incl_911_rate


def aviation_attack_count(d: dict[str, float] | None = None) -> int:
    d = d or load_inputs()
    return int(d["aviation_attacks_1970s"] + d["aviation_attacks_1980s"] + d["aviation_attacks_1990s"])


def scenarios(d: dict[str, float] | None = None) -> list[Scenario]:
    d = d or load_inputs()
    screenings = d["tsa_screenings_2024"]
    life_years = d["life_expectancy_us_2024"]
    _, pre_rate, incl_rate = aviation_baselines(d)
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
        rows.append(
            Scenario(
                key=key,
                label=label,
                short_label=short_label,
                year_label=year_label,
                wait_minutes=wait,
                wait_hours=hours,
                person_years=years,
                lifetime_equivalents=equiv,
                ratio_aviation_pre_911=equiv / pre_rate,
                ratio_aviation_incl_911=equiv / incl_rate,
            )
        )
    return rows
