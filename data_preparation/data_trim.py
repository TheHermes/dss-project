import pandas as pd
import numpy as np
from collections import Counter

recs = "data/recommendations.csv"
users = "data/users_trimmed.csv"
output_path = "data/recommendations_trimmed.csv"


users_df = pd.read_csv(users)

#users_sample = users_df.sample(n=100_000, random_state=42)

#users_sample.to_csv("data/users_trimmed.csv", index=False)

user_ids = set(users_df["user_id"])


user_counts = Counter()



chunksize = 500_000

for chunk in pd.read_csv(recs, usecols=["user_id"], chunksize=chunksize):
    # Count per user
    user_counts.update(chunk["user_id"].value_counts().to_dict())


# Convert to a dataframe for convenience
user_counts_df = pd.DataFrame(list(user_counts.items()), columns=["user_id", "count"])
user_counts_df = user_counts_df[user_counts_df["user_id"].isin(user_ids)]

# Normalize so total = 500k
user_counts_df["target"] = (user_counts_df["count"] / user_counts_df["count"].sum()) * 500_000
user_counts_df["target"] = user_counts_df["target"].round().astype(int)

output_path = "data/recommendations_trimmed.csv"
chunksize = 500_000

remaining = dict(zip(user_counts_df["user_id"], user_counts_df["target"]))
collected = []

for chunk in pd.read_csv(recs, chunksize=chunksize):
    chunk = chunk[chunk["user_id"].isin(remaining)]
    # Keep at most the number we still need for each user
    chunk["keep"] = chunk["user_id"].apply(lambda uid: min(remaining[uid], 1))
    selected = chunk.groupby("user_id", group_keys=False).apply(
        lambda g: g.sample(n=min(len(g), remaining[g.name]), random_state=42)
    )
    collected.append(selected)
    # Update how many are left to collect
    for uid in selected["user_id"].value_counts().index:
        remaining[uid] -= selected["user_id"].value_counts()[uid]
    # Stop if we've hit the target total
    if sum(v for v in remaining.values()) <= 0:
        break

final_recs = pd.concat(collected)
final_recs.to_csv(output_path, index=False)