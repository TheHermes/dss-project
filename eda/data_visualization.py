import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
users = pd.read_csv("data/users_1000.csv")
games = pd.read_csv("data/games_merged.csv")
recommendations = pd.read_csv("data/recommendations_1000.csv")

# Convert date columns to datetime
games["date_release"] = pd.to_datetime(games["date_release"])
recommendations["date"] = pd.to_datetime(recommendations["date"])

# Plot 1: Number of games released per year
plt.figure(figsize=(15, 6))
games["date_release"].dt.year.value_counts().sort_index().plot(kind="line", marker="o")
plt.title("Antal spel släppta per år")
plt.xlabel("År")
plt.ylabel("Antal spel")
plt.grid(alpha=0.3)
plt.tight_layout()

# Plot 2: Games per platform
platform_counts = pd.Series({
    "Windows": games["win"].sum(),
    "Mac": games["mac"].sum(),
    "Linux": games["linux"].sum()
})

plt.figure(figsize=(10, 6))
platform_counts.plot(kind="bar", color=["#1f77b4", "#ff7f0e", "#2ca02c"])
plt.title("Spel per plattform")
plt.ylabel("Antal spel")
plt.xticks(rotation=0)
plt.tight_layout()

# --- Plot 3: Distribution of game ratings ---
plt.figure(figsize=(12, 6))
#games["rating"].value_counts().sort_index().plot(kind="bar", color="#6a5acd")
games["rating"].value_counts().sort_values(ascending=False).plot(kind="bar", color="#6a5acd")
plt.title("Distribution av spelbetyg")
plt.xlabel("Betyg")
plt.ylabel("Antal")
plt.xticks(rotation=45)
plt.tight_layout()

# Plot 4: Most reviewed games (recommendations)
review_counts = (
    recommendations["app_id"]
    .value_counts()
    .head(10)
    .rename_axis("app_id")
    .reset_index(name="review_count")
)

# Merge with games to get readable game names
top_reviewed = review_counts.merge(
    games[["app_id", "title"]],
    on="app_id",
    how="left"
)

plt.figure(figsize=(14, 6))
plt.barh(top_reviewed["title"], top_reviewed["review_count"], color="#20b2aa")
plt.title("Topp 10 mest recenserade spel")
plt.xlabel("Antal recensioner")
plt.ylabel("Spel")
plt.gca().invert_yaxis()  # so the most reviewed appears on top
plt.tight_layout()

plt.show()