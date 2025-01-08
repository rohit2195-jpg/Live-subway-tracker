import time

from Main import progress_ratio


class Train:
    def __init__(self, trip_id, departure, arrival,remaining_stops, remaining_stop_times, delay, past_station, initial_progress, shape_id):
        self.trip_id = trip_id
        self.departure = departure
        self.arrival = arrival
        self.remaining_stops = remaining_stops
        self.remaining_stop_times = remaining_stop_times
        self.delay = delay
        self.past_station = past_station
        self.initial_progress = initial_progress
        self.shape_id = shape_id
    def update_progress(self):
        current_time = time.time()
        adjusted_departure = self.departure
        adjusted_arrival = self.arrival

        if current_time > adjusted_arrival:
            self.progress_ratio = 1  # Train has arrived
            return self.update_station()

        elif current_time < adjusted_departure:
            self.progress_ratio = 0  # Train hasn’t departed yet
            return True
        else:
            # Calculate progress ratio
            total_time = adjusted_arrival - adjusted_departure
            elapsed_time = current_time - adjusted_departure
            self.progress_ratio = elapsed_time / total_time
            print(self.trip_id, self.departure, self.arrival, sep="\t")
            print("current tiime" +  str(current_time))
            print("progress" + str(self.progress_ratio))
            print("-"*30)

            return True
    def update_station(self):
        current_time = time.time()
        adjusted_departure = self.departure
        adjusted_arrival = self.arrival

        if(len(self.remaining_stop_times) > 0):

            self.past_station = self.remaining_stops[0][0:3]
            self.remaining_stops.pop(0)
            self.departure = self.remaining_stop_times.pop(0)
            self.arrival = self.remaining_stop_times[0]

            total_time = adjusted_arrival - adjusted_departure
            elapsed_time = current_time - adjusted_departure
            self.progress_ratio = elapsed_time / total_time
            print(self.trip_id, self.departure, self.arrival, sep="\t")
            print("current tiime" + str(current_time))
            print("progress" + str(self.progress_ratio))
            print("-" * 30)

            return True
        return False

    def getProgress(self):
        return self.progress_ratio
    def estimatedPosition(self):
        shapes = open("/Users/rohitsattuluri/PycharmProjects/wallpaper/gtfs_subway/shapes.txt", "r")
        shape_lines = shapes.readlines()

        route_path = []

        for line in shape_lines:
            l = line.split(",")
            if (l[0] == self.shape_id):
                route_path.append(line)

        index = int(progress_ratio * len(route_path))






