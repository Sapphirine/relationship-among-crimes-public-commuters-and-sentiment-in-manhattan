import pandas as pd
import numpy as np
import json
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

with open('./police_precincts.geojson') as f:
    data = json.load(f)

df = pd.read_csv("criminal_lat_long_01.csv", index_col=False)

def checkIfPoint(long_point, lat_point):
    point = Point(long_point, lat_point)
    for feature in data['features']:
        # print (feature['geometry']['type'])
        # print (feature['geometry']['coordinates'])
        if(feature["geometry"]["type"] == "Polygon"):
            for polygons in feature['geometry']['coordinates']:
                polygon_obj = Polygon(np.array(polygons))
                try:
                    if(point.within(polygon_obj) == True):
                        return True
                except:
                    return True
        else:
            for multipolygons in feature['geometry']['coordinates']:
                for polygons in multipolygons:
                    polygon_obj = Polygon(np.array(polygons))
                    try:
                        if(point.within(polygon_obj) == True):
                            return True
                    except:
                        print(len(multipolygons))
                        print(len(polygons))
                        # return True
    return False

point_list = []
for index, row in df.iterrows():
    print("%d / %d"%(index, len(df)))
    if(checkIfPoint(float(row["long"]), float(row["lat"])) == True):
        point_list.append(True)
    else:
        point_list.append(False)

point_se = pd.Series(point_list)
df["isWithin"] = point_se

print(len(df))
df = df[df["isWithin"] == True]
print(len(df))
df.to_csv("criminal_lat_long_01_clean.csv", index=False)

# #lons_lats_vect = np.column_stack((lons_vect, lats_vect)) # Reshape coordinates
# polygon = Polygon(data["features"][0]['geometry']['coordinates'][0][0]) # create polygon
# point = Point(-74.046, 40.70) # create point
# print(polygon.contains(point)) # check if polygon contains point
# print(point.within(polygon)) # check if a point is in the polygon 
