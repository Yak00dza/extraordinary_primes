import matplotlib.pyplot as plt
from math import log
import pandas as pd
import numpy as np
import json


data_files = (
    'curves_noniso_l_results.txt',
    'curves_noniso_l_250-500_results.txt',
    'curves_noniso_l_500-750_results.txt',
)

dfs = []

seen_curves_global = None
for filename in data_files:
    eoprimes = []
    seen_curves = set()
    with open(filename, 'r') as f:
        for line in f:
            curve_data = json.loads(line.strip())
            A, B = curve_data['A'], curve_data['B']
            seen_curves.add((A, B))
            for eoprime in curve_data['extraordinary']:
                eoprimes.append({
                    'A': A,
                    'B': B,
                    'p': eoprime,
                })
        
    if seen_curves_global is None:
        seen_curves_global = seen_curves
    else:
        seen_curves_global &= seen_curves

    dfs.append(pd.DataFrame(eoprimes))

df = pd.concat(dfs)
df = df[df[['A', 'B']].apply(tuple, axis=1).isin(seen_curves_global)]
total_curves = len(seen_curves_global)


# Number of extraordinary primes with each value of p
counts = df['p'].value_counts().sort_index()

# Cumulative number up to each p
cum = counts.cumsum()

# Fill missing p values and divide by total number of curves
averages = (
    cum.reindex(range(751), fill_value=np.nan)
       .ffill()
       .fillna(0)
       .to_frame()
        / total_curves
)

C = 0.58
averages['hypothesis'] = C * np.log(np.log(averages.index))

plt.plot(averages.index, averages['count'], label='Observed')
plt.plot(averages.index, averages['hypothesis'], label='Hypothesis')
plt.xlabel("n")
plt.ylabel("Average extraordinary primes per curve")
plt.grid(True)
plt.legend()
plt.savefig("density_function.png")
averages = []

# print(result.shape)


# counts = (
#     df.groupby("count")
#       .size()
#       .reset_index(name="num_curves")
# )

# # Plot counts as bars
# plt.figure(figsize=(10, 6))
# plt.bar(counts["count"], counts["num_curves"], color='skyblue')
# plt.xlabel("Number of Extraordinary Primes below 250")
# plt.ylabel("Number of Curves")
# plt.title("Distribution of Extraordinary Primes for Curves A,B")
# plt.savefig("plot.png", dpi=300, bbox_inches="tight")

# print(counts)
# total_curves = sum(counts['num_curves'])
# total_eoprimes = sum(df['count'])
# average_count = total_eoprimes / total_curves
# print('The average count is', average_count)

