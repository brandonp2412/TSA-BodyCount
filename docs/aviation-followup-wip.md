# Aviation-only follow-up — work in progress

Resume this analysis on `glass`.

## Goal

Replace the all-U.S.-terrorism denominator with an aviation-only terrorism baseline so the study compares TSA checkpoint time against deaths from terrorism that actually targeted airports/aircraft or involved aviation hijacking.

## Current research state

START's report *Patterns of Terrorism in the United States, 1970–2013* explicitly breaks out U.S. attacks against **Airports & Aircraft** by decade. The report shows:

- 1970s: 43 attacks
- 1980s: 23 attacks
- 1990s: 2 attacks
- 2000s: includes the four 9/11 aircraft attacks

So there were 68 U.S. airport/aircraft attacks from 1970–1999. The two 1990s incidents caused no deaths.

Source:
https://www.start.umd.edu/pubs/START_TEVUS_GTDPatternsofTerrorisminUS1970-2013_Oct2014.pdf

A GTD CSV mirror was also located for event-level filtering. The relevant fields include country/country_txt, year, target type (`Airports & Airlines` in older GTD exports), attack type, and `nkill`.

Example mirror used during the research pass:
https://github.com/daattali/statsTerrorismProject/blob/master/globalterrorismdb.csv

## Next steps on glass

1. Download/import a GTD dataset with event-level rows.
2. Filter to United States and target type `Airports & Aircraft` / `Airports & Airlines` (schema wording varies by export).
3. Restrict the primary baseline to 1970–1999 or 1980–1999 and total:
   - incidents
   - fatalities (`nkill`)
   - annual deaths
4. Keep a second version including 9/11 for the same joke-study contrast.
5. Add a checked-in aviation-event CSV or derived summary so the calculation is reproducible.
6. Change `model.py`, `analysis.py`, README headline ratios, and all four charts to use the aviation-only denominator.
7. Run `make all` and `make check`; confirm Actions passes.

## Presentation direction

Keep the repo's current direct/joke-study style. Do not reintroduce academic hedging language or the word `counterfactual`.

Headline framing should remain obvious, e.g.:

- `WAITING IN TSA` vs `KILLED IN AVIATION TERROR ATTACKS`
- `TSA burns X× more human life`

The aviation-only denominator should become the primary comparison because it matches what airport security could plausibly affect.
