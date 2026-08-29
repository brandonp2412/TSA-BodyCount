# Methodology

## The question

How much human life does TSA burn in airport lines, and how does that body count compare with terrorists?

The study measures two annual numbers:

1. Human time spent waiting in TSA lines, converted into 79-year lives.
2. People killed by terrorists per year using FBI pre-TSA history.

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

Every minute of average TSA wait therefore burns:

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

The charts keep each published measurement separate and label its year directly.

## Terrorist body count

### 1980–1999

FBI totals:

- **327 incidents**
- **205 deaths**

Annual rate:

```text
205 / 20 = 10.25 deaths per year
```

This is the main terrorist rate used for the TSA comparison.

### Including 9/11

FBI totals:

- 1980–1999: **205 deaths**
- 2000: **0 deaths**
- 2001: **2,788 deaths**

Total:

```text
2,993 / 22 = 136.05 deaths per year
```

The FBI attributes **2,783 deaths** to 9/11. START reports that 9/11 caused **85% of U.S. terrorism deaths from 1970–2013**.

## TSA vs. terrorists

Using TSA's 13.0-minute measured wait:

```text
283.0 / 10.25 = 27.6×
```

Using the passenger-reported 20.4-minute wait:

```text
443.8 / 10.25 = 43.3×
```

Including 9/11 in the terrorist annual rate:

```text
283.0 / 136.05 = 2.08×
443.8 / 136.05 = 3.26×
```

## Primary sources

- BTS wait times: https://www.bts.gov/archive/publications/airline_passenger_opinions_on_security_screening_procedures/entire
- GAO FY2004–FY2006 wait times: https://www.gao.gov/products/gao-07-299
- TSA 2024 screening volume: https://www.tsa.gov/sites/default/files/tsa_2024_yir_by_the_numbers.pdf
- CDC/NCHS 2024 life expectancy: https://www.cdc.gov/nchs/products/databriefs/db548.htm
- FBI 1980–1999 terrorism statistics: https://www.fbi.gov/file-repository/counterterrorism/stats-services-publications-terror_99.pdf/view
- FBI 2000/2001 terrorism statistics: https://www.fbi.gov/file-repository/counterterrorism/stats-services-publications-terror-terror00_01.pdf/view
- START U.S. terrorism patterns: https://www.start.umd.edu/pubs/START_TEVUS_GTDPatternsofTerrorisminUS1970-2013_Oct2014.pdf
