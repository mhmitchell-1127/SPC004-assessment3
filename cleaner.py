import pandas as pd
import random

# ── Script 1: Data Cleaning ──────────────────────────────────────────────────
# Input:  like_dataset.txt  (raw CQPweb download)
# Output: like_annotation_template.csv  (150-row sample ready for manual coding)


df = pd.read_csv('like_dataset.txt', sep='\t')

# Keep useful columns only
df_clean = df[['Number of hit', 'Text ID', 'Context before', 
               'Query item', 'Context after', 'Type']].copy()
df_clean.columns = ['hit_num', 'text_id', 'left_context', 
                    'keyword', 'right_context', 'spoken_type']

# Normalise keyword to lowercase
df_clean['keyword'] = df_clean['keyword'].str.lower()

# Keep only rows where keyword is exactly 'like' (removes likely, likewise etc.)
df_clean = df_clean[df_clean['keyword'] == 'like']

print(f"Total clean hits: {len(df_clean)}")
print(f"Spoken type breakdown:\n{df_clean['spoken_type'].value_counts()}\n")

# Sample 150 rows for manual annotation
df_sample = df_clean.sample(n=150, random_state=42).reset_index(drop=True)

# Add blank function column for manual annotation
# Fill each row with one of these labels:
#   VERB    – expresses preference or liking   e.g. "I like tea"
#   PREP    – introduces a comparison          e.g. "looks like his dad"
#   QUOT    – quotative: 'be like' + speech    e.g. "she was like 'no way'"
#   APPROX  – approximates a quantity          e.g. "like five minutes ago"
#   DM      – clause-initial discourse marker  e.g. "Like, I don't know"
#   DP      – medial/final discourse particle  e.g. "it was, like, strange"
df_sample['function'] = ''

df_sample.to_csv('like_annotated.csv', index=False)
print("Saved: like_annotation_template.csv")
print("Open the file, read each row, and fill in the 'function' column.")
