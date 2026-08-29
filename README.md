# TSA Body Count

Who burns more human life: the TSA or aviation terrorists?

Take the time Americans spend standing in TSA lines, divide it by a **79-year human life**, and compare it with people killed in **U.S. terrorism involving airports, aircraft, or aviation hijackings**.

Using TSA's own **13-minute measured wait**, 2024 passenger volume burns **283 lives per year** in line.

START's Global Terrorism Database aviation subset records **17 deaths across 30 covered pre-TSA years**. That is **0.57 aviation-terrorist deaths per year**.

**TSA burns 499× more human life.**

Throw 9/11 into the terrorist average too: **2,994 deaths across 31 covered years = 96.58 deaths/year**. TSA still burns **2.93× more human life**.

Using the **20.4-minute passenger-reported wait**, TSA burns **444 lives per year — 783× the pre-TSA aviation-terrorist rate and 4.60× the rate with 9/11 included.**

## TSA lives burned each year

The year under each bar is the year of the federal wait-time measurement. Every bar applies that wait to TSA's 2024 screening volume.

![TSA lives burned each year](charts/tsa_lives_by_year.svg)

## TSA vs. aviation terrorists

**WAITING IN TSA** vs. **KILLED BY TERRORISTS**. Airports, aircraft, and aviation hijackings only.

![TSA versus aviation terrorists](charts/tsa_vs_terrorists.svg)

## TSA wins at every wait-time measurement

Every bar uses the pre-TSA aviation-terrorist rate: **17 deaths / 30 GTD-covered years = 0.57 deaths/year**.

![TSA wins at every wait time](charts/how_many_times_worse.svg)

## What one extra minute costs

At 904 million screenings per year, every extra minute in line burns **21.8 full human lives per year**.

![One extra TSA minute](charts/one_minute_cost.svg)

## The numbers

| Wait measurement | Wait | TSA lives / year | vs. pre-TSA aviation terrorists | vs. aviation terrorists incl. 9/11 |
|---|---:|---:|---:|---:|
| GAO 2006 | 8.2 min | 178 | 315× | 1.85× |
| GAO 2005 | 8.9 min | 194 | 342× | 2.00× |
| GAO 2004 | 9.4 min | 205 | 361× | 2.12× |
| TSA 2003–04 | 13.0 min | 283 | **499×** | **2.93×** |
| Passengers 2003–04 | 20.4 min | 444 | **783×** | **4.60×** |

## Aviation terrorist body count

The checked-in GTD-derived subset is [`data/aviation_events.csv`](data/aviation_events.csv). The filter keeps U.S. incidents from 1970–2001 when any GTD target is **Airports & Aircraft** / **Airports & Airlines**, plus aviation-specific hijackings so aircraft hijackings cannot disappear behind another primary target category.

The five lethal pre-TSA aviation events are:

| Year | GTD event | Deaths |
|---|---|---:|
| 1974 | Los Angeles International Airport bombing | 3 |
| 1975 | LaGuardia Airport bombing | 11 |
| 1976 | TWA Flight 355 hijacking / Grand Central bomb | 1 |
| 1981 | Pan Am terminal bombing at JFK | 1 |
| 1982 | Pan Am Flight 830 bombing | 1 |
| | **Total** | **17** |

GTD has no event-level records for 1993, so the pre-TSA rate uses the **30 GTD-covered years from 1970–2000**:

```text
17 / 30 = 0.5667 deaths per year
```

Add the **2,977 people killed on 9/11** and extend through 2001:

```text
(17 + 2,977) / 31 = 96.5806 deaths per year
```

The 13-minute TSA line then lands at:

```text
282.84 / 0.5667 = 499.13×
282.84 / 96.5806 = 2.93×   # even with 9/11
```

## Reproduce everything

Python 3.10+. No third-party packages.

```bash
make all
make check
```

`make all` regenerates the results CSV and every chart from [`data/inputs.csv`](data/inputs.csv) and [`data/aviation_events.csv`](data/aviation_events.csv). `make check` fails if committed results or charts differ. GitHub Actions runs the same reproducibility check on every push and pull request.

The GTD-derived event file can be rebuilt from the pinned 2018 START/Kaggle snapshot:

```bash
python3 scripts/extract_aviation_events.py globalterrorismdb_0718dist.csv > data/aviation_events.csv
```

The extractor pins the source file SHA-256 and contains the exact aviation filter.

## Primary sources

- [START — Global Terrorism Database](https://www.start.umd.edu/data-tools/GTD)
- [START — GTD codebook](https://www.start.umd.edu/sites/default/files/2024-10/Codebook.pdf)
- [START — GTD FAQ, including the missing 1993 event-level data](https://www.start.umd.edu/gtd-faqs)
- [START — Patterns of Terrorism in the United States, 1970–2013](https://www.start.umd.edu/pubs/START_TEVUS_GTDPatternsofTerrorisminUS1970-2013_Oct2014.pdf)
- [START/DHS — Terrorist Attacks Targeting Critical Infrastructure in the United States, 1970–2015](https://www.start.umd.edu/pubs/START_DHS_GTD_Targeting%20Critical%20Infrastructure%20in%20the%20US_June2016.pdf)
- [Kaggle — START GTD 2018 snapshot metadata](https://www.kaggle.com/START-UMD/gtd/metadata)
- [Archive.org — pinned `globalterrorismdb_0718dist.csv` copy used by the extractor](https://archive.org/download/globalterrorismdb_0718dist/globalterrorismdb_0718dist.csv)
- [U.S. Court of Appeals — TWA Flight 355 hijacking facts](https://law.justia.com/cases/federal/appellate-courts/F2/549/252/342112/)
- [TSA — 2024 screening volume](https://www.tsa.gov/sites/default/files/tsa_2024_yir_by_the_numbers.pdf)
- [CDC/NCHS — Mortality in the United States, 2024](https://www.cdc.gov/nchs/products/databriefs/db548.htm)
- [BTS — Air Passenger Opinions on Security Screening Procedures](https://www.bts.gov/archive/publications/airline_passenger_opinions_on_security_screening_procedures/entire)
- [GAO-07-299 — TSA average peak wait times](https://www.gao.gov/products/gao-07-299)
- [U.S. Congress — 2,977 victims killed on September 11, 2001](https://www.govinfo.gov/content/pkg/CHRG-116hhrg39837/pdf/CHRG-116hhrg39837.pdf)

## Repository layout

- `data/inputs.csv` — TSA, life-expectancy, GTD-coverage, and 9/11 source values
- `data/aviation_events.csv` — checked-in GTD-derived aviation incident subset
- `scripts/extract_aviation_events.py` — deterministic GTD aviation filter pinned to the source snapshot
- `model.py` — shared calculations
- `analysis.py` — generates `results/annualized_2024.csv`
- `generate_charts.py` — generates every SVG using only Python's standard library
- `charts/` — generated graphs embedded above
- `docs/methodology.md` — formulas and source definitions
