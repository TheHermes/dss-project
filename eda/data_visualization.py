import pandas as pd
import matplotlib.pyplot as plt
import ast
from collections import Counter

# AI has been used to assist in creation of these visualizations

users = pd.read_csv("data/users_1000.csv")
games = pd.read_csv("data/games_merged.csv")
recommendations = pd.read_csv("data/recommendations_1000.csv")

games["date_release"] = pd.to_datetime(games["date_release"])
recommendations["date"] = pd.to_datetime(recommendations["date"])


plt.figure(figsize=(15, 6))
games["date_release"].dt.year.value_counts().sort_index().plot(kind="line", marker="o")
plt.title("Antal spel släppta per år")
plt.xlabel("År")
plt.ylabel("Antal spel")
plt.grid(alpha=0.3)
plt.tight_layout()

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

plt.figure(figsize=(12, 6))
games["rating"].value_counts().sort_values(ascending=True).plot(kind="bar", color="#6a5acd")
plt.title("Distribution av spelbetyg")
plt.xlabel("Betyg")
plt.ylabel("Antal")
plt.xticks(rotation=45)
plt.tight_layout()

# Hur mångs recensioner finns det i vårt skapade dataset
review_counts = (
    recommendations["app_id"]
    .value_counts()
    .head(10)
    .rename_axis("app_id")
    .reset_index(name="review_count")
)

top_reviewed = review_counts.merge(
    games[["app_id", "title"]],
    on="app_id",
    how="left"
)

plt.figure(figsize=(14, 6))
plt.barh(top_reviewed["title"], top_reviewed["review_count"], color="#20b2aa")
plt.title("Topp 10 mest recenserade spel i vårt unika dataset")
plt.xlabel("Antal recensioner")
plt.ylabel("Spel")
plt.gca().invert_yaxis()
plt.tight_layout()

# Hur många finns det egentligen på steam
top_games = games.nlargest(10, "user_reviews")
plt.figure(figsize=(12, 6))
plt.barh(top_games["title"], top_games["user_reviews"], color="#20b2aa")
plt.title("Top 10 mest recenserade spel finns det totalt på steam")
plt.xlabel("Antal recensioner")
plt.ylabel("Spel")
plt.gca().invert_yaxis()
plt.tight_layout()

tag_counts = Counter(
    tag
    for tags_str in games["tags"].dropna()
    for tag in ast.literal_eval(tags_str)
)
plt.figure(figsize=(12, 6))
pd.Series(tag_counts).nlargest(10).plot(kind="barh", color="#ff69b4")
plt.title("Top 20 vanligaste tag")
plt.xlabel("Antal")
plt.tight_layout()

plt.show()