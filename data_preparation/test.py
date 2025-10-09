import pandas as pd


import matplotlib.pyplot as plt

rec_df = pd.read_csv("data/recommendations_stratified.csv")
user_df = pd.read_csv("data/users_stratified_sample.csv")

print(len(rec_df))
print(len(rec_df['user_id'].unique()))

print("USer df things")
print(len(user_df))
print(len(user_df["user_id"].unique()))

"""users_df = pd.read_csv("data/users.csv")
"""
"""plt.figure(figsize=(8,5))
plt.hist(rec_df["user_id"], bins=50, log=True, color="skyblue", edgecolor="black")
plt.title("Distribution of Number of Reviews per User")
plt.xlabel("Reviews per User")
plt.ylabel("Number of Users (log scale)")
plt.show()

plt.figure(figsize=(8,5))
plt.hist(user_df["user_id"], log=True, color="skyblue", edgecolor="black")
plt.title("Distribution of Number of Reviews per User")
plt.xlabel("Reviews per User")
plt.ylabel("Number of Users (log scale)")
plt.show()
"""