import pandas as pd

#
#  Create 1000 user.csv
#

# Load your users file (only needed columns)
users = pd.read_csv("data/users.csv")

# Define bins and desired sample sizes
bins = [(5, 15), (16, 25), (26, 35), (36, 45), (46, 55), (56, 65), (66, 75), (76, 85), (86, 95), (96, 120)]
sample_per_bin = 100  # users per bin
sampled_frames = []

# Loop through each bin and sample users
for low, high in bins:
    group = users[(users["reviews"] >= low) & (users["reviews"] <= high)]
    if len(group) > 0:
        n = min(sample_per_bin, len(group))
        sample = group.sample(n=n, random_state=42)
        sampled_frames.append(sample)
        print(f"{n} users from {low}-{high} reviews (available: {len(group)})")
    else:
        print(f"No users found for range {low}-{high}")

# Concatenate all the samples
final_sample = pd.concat(sampled_frames, ignore_index=True)

print(f"\nTotal sampled users: {len(final_sample)}")
final_sample.to_csv("data/users_stratified_sample.csv", index=False)
print("Saved to: data/users_stratified_sample.csv")
