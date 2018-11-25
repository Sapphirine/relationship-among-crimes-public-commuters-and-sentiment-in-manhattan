import pandas as pd
import numpy as np
import json

PROCESS_FILE_NAME_LIST = ["taxi_sort_001"]
PROCESS_FILE_SUFFIX_LIST  = [".csv" for _ in range(len(PROCESS_FILE_NAME_LIST))]

for process_file_name, process_file_suffix in zip(PROCESS_FILE_NAME_LIST, PROCESS_FILE_SUFFIX_LIST):
    df = pd.read_csv(process_file_name + process_file_suffix, index_col=False)
    df_precinct_center = pd.read_csv("precinct_center.csv", index_col=False)

    precinct_list = []
    for idx1, row1 in df.iterrows():
        if(idx1 % 1000 == 0 or idx1 == len(df)):
            print("%d / %d"%(idx1 + 1, len(df)))
        lat1 = row1["lat"]
        long1 = row1["long"]
        min_dis = float("inf")
        min_precinct = 0
        for idx2, row2 in df_precinct_center.iterrows():
            precinct = row2["precinct"]
            lat2 = row2["lat"]
            long2 = row2["long"]
            dis = (lat1 - lat2) ** 2 + (long1 - long2) ** 2
            if(dis < min_dis):
                min_dis = dis
                min_precinct = precinct

        precinct_list.append(min_precinct)

    precinct_se = pd.Series(precinct_list)
    df["precinct"] = precinct_se
    
    df = df.drop(["lat", "long"], axis=1)

    df.to_csv(process_file_name + "_precinct" + process_file_suffix, index=False)
