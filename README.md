# TSA Body Count

A reproducible counterfactual study of the aggregate human time consumed by U.S. airport security queues versus historical U.S. terrorism fatalities.

The deliberately provocative unit is a **lifetime-equivalent of elapsed time**: total passenger-hours spent waiting at TSA checkpoints divided by current U.S. life expectancy. It is **not** a claim that waiting in line literally kills that many people.

## Headline annualized result

Using TSA's **904 million travelers screened in 2024** and CDC's **79.0-year U.S. life expectancy**, the available federal national wait-time measurements imply:

| Wait-time scenario | Minutes / screening | Aggregate person-years / year | 79-year lifetime-equivalents / year | vs. 1980–1999 terrorism deaths/year | vs. 1980–2001 incl. 9/11 deaths/year |
|---|---:|---:|---:|---:|---:|
| GAO FY2006 average peak | 8.2 | 14,094 | 178.4 | 17.4× | 1.31× |
| GAO FY2005 average peak | 8.9 | 15,297 | 193.6 | 18.9× | 1.42× |
| GAO FY2004 average peak | 9.4 | 16,157 | 204.5 | 20.0× | 1.50× |
| TSA Dec 2003–Nov 2004 average peak | 13.0 | 22,344 | 282.8 | 27.6× | 2.08× |
| BTS traveler-reported Dec 2003–Nov 2004 | 20.4 | 35,063 | 443.8 | 43.3× | 3.26× |

These are **sensitivity scenarios**, not a claim that 2004/2006 wait times exactly describe 2024. I could not find a current authoritative published *national annual mean* checkpoint wait time. BTS/TSA and GAO provide unusually useful national federal measurements, but they are historical and often measure **peak queue time** rather than all-day passenger-weighted time.

### Terrorism continuation baselines

The FBI recorded **327 terrorist incidents or suspected incidents and 205 deaths in the United States from 1980–1999**. A deliberately naive continuation of that pre-9/11 history is therefore:

- **16.35 incidents/suspected incidents per year**
- **10.25 terrorism deaths per year**

The FBI recorded **8 incidents and zero deaths in 2000**, then **14 incidents and 2,788 deaths in 2001**, of which **2,783 were from September 11**. If 1980–2001 is averaged together, the baseline becomes:

- **15.86 incidents per year**
- **136.05 terrorism deaths per year**

That second number is overwhelmingly a 9/11 artifact. START's Global Terrorism Database analysis explicitly reports that U.S. attack lethality varies considerably over time and **does not appear to follow a particular trend**; 85% of U.S. terrorism deaths in 1970–2013 were from 9/11 alone. A linear “trend” model is therefore not treated as a credible estimator here.

## Formula

```text
annual_wait_hours = annual_screenings × wait_minutes / 60
annual_wait_years = annual_wait_hours / (24 × 365.2425)
lifetime_equivalents = annual_wait_years / life_expectancy_years
```

For the historical-continuation comparison:

```text
pre_9_11_deaths_per_year = 205 / 20 = 10.25
incl_9_11_deaths_per_year = (205 + 0 + 2788) / 22 = 136.045...
ratio = lifetime_equivalents / historical_deaths_per_year
```

Run `python3 analysis.py` to reproduce the table from the checked-in inputs.

## The causal caveat that matters

This project currently measures **gross TSA-era queue time**, not time *caused by the existence of TSA*. Airport passenger screening existed before TSA: before the Aviation and Transportation Security Act, passenger and baggage screening was performed by private companies under contract to airlines, with FAA oversight. TSA federalized that system after 9/11.

Therefore **“no TSA” is not the same counterfactual as “no airport screening.”** A causal estimate of incremental TSA waiting cost would need a comparable pre-TSA queue-time baseline and would need to account for other post-9/11 defenses such as hardened cockpit doors, intelligence/watch-list changes, air marshals, changed passenger behavior, and screening technology.

Likewise, the FBI fatality baseline covers **all U.S. terrorism**, much of which an airport checkpoint could not plausibly prevent. The 10.25 and 136.05 figures are historical-continuation benchmarks, **not estimates of deaths TSA actually prevented**. GAO has itself found that measuring deterrence and system-wide cost/effectiveness across aviation countermeasures is difficult and historically incomplete.

The useful question this repository can answer objectively is therefore:

> **How large is the aggregate checkpoint time burden, expressed in whole-lifetime units, compared numerically with plausible historical terrorism-fatality baselines?**

A later aviation-only model can narrow the counterfactual further.

## Primary sources

- [Bureau of Transportation Statistics — Air Passenger Opinions on Security Screening Procedures](https://www.bts.gov/archive/publications/airline_passenger_opinions_on_security_screening_procedures/entire) — 13.0-minute TSA measured peak mean and 20.4-minute traveler-reported mean, Dec 2003–Nov 2004; includes methodology.
- [GAO-07-299](https://www.gao.gov/products/gao-07-299) — TSA average peak wait times: 9.4 min FY2004, 8.9 FY2005, 8.2 FY2006.
- [TSA — 2024 By the Numbers](https://www.tsa.gov/sites/default/files/tsa_2024_yir_by_the_numbers.pdf) — 904 million travelers screened in 2024.
- [CDC/NCHS Data Brief 548](https://www.cdc.gov/nchs/products/databriefs/db548.htm) — U.S. life expectancy at birth was 79.0 years in 2024.
- [FBI — Terrorism in the United States 1999](https://www.fbi.gov/file-repository/counterterrorism/stats-services-publications-terror_99.pdf/view) — 327 incidents/suspected incidents and 205 deaths, 1980–1999.
- [FBI — Terrorism 2000/2001](https://www.fbi.gov/file-repository/counterterrorism/stats-services-publications-terror-terror00_01.pdf/view) — 2000: 8 incidents, zero deaths; 2001: 14 incidents, 2,788 deaths; 2,783 deaths from 9/11.
- [START — Patterns of Terrorism in the United States, 1970–2013](https://www.start.umd.edu/pubs/START_TEVUS_GTDPatternsofTerrorisminUS1970-2013_Oct2014.pdf) — lethality is highly irregular; 85% of fatalities in that period were from 9/11.
- [GAO-09-27R](https://www.gao.gov/products/gao-09-27r) — pre-ATSA screening was performed by private screening companies under airline contracts; TSA federalization followed ATSA.
- [GAO-17-794](https://www.gao.gov/products/gao-17-794) — limits in TSA countermeasure effectiveness/deterrence measurement and system-wide cost/effectiveness analysis.

## Repository layout

- `data/inputs.csv` — hand-curated authoritative inputs with source links.
- `analysis.py` — dependency-free reproduction of the annualized calculations.
- `results/annualized_2024.csv` — checked-in normalized results.
- `docs/methodology.md` — counterfactual definitions, limitations, and next steps.
