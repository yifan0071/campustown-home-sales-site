# Agent log

Add a dated entry each time you work with your AI coding agent, with the newest entry at the bottom. Each entry records what you asked the agent, what it produced, and what you checked or changed. Paste your key prompts in exactly as you typed them. Include at least one time the agent got something wrong, and how you caught it.

Copy this outline for each entry:

```markdown
## YYYY-MM-DD: What you worked on

- **Asked:** "Paste your prompt here."
- **Agent produced:** What it made or changed.
- **Checked or changed:** How you checked it, and what you fixed.
```

## 2026-11-18: Summary script and city/distance page

- **Asked:** "可以的，开始做吧" (after I had proposed a plan: count sales priced between $10,000 and $5,000,000, a town comparison table, and a distance-to-campus table).
- **Agent produced:** `scripts/make_city_summary.py`, which writes `data/city_summary.json` and `data/distance_summary.json`; a rewritten `index.html` that loads those files; and a rewritten README (site purpose, data notes, tools).
- **Checked or changed:**
  - I compared the script's city figures with a separate SQLite query. Gainesville, State College, Pittsboro and Davis matched, except that Pittsboro's median differed by 0.5 dollars from rounding.
  - The agent's first draft of the page said sales outside the price range were "not plausible for a home." That overstated what the data shows, since a $5 million+ home can be real. I caught it on review and changed the wording to "treated as likely data errors or outliers."
  - The agent tried to start a local test server and run a browser test, and the command was blocked by the tool's permission check. The page has not been tested in a browser yet. I will check the live site after publishing.
  - The agent also wrote a log file to `/tmp` by mistake. It should have used the session scratchpad folder.

## 2026-11-19: Price by sale year and by bedrooms

- **Asked:** "1 就你推荐的这两个" (the two additions I proposed: median price by sale year, and median price by bedroom count) and "2 是的" (keep the page in English).
- **Agent produced:** new outputs in `scripts/make_city_summary.py` written to `data/trends_summary.json`; two new tables in `index.html`; new data notes in the README and on the page.
- **Checked or changed:**
  - The three JSON outputs were regenerated. The city and distance files came out byte-for-byte unchanged.
  - I cross-checked 3 towns (Gainesville, Pittsboro, State College) for each year and each bedroom group against the SQLite file with a read-only query. All matched.
  - The agent first wrote an empty extra column header in the year table. I caught it on re-reading the page code and removed it.
  - Not yet checked: the rendered page in a browser. I will ask you to check the live site after merging.
