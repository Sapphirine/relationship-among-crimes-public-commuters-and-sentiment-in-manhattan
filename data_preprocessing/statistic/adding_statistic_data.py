import pandas as pd

def crime_and_traffic():
    df = pd.read_csv("chart_plot_combine_precinct.csv", index_col=False)

    max_crime_arr = []
    min_crime_arr = []
    max_traffic_arr = []
    min_traffic_arr = []
    max_crime_time_arr = []
    min_crime_time_arr = []
    max_traffic_time_arr = []
    min_traffic_time_arr = []
    max_crime_change_arr = []
    max_traffic_change_arr = []

    crimeMap = {}
    trafficMap = {}
    prev_day = 0
    count = 0
    for idx, row in df.iterrows():
        curr_day = row["day"]
        curr_precinct = row["precinct"]
        if(curr_day != prev_day or idx == len(df) - 1):

            for day_iter_idx, day_row in df.iterrows():
                if(day_iter_idx == count):
                    break
                day_precinct = day_row["precinct"]
                max_crime = max(crimeMap[day_precinct])
                min_crime = min(crimeMap[day_precinct])
                max_crime_time = crimeMap[day_precinct].index(max_crime)
                min_crime_time = crimeMap[day_precinct].index(min_crime)
                max_crime_change = round(max_crime / min_crime, 2)

                max_traffic = max(trafficMap[day_precinct])
                min_traffic = min(trafficMap[day_precinct])
                max_traffic_time = trafficMap[day_precinct].index(max_traffic)
                min_traffic_time = trafficMap[day_precinct].index(min_traffic)
                max_traffic_change = round(max_traffic / min_traffic, 2)

                max_crime_arr.append(max_crime)
                min_crime_arr.append(min_crime)
                max_traffic_arr.append(max_traffic)
                min_traffic_arr.append(min_traffic)
                max_crime_time_arr.append(max_crime_time)
                min_crime_time_arr.append(min_crime_time)
                max_traffic_time_arr.append(max_traffic_time)
                min_traffic_time_arr.append(min_traffic_time)
                max_crime_change_arr.append(max_crime_change)
                max_traffic_change_arr.append(max_traffic_change)

            prev_day = curr_day
            count = 1
            crimeMap = {}
            trafficMap = {}
        else:
            count += 1
            if(curr_precinct not in crimeMap):
                crimeMap[curr_precinct] = [row["criminal"]]
            else:
                crimeMap[curr_precinct].append(row["criminal"])
            if(curr_precinct not in trafficMap):
                trafficMap[curr_precinct] = [row["traffic"]]
            else:
                trafficMap[curr_precinct].append(row["traffic"])

    max_crime_se = pd.Series(max_crime_arr)
    min_crime_se = pd.Series(min_crime_arr)
    max_traffic_se =  pd.Series(max_traffic_arr)
    min_traffic_se =  pd.Series(min_traffic_arr)
    max_crime_time_se =  pd.Series(max_crime_time_arr)
    min_crime_time_se =  pd.Series(min_crime_time_arr)
    max_traffic_time_se =  pd.Series(max_traffic_time_arr)
    min_traffic_time_se =  pd.Series(min_traffic_time_arr)
    max_crime_change_se =  pd.Series(max_crime_change_arr)
    max_traffic_change_se =  pd.Series(max_traffic_change_arr)

    df["max_crime"] = max_crime_se
    df["min_crime"] = min_crime_se
    df["max_traffic"] = max_traffic_se
    df["min_traffic"] = min_traffic_se
    df["max_crime_time"] = max_crime_time_se
    df["min_crime_time"] = min_crime_time_se
    df["max_traffic_time"] = max_traffic_time_se
    df["min_traffic_time"] = min_traffic_time_se
    df["max_crime_change"] = max_crime_change_se
    df["max_traffic_change"] = max_traffic_change_se

    df.to_csv("statistic_crime_and_traffic.csv", index=False)

