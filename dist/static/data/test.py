import pandas as pd

df = pd.read_csv("combine_precinct_0006.csv", index_col=False)

print(df.head())

for idx, row in df.iterrows():
    traffic = row["traffic"]
    criminal = row["criminal"]

    if(traffic > 8000 and criminal < 200):
        df.loc[idx, "criminal"] += 100

    if(traffic > 500 and traffic <= 8000 and criminal < 150):
        df.loc[idx, "criminal"] += 50

df.to_csv("combine_precinct_0006_temp.csv", index=False)
