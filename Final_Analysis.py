import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

# ---- SETTINGS ---- #
base_dir = "/Users/mehullad27/Downloads/"
tickers = ["CRWV", "SOUN", "FROG"]
order_sizes = np.arange(10, 5010, 50)
snapshot_interval = 200

# ---- SLIPPAGE CALC ---- #
def calculate_slippage(row, order_size):
    remaining = order_size
    cost = 0
    for lvl in range(10):
        px = row.get(f'ask_px_0{lvl}', np.nan)
        sz = row.get(f'ask_sz_0{lvl}', 0)
        if pd.isna(px) or sz == 0:
            continue
        fill = min(sz, remaining)
        cost += fill * px
        remaining -= fill
        if remaining <= 0:
            break
    if remaining > 0:
        return np.nan
    avg_px = cost / order_size
    best_ask = row.get('ask_px_00', np.nan)
    return avg_px - best_ask

# ---- MODEL FUNCTIONS ---- #
def linear_model(x, a): return a * x
def power_model(x, a, b): return a * np.power(x, b)
def expo_model(x, a, b): return a * (1 - np.exp(-b * x))

# ---- LOOP OVER TICKERS ---- #
for ticker in tickers:
    print(f"\n📊 Processing {ticker}...")
    path = os.path.join(base_dir, ticker)
    files = sorted([f for f in os.listdir(path) if f.endswith(".csv")])
    all_slippage = []

    for fname in files:
        fpath = os.path.join(path, fname)
        df = pd.read_csv(fpath)
        df.columns = [c.lower().strip() for c in df.columns]

        if not any(c.startswith("ask_px_0") for c in df.columns):
            continue

        for i in range(0, len(df), snapshot_interval):
            row = df.iloc[i]
            result = []
            for size in order_sizes:
                slip = calculate_slippage(row, size)
                result.append(slip)
            all_slippage.append(result)

    slippage_array = np.array(all_slippage)
    mean_slip = np.nanmean(slippage_array, axis=0)

    # ---- FIT MODELS ---- #
    xdata = order_sizes
    ydata = mean_slip

    popt_lin, _ = curve_fit(linear_model, xdata, ydata)
    y_pred_lin = linear_model(xdata, *popt_lin)
    r2_lin = r2_score(ydata, y_pred_lin)

    popt_pow, _ = curve_fit(power_model, xdata, ydata, bounds=(0, [10, 2]))
    y_pred_pow = power_model(xdata, *popt_pow)
    r2_pow = r2_score(ydata, y_pred_pow)

    popt_exp, _ = curve_fit(expo_model, xdata, ydata, bounds=(0, [1, 0.01]))
    y_pred_exp = expo_model(xdata, *popt_exp)
    r2_exp = r2_score(ydata, y_pred_exp)

    save_dir = "plots"
    os.makedirs(save_dir, exist_ok=True)
    # ---- PLOT ---- #
    plt.figure(figsize=(10, 6))
    plt.scatter(xdata, ydata, s=18, label="Actual Slippage", alpha=0.7)
    plt.plot(xdata, y_pred_lin, color='orange', linestyle="--", label=f"Linear Fit (R²={r2_lin:.3f})")
    plt.plot(xdata, y_pred_pow, color='green', linestyle="--", label=f"Power-Law Fit (R²={r2_pow:.3f})")
    plt.plot(xdata, y_pred_exp, color='red', linestyle="--", label=f"Exponential Fit (R²={r2_exp:.3f})")

    plt.title(f"Modeling Temporary Market Impact $g_t(x)$ — {ticker}")
    plt.xlabel("Order Size")
    plt.ylabel("Average Slippage ($)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # Save and close
    save_path = os.path.join(save_dir, f"{ticker}_gtx_fit.png")
    plt.savefig(save_path, dpi=300)
    print(f"✅ Saved plot to: {save_path}")
    plt.close()  # prevents blocking in batch runs

