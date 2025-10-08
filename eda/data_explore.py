import pandas as pd

users_df = pd.read_csv('data/users_trimmed.csv')
games_df = pd.read_csv('data/games_merged.csv')
recommendations_df = pd.read_csv("data/recommendations_trimmed.csv")

print(users_df.head())
print(games_df.head())
print(recommendations_df.head())

# Basic information about datasets
print("\nTrimmed Users Dataset Info:")
print(users_df.info())
print("\nGames Dataset Info:")
print(games_df.info())
print("\nTrimmed Recommendations Dataset Info:")
print(recommendations_df.info())

# Check for missing values
print("\nMissing Values:")
print("Users Dataset:\n", users_df.isnull().sum())
print("\nGames Dataset:\n", games_df.isnull().sum())
print("\nRecommendations Dataset:\n", recommendations_df.isnull().sum())

