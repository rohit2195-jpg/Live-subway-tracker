

from google.transit import gtfs_realtime_pb2
import requests
import time
from datetime import datetime
from datetime import date
from Train import Train
from flask import Flask, jsonify
import pickle

app = Flask(__name__)



@app.route('/setupTrainList', methods=['GET'])
def getTrainList():
  print("setup endpoint called")
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

  tripID_to_shapeID = {}
  trip_info = open("/Users/rohitsattuluri/PycharmProjects/wallpaper/gtfs_subway/trips.txt", "r")
  tripinfo_lines = trip_info.readlines()
  for line in tripinfo_lines:
    l = line.split(",")
    tripID_to_shapeID[l[1]] = l[5]






  feed = gtfs_realtime_pb2.FeedMessage()
  response = requests.get('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l')
  feed.ParseFromString(response.content)
  #print(stopID_to_location)



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
    vehicleID = entity.vehicle.congestion_level
    #capacity =


    trip_id = entity.trip_update.trip.trip_id
    print(remaining_stops)
    print(remaining_stop_times)

    print("arrival time: " + str(expected_time_to_next_station))
    print("delay time: " + str(delay))
    print("trip id" + trip_id)
    #print(entity.trip_update)






    train1 = Train(trip_id, expected_time_to_next_station, remaining_stops, remaining_stop_times, delay, stop_list, vehicleID, stopID_to_location, tripID_to_shapeID)
    train_list.append(train1)



  print(len(train_list))

  file = open("Train Database/L_line_trains", "wb")
  pickle.dump(train_list, file)

  return '', 204


@app.route('/trainLocation', methods=['GET'])
def getTrainLocation():
  print("location endpoint called")
  updateNeeded = False
  index = 0
  train_location = []

  database = open("Train Database/L_line_trains", "rb")
  train_list = pickle.load(database)

  while(index < len(train_list)):
    time.sleep(1)
    if(not train_list[index].update_progress()):
      updateNeeded = True
      print("API called again, train fnished all stops")
      getTrainList()
      database = open("Train Database/L_line_trains", "rb")
      train_list = pickle.load(database)
      index = 0
      train_list[index].update_progress()

    if(train_list[index].validTrain == False):
      train_list.pop(index)
      index -= 1
    location = train_list[index].estimatedPosition()
    train_location.append(location)
    '''

    print(location)
    print(train_list[index].trip_id)
    print(train_list[index].remaining_stop_times)
    print(train_list[index].departure_time)
    print(time.time())
    print("-"*30)
    '''


    index += 1
  file = open("Train Database/L_line_trains", "wb")
  pickle.dump(train_list, file)

  print(train_location)
  return jsonify(train_location)

if __name__ == '__main__':
    app.run(debug=True, port = 5001)


