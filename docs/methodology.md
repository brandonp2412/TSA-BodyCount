# Methodology

## The question

How much human life does TSA burn in airport lines, and how does that body count compare with **aviation terrorists**?

The study measures two annual numbers:

1. Human time spent waiting in TSA lines, converted into 79-year lives.
2. People killed in U.S. terrorist attacks against airports and aircraft.

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

## Aviation terrorist body count

The terrorist side is restricted to START GTD's U.S. **Airports & Aircraft** target category.

START counts:

- **43 attacks** in the 1970s
- **23 attacks** in the 1980s
- **2 attacks** in the 1990s

That is **68 attacks** from 1970–1999.

The lethal pre-9/11 aviation attacks used by the model are stored in `data/aviation_deaths.csv`:

- 1974 Los Angeles International Airport bombing: **3 deaths**
- 1975 LaGuardia Airport bombing: **11 deaths**
- 1981 Pan Am terminal bombing at JFK: **1 death**
- 1982 Pan Am Flight 830 bombing: **1 death**

Total through 2000:

```text
16 deaths / 31 years = 0.516129 deaths per year
```

## Including 9/11

The U.S. government count used here is **2,977 people killed on September 11, 2001**.

Add that to the 16 earlier aviation-terrorism deaths and average the entire 1970–2001 period:

```text
(16 + 2,977) / 32 = 93.53125 deaths per year
```

This **93.53125 deaths/year** rate drives the main charts.

## TSA vs. aviation terrorists

Using TSA's 13.0-minute measured wait:

```text
282.84 / 93.53125 = 3.024×
```

Using the passenger-reported 20.4-minute wait:

```text
443.84 / 93.53125 = 4.745×
```

Against the pre-9/11 aviation rate:

```text
282.84 / 0.516129 = 548.0×
443.84 / 0.516129 = 859.9×
```

## Primary sources

- BTS wait times: https://www.bts.gov/archive/publications/airline_passenger_opinions_on_security_screening_procedures/entire
- GAO FY2004–FY2006 wait times: https://www.gao.gov/products/gao-07-299
- TSA 2024 screening volume: https://www.tsa.gov/sites/default/files/tsa_2024_yir_by_the_numbers.pdf
- CDC/NCHS 2024 life expectancy: https://www.cdc.gov/nchs/products/databriefs/db548.htm
- START U.S. airport/aircraft attack counts: https://www.start.umd.edu/pubs/START_TEVUS_GTDPatternsofTerrorisminUS1970-2013_Oct2014.pdf
- START/DHS lethal transportation attacks: https://www.start.umd.edu/pubs/START_DHS_GTD_Targeting%20Critical%20Infrastructure%20in%20the%20US_June2016.pdf
- U.S. Congress 9/11 victim count: https://www.govinfo.gov/content/pkg/CHRG-116hhrg39837/pdf/CHRG-116hhrg39837.pdf
