

from google.transit import gtfs_realtime_pb2
import requests

from Train import Train
from flask import Flask, render_template, jsonify
import pickle
import folium
import json
from flask_cors import CORS
import time
import threading
import concurrent.futures

app = Flask(__name__)
CORS(app)

lock = threading.Lock()

API_LINK = ['https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace', "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g",
            "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-jz", "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l",
            "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm", "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw",
            "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs"]
'''
['https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace', "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g",
            "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-jz", "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l",
            "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm", "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw",
            "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs"]
'''
storage_path = API_LINK[0][API_LINK[0].rfind("gtfs"):] + ".txt"
#change this above for single use


@app.route('/setupTrainList', methods=['GET'])
def getTrainList():
  print("setup endpoint called")
  stopID_to_location = {}
  stop_info = open("/Users/rohitsattuluri/PycharmProjects/wallpaper/gtfs_subway/stops.txt", 'r')
  lines = stop_info.readlines()
  for line in lines:
    l = line.split(",")
    stopID_to_location[l[0]] = l[2] + "," + l[3]


  tripID_to_shapeID = {}
  trip_info = open("/Users/rohitsattuluri/PycharmProjects/wallpaper/gtfs_subway/trips.txt", "r")
  tripinfo_lines = trip_info.readlines()
  for line in tripinfo_lines:
    l = line.split(",")
    tripID_to_shapeID[l[1][l[1].index('_') + 1:]] = l[5]

  trip_id_to_departure_time = {}
  stop_times = open("/Users/rohitsattuluri/PycharmProjects/wallpaper/gtfs_subway/stop_times.txt", "r")
  contents = stop_times.readlines()
  for i in range(1, len(contents)):
    line = contents[i].split(",")
    prev_line = contents[i - 1].split(",")
    ##get departure time in different way, not with stop_list but with stopsequence on stop_times.txt
    if (line[0][line[0].index('_') + 1:]) not in trip_id_to_departure_time:
      trip_id_to_departure_time[line[0][line[0].index('_') + 1:]] = {
        "stations": [],
        "departures": [],
      }
    trip_id_to_departure_time[line[0][line[0].index('_') + 1:]]["stations"].append(line[1])
    trip_id_to_departure_time[line[0][line[0].index('_') + 1:]]["departures"].append(line[3])

  shapes = open("/Users/rohitsattuluri/PycharmProjects/wallpaper/gtfs_subway/shapes.txt", "r")
  shape_lines = shapes.readlines()
  shape_id_to_coordinate = {}

  for line in shape_lines:
    l = line.split(",")

    if (l[0] not in shape_id_to_coordinate):
      shape_id_to_coordinate[l[0]] = []
    shape_id_to_coordinate[l[0]].append(line)


  train_list = []

  for link in API_LINK:

    feed = gtfs_realtime_pb2.FeedMessage()
    ##change this link for different api

    response = requests.get(link)
    feed.ParseFromString(response.content)
    # print(stopID_to_location)
    length = 0

    for entity in feed.entity:

      remaining_stops = []
      remaining_stop_times = []



      for stop in entity.trip_update.stop_time_update:
        remaining_stops.append(stop.stop_id)
        remaining_stop_times.append(stop.arrival.time)

      if(len(remaining_stops) == 0 ): ##or len(remaining_stops) == len(stop_list)
        continue

      length += 1





      #print(remaining_stops)



      expected_time_to_next_station = remaining_stop_times[0]

      delay = entity.trip_update.stop_time_update[0].arrival.delay
      vehicleID = entity.vehicle.congestion_level
      #capacity =


      trip_id = entity.trip_update.trip.trip_id
      '''
      print(remaining_stops)
      print(remaining_stop_times)
  
      print("arrival time: " + str(expected_time_to_next_station))
      print("delay time: " + str(delay))
      print("trip id" + trip_id)
      '''
      #print(entity.trip_update)







      train1 = Train(trip_id, expected_time_to_next_station, remaining_stops, remaining_stop_times, delay,  vehicleID, stopID_to_location, tripID_to_shapeID, storage_path, trip_id_to_departure_time, shape_id_to_coordinate)
      train_list.append(train1)





  print(len(train_list))

  file = open("Train Database/"+storage_path, "wb")
  pickle.dump(train_list, file)

  return "setup_done", 200


@app.route('/trainLocation', methods=['GET'])
def getTrainLocation():
  print("location endpoint called")
  train_location = []
  train_location_lock = threading.Lock()

  # Function for processing a chunk of trains
  def process_train_chunk(train_chunk):
    local_locations = []
    index = 0
    for train in train_chunk:
      if not train.update_progress():
        print("API called again, train finished all stops")
        continue

      if not train.validTrain:
        continue

      location = train.estimatedPosition()

      if train.validTrain:
        local_locations.append(location)
      print(index)
      index += 1

    with train_location_lock:
      train_location.extend(local_locations)

  # Load the train list
  database_path = "Train Database/" + storage_path
  with open(database_path, "rb") as database:
    train_list = pickle.load(database)

  # Split train_list into smaller chunks for threads
  chunk_size =25
  chunks = [train_list[i:i + chunk_size] for i in range(0, len(train_list), chunk_size)]

  # Create and start threads
  threads = []
  for chunk in chunks:
    thread = threading.Thread(target=process_train_chunk, args=(chunk,))
    threads.append(thread)
    thread.start()

  # Wait for all threads to finish
  for thread in threads:
    thread.join()

  # Update the train database after all threads complete
  with open(database_path, "wb") as database:
    pickle.dump(train_list, database)

  print("Train locations updated and database saved.")


  print(train_location)

  return jsonify(train_location)


if __name__ == '__main__':
    app.run(debug=True, port = 5001)

getTrainList()
while True:
  getTrainLocation()

