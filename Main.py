def stop_is_increasing(stops):

  if(len(stops) == 1):
    if(int(stops[0][1:3]) == int(stop_list[-1][1:3])):
      return True
    elif (int(stops[0][1:3]) == int(stop_list[0][1:3])):
      return False

  initial = int(stops[0][1:3])
  for stop in stops:
    if(int(stop[1:3]) > initial):
      return True
    elif (int(stop[1:3]) < initial):
      return False


from google.transit import gtfs_realtime_pb2
import requests
import time
from datetime import datetime
from datetime import date

stop_names = {}
stop_list = []
stopID_to_location = {}
subwayID_to_location = {}
stop_info = open("/Users/rohitsattuluri/PycharmProjects/wallpaper/gtfs_subway/stops.txt", 'r')
lines = stop_info.readlines()
for line in lines:
  l = line.split(",")
  stop_names[l[0]] = l[1]
  stopID_to_location[l[0]] = l[2] + "," + l[3]
  if(l[0][0] == "L" and "N" not in l[0] and "S" not in l[0]):
    stop_list.append(l[0])





feed = gtfs_realtime_pb2.FeedMessage()
response = requests.get('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l')
feed.ParseFromString(response.content)
#print(stopID_to_location)


for entity in feed.entity:

  remaining_stops = []



  for stop in entity.trip_update.stop_time_update:
    remaining_stops.append(stop.stop_id)

  if(len(remaining_stops) == 0 or len(remaining_stops) == len(stop_list)):
    continue

  #print(remaining_stops)
  index_prev_stop = 0
  for stop in stop_list:
    if(stop == remaining_stops[0][0:3]):
      direction = stop_is_increasing(remaining_stops)
      if(direction):
        index_prev_stop -=1
        break
      else:
        index_prev_stop += 1
        break
    index_prev_stop += 1

  #print(remaining_stops)
  #print(stop_list[index_prev_stop])
  expected_time_to_next_station = entity.trip_update.stop_time_update[0].arrival.time
  current_time = time.time()
  delay = entity.trip_update.stop_time_update[0].arrival.delay
  departure_time = 0

  trip_id = entity.trip_update.trip.trip_id
  stop_times = open("/Users/rohitsattuluri/PycharmProjects/wallpaper/gtfs_subway/stop_times.txt", "r")
  contents = stop_times.readlines()
  for content in contents:
      line = content.split(",")
      if(trip_id in line[0] and line[1] == (stop_list[index_prev_stop] + remaining_stops[0][-1])):
        departure_time = line[3]
        break
  if(departure_time == 0 or expected_time_to_next_station == 0):
    continue




  ##do calculations here


  date_str = date.today()

  departure_time = datetime.strptime(f"{date_str} {departure_time}", "%Y-%m-%d %H:%M:%S")
  departure_time = int(departure_time.timestamp())
  expected_time_to_next_station += delay

  print("deaprture timie: " + str(departure_time))
  print("arrival time: " + str(expected_time_to_next_station))
  print("current tiime: " + str(current_time))
  print("delay time: " + str(delay))
  print("trip id" + trip_id)
  #print(entity.trip_update)

  progress_ratio = (current_time - departure_time) / ((current_time - departure_time) + (expected_time_to_next_station - current_time))
  print(progress_ratio)
  print("-"*30)











  #print(entity.trip_update.stop_time_update)

