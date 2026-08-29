# Methodology

## The question

How much human life does TSA burn in airport lines, and how does that body count compare with **aviation terrorists**?

The study measures two annual numbers:

1. Human time spent waiting in TSA lines, converted into 79-year lives.
2. People killed in U.S. terrorism involving airports, aircraft, or aviation hijackings.

## TSA body count

For `N` annual screenings and `w` minutes waiting per screening:

```text
hours = N × w / 60
years = hours / (24 × 365.2425)
lives_burned = years / 79
```

Inputs:

- TSA screened **904 million people in 2024**.
- CDC/NCHS puts 2024 U.S. life expectancy at **79.0 years**.

Every minute of average TSA wait burns:

```text
904,000,000 / 60 / 24 / 365.2425 / 79 = 21.7569 lives per year
```

So:

- 8.2 minutes = **178 lives/year**
- 8.9 minutes = **194 lives/year**
- 9.4 minutes = **205 lives/year**
- 13.0 minutes = **283 lives/year**
- 20.4 minutes = **444 lives/year**

## TSA wait-time measurements

GAO reports TSA average peak wait times across airport categories:

- FY2004: **9.4 minutes**
- FY2005: **8.9 minutes**
- FY2006: **8.2 minutes**

BTS reports two measurements for December 2003 through November 2004:

- TSA-measured average peak wait: **13.0 minutes**
- Passenger-reported mean wait: **20.4 minutes**

## Aviation-terrorism filter

The event source is START's Global Terrorism Database 2018 distribution, pinned by SHA-256 in `scripts/extract_aviation_events.py`.

The extractor keeps GTD events when all of these are true:

- country is `United States`
- year is 1970–2001
- at least one GTD target type is `Airports & Aircraft` / `Airports & Airlines`, **or** the attack is an aviation-specific hijacking

All matching rows are checked into `data/aviation_events.csv`.

This catches the four 9/11 attacks even though their primary targets are people, businesses, government, and military targets: each attack also has an `Airports & Aircraft` target for the hijacked aircraft.

## Pre-TSA aviation terrorist body count

The GTD-derived subset has five lethal events before 2001:

- 1974 Los Angeles International Airport bombing: **3 deaths**
- 1975 LaGuardia Airport bombing: **11 deaths**
- 1976 TWA Flight 355 hijacking / Grand Central bomb: **1 death**
- 1981 Pan Am terminal bombing at JFK: **1 death**
- 1982 Pan Am Flight 830 bombing: **1 death**

Total: **17 deaths**.

GTD has no event-level data for 1993. The baseline therefore uses every GTD-covered pre-TSA year from 1970 through 2000: **30 years**.

```text
17 / 30 = 0.5666667 deaths per year
```

This is the primary terrorist rate used by the charts.

## Including 9/11

The U.S. government count used here is **2,977 people killed on September 11, 2001**.

Add that body count and extend the same GTD-covered run through 2001:

```text
(17 + 2,977) / 31 = 96.5806452 deaths per year
```

This is the secondary "even with 9/11" comparison.

## TSA vs. aviation terrorists

Using TSA's 13.0-minute measured wait:

```text
282.8400 / 0.5666667 = 499.13×
282.8400 / 96.5806452 = 2.93×
```

Using the passenger-reported 20.4-minute wait:

```text
443.8413 / 0.5666667 = 783.25×
443.8413 / 96.5806452 = 4.60×
```

## Rebuilding the GTD subset

Download the pinned `globalterrorismdb_0718dist.csv` snapshot and run:

```bash
python3 scripts/extract_aviation_events.py globalterrorismdb_0718dist.csv > data/aviation_events.csv
```

The script checks the raw file SHA-256 before producing output. `make all` then regenerates headline results and charts entirely from checked-in inputs.

## Primary sources

- START GTD: https://www.start.umd.edu/data-tools/GTD
- START GTD codebook: https://www.start.umd.edu/sites/default/files/2024-10/Codebook.pdf
- START GTD FAQ: https://www.start.umd.edu/gtd-faqs
- START U.S. terrorism report: https://www.start.umd.edu/pubs/START_TEVUS_GTDPatternsofTerrorisminUS1970-2013_Oct2014.pdf
- START/DHS transportation infrastructure report: https://www.start.umd.edu/pubs/START_DHS_GTD_Targeting%20Critical%20Infrastructure%20in%20the%20US_June2016.pdf
- START/Kaggle GTD 2018 snapshot metadata: https://www.kaggle.com/START-UMD/gtd/metadata
- Pinned raw GTD snapshot: https://archive.org/download/globalterrorismdb_0718dist/globalterrorismdb_0718dist.csv
- U.S. Court of Appeals, TWA Flight 355: https://law.justia.com/cases/federal/appellate-courts/F2/549/252/342112/
- BTS wait times: https://www.bts.gov/archive/publications/airline_passenger_opinions_on_security_screening_procedures/entire
- GAO FY2004–FY2006 wait times: https://www.gao.gov/products/gao-07-299
- TSA 2024 screening volume: https://www.tsa.gov/sites/default/files/tsa_2024_yir_by_the_numbers.pdf
- CDC/NCHS 2024 life expectancy: https://www.cdc.gov/nchs/products/databriefs/db548.htm
- U.S. Congress 9/11 victim count: https://www.govinfo.gov/content/pkg/CHRG-116hhrg39837/pdf/CHRG-116hhrg39837.pdf
