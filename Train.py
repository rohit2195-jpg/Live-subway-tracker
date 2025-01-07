import time

class Train:
    def __init__(self, trip_id, departure, arrival,remaining_stops, remaining_stop_times, delay, past_station, initial_progress):
        self.trip_id = trip_id
        self.departure = departure
        self.arrival = arrival
        self.remaining_stops = remaining_stops
        self.remaining_stop_times = remaining_stop_times
        self.delay = delay
        self.past_station = past_station
        self.initial_progress = initial_progress
    def update_progress(self):
        current_time = time.time()
        adjusted_departure = self.departure_time + self.delay
        adjusted_arrival = self.arrival_time + self.delay

        if current_time > adjusted_arrival:
            self.progress_ratio = 1  # Train has arrived
            self.update_station()
        elif current_time < adjusted_departure:
            self.progress_ratio = 0  # Train hasn’t departed yet
            return True
        else:
            # Calculate progress ratio
            total_time = adjusted_arrival - adjusted_departure
            elapsed_time = current_time - adjusted_departure
            self.progress_ratio = elapsed_time / total_time
            return True
    def update_station(self):
        if(len(self.remaining_stop_times) > 0):
            self.progress_ratio = 0
            self.past_station = self.remaining_stops[0]
            self.remaining_stops = self.remaining_stops.pop(0)
            self.remaining_stop_times = self.remaining_stop_times.pop(0)
            return True
        return False
