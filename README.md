# College-town home sales

## What this site is for

A reference for people comparing homes in college towns. It shows completed home sales from March 2023 to March 2026 in 18 towns around 11 universities, so a reader can compare typical prices, price per square foot, time to contract, and how price changes with distance from campus. It describes past sales only. It is not an appraisal or investment advice.

## Live site

https://yifan0071.github.io/campustown-home-sales-site/

## Data notes

**Source.** `data/college_town_home_sales.csv`, version 1.0, collected March 2026. Sales run from 2023-03-27 to 2026-03-25.

**Rows left out.** A sale is used only if its price is between $10,000 and $5,000,000. Sales outside that range are treated as likely data errors or outliers and are not counted. The count of excluded sales is shown on the site. Nothing else is removed.

**How each figure is defined.**
- *Sales*: the number of sales used for that town (after the price rule).
- *Median price*: the middle sale price, rounded to the whole dollar.
- *Median price per sq ft*: sale price divided by `living_area_sqft`, using only sales where that area is above zero.
- *Median days to contract*: `contract_date` minus `list_date`, for sales where both dates are present. This is the time from listing to signed contract, not to closing.
- *Sales with no listing date*: the share of a town's sales where `list_date` is blank. Those sales are left out of the days-to-contract figure.
- *Distance bands*: `miles_to_campus` (straight-line distance) grouped into bands. Medians are taken within each band.
- *Median price by sale year*: sales grouped by the year in `sale_date`. The first year (2023) starts on 2023-03-27 and the last year (2026) ends on 2026-03-25, so both are partial years.
- *Median price by bedrooms*: sales grouped by `beds`. Counts of 5 or more are grouped together. Records with 0 bedrooms are left out.
- *Minimum sample for a median*: a town-year or town-bedroom group shows a median only with at least 30 sales. Smaller groups show a dash.

**Known limits.**
- Prices are from completed sales in the source, not verified against county records.
- `tax_assessed_value` is not used as a price.
- Towns with few sales (for example Pittsboro, Newberry and Carrboro) have wide swings, and the sample size is shown next to each figure.
- Some addresses appear more than once because they are separate condo units. Records are counted by `listing_id`, so these units are not merged.

**How the figures were made.** `scripts/make_city_summary.py` reads the CSV and writes `data/city_summary.json`, `data/distance_summary.json` and `data/trends_summary.json`. Run it from the repository root with `python3 scripts/make_city_summary.py`. It needs only Python 3. The page reads these three JSON files.

## Tools we used

- **AI coding agent:** Claude Code (Anthropic), working in this repository through its own branch and pull requests.
- **Libraries:** none. The page is plain HTML, CSS and JavaScript. The summary script uses only the Python standard library.
- **Checks:** figures were cross-checked against the SQLite file with a read-only query.

## Citation

College-town home sales dataset, version 1.0 (2026). University of Illinois-Deloitte Foundation Center for Business Emerging Technologies. Data collected March 2026.

## Who did what

Yifan Wang did this project alone. Yifan Wang chose the site's question, reviewed and approved every change, and merged each pull request. Claude Code wrote the code, the data script and the documentation under Yifan Wang's direction.
