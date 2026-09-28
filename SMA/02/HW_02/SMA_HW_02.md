# SMA Zoomcamp 2026 — Homework 2: Dataframe Analysis

Q1–Q4 calculations: [[2026]_Module_02_Homework.ipynb](https://github.com/zakard114/ZoomCamp/blob/main/SMA/02/HW_02/%5B2026%5D_Module_02_Homework.ipynb)

---

## Form answers

| # | Choice |
|---|--------|
| 1 | **500** |
| 2 | **0.04** |
| 3 | **1** |
| 4 | **65** |
| 5 | see Q5 below |

---

## Setup

- Kernel: SMA / `HW_02/.venv` → `SMA/.venv` → `ML/.venv`
- Official text: `materials/homework2.md` (do not edit)
- Launch: `bash run-nbclassic.sh` — do not use `jupyter notebook`

---

## Q1 — Withdrawn IPOs by Company Type

**Question:** Total withdrawn IPO value ($ millions) for the company class with the highest total.

`pandas.read_html` tried to open the HTML as a file path, so I wrapped it in `StringIO`. The page had **34** withdrawn rows, not the 32 in the prompt. A `-` price made `Shares * Avg_price` empty, so those rows use `Est $ Vol`.

**Answer:** **Acquisition Corp, 499.985**. The form choice is the nearest option, **500**.

---

## Q2 — Median Sharpe Ratio for 2025 IPOs (first 8 months)

**Question:** Median Sharpe on 11 September 2026 for IPOs before 1 September 2025.

I dropped a 0% return and got **146** names, not 148. One download locked yfinance's timezone database, so I pulled 20 tickers at a time. Delisted symbols 404'd. **132** names came back with a Close. Columns were a MultiIndex, and the date index was timezone-aware, so I took the `Close` level and stripped the timezone before matching `2026-09-11`. A flat close made volatility 0 and Sharpe infinite; I dropped those before `describe()`.

Mean `growth_252d` was about 1.05 and the median about 0.59.

**Answer:** **0.049**. The form choice is the nearest option, **0.04**.

---

## Q3 — Fixed Months Holding Strategy

**Question:** Holding period (1–12 months, 21 trading days each) with the highest median growth from the IPO close.

One tiny first close blew the mean up into the thousands. The median falls as the hold gets longer and stays under 1.

**Answer:** **1 month, median growth 0.935**. The form choice is the nearest option, **1**.

---

## Q4 — Simple RSI-Based Trading Strategy

**Question:** Net income, in $ thousands, from $1000 every time RSI < 30 between 2000-01-01 and 2025-06-01.

`gdown` was not in the venv, and this version has no `fuzzy=` argument, so I used the `uc?id=` URL. The column is lowercase `rsi`; `RSI` matched nothing. **5,206** trades. Mean 30-day growth 1.26%, win rate 55.1%.

**Answer:** **65.8**. The form choice is the nearest option, **65**.

---

## Q5 — Predicting a Positive-Return IPO (optional)

I would not buy every IPO; I would drop acquisition/blank-check names and keep only names that are up after the first month.
