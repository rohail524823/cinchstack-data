# CinchStack software pricing dataset

What small-business software really costs: {{tools}} tools, {{plans}} plans and {{scenarios}} team-size cost estimates. Each figure carries the date it was read from the vendor's own pricing page and the page it came from. Last checked: {{lastChecked}}.

The dataset is published at **[cinchstack.com/data](https://cinchstack.com/data/)**. This repository is an automatic copy. A GitHub Action downloads the files from the site every day and commits any change, so this repository's history is also a dated record of how the prices changed.

## Files

| File | What it holds |
|---|---|
| `pricing.csv` | One row per plan: the price billed month to month (`monthly_usd`), the effective monthly price billed yearly (`annual_monthly_usd`), the unit, the seats included, the date checked and the source URL. |
| `scenarios.csv` | One row per tool and team size: CinchStack's estimate of the real monthly bill (`monthly_usd`), its confidence and the date checked. |
| `pricing.json` | Everything above, plus add-ons, usage fees, extra costs, the assumptions behind each estimate and every source. |

## Use it

```python
import pandas as pd

base = "https://raw.githubusercontent.com/rohail524823/cinchstack-data/main/"
plans = pd.read_csv(base + "pricing.csv")
team_costs = pd.read_csv(base + "scenarios.csv")
```

## Field notes

- All money is US dollars, as shown to a US buyer.
- `monthly_usd` is empty when a plan is sold only on a yearly contract; `annual_monthly_usd` is empty when there is no yearly option.
- Team-size costs are estimates for the assumptions written into each scenario, for comparison, not quotes.
- Card processing fees on e-commerce tools are listed as extra costs and are not added into the monthly totals.
- Each Monday a script re-reads the vendor pricing pages it can open. Every change is logged at [cinchstack.com/changes](https://cinchstack.com/changes/).

## License and citation

CC BY 4.0 (see `LICENSE`): copy, share and adapt it for any purpose, including commercial use. Please credit and link back:

> CinchStack, "Software pricing dataset", https://cinchstack.com/data/, licensed CC BY 4.0.

GitHub's "Cite this repository" button uses `CITATION.cff`. If you quote a single price, link to that tool's pricing page on [cinchstack.com](https://cinchstack.com/) so readers can see the date it was checked. Prices change; a figure is only as good as the date beside it.

## Corrections

Seen a price that has changed? Report it at [cinchstack.com/contact](https://cinchstack.com/contact/). Corrections are made on the site and reach this copy within a day.
