import matplotlib.pyplot as plt
import pandas as pd

users_df = pd.read_csv('data/users_trimmed.csv')
games_df = pd.read_csv('data/games_merged.csv')
recommendations_df = pd.read_csv("data/recommendations_trimmed.csv")

games_df['date_release'] = pd.to_datetime(games_df['date_release'])
recommendations_df['date'] = pd.to_datetime(recommendations_df['date'])

plt.figure(figsize=(15, 6))
games_df['date_release'].dt.year.value_counts().sort_index().plot(kind='line')
plt.title('Antal spel utsläppta per år')
plt.xlabel('År')
plt.ylabel('Antal Spel')

platforms = pd.DataFrame({
    'Windows': games_df['win'].sum(),
    'Mac': games_df['mac'].sum(),
    'Linux': games_df['linux'].sum()
}, index=[0]).T
plt.figure(figsize=(10, 6))
platforms.plot(kind='bar')
plt.title('Spel per platform')
plt.ylabel('Antal Spel')

plt.figure(figsize=(12, 6))
games_df['rating'].value_counts().plot(kind='bar')
plt.title('Distribution av spel betyg')
plt.xlabel('Betyg')
plt.ylabel('Antal')
plt.xticks(rotation=45)
plt.show()