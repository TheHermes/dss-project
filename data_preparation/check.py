import pandas as pd

# Load the trimmed datasets
users_trimmed = pd.read_csv("data/users_trimmed.csv")
recs_trimmed = pd.read_csv("data/recommendations_trimmed.csv")

# Extract user_id column name (replace with your actual name)
user_col = "user_id"

# Check all IDs in recs exist in users
valid_users = set(users_trimmed[user_col])
invalid = recs_trimmed.loc[~recs_trimmed[user_col].isin(valid_users)]

if invalid.empty:
    print("✅ All recommendations have valid user_ids present in users_trimmed.csv")
else:
    print(f"⚠️ Found {len(invalid)} invalid rows (user_ids not in users_trimmed.csv)")
    print(invalid.head())