def sentiment_data():
    df = pd.read_csv("sentiment_number.csv", index_col=False)
    df = df.drop(["neutral"], axis=1)
    total_se = df["positive"] + df["negative"]
    df["positive"] = (df["positive"] / total_se * 100).round(2)
    df["negative"] = 100 - df["positive"]

    max_positive_arr = []
    min_positive_arr = []
    max_positive_time_arr = []
    min_positive_time_arr = []
    max_positive_change_arr = []

    positive = []
    negative = []
    prev_day = 0
    count = 0
    for idx, row in df.iterrows():
        curr_day = row["day"]
        if(curr_day != prev_day or idx == len(df) - 1):
            for day_iter_idx, day_row in df.iterrows():
                if(day_iter_idx == count):
                    break
                max_positive = max(positive)
                min_positive = min(positive)
                max_positive_time = positive.index(max_positive)
                min_positive_time = positive.index(min_positive)
                max_positive_change = round(max_positive / min_positive, 2)

                max_positive_arr.append(max_positive)
                min_positive_arr.append(min_positive)
                max_positive_time_arr.append(max_positive_time)
                min_positive_time_arr.append(min_positive_time)
                max_positive_change_arr.append(max_positive_change)

            prev_day = curr_day
            count = 1
            positive = []
            negative = []
        else:
            count += 1
            positive.append(row["positive"])
            negative.append(row["negative"])

    max_positive_se = pd.Series(max_positive_arr)
    min_positive_se = pd.Series(min_positive_arr)
    max_positive_time_se =  pd.Series(max_positive_time_arr)
    min_positive_time_se =  pd.Series(min_positive_time_arr)
    max_positive_change_se =  pd.Series(max_positive_change_arr)


    df["max_positive"] = max_positive_se
    df["min_positive"] = min_positive_se
    df["max_positive_time"] = max_positive_time_se
    df["min_positive_time"] = min_positive_time_se
    df["max_positive_change"] = max_positive_change_se

    df.to_csv("statistic_sentiment.csv", index=False)

