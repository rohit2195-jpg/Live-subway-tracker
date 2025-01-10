

from google.transit import gtfs_realtime_pb2
import requests
import time
from datetime import datetime
from datetime import date
from Train import Train



stop_names = {}
stop_list = []
stopID_to_location = {}
subwayID_to_location = {}
tripID_to_shapeID = {}
stop_info = open("/Users/rohitsattuluri/PycharmProjects/wallpaper/gtfs_subway/stops.txt", 'r')
lines = stop_info.readlines()
for line in lines:
  l = line.split(",")
  stop_names[l[0]] = l[1]
  stopID_to_location[l[0]] = l[2] + "," + l[3]
  if(l[0][0] == "L" and "N" not in l[0] and "S" not in l[0]):
    stop_list.append(l[0])

trip_info = open("/Users/rohitsattuluri/PycharmProjects/wallpaper/gtfs_subway/trips.txt", "r")
tripinfo_lines = trip_info.readlines()
for line in tripinfo_lines:
  l = line.split(",")
  tripID_to_shapeID[l[1]] = l[5]




feed = gtfs_realtime_pb2.FeedMessage()
response = requests.get('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l')
feed.ParseFromString(response.content)
#print(stopID_to_location)

for entity in feed.entity:
  print(entity.trip_update.trip.trip_id)

while True:
  train_list = []


  for entity in feed.entity:

    remaining_stops = []
    remaining_stop_times = []



    for stop in entity.trip_update.stop_time_update:
      remaining_stops.append(stop.stop_id)
      remaining_stop_times.append(stop.arrival.time)

    if(len(remaining_stops) == 0 or len(remaining_stops) == len(stop_list)):
      continue


    #print(remaining_stops)



    expected_time_to_next_station = remaining_stop_times[0]

    delay = entity.trip_update.stop_time_update[0].arrival.delay
    #capacity =


    trip_id = entity.trip_update.trip.trip_id
    print(remaining_stops)
    print(remaining_stop_times)

    print("arrival time: " + str(expected_time_to_next_station))
    print("delay time: " + str(delay))
    print("trip id" + trip_id)
    #print(entity.trip_update)






    train1 = Train(trip_id, expected_time_to_next_station, remaining_stops, remaining_stop_times, delay, stop_list)
    train_list.append(train1)



  print(len(train_list))
  updateNeeded = False
  while(not updateNeeded):
    index = 0
    while(index < len(train_list)):
      time.sleep(1)
      if(not train_list[index].update_progress()):
        updateNeeded = True
        print("API called again, train fnished all stops")
        break
      if(train_list[index].validTrain == False):
        train_list.pop(index)
        index -= 1
      print(train_list[index].getShapeID(tripID_to_shapeID))

      index += 1

