# SMA Zoomcamp 2026 — Homework 1: Intro and Data Sources

Write-up for the homework form. Notebook I ran: `[2026]_Module_01_Homework.ipynb`. Official questions (untouched): `materials/homework1.md`.

**Course:** [Stock Markets Analytics Zoomcamp 2026](https://courses.datatalks.club)  
**Instructions:** [cohorts/2026/homework1.md](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/cohorts/2026/homework1.md)  
**Submit:** https://courses.datatalks.club/sma-zoomcamp-2026/homework/hw01

---

## Form answers

| # | Choice |
|---|--------|
| 1 | **2025** |
| 2 | **2** |
| 3 | **8** |
| 4 | **0.35** |
| 5 | see Q5 below |
| 6 | see Q6 below |

---

## Setup

I ran `[2026]_Module_01_Homework.ipynb` in local Jupyter, same environment as the Module 1 lesson.

---

## Q1 — S&P 500 additions (from 2020)

Wikipedia list → DataFrame of ticker, name, year added → count by year.

Wikipedia returned **403** until I sent a browser `User-Agent`. `pd.read_html(response.text)` also blew up (it tried to open the HTML as a file), so I wrapped it in `StringIO`.

```python
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
# I got 403 until I sent a browser User-Agent
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
response = requests.get(url, headers=headers, timeout=30)
response.raise_for_status()

# pandas treated the HTML as a filepath until I wrapped it in StringIO
tables = pd.read_html(StringIO(response.text))
df = tables[0][["Symbol", "Security", "Date added"]].copy()
df["Date added"] = pd.to_datetime(df["Date added"], errors="coerce")
df["added_year"] = df["Date added"].dt.year

yearly = (
    df.loc[df["added_year"] >= 2020, "added_year"]
    .value_counts()
    .sort_index()
)
# count finished years only — the 224 twenty-year names aren't this answer
finished = yearly.loc[yearly.index < 2026]
print(yearly)
print(int(finished.idxmax()), int(finished.max()))
```

**Output (current Wikipedia table when I ran it):**

```text
2020    10
2021    10
2022    15
2023    15
2024    16
2025    18
2026    13
```

2026 isn’t a finished year, so I took the max over 2020–2025. That’s **2025** (18 names). 2024 was 16.

I also counted names added at least 20 years ago (224). Extra — not the year-with-most-additions question.

**Answer:** **2025**

---

## Q2 — Indexes YTD vs the US (as of 21 August 2026)

Close-to-close from 2026-01-01 to 2026-08-21. Count how many of the **10 non-US** indexes beat `^GSPC`. No FX.

`history(end="2026-08-21")` skipped 21 Aug on my run, so I used `end="2026-08-22"`.

```python
tickers = {
    "US": "^GSPC", "China": "000001.SS", "Hong Kong": "^HSI",
    "Australia": "^AXJO", "India": "^NSEI", "Canada": "^GSPTSE",
    "Germany": "^GDAXI", "UK": "^FTSE", "Japan": "^N225",
    "Mexico": "^MXX", "Brazil": "^BVSP",
}
start_date, end_date = "2026-01-01", "2026-08-21"
# yfinance end is exclusive, so I used the next day to keep 21 Aug
download_end = "2026-08-22"
```

**YTD % I got:**

```text
Japan 27.36
Canada 14.86
US 11.90
UK 8.70
Brazil 6.54
Germany 6.51
Australia 3.79
Mexico 2.48
Hong Kong -1.25
China -2.94
India -7.25
```

Only Japan and Canada were above the US.

I also compared 3-, 5-, and 10-year windows. Extra, not the form.

**Answer:** **2**

---

## Q3 — Median S&P 500 correction drawdown

I marked an ATH when close beat the prior cummax, took the trough between consecutive ATHs, and kept only ≥5% drops. Then `(peak - trough) / peak * 100`.

```python
spx = yf.Ticker("^GSPC").history(start="1950-01-01", interval="1d")["Close"]
prev_peak = spx.shift(1).cummax()
is_ath = spx > prev_peak  # ATH if close beats the prior running max
# trough between those ATHs; I kept drawdowns >= 5%; median landed near 8
```

Largest ones matched the list in the homework (2007–09, 2000–02, 1973–74, …). Percentiles on my run:

```text
drawdown %  25 / 50 / 75  ≈  6.23 / 7.99 / 14.02
median drawdown %  ≈  8
```

**Answer:** **8**

---

## Q4 — AMZN, median 2-day return after a positive surprise

`get_earnings_dates()` gave me 25 rows from 2020-10-29 (one future date with empty EPS).

I treated the announcement as Day 2, so the 2-day return is `Close3 / Close1 - 1`, then kept `Surprise(%) > 0` and took the median in **percent**.

```python
amzn = yf.Ticker("AMZN")
earnings = amzn.get_earnings_dates()
close = amzn.history(period="max")["Close"]
ret_2d = close.shift(-1) / close.shift(1) - 1  # Day 2 = announcement; Close3 / Close1 - 1
pos = earnings[earnings["Surprise(%)"] > 0]  # positive surprises only
```

**Output:**

```text
positive surprises: 20
median 2-day %: 0.35
```

**Answer:** **0.35**

Bull vs bear split was extra, not the form.

---

## Q5 — Capstone idea

I want a short-term prediction model for the US stock market, focusing on the S&P 500 and a few large names like AMZN, over about a 30-day horizon after a dip.

Q3 was about 5% drops from all-time highs, and the homework mentioned “buy the dip”, so I would start there. I am not sure about the model yet. For inputs I would reuse the correction size/length from Q3, earnings surprises like Q4, and the FRED series we already pulled in the lesson notebook (Fed funds and core CPI).

---

## Q6 — Extra metrics for that idea

I reused a few FRED downloads from the Module 1 notebook.

```python
import pandas_datareader as pdr

start = date(1990, 1, 1)
fedfunds = pdr.DataReader("FEDFUNDS", "fred", start=start)
cpilfesl = pdr.DataReader("CPILFESL", "fred", start=start)
dgs5 = pdr.DataReader("DGS5", "fred", start=start)

print(fedfunds.tail(3))
print(cpilfesl.tail(3))
print(dgs5.tail(3))
```

- FEDFUNDS — Fed funds rate from class. I want to see if buying the dip looks different when rates are high.
- CPILFESL — core CPI from class. Inflation might change how the market comes back.
- DGS5 — 5-year Treasury from class (we also downloaded DGS1). Extra rates series.

They are not all daily, so for now I would just take the last value before the dip.
