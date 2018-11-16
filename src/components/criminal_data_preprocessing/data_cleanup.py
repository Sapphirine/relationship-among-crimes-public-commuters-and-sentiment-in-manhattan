import numpy as np;
import pandas as pd;
import datetime;

def ori_groupby_date():
    df = pd.read_csv("NYPD_Complaint_Data_Historic.csv")
    df = df.dropna(subset=['ADDR_PCT_CD', 'CMPLNT_FR_DT', "LAW_CAT_CD"])
    dataMap = {}

    # ADDR_PCT_CD
    # CMPLNT_FR_DT
    # LAW_CAT_CD
    precinctList = [int(precinct) for precinct in list(df.ADDR_PCT_CD.unique())]
    hoursList = [str(index) for index in range(24)]

    for idx, row in df.iterrows():
        
        if(row["CMPLNT_FR_DT"] not in dataMap):
            datetimeObj = datetime.datetime.strptime(row["CMPLNT_FR_DT"], '%m/%d/%Y')
            #if(datetimeObj.year != 2015 and datetimeObj.year != 2014):
            #    continue
            dataMap[row["CMPLNT_FR_DT"]] = {}
            for hour in hoursList:
                dataMap[row["CMPLNT_FR_DT"]][hour] = {}
                for precintNum in precinctList:
                    dataMap[row["CMPLNT_FR_DT"]][hour][precintNum] = {}
                    dataMap[row["CMPLNT_FR_DT"]][hour][precintNum]["totalNumber"] = 0
                    dataMap[row["CMPLNT_FR_DT"]][hour][precintNum]["felony"] = 0
                    dataMap[row["CMPLNT_FR_DT"]][hour][precintNum]["misdemeanor"] = 0
                    dataMap[row["CMPLNT_FR_DT"]][hour][precintNum]["violation"] = 0
        
        currHour = row["CMPLNT_FR_TM"][:row["CMPLNT_FR_TM"].find(":")]
        precinct = int(row["ADDR_PCT_CD"])
        dataMap[row["CMPLNT_FR_DT"]][currHour][precinct]["totalNumber"] += 1
        if(row["LAW_CAT_CD"] == "FELONY"):
            dataMap[row["CMPLNT_FR_DT"]][currHour][precinct]["felony"] += 1
        elif(row["LAW_CAT_CD"] == "MISDEMEANOR"):
            dataMap[row["CMPLNT_FR_DT"]][currHour][precinct]["misdemeanor"] += 1
        elif(row["LAW_CAT_CD"] == "VIOLATION"):
            dataMap[row["CMPLNT_FR_DT"]][currHour][precinct]["violation"] += 1
        else:
            continue

    col = ["datetime", "time", "precinct", "totalNumber", "felony", "misdemeanor", "violation"] 
    newDf = pd.DataFrame(columns=col)

    tmpDict = {}
    for key1, value1 in dataMap.items():
        for key2, value2 in value1.items():
            for key3, value3 in value2.items():
                tmpDict[len(tmpDict)] = [key1, key2, key3, value3["totalNumber"], value3["felony"],
                                        value3["misdemeanor"], value3["violation"]]
    tmpDf = pd.DataFrame.from_dict(tmpDict, orient='index')
    tmpDf.columns = ["datetime", "time", "precinct", "totalNumber", "felony", "misdemeanor", "violation"]
    newDf = newDf.append(tmpDf, ignore_index=True)


    newDf.to_csv("NYPD_crime_group_by_date.csv", index=False, columns=["datetime", "precinct", "totalNumber", "felony", "misdemeanor", "violation"])

def group_by_date_to_daily_aggregation():
    df = pd.read_csv("NYPD_crime_group_by_date.csv")
    dailyMap = {}

    for i in range(1, 13):
        dailyMap[i] = {}
        for j in range(24):
            dailyMap[i][j] = {}

    for idx, row in df.iterrows():
        datetimeObj = datetime.datetime.strptime(row["datetime"], '%m/%d/%Y')
        currMonth = datetimeObj.month
        currHour = int(row["time"])
        precinct = int(row["precinct"])
        if(precinct not in dailyMap[currMonth][currHour]):
            dailyMap[currMonth][currHour][precinct] = {}
            dailyMap[currMonth][currHour][precinct]["totalNumber"] = 0
            dailyMap[currMonth][currHour][precinct]["felony"] = 0
            dailyMap[currMonth][currHour][precinct]["misdemeanor"] = 0
            dailyMap[currMonth][currHour][precinct]["violation"] = 0

        dailyMap[currMonth][currHour][precinct]["totalNumber"] += row["totalNumber"]
        dailyMap[currMonth][currHour][precinct]["felony"] += row["felony"]
        dailyMap[currMonth][currHour][precinct]["misdemeanor"] += row["misdemeanor"]
        dailyMap[currMonth][currHour][precinct]["violation"] += row["violation"]

    tmpMap = {}
    for key1, value1 in dailyMap.items():
        for key2, value2 in value1.items():
            for key3, value3 in value2.items():
                tmpMap[len(tmpMap)] = {
                    "month": key1, "hour": key2, "precinct": key3,
                    "totalNumber": value3["totalNumber"], "felony": value3["felony"],
                    "misdemeanor": value3["misdemeanor"], "violation": value3["violation"],
                    }
    newDf = pd.DataFrame.from_dict(tmpMap, orient="index")
    newDf.columns = ["month", "hour", "precinct", "totalNumber", "felony", "misdemeanor", "violation"]  
    newDf.to_csv("NYPD_crime_daily_aggregation.csv", columns=["month", "hour", "precinct", "totalNumber", "felony", "misdemeanor", "violation"])

if __name__ == "__main__":
    #ori_groupby_date()
    group_by_date_to_daily_aggregation()