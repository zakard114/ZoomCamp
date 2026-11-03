# SMA Zoomcamp 2026 — Homework 5: Research Ideas

Q1–Q3 write-up cells: [[2026]_Module_05_Homework.ipynb](https://github.com/zakard114/ZoomCamp/blob/main/SMA/05/HW_05/%5B2026%5D_Module_05_Homework.ipynb)

---

## Form answers

| # | Choice |
|---|--------|
| 1 | see Q1 below |
| 2 | see Q2 below |
| 3 | see Q3 below |

All three are free-text exploratory answers. No numeric bubbles.

---

## Setup

- Kernel: SMA / `HW_05/.venv` → `SMA/.venv` → `ML/.venv`
- Official text: `materials/homework5.md` (do not edit)
- Launch: `bash run-nbclassic.sh` — do not use `jupyter notebook`
- Official note: no code, trained model, or completed backtest is required
- Submit: https://courses.datatalks.club/sma-zoomcamp-2026/homework/hw05
- Deadline: 6 November 2026, 22:59

The three ideas use different mechanisms on purpose: a local-language disclosure edge (Korea), a relative-value / pairs idea (memory semis), and a macro-surprise idea (US CPI surprise vs rate-sensitive names). That matches the homework hint to vary the economic story, not just the ticker.

---

## Q1 — Korea mid/small-cap disclosures (local-language information)

**1. Market and scope.** Korea Exchange (KRX) mid and small caps with limited English analyst coverage, especially industrials and materials names that file mainly in Korean on DART. Horizon: about 5–20 trading days after a material filing or local industry print.

**2. Investment thesis.** When a company files a material update in Korean (order backlog, plant utilization, related-party contract, guidance change), local readers can update their view before a thin English coverage set catches up. I expect short-horizon abnormal returns around those events for names outside the usual global-coverage set, not because “Korea grows,” but because the information arrives unevenly.

**3. Potential edge.** The edge is language and coverage, not a secret indicator. I read Korean filings directly. Many screeners and English summaries lag or skip mid/small names. Liquidity is the constraint that can erase the edge, so I would stay away from the thinnest names.

**4. Data and sources.**
- Checked / already used in this course context: Yahoo Finance `.KS` prices (same style as the course frame), basic OHLCV.
- To verify next: Korea FSS DART open API for filing timestamps and document types; KRX market-cap and trading-value filters; optional Bank of Korea or Statistics Korea industry prints for the sector.
- What they measure: filing time and type (information event), price path after the event, and whether the name was liquid enough to trade.

**5. Research approach.** Event study, not a deep neural net. Define an event as a DART filing in a chosen material category. Measure cumulative abnormal return vs KOSPI (or a size-matched KRX basket) over 1, 5, and 20 days. Trade rule for a later simulation: long the name only if the filing category is “positive operations” and 20-day average won volume clears a floor. Module 4-style fees and daily trade caps would still apply if this becomes a strategy.

**6. Validation and risks.** Benchmark: KOSPI buy-and-hold and a random-filing placebo. Reject the idea if abnormal returns disappear after costs, if they only appear in names too thin to trade, or if English wire coverage timestamps already match Korean filing times for the sample. Other limits: DART API quirks, survivorship, and the fact that a growing Korea story alone is not the signal.

---

## Q2 — Memory-semiconductor relative value (pairs / co-movement)

**1. Market and scope.** Two economically linked memory names whose cash flows share DRAM/NAND cycles — for a first test, Samsung Electronics vs SK hynix (KRX), with a US-listed alternative pair (e.g. Micron vs a memory-exposed ETF) only as a robustness check. Horizon: days to a few weeks while the spread is stretched, not a multi-year “AI winner” bet.

**2. Investment thesis.** Memory pricing and inventory cycles pull related producers together. Temporary gaps in the relative price should mean-revert when the shared cycle is intact. The idea is relative value, not a call that AI demand rises forever.

**3. Potential edge.** Single-name momentum and headline AI narratives treat the names as independent stories. A spread that uses both price history and a shared cycle indicator (spot memory prices or Korea semiconductor export stats) can flag a temporary dislocation the headline tape ignores.

**4. Data and sources.**
- Checked: Yahoo Finance prices for the pair; course-style growth and macro columns if I reuse the combined frame later.
- To verify: public DRAM/NAND spot or contract price series (vendor choice still open), Korea semiconductor export statistics, and a clean mapping of corporate actions / dual listings so the ratio is not broken by splits.
- What they measure: relative equity price vs a shared industry stress indicator.

**5. Research approach.** Fit a rolling residual of log(price A) on log(price B) (or an ECM). Signal when the z-score of the residual exceeds ±2 and the memory-cycle indicator has not also broken its own trend. Decision: long the lagging name / short the leader (or long only if shorting is hard), exit at z≈0 or at a hard time stop. Reject trades when the rolling correlation collapses — that is the “relationship broken” flag.

**6. Validation and risks.** Benchmark: buy-and-hold either leg, and a plain price-ratio z-score with no cycle filter. Reject if the half-life of the residual is too long for the capital, if costs eat the average reversion, or if AI-capex regime shifts permanently change the beta between the names. Liquidity and borrow costs matter on the short leg.

---

## Q3 — US CPI surprise vs rate-sensitive equities (macro event)

**1. Market and scope.** US large-cap rate-sensitive groups: equity REITs, utilities, and regional-bank ETFs (liquid proxies first; single names later). Horizon: announcement day through about five trading days after the CPI print.

**2. Investment thesis.** In Module 3 I noted that the tree leaned on CPI-related features and that a CPI *surprise* (actual minus consensus), not only the level, is what I would want. Thesis: when CPI prints hotter or colder than consensus, rate-sensitive baskets move more than the broad market over a short window because discount-rate expectations jump. The signal is the surprise, not “inflation is high.”

**3. Potential edge.** Many models use lagged CPI levels already in FRED. Consensus-relative surprises and same-morning nowcasts are easier to underweight in a slow monthly feature set. The edge is timing around the print, not a claim that utilities always beat the S&P.

**4. Data and sources.**
- Checked / named in my Module 3 notes: Cleveland Fed inflation nowcast as a public nowcasting reference; FRED for CPI and policy-rate series; liquid ETF prices via Yahoo Finance.
- To verify: a free or low-cost consensus print source (or reconstruct surprise from nowcast vs print if consensus is paid), exact release timestamps, and a stable REIT/utility/bank ETF list.
- What they measure: surprise size and sign, and subsequent relative returns of rate-sensitive proxies vs SPY.

**5. Research approach.** Event study around CPI releases. Signal: surprise = actual − consensus (or actual − prior nowcast). Rule sketch: if surprise is above a positive threshold, short the rate-sensitive basket vs SPY for N days; if below a negative threshold, long the basket vs SPY. Keep Module 4 fee assumptions. No need for a deep model on day one — a signed surprise bucket table is enough to see if anything exists.

**6. Validation and risks.** Benchmark: SPY, and the same baskets traded on random Wednesdays. Reject if results only appear before costs, if they vanish after 2015 (or another regime cut), or if the open already reflects the print so the close-to-close window is empty. Publication timing, ETF spreads, and overlapping FOMC weeks are the main operational risks.

---

## Before submit checklist

- Each idea has a thesis, named data, a first test, and a failure mode.
- Mechanisms differ: disclosure lag (KR) vs relative value (memory pair) vs macro surprise (US CPI).
- None of the three is “use AI to predict prices.”
