# TSA Body Count

Who wastes more human life: the TSA or aviation terrorists?

Take the time Americans spend standing in TSA lines, divide it by a **79-year human life**, and compare it with people killed in **U.S. attacks against airports and aircraft**.

Using TSA's own **13-minute measured wait**, 2024 passenger volume burns **283 lives per year** in line.

Aviation terrorists killed **16 people from 1970–2000**. Then 9/11 killed **2,977**. Average all of that across 1970–2001 and aviation terrorists killed **93.53 people per year**.

**TSA: 3.02× more human life lost — even with 9/11 included.**

Before 9/11, the aviation-terrorist rate was only **0.52 deaths per year**. Against that rate, TSA's 13-minute line burns **548× more human life**.

Using the **20.4-minute passenger-reported wait**, TSA burns **444 lives per year — 4.75× the aviation-terrorist rate even with 9/11 included.**

## TSA lives burned each year

The year under each bar is the year of the federal wait-time measurement. Every bar applies that wait to TSA's 2024 screening volume.

![TSA lives burned each year](charts/tsa_lives_by_year.svg)

## TSA vs. aviation terrorists

Blue is human life burned waiting in TSA lines. Red is people killed by aviation terrorists, with 9/11 included.

![TSA versus aviation terrorists](charts/tsa_vs_terrorists.svg)

## TSA wins at every wait-time measurement

Every bar uses the aviation-only terrorist rate with 9/11 included.

![TSA wins at every wait time](charts/how_many_times_worse.svg)

## What one extra minute costs

At 904 million screenings per year, every extra minute in line burns **21.8 full human lives per year**.

![One extra TSA minute](charts/one_minute_cost.svg)

## The numbers

| Wait measurement | Wait | TSA lives / year | vs. aviation terrorists incl. 9/11 | vs. aviation terrorists before 9/11 |
|---|---:|---:|---:|---:|
| GAO 2006 | 8.2 min | 178 | 1.91× | 346× |
| GAO 2005 | 8.9 min | 194 | 2.07× | 375× |
| GAO 2004 | 9.4 min | 205 | 2.19× | 396× |
| TSA 2003–04 | 13.0 min | 283 | **3.02×** | **548×** |
| Passengers 2003–04 | 20.4 min | 444 | **4.75×** | **860×** |

## Aviation terrorist body count

START's Global Terrorism Database counts **68 U.S. attacks against airports and aircraft from 1970–1999**:

- 1970s: **43 attacks**
- 1980s: **23 attacks**
- 1990s: **2 attacks**

The attacks that killed people before 9/11 were:

| Year | Attack | Deaths |
|---|---|---:|
| 1974 | Los Angeles International Airport bombing | 3 |
| 1975 | LaGuardia Airport bombing | 11 |
| 1981 | Pan Am terminal bombing at JFK | 1 |
| 1982 | Pan Am Flight 830 bombing | 1 |
| | **Total, 1970–2000** | **16** |

So the pre-9/11 aviation-terrorist rate is:

```text
16 / 31 years = 0.516 deaths per year
```

Give terrorists the full 9/11 body count as well:

```text
(16 + 2,977) / 32 years = 93.531 deaths per year
```

That **93.53 deaths/year** number is the terrorist side of the main comparison.

## Formula

```text
annual_wait_hours = annual_screenings × wait_minutes / 60
annual_wait_years = annual_wait_hours / (24 × 365.2425)
tsa_lives_burned = annual_wait_years / 79
aviation_terrorist_rate = (16 + 2,977) / 32
ratio_vs_terrorists = tsa_lives_burned / aviation_terrorist_rate
```

## Reproduce everything

Python 3.10+. No third-party packages.

```bash
make all
```

This regenerates the results CSV and every chart from [`data/inputs.csv`](data/inputs.csv) and [`data/aviation_deaths.csv`](data/aviation_deaths.csv).

```bash
make check
```

`make check` regenerates everything and fails if the committed results or charts differ. GitHub Actions runs the same check on every push and pull request.

## Primary sources

- [TSA — 2024 screening volume](https://www.tsa.gov/news/press/releases/2025/01/15/tsa-intercepts-6678-firearms-airport-security-checkpoints-2024)
- [CDC/NCHS — Mortality in the United States, 2024](https://www.cdc.gov/nchs/products/databriefs/db548.htm)
- [BTS — Air Passenger Opinions on Security Screening Procedures](https://www.bts.gov/archive/publications/airline_passenger_opinions_on_security_screening_procedures/entire)
- [GAO-07-299 — TSA average peak wait times](https://www.gao.gov/products/gao-07-299)
- [START — Patterns of Terrorism in the United States, 1970–2013](https://www.start.umd.edu/pubs/START_TEVUS_GTDPatternsofTerrorisminUS1970-2013_Oct2014.pdf)
- [START/DHS — Targeting Critical Infrastructure in the United States](https://www.start.umd.edu/pubs/START_DHS_GTD_Targeting%20Critical%20Infrastructure%20in%20the%20US_June2016.pdf)
- [U.S. Congress — 2,977 victims killed on September 11, 2001](https://www.govinfo.gov/content/pkg/CHRG-116hhrg39837/pdf/CHRG-116hhrg39837.pdf)

## Repository layout

- `data/inputs.csv` — source values and links
- `data/aviation_deaths.csv` — every lethal pre-9/11 U.S. airport/aircraft attack used in the denominator
- `model.py` — shared calculations
- `analysis.py` — generates `results/annualized_2024.csv`
- `generate_charts.py` — generates every SVG using only Python's standard library
- `charts/` — generated graphs embedded above
- `docs/methodology.md` — formulas and source definitions
