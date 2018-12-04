import pandas as pd
import matplotlib.pyplot as plt

col = ["month", "hour", "precinct", "totalNumber"]
df = pd.read_csv("NYPD_crime_daily_aggregation.csv", index_col=None)

df = df[col]

for i in range(123):
    df_precinct = df[df["precinct"]==i]
    if(len(df_precinct) > 0):
        for j in range(13):
            month_df = df_precinct[df_precinct["month"]==j]
            x = month_df["hour"]
            y = month_df["totalNumber"]
            plt.figure()
            plt.plot(x, y)
            plt.show()

