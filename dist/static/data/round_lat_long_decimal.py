import pandas as pd

CLEAN_FILE_NAME_LIST = ["taxi_sort_001_clean"]
CLEAN_FILE_SUFFIX_LIST= [".csv" for _ in range(len(CLEAN_FILE_NAME_LIST))]

for clean_file_name, clean_file_suffix in zip(CLEAN_FILE_NAME_LIST, CLEAN_FILE_SUFFIX_LIST):
    df = pd.read_csv(clean_file_name + clean_file_suffix, index_col=False)

    df["lat"] = df["lat"].round(4)
    df["long"] = df["long"].round(4)

    df.to_csv(clean_file_name + "_round" + clean_file_suffix, index=False)