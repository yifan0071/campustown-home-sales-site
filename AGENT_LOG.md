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
