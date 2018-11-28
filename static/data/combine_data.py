import pandas as pd
import numpy as np

CRIMINAL_DATA = "./combine_precinct.csv"
TAXIS_DATA = "./taxi_sort_001_precinct.csv"

df1 = pd.read_csv(CRIMINAL_DATA, index_col=False)
df2 = pd.read_csv(TAXIS_DATA, index_col=False)

new_df = df2.groupby(["weekday", "pick_hour", "precinct"])["sum"].sum()

# agg_list = []
# for d in range(7):
#     for h in range(24):
#         val = df2[df2["weekday" == d] & df2["pick_hour" == h]]["sum"]
#         agg_list

new_df.to_csv("tmp.csv")

new_df = pd.read_csv("tmp.csv", index_col=False)
new_df.columns = ["day", "hour", "precinct", "sum"]

newnew_df = pd.merge(df1, new_df, on=['day','hour', 'precinct'],  how = 'inner')

newnew_df = newnew_df.drop(["Unnamed: 0"], axis=1)

newnew_df.columns = ["day", "hour", "precinct", "criminal", "traffic"]

newnew_df.to_csv("combine_precinct.csv", index=False)