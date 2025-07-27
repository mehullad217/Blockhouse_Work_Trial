import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

# Change this to your local directory path with renamed files
base_dir = "/Users/mehullad27/Downloads/CRWV/"
order_sizes = np.arange(10, 5010, 50)
snapshot_interval = 200

def calculate_slippage_from_lob(row, order_size):
    remaining = order_size
    cost = 0

    for level in range(10):
        ask_price = row.get(f'ask_px_0{level}', np.nan)
        ask_size = row.get(f'ask_sz_0{level}', 0)

        if pd.isna(ask_price) or ask_size == 0:
            continue

        fill = min(ask_size, remaining)
        cost += fill * ask_price
        remaining -= fill

        if remaining <= 0:
            break

    if remaining > 0:
        return np.nan

    avg_fill_price = cost / order_size
    best_ask = row.get('ask_px_00', np.nan)
    return avg_fill_price - best_ask

# Read and process all files
all_files = sorted([f for f in os.listdir(base_dir) if f.endswith(".csv")])
print(f"✅ Total CSVs found: {len(all_files)}")

slippage_results = []

for fname in all_files:
    path = os.path.join(base_dir, fname)
    df = pd.read_csv(path)
    df.columns = [c.lower().strip() for c in df.columns]

    # Check basic column structure
    if not any(c.startswith("ask_px_0") for c in df.columns):
        print(f"⛔ Skipping file {fname}, missing LOB columns.")
        continue

    for i in range(0, len(df), snapshot_interval):
        row = df.iloc[i]
        #print(f"\n📌 Snapshot at row {i} — sample LOB:")
        # for lvl in range(10):
        #     px = row.get(f'ask_px_0{lvl}')
        #     sz = row.get(f'ask_sz_0{lvl}')
        #     print(f"Level {lvl}: Price = {px}, Size = {sz}")
        # break  # 🔁 Only inspect first snapshot; remove this to see all
        snapshot_result = []
        for size in order_sizes:
            slip = calculate_slippage_from_lob(row, size)
            snapshot_result.append(slip)
        slippage_results.append(snapshot_result)

# Aggregate slippage
slippage_array = np.array(slippage_results)
mean_slippage = np.nanmean(slippage_array, axis=0)

# Plot slippage curve
plt.figure(figsize=(10, 6))
plt.plot(order_sizes, mean_slippage, marker='o', label='Mean Slippage (CRWV)')
plt.title("Buy-Side Slippage Curve over 30 Days (CRWV)")
plt.xlabel("Order Size")
plt.ylabel("Average Slippage ($)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("slippage_curve_crwv_all_days.png")
plt.show()


