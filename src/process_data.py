import pandas as pd

df = pd.read_csv("data/raw/crimedata_csv_AllNeighbourhoods_AllYears.csv")

df = df[df["YEAR"] >= 2003][df["YEAR"] <= 2022]
df = df.groupby(["YEAR", "NEIGHBOURHOOD", "TYPE"]).size().reset_index()
df = df.rename(columns={
               'YEAR': 'year', 'NEIGHBOURHOOD': 'neighbourhood', 'TYPE': 'type', 0: 'count'})
df = df.reset_index(drop=True)

df.to_csv("data/processed/crimedata_aggregated.csv", index=False)
