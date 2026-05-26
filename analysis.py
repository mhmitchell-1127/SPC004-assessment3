import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ── Script 3: Analysis & Visualisation ──────────────────────────────────────
# Input:  like_annotated.csv  (your completed annotation file)
# Output: frequency_table printed + bar chart saved as like_functions_chart.png
#
# HOW TO USE:
#   1. Complete the 'function' column in like_annotation_template.csv
#   2. Save that file as like_annotated.csv
#   3. Run this script

df = pd.read_csv('like_annotated.csv')

# Remove any rows left blank
print(df['function'].value_counts(dropna=False))
df['function'] = df['function'].fillna('').astype(str).str.strip().str.upper()
df = df[df['function'] != '']

total = len(df)
print(f"Total annotated tokens: {total}\n")

# Frequency table
counts = df['function'].value_counts()
pct = (counts / total * 100).round(1)
table = pd.DataFrame({'Count': counts, 'Percentage': pct})
table.index.name = 'Function'
print("── Frequency Table ──────────────────────────────")
print(table.to_string())
print(f"\nTotal: {total}\n")

# Optional: breakdown by spoken_type if column exists
if 'spoken_type' in df.columns:
    print("── By Spoken Type ───────────────────────────────")
    cross = pd.crosstab(df['function'], df['spoken_type'])
    print(cross.to_string())
    print()

# Bar chart
CATEGORY_ORDER = ['VERB', 'PREP', 'QUOT', 'APPROX', 'DM', 'DP']
ordered_counts = counts.reindex(CATEGORY_ORDER, fill_value=0)

colours = ['#4C72B0', '#DD8452', '#55A868', '#C44E52', '#8172B2', '#937860']

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(ordered_counts.index, ordered_counts.values, color=colours,
              edgecolor='white', linewidth=0.8, width=0.6)

# Add count + percentage labels above bars
for bar, val in zip(bars, ordered_counts.values):
    pct_val = val / total * 100
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
            f"{val}\n({pct_val:.1f}%)", ha='center', va='bottom', fontsize=9)

ax.set_xlabel("Function", fontsize=11)
ax.set_ylabel("Frequency (n)", fontsize=11)
ax.set_title("Pragmatic Functions of like in BNC Spoken Conversation (n=150)", fontsize=12)
ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig('like_functions_chart.png', dpi=150)
print("Chart saved: like_functions_chart.png")
plt.show()