def correlation():
    df = pd.read_csv("chart_plot_combine_precinct.csv", index_col=False)

    pearson_corr = []
    kendall_corr = []
    spearman_corr = []
    day_arr = []
    hour_arr = []

    max_pearson_val_arr = []
    max_pearson_time_arr = []
    min_pearson_val_arr = []
    min_pearson_time_arr = []
    
    max_kendall_val_arr = []
    max_kendall_time_arr = []
    min_kendall_val_arr = []
    min_kendall_time_arr = []
    
    max_spearman_val_arr = []
    max_spearman_time_arr = []
    min_spearman_val_arr = []
    min_spearman_time_arr = []

    for day in range(7):
        for hour in range(24):
            day_hour_se = df[(df["day"] == day) & (df["hour"] == hour)][["criminal", "traffic"]]

            pearson = day_hour_se.corr(method='pearson', min_periods=1)["criminal"]["traffic"]
            kendall = day_hour_se.corr(method='kendall', min_periods=1)["criminal"]["traffic"]
            spearman = day_hour_se.corr(method='spearman', min_periods=1)["criminal"]["traffic"]

            pearson_corr.append(pearson)
            kendall_corr.append(kendall)
            spearman_corr.append(spearman)
            day_arr.append(day)
            hour_arr.append(hour)
        
        max_pearson = max(pearson_corr)
        max_pearson_time = pearson_corr.index(max_pearson)
        min_pearson = min(pearson_corr)
        min_pearson_time = pearson_corr.index(min_pearson)
        
        max_kendall = max(kendall_corr)
        max_kendall_time = kendall_corr.index(max_kendall)
        min_kendall = min(kendall_corr)
        min_kendall_time = kendall_corr.index(min_kendall)
        
        max_spearman = max(spearman_corr)
        max_spearman_time = spearman_corr.index(max_spearman)
        min_spearman = min(spearman_corr)
        min_spearman_time = spearman_corr.index(min_spearman)

        for _ in range((24)):
            max_pearson_val_arr.append(max_pearson)
            max_pearson_time_arr.append(max_pearson_time)
            min_pearson_val_arr.append(min_pearson)
            min_pearson_time_arr.append(min_pearson_time)

            max_kendall_val_arr.append(max_kendall)
            max_kendall_time_arr.append(max_kendall_time)
            min_kendall_val_arr.append(min_kendall)
            min_kendall_time_arr.append(min_kendall_time)

            max_spearman_val_arr.append(max_spearman)
            max_spearman_time_arr.append(max_spearman_time)
            min_spearman_val_arr.append(min_spearman)
            min_spearman_time_arr.append(min_spearman_time)
    
    day_se = pd.Series(day_arr)
    hour_se = pd.Series(hour_arr)
    pearson_corr_se = pd.Series(pearson_corr)
    kendall_corr_se = pd.Series(kendall_corr)
    spearman_corr_se = pd.Series(spearman_corr)

    max_pearson_val_se = pd.Series(max_pearson_val_arr)
    max_pearson_time_se = pd.Series(max_pearson_time_arr)
    min_pearson_val_se = pd.Series(min_pearson_val_arr)
    min_pearson_time_se = pd.Series(min_pearson_time_arr)

    max_kendall_val_se = pd.Series(max_kendall_val_arr)
    max_kendall_time_se = pd.Series(max_kendall_time_arr)
    min_kendall_val_se = pd.Series(min_kendall_val_arr)
    min_kendall_time_se = pd.Series(min_kendall_time_arr)

    max_spearman_val_se = pd.Series(max_spearman_val_arr)
    max_spearman_time_se = pd.Series(max_spearman_time_arr)
    min_spearman_val_se = pd.Series(min_spearman_val_arr)
    min_spearman_time_se = pd.Series(min_spearman_time_arr)

    new_df = pd.DataFrame()
    new_df["day"] = day_se
    new_df["hour"] = hour_se
    new_df["pearson"] = pearson_corr_se
    new_df["kendall"] = kendall_corr_se
    new_df["spearman"] = spearman_corr_se

    new_df["max_pearson_val"] = max_pearson_val_se
    new_df["max_pearson_time"] = max_pearson_time_se
    new_df["min_pearson_val"] = min_pearson_val_se
    new_df["min_pearson_time"] = min_pearson_time_se

    new_df["max_kendall_val"] = max_kendall_val_se
    new_df["max_kendall_time"] = max_kendall_time_se
    new_df["min_kendall_val"] = min_kendall_val_se
    new_df["min_kendall_time"] = min_kendall_time_se

    new_df["max_spearman_val"] = max_spearman_val_se
    new_df["max_spearman_time"] = max_spearman_time_se
    new_df["min_spearman_val"] = min_spearman_val_se
    new_df["min_spearman_time"] = min_spearman_time_se

    new_df["pearson"] = new_df["pearson"].round(2)
    new_df["kendall"] = new_df["kendall"].round(2)
    new_df["spearman"] = new_df["spearman"].round(2)

    new_df["max_pearson_val"] =  new_df["max_pearson_val"] .round(2)
    new_df["max_pearson_time"] = new_df["max_pearson_time"].round(2)
    new_df["min_pearson_val"] =  new_df["min_pearson_val"] .round(2)
    new_df["min_pearson_time"] = new_df["min_pearson_time"].round(2)

    new_df["max_kendall_val"] = new_df["max_kendall_val"].round(2)
    new_df["max_kendall_time"] =new_df["max_kendall_time"].round(2)
    new_df["min_kendall_val"] = new_df["min_kendall_val"].round(2)
    new_df["min_kendall_time"] =new_df["min_kendall_time"].round(2)

    new_df["max_spearman_val"] =     new_df["max_spearman_val"] .round(2)
    new_df["max_spearman_time"] =    new_df["max_spearman_time"].round(2)
    new_df["min_spearman_val"] =     new_df["min_spearman_val"] .round(2)
    new_df["min_spearman_time"] =    new_df["min_spearman_time"].round(2)

    new_df.to_csv("statistic_correlation.csv", index=False)

if __name__ == "__main__":
    # crime_and_traffic()
    # sentiment_data()
    correlation()