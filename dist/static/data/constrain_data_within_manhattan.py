import pandas as pd
import numpy as np
import json
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

with open('./police_precincts.geojson') as f:
    data = json.load(f)

CLEAN_FILE_NAME_LIST = ["taxi_sort_01", "taxi_sort_001", "taxi_sort_002", "taxi_sort_003", "taxi_sort_004", "taxi_sort_005", "taxi_sort_006", "taxi_sort_007", "taxi_sort_008", "taxi_sort_009", "taxi_sort_0006", "taxi_sort_0007", "taxi_sort_0008", "taxi_sort_0009", "criminal_lat_long_01", "criminal_lat_long_001", "criminal_lat_long_002", "criminal_lat_long_003", "criminal_lat_long_004", "criminal_lat_long_005", "criminal_lat_long_006", "criminal_lat_long_007", "criminal_lat_long_008", "criminal_lat_long_009"]
CLEAN_FILE_SUFFIX_LIST= [".csv" for _ in range(len(CLEAN_FILE_NAME_LIST))]

for clean_file_name, clean_file_suffix in zip(CLEAN_FILE_NAME_LIST, CLEAN_FILE_SUFFIX_LIST):
    df = pd.read_csv(clean_file_name + clean_file_suffix, index_col=False)

    def checkIfPoint(long_point, lat_point):
        point = Point(long_point, lat_point)
        for feature in data['features']:
            # print (feature['geometry']['type'])
            # print (feature['geometry']['coordinates'])
            if(feature["geometry"]["type"] == "Polygon"):
                for polygons in feature['geometry']['coordinates']:
                    if(len(polygons) <= 4):
                        continue
                    try:
                        polygon_obj = Polygon(np.array(polygons))
                        if(point.within(polygon_obj) == True):
                            return True
                    except:
                        pass
                        # return True
            else:
                for multipolygons in feature['geometry']['coordinates']:
                    for polygons in multipolygons:
                        if(len(polygons) <= 4):
                            continue
                        try:
                            polygon_obj = Polygon(np.array(polygons))
                            if(point.within(polygon_obj) == True):
                                return True
                        except:
                            pass
                            #print(len(multipolygons))
                            #print(len(polygons))
                            # return True
        return False

    point_list = []
    for index, row in df.iterrows():
        if(index % 1000 == 0 or index == (len(df))):
            print("%d / %d"%(index + 1, len(df)))
        if(checkIfPoint(float(row["long"]), float(row["lat"])) == True):
            point_list.append(True)
        else:
            point_list.append(False)

    point_se = pd.Series(point_list)
    df["isWithin"] = point_se

    print("before_clean: ", len(df))
    df = df[df["isWithin"] == True]
    df = df.drop(["isWithin"], axis = 1)
    df["lat"] = df["lat"].round(4)
    df["long"] = df["long"].round(4)
    print("after_clean: ", len(df))
    df.to_csv(clean_file_name + "_clean" + clean_file_suffix, index=False)