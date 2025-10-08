import pandas as pd

# Create recommendations based on 1000 users from user_stratified_sampel.csv

# -----------------------------
# Step 1: Load sampled users
# -----------------------------
users_sample_path = "data/users_stratified_sample.csv"
recs_path = "data/recommendations.csv"
output_path = "data/recommendations_stratified.csv"

print("🔹 Loading stratified user sample...")
users_sample = pd.read_csv(users_sample_path)
user_ids = set(users_sample["user_id"])
print(f"Loaded {len(user_ids)} user IDs from sample")

# -----------------------------
# Step 2: Filter recommendations
# -----------------------------
chunksize = 500_000  # tune for memory
filtered_chunks = []
total_kept = 0
chunk_count = 0

print("🔹 Filtering recommendations.csv ...")
for chunk in pd.read_csv(recs_path, chunksize=chunksize):
    chunk_count += 1
    filtered = chunk[chunk["user_id"].isin(user_ids)]
    total_kept += len(filtered)
    filtered_chunks.append(filtered)
    print(f"  Processed chunk {chunk_count:>3}, kept {len(filtered):>7} rows")

# -----------------------------
# Step 3: Combine and save
# -----------------------------
if filtered_chunks:
    final_recs = pd.concat(filtered_chunks, ignore_index=True)
    print(f"\nTotal recommendations kept: {len(final_recs)}")
    final_recs.to_csv(output_path, index=False)
    print(f"Saved to: {output_path}")
else:
    print("No matching recommendations found for sampled users.")
