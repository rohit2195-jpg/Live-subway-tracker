import time
from datetime import datetime, timedelta
from datetime import date
from warnings import catch_warnings

from geopy.distance import geodesic



class Train:
    def __init__(self, trip_id, arrival,remaining_stops, remaining_stop_times, delay, vehicleID, stopID_to_location, tripID_to_shapeID, storage_path):
        self.trip_id = trip_id

        self.arrival = arrival
        self.remaining_stops = remaining_stops
        self.remaining_stop_times = remaining_stop_times
        self.delay = delay

        self.validTrain = True
        self.departure_time = 0
        self.vehicleID = vehicleID
        self.stopID_to_location = stopID_to_location
        self.tripID_to_shapeID = tripID_to_shapeID
        self.progress_ratio = 0
        self.storage_apth = storage_path

    def update_progress(self):
        current_time = time.time()
        self.departure_time = self.findDepartureTime()
        if(self.departure_time == 0):
            self.validTrain = False
            return True
        adjusted_departure = self.departure_time
        adjusted_arrival = self.arrival
        try:
            total_time = adjusted_arrival - adjusted_departure

            elapsed_time = current_time - adjusted_departure
            self.progress_ratio = elapsed_time / total_time
        except:
            self.validTrain = False



        if current_time > adjusted_arrival:
            self.progress_ratio = 1  # Train has arrived
            return self.update_station()

        elif current_time < adjusted_departure:
            self.progress_ratio = 0  # Train hasn’t departed yet
            return True
        else:
            # Calculate progress ratio


            '''
            print(self.trip_id, adjusted_departure, adjusted_arrival, sep="\t")
            print(self.remaining_stops)
            print(self.remaining_stop_times)
            print("current tiime" +  str(current_time))
            print("progress" + str(self.progress_ratio))
            '''


            return True
    def update_station(self):
        current_time = time.time()


        if(len(self.remaining_stop_times) > 1):

            if(self.remaining_stop_times[0]  == self.remaining_stop_times[1]):
                self.past_station = self.remaining_stops[0][0:3]
                self.remaining_stops.pop(0)
                self.remaining_stop_times.pop(0)
                self.arrival = self.remaining_stop_times[0]
            else:



                self.past_station = self.remaining_stops[0][0:3]
                self.remaining_stops.pop(0)
                self.departure_time = self.remaining_stop_times.pop(0)
                self.arrival = self.remaining_stop_times[0]

            try:
                total_time = self.arrival - self.departure_time
                elapsed_time = current_time - self.departure_time
                self.progress_ratio = elapsed_time / total_time
            except:
                print("figure out why thisi is happning")

            '''
            print(self.trip_id, self.departure_time, self.arrival, sep="\t")
            print(self.remaining_stops)
            print(self.remaining_stop_times)
            print("current tiime" + str(current_time))
            print("updated_ progress" + str(self.progress_ratio))
            '''

            return True
        return False



    def findDepartureTime(self):
        estimateddeparture = 0
        backup_departure = 0
        backup_tripID = self.trip_id[0:self.trip_id.index(".")]
        stop_times = open("/Users/rohitsattuluri/PycharmProjects/wallpaper/gtfs_subway/stop_times.txt", "r")
        contents = stop_times.readlines()
        for i in range(1, len(contents)):
            line = contents[i].split(",")
            prev_line = contents[i-1].split(",")
            ##get departure time in different way, not with stop_list but with stopsequence on stop_times.txt


            if (self.trip_id in line[0] and line[1] == (self.remaining_stops[0])):
                estimateddeparture = prev_line[3]
                self.past_station = prev_line[1]
                break
            if(backup_tripID in line[0] and line[1] == (self.remaining_stops[0])):
                backup_departure = prev_line[3]
                self.past_station = prev_line[1]


        if(estimateddeparture == 0):
            estimateddeparture = backup_departure
        if(estimateddeparture == 0 and backup_departure == 0):
            self.validTrain = False

        try:
            date_str = date.today()

            estimateddeparture = datetime.strptime(f"{date_str} {estimateddeparture}", "%Y-%m-%d %H:%M:%S")
            estimateddeparture = int(estimateddeparture.timestamp())
        except ValueError:
            estimateddeparture = 0


        return estimateddeparture

    def getProgress(self):

        return self.progress_ratio
    def getShapeID(self, tripID_to_shapeID):
        shape_id = "example"
        trip_id_backup = self.trip_id[0: self.trip_id.index(".")]
        shape_id_backup=""
        for key in tripID_to_shapeID:
            if (self.trip_id in key):
                shape_id = tripID_to_shapeID[key].strip()
                break
            if(trip_id_backup in key):
                shape_id_backup = tripID_to_shapeID[key].strip()
        if(shape_id == "example"):
            shape_id = shape_id_backup
        return shape_id

    def estimatedPosition(self):

        shape_id = self.getShapeID(self.tripID_to_shapeID)
        shapes = open("/Users/rohitsattuluri/PycharmProjects/wallpaper/gtfs_subway/shapes.txt", "r")
        shape_lines = shapes.readlines()

        route_path = []
        try:
            location_prev = self.stopID_to_location[self.past_station]
            location_front = self.stopID_to_location[self.remaining_stops[0]]

            for line in shape_lines:
                l = line.split(",")
                if (l[0] == shape_id):
                    route_path.append(line)

            start_line = self.getNearestPoint(location_prev.split(",")[0], location_prev.split(",")[1], route_path)
            end_line = self.getNearestPoint(location_front.split(",")[0], location_front.split(",")[1], route_path)
        except:
            self.validTrain = False
            return [0,0]

        path_to_stop = []
        inbetween = False
        for line in route_path:
            l = line.split(",")
            if(line == start_line):
                inbetween = True
            elif(line == end_line):
                inbetween = False
                path_to_stop.append(l[2]+","+l[3])
            if(inbetween):
                path_to_stop.append(l[2]+","+l[3])

        cumulative_distance = [0]
        total_distance = 0

        for i in range(1, len(path_to_stop)):
            point1 = (path_to_stop[i-1].split(",")[0], path_to_stop[i-1].split(",")[1])
            point2 = (path_to_stop[i].split(",")[0], path_to_stop[i].split(",")[1])

            distance = geodesic(point1, point2).meters
            total_distance += distance
            cumulative_distance.append(total_distance)


        target_distance = self.progress_ratio * total_distance

        for i in range(1, len(cumulative_distance)):
            if cumulative_distance[i - 1] <= target_distance <= cumulative_distance[i]:
                # Calculate the ratio between the two points based on distance
                segment_ratio = (target_distance - cumulative_distance[i - 1]) / (cumulative_distance[i] - cumulative_distance[i - 1])

                lat1, lon1 = float(path_to_stop[i - 1].split(",")[0]), float(path_to_stop[i - 1].split(",")[1].strip())
                lat2, lon2 = float(path_to_stop[i].split(",")[0]), float(path_to_stop[i].split(",")[1].strip())

                # Interpolate lat and lon
                lat = lat1 + segment_ratio * (lat2 - lat1)
                lon = lon1 + segment_ratio * (lon2 - lon1)

                return [lat, lon]

        if(len(path_to_stop) == 0):
            self.validTrain = False
            return [0,0]
        return [float(path_to_stop[-1].split(",")[0].strip()), float(path_to_stop[-1].split(",")[1].strip())]




    def getNearestPoint(self, lat, long, route_path):
        min_distance = float('inf')
        nearest_point_line = None
        for point in route_path:
            line = point.split(",")
            point_coords = (line[2], line[3])
            stop_coords = (lat, long)
            distance = geodesic(stop_coords, point_coords).meters  # Calculate distance in meters
            if distance < min_distance:
                min_distance = distance
                nearest_point_line = point
        return nearest_point_line





