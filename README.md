# Algorithmic Backtester
A Python execution of a moving average backtester

## Overview
This project tests rule-based trading signals against historical price series. The strategy implements a **Dual Moving Average Crossover**:
* **Long Signal:** Fast SMA crosses above the Slow SMA (bullish momentum)
* **Short Signal:** Fast SMA crosses below the Slow SMA (bearish momentum)

The engine parses raw OHLCV market data, determines daily signals, simulates trade execution without lookahead bias, and outputs key portfolio performance metrics

---

## Strategy Logic & Mathematics

### Simple Moving Average (SMA)
For a price series $P$ over a window period $k$:

$$SMA_k(t) = \frac{1}{k} \sum_{i=0}^{k-1} P_{t-i}$$

* **Fast SMA ($k_{fast}$):** Captures short-term price trend (e.g., 20-day)
* **Slow SMA ($k_{slow}$):** Captures long-term price trend (e.g., 50-day)

### Maximum Drawdown (MDD)
Measures the maximum observed loss from a peak to a trough of a portfolio before a new peak is attained:

$$MDD = \max_{\tau \le t} \left( \frac{P_{peak}(\tau) - P(t)}{P_{peak}(\tau)} \right)$$

---

## Tech Stack & Dependencies

* **Language:** Python 3.x
* **Environment:** Jupyter Notebook / Anaconda
* **Core Libraries:**
  * `pandas` — Time-series data handling and portfolio indexing
  * `numpy` — Array manipulations and vectorized calculation
 
---

## Getting Started

### Prerequisites
Ensure you have Python and Jupyter installed. You can install all dependencies via pip:

```bash
pip install numpy pandas
```

### Usage
1. Clone the repository:
```bash
git clone https://github.com/matthewhdanter/Algorithmic-Backtester.git
cd Algorithmic-Backtester
```
2. Download OHLCV data in CSV format (i.e., from Yahoo Finance)
3. Open the main script, adjust parameters, and run the backtester
