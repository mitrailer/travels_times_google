import googlemaps
import csv
from apikey import key

# B - Public Transit (excluding GO Rail)
# C - Bicycle
# D - Auto Driver
# S - School Bus
# T -Taxi
# W -Walk
g_maps = googlemaps.Client(key=key)


def get_travel_time(o, d, mode):
    consult = g_maps.distance_matrix(o, d,
                                     mode=mode,
                                     language="en",
                                     region=".ca",
                                     units="metric",
                                     departure_time="1562140800",
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


with open('Coordinates_Oakville_Johannes.csv', 'r') as csvinput:
    with open('Oakville_trips_tt_and_d.csv', 'w') as csvoutput:
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
            # ID,origY,origX,destY,destX
            # print(row[0])
            origin = (row[1], row[2])
            destination = (row[3], row[4])
            if row[0] == "D" or row[0] == "S" or row[0] == "T":
                travel_time, distance = get_travel_time(origin, destination, "driving")
            if row[0] == "C":
                travel_time, distance = get_travel_time(origin, destination, "bicycling")
            if row[0] == "B":
                travel_time, distance = get_travel_time(origin, destination, "transit")
            if row[0] == "W":
                travel_time, distance = get_travel_time(origin, destination, "walking")
            row.append(travel_time)
            row.append(distance)
            all.append(row)
            print(i)
            i += 1

        writer.writerows(all)
