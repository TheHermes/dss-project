import pandas as pd

csv_path = "data/games.csv"

json_path = "data/games_metadata.json"

games_df = pd.read_csv(csv_path)

metadata_df = pd.read_json(json_path, lines=True)

print(games_df.columns)
print(metadata_df.columns)

print(games_df['app_id'].nunique(), metadata_df['app_id'].nunique())

merged_df = games_df.merge(metadata_df, on="app_id", how="inner")

merged_df.info()
merged_df.head()

merged_df.to_csv("data/games_merged.csv", index=False)