import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Paths to April 3rd CSVs
sample_files = {
    "FROG": '/Users/mehullad27/Downloads/FROG/FROG_2025-04-03 00:00:00+00:00.csv',
    "CRVW": '/Users/mehullad27/Downloads/CRWV/CRWV_2025-04-03 00:00:00+00:00.csv',
    "SOUN":'/Users/mehullad27/Downloads/SOUN/SOUN_2025-04-03 00:00:00+00:00.csv'
}

# Load each CSV into a dictionary of DataFrames
dfs = {ticker: pd.read_csv(path) for ticker, path in sample_files.items()}

# Sample 5 snapshot indices per file (early, mid, late)
snapshot_indices = [30, 90, 150, 210, 270]

def compute_buy_side_slippage(row, order_size):
    total_shares_to_fill = order_size
    shares_filled = 0
    total_cost = 0.0

    for i in range(10):
        ask_price = row.get(f'ask_px_0{i}', np.nan)
        ask_size = row.get(f'ask_sz_0{i}', 0)

        if np.isnan(ask_price) or ask_size == 0:
            continue

        fill_qty = min(ask_size, total_shares_to_fill)
        total_cost += fill_qty * ask_price
        shares_filled += fill_qty
        total_shares_to_fill -= fill_qty

        if total_shares_to_fill == 0:
            break

    if shares_filled < order_size:
        return None

    avg_exec_price = total_cost / shares_filled
    best_ask = row.get('ask_px_00', np.nan)
    return avg_exec_price - best_ask


def plot_slippage_curve(df, row_index, ticker, save_dir):
    row = df.iloc[row_index]
    sizes = list(range(10, 1001, 10))
    slippages = [compute_buy_side_slippage(row, s) for s in sizes]
    
    sizes, slippages = zip(*[(s, slip) for s, slip in zip(sizes, slippages) if slip is not None])
    
    plt.figure(figsize=(7, 4))
    plt.plot(sizes, slippages, marker='o', linewidth=2)
    plt.title(f"{ticker} - Snapshot {row_index}")
    plt.xlabel("Order Size")
    plt.ylabel("Buy-Side Slippage ($)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, f"{ticker}_snapshot_{row_index}.png"))
    plt.close()



save_dir = "slippage_plots"
os.makedirs(save_dir, exist_ok=True)

# Loop through each ticker + snapshot
for ticker, df in dfs.items():
    for idx in snapshot_indices:
        plot_slippage_curve(df, idx, ticker, save_dir)

print("✅ Slippage curves saved to:", save_dir)


