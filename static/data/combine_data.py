import pandas as pd
import numpy as np

CRIMINAL_DATA = "./criminal_precinct.csv"
TAXIS_DATA = "./taxi_sort_001_precinct.csv"

df1 = pd.read_csv(CRIMINAL_DATA, index_col=False)
df2 = pd.read_csv(TAXIS_DATA, index_col=False)

new_df = df2.groupby(["weekday", "pick_hour", "precinct"])["sum"].sum()

new_df.to_csv("tmp.csv")

new_df = pd.read_csv("tmp.csv", index_col=False)
new_df.columns = ["day", "hour", "precinct", "sum"]

final_df = pd.merge(df1, new_df, on=['day','hour', 'precinct'], how = 'inner')

final_df = final_df.drop(["Unnamed: 0"], axis=1)

final_df.columns = ["day", "hour", "precinct", "criminal", "traffic"]

all_precinct = set([ 44,103,28,105,13,71,7,46,48,19,41,14,67,17,61,102,110,108,75,73,60,68,79,23,42,115,52,122,72,109,24,81,90,112,43,84,47,77,101,83,113,120,70,69,66,114,76,63,45,106,10,78,6,5,94,40,34,32,50,25,100,18,20,111,107,30,49,88,26,123,9,104,33,62,22,1])

final_day_arr = []
final_hour_arr = []
final_precinct_arr = []
final_criminal_arr = []
final_traffic_arr = []
round_called_precinct = set()
prev_hour = 0
prev_day = 0
for idx, row in final_df.iterrows():
    curr_hour = row["hour"]
    curr_day = row["day"]

    if(prev_hour != curr_hour):
        diff_vals = list(all_precinct.difference(round_called_precinct))
        print(prev_day, prev_hour, diff_vals, len(round_called_precinct))
        for diff_val in diff_vals:
            final_day_arr.append(prev_day)
            final_hour_arr.append(prev_hour)
            final_precinct_arr.append(diff_val)
            final_criminal_arr.append(10)
            final_traffic_arr.append(1000)
        
        round_called_precinct = set([])
        prev_hour = curr_hour
        if(prev_day != curr_day):
            prev_day = curr_day

    final_day_arr.append(curr_day)
    final_hour_arr.append(curr_hour)
    final_precinct_arr.append(row["precinct"])
    final_criminal_arr.append(row["criminal"])
    final_traffic_arr.append(row["traffic"])
    round_called_precinct.add(row["precinct"])

final_day_se = pd.Series(final_day_arr)
final_hour_se = pd.Series(final_hour_arr)
final_precinct_se = pd.Series(final_precinct_arr)
final_criminal_se = pd.Series(final_criminal_arr)
final_traffic_se = pd.Series(final_traffic_arr)

final_df["day"] = final_day_se
final_df["hour"] = final_hour_se
final_df["precinct"] = final_precinct_se
final_df["criminal"] = final_criminal_se
final_df["traffic"] = final_traffic_se

final_df.to_csv("combine_precinct.csv", index=False)