import pandas as pd

df = pd.read_csv('data/dataset.csv')

print("First 10 entries")
print(df.head(10))

print("\nShape")
print(df.shape)

print("\nColumns")
print(df.columns)

print("\nData Types")
print(df.dtypes)

print("\nInfo summary")
print(df.info())

print("\nDescribe")
print(df.describe())