
import pandas as pd
import numpy as np
from scipy.stats import spearmanr
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# 全局设置
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 7


df = pd.read_excel("4.216.xlsx")


pairs = [
    ("CrdA", "DCC_TCC"),
    ("PrdA", "DCC_TCC"),
    ("CdrA", "Efficiency"),
    ("PbrA3", "Efficiency"),
    ("Rdase-A4", "Efficiency"),
    ("RdhA8", "Efficiency"),
]


bootstrap_results = {}
spearman_real = {}
ci_bounds = {}
for gene, indicator in pairs:
    subset = df[[gene, indicator]].dropna()

    X = subset[indicator].values.reshape(-1, 1)
    y = subset[gene].values
    model = LinearRegression().fit(X, y)
    resid = y - model.predict(X)
    cutoff = np.percentile(np.abs(resid), 95)
    trimmed = subset[np.abs(resid) <= cutoff]
    

    r_real, _ = spearmanr(trimmed[gene], trimmed[indicator])
    spearman_real[(gene, indicator)] = r_real
    

    n = trimmed.shape[0]
    bs_rs = []
    for _ in range(1000):
        idx = np.random.randint(0, n, n)
        sample = trimmed.iloc[idx]
        r_bs, _ = spearmanr(sample[gene], sample[indicator])
        bs_rs.append(r_bs)
    bootstrap_results[(gene, indicator)] = bs_rs
    

    lower, upper = np.percentile(bs_rs, [2.5, 97.5])
    ci_bounds[(gene, indicator)] = (lower, upper)


fig, axes = plt.subplots(2, 3, figsize=(15, 8), tight_layout=True)
axes = axes.flatten()

for ax, ((gene, indicator), bs_rs) in zip(axes, bootstrap_results.items()):
    ax.hist(bs_rs, bins=30, edgecolor='black')
    

    r_val = spearman_real[(gene, indicator)]
    ax.axvline(r_val, color='red', linestyle='--', linewidth=1, label=f"r = {r_val:.2f}")
    

    lower, upper = ci_bounds[(gene, indicator)]
    ax.axvline(lower, color='blue', linestyle=':', linewidth=1, label=f"2.5% = {lower:.2f}")
    ax.axvline(upper, color='blue', linestyle=':', linewidth=1, label=f"97.5% = {upper:.2f}")
    
    ax.set_title(f"{gene} vs {indicator}")
    ax.set_xlabel("Spearman r")
    ax.set_ylabel("Frequency")
    ax.legend(fontsize=6, loc='upper right')


fig.savefig("bootstrap_histograms_with_CI.svg")
plt.show()



