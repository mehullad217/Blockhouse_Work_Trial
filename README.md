# 📊 Blockhouse Work Trial – Market Impact Modeling & Execution Optimization

Welcome to my submission for the Blockhouse Work Trial! This project investigates **temporary market impact modeling** and **optimal trade execution** using real LOB snapshots and order flow data across three tickers.

---

## 🧠 Project Structure and Methodology

This project is divided into **two key phases**:

### 🔹 Part 1: Slippage Estimation & Curve Fitting
We model the function \( g_t(x) \): temporary price impact of trading \( x \) shares at time \( t \). The goal is to empirically find a functional form that best captures slippage behavior.

#### `slippage_analysis.py`
- **Goal**: Initial exploratory modeling using 5–10 sample points per stock.
- **Stocks**: CRWV, FROG, SOUN.
- **Fits tried**: Linear, power-law, exponential.
- **Outcome**: Exponential model showed the best consistency across names.

#### `Models.py`
- **Goal**: Deeper modeling on a **single stock (CRWV)**.
- **Approach**: Used ~200 points to fit all three models and evaluate R².
- **Outcome**: Confirmed exponential form is best suited for optimization.

#### `Final_Analysis.py`
- **Goal**: Scale modeling to **all three stocks** using full datasets.
- **Process**: Fit exponential, power-law, and linear models.
- **Output**: Saved plots in `slippage_plots/` for side-by-side comparison.

---

### 🔹 Part 2: Execution Schedule Optimization

We formulate how to split a large total order \( S \) into slices \( x_1, x_2, ..., x_N \) over time to minimize total impact \( \sum g_t(x_t) \).

#### `Blockhouse_Trial_task_Pt2.pdf` / `Execution_Schedule_Model.md`
### 🎯 Objective Formulation

We want to minimize total market impact when executing a large order `S` across `N` time slices:

**Minimize:**  
&nbsp;&nbsp;&nbsp;&nbsp;∑ aᵢ · (1 − exp(−bᵢ · xᵢ))

**Subject to:**  
&nbsp;&nbsp;&nbsp;&nbsp;∑ xᵢ = S  
&nbsp;&nbsp;&nbsp;&nbsp;xᵢ ≥ 0


---

## 📁 Folder Structure

```bash
Blockhouse_Work_Trial/
│
├── slippage_analysis.py         # Initial modeling on small samples
├── slippage_analysis2.py        # Extended exploratory version
├── Models.py                    # Curve fitting for a single stock
├── Final_Analysis.py            # Batch modeling for all 3 tickers
│
├── plots/                       # Extra visualizations
├── slippage_plots/             # Saved model fit plots
├── blockhouse_data/            # (Optional) Raw or processed LOB data
├── models/                     # Saved regression models or params
│
├── Blockhouse_Trial_task_Pt2.pdf   # Execution strategy formulation
├── Modeling_Temporary_gt(x).pdf    # Part 1 results and visuals
└── README.md                      # This file!


🚀 Tools & Libraries
Python 3.10+

matplotlib, numpy, pandas, scipy, sklearn

Optional for optimization: cvxpy, sympy


🧑‍💻 Author & Attribution
Author: Mehul Lad
Email: mehullad667@gmail.com
GitHub: github.com/mehullad217
Institution: University of Maryland, Baltimore County (UMBC)
Program: M.S. in Statistics, 1st Year
Submission: Blockhouse Quant Work Trial Task (Summer 2025)

