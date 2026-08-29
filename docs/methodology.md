# Methodology

## 1. Question

The project compares two annual quantities:

1. Aggregate elapsed human time spent waiting in TSA checkpoint queues, converted to a rhetorical unit of whole U.S. lifetimes.
2. Historical U.S. terrorism fatalities per year under simple pre-TSA continuation baselines.

The comparison is intentionally easy to understand, but it must not be mistaken for a mortality or causal-effect estimate.

## 2. Queue-time burden

For a scenario with `N` annual screenings and `w` minutes of queueing per screening:

```text
hours = N * w / 60
years = hours / (24 * 365.2425)
lifetime_equivalents = years / L
```

`L = 79.0` years, the CDC/NCHS final 2024 U.S. life expectancy at birth.

The current annualization uses TSA's reported 904 million travelers screened in 2024. The wait-time inputs are historical federal measurements because no current authoritative national annual passenger-weighted mean was identified in the initial research pass.

### Wait-time definitions differ

BTS describes TSA's 13.0-minute figure as an average **peak** wait measured by giving timestamped cards to randomly selected passengers as they entered the queue and collecting them before the passenger walked through the metal detector. It therefore excludes the actual screening process.

BTS's 20.4-minute estimate is passenger self-reporting. BTS explicitly notes that recall/rounding error may be present and respondents may include some of the actual screening process.

GAO's 8.2–9.4-minute figures are TSA average peak wait times across airport categories for FY2004–FY2006.

These are kept as separate scenarios rather than blended into a false-precision point estimate.

## 3. Terrorism continuation baselines

### Baseline A: pre-9/11 ordinary history

FBI, 1980–1999:

- 327 incidents or suspected incidents / 20 years = **16.35/year**
- 205 fatalities / 20 years = **10.25/year**

This is the primary simple historical mean because it does not let a single unprecedented 9/11 observation dominate the estimate.

### Baseline B: include 9/11

FBI:

- 1980–1999: 327 incidents/suspected incidents, 205 deaths
- 2000: 8 incidents, 0 deaths
- 2001: 14 incidents, 2,788 deaths

Therefore 1980–2001:

- 349 / 22 = **15.86 incidents/year**
- 2,993 / 22 = **136.05 deaths/year**

The 2001 FBI fatality count attributes 2,783 deaths to September 11, so this baseline is dominated by one observation.

### Why not fit a linear fatality trend?

START's Global Terrorism Database analysis of U.S. terrorism from 1970–2013 says the prevalence of lethal attacks varies considerably and **does not appear to follow a particular trend**. It also reports that 85% of all U.S. terrorism fatalities in the period came from 9/11 and another 5% from the Oklahoma City bombing.

A least-squares trend line through such a sparse, heavy-tailed process would produce numerical precision without a defensible statistical interpretation. The project therefore presents historical means and sensitivity analyses instead.

## 4. What “without TSA” cannot mean

TSA did not invent airport screening. GAO documents that before ATSA, passenger and baggage screening was performed by private screening companies under contract to airlines, with FAA regulatory oversight. ATSA shifted responsibility to TSA and required a federal screening workforce by November 2002.

Consequently, the current queue estimate is **gross TSA queue time**. It is not yet **incremental TSA-caused queue time**.

A causal incremental model would require:

```text
incremental_time = TSA-era screening time - credible counterfactual screening time
```

A directly comparable national pre-TSA queue-time series has not yet been found.

## 5. What TSA could plausibly prevent

The FBI 1980–2001 terrorism series includes domestic and international attacks against many non-aviation targets. Most such attacks are outside the causal scope of airport checkpoints.

Therefore the all-terrorism historical mean is best understood as a provocative upper-level comparison, not an estimate of checkpoint-preventable deaths.

The stronger next model should isolate attacks involving commercial aviation or airport-security failure and separately model security measures that changed after 9/11, including cockpit hardening, passenger/crew response, intelligence and watch-list systems, air marshals, baggage screening, and checkpoint screening.

## 6. Effectiveness uncertainty

GAO reported in 2017 that TSA had effectiveness data for some aviation security countermeasures but lacked a system-wide method for measuring deterrence and had not systematically evaluated cost/effectiveness tradeoffs across all countermeasures. The recommendation was later closed as implemented after TSA expanded its analytical work, but the core counterfactual remains unobservable: we do not directly observe how many attacks would have occurred in a world without a particular security measure.

The project should therefore report results as **historical-continuation counterfactuals**, with assumptions visible, rather than as discovered facts about attacks “prevented by TSA.”

## 7. Primary sources

- BTS wait-time methodology and 13.0 / 20.4 minute estimates: https://www.bts.gov/archive/publications/airline_passenger_opinions_on_security_screening_procedures/entire
- GAO FY2004–FY2006 TSA peak wait times: https://www.gao.gov/products/gao-07-299
- TSA 2024 traveler screenings: https://www.tsa.gov/sites/default/files/tsa_2024_yir_by_the_numbers.pdf
- CDC/NCHS 2024 life expectancy: https://www.cdc.gov/nchs/products/databriefs/db548.htm
- FBI 1980–1999 terrorism statistics: https://www.fbi.gov/file-repository/counterterrorism/stats-services-publications-terror_99.pdf/view
- FBI 2000/2001 terrorism statistics: https://www.fbi.gov/file-repository/counterterrorism/stats-services-publications-terror-terror00_01.pdf/view
- START U.S. terrorism patterns: https://www.start.umd.edu/pubs/START_TEVUS_GTDPatternsofTerrorisminUS1970-2013_Oct2014.pdf
- GAO pre-/post-ATSA screening structure: https://www.gao.gov/products/gao-09-27r
- GAO countermeasure effectiveness review: https://www.gao.gov/products/gao-17-794
