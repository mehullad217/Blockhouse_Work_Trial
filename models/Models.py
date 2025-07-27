import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
from slippage_analysis2 import order_sizes, mean_slippage

order_sizes = order_sizes
# Replace this with your actual slippage values
mean_slippage = mean_slippage


# --- MODEL DEFINITIONS ---
def linear_model(x, beta):
    return beta * x

def power_law_model(x, alpha, gamma):
    return alpha * np.power(x, gamma)

def exponential_model(x, a, b):
    return a * (1 - np.exp(-b * x))

# --- FIT MODELS ---
popt_lin, _ = curve_fit(linear_model, order_sizes, mean_slippage)
popt_pow, _ = curve_fit(power_law_model, order_sizes, mean_slippage, maxfev=10000)
popt_exp, _ = curve_fit(exponential_model, order_sizes, mean_slippage, maxfev=10000)

# --- PREDICTIONS ---
slip_lin = linear_model(order_sizes, *popt_lin)
slip_pow = power_law_model(order_sizes, *popt_pow)
slip_exp = exponential_model(order_sizes, *popt_exp)

# --- R² SCORES ---
r2_lin = r2_score(mean_slippage, slip_lin)
r2_pow = r2_score(mean_slippage, slip_pow)
r2_exp = r2_score(mean_slippage, slip_exp)

# --- PLOT ---
plt.figure(figsize=(10, 6))
plt.plot(order_sizes, mean_slippage, 'o', label='Actual Slippage', alpha=0.6)
plt.plot(order_sizes, slip_lin, '--', label=f'Linear Fit (R²={r2_lin:.3f})')
plt.plot(order_sizes, slip_pow, '--', label=f'Power-Law Fit (R²={r2_pow:.3f})')
plt.plot(order_sizes, slip_exp, '--', label=f'Exponential Fit (R²={r2_exp:.3f})')

plt.title("Modeling Temporary Market Impact $g_t(x)$")
plt.xlabel("Order Size")
plt.ylabel("Average Slippage ($)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
