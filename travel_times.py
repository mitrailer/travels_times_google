import googlemaps
import csv
from apikey import key

# load your api key
g_maps = googlemaps.Client(key=key)
# 1602144000
# 1589443200
def get_travel_time(o, d, mode):
    consult = g_maps.distance_matrix(o, d,
                                     mode=mode,
                                     language="en",
                                     region=".ca",
                                     units="metric",
                                     departure_time="1589443200",
                                     traffic_model="best_guess")
    if mode == "driving":
        try:
            t_time = consult["rows"][0]["elements"][0]["duration_in_traffic"]['value']
            dist = consult["rows"][0]["elements"][0]["distance"]['value']
        except:
            t_time = 0
            dist = 0
    else:
        try:
            t_time = consult["rows"][0]["elements"][0]["duration"]['value']
            dist = consult["rows"][0]["elements"][0]["distance"]['value']
        except:
            t_time = 0
            dist = 0
    # print(t_time,dist)
    return t_time, dist


with open('data/o-d.csv', 'r') as csvinput:
    with open('data/o-d_travel_times.csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvinput)
        all = []
        row = next(reader)
        row.append('Travel_Time(sec)')
        row.append('Distance(mts)')
        all.append(row)
        # send api code
        i = 0
        for row in reader:
            # The pair is (y,x) or (Lat,Long)
            origin = (row[1], row[0])
            destination = (row[3], row[2])
            travel_time, distance = get_travel_time(origin, destination, "driving")
            row.append(travel_time)
            row.append(distance)
            all.append(row)
            print(i)
            i += 1
        writer.writerows(all)
