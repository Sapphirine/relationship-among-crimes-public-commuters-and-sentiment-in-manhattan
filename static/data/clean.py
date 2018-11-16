import pandas as pd

df = pd.read_csv("clean-summons-data.csv")

df = df[df["Violation"] == "CONSUMPTION OF ALCOHOL"]

df.to_csv("clean-summons-data.csv")