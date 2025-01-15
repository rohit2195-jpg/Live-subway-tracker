

from google.transit import gtfs_realtime_pb2
import requests
import time
from datetime import datetime
from datetime import date
from Train import Train
from flask import Flask, render_template, jsonify
import pickle
import folium
import json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
  lines_to_colors = {
    "A": "blue",
    "C": "blue",
    "E": "blue",
    "S": "grey",
    "B": "orange",
    "D": "orange",
    "F": "orange",
    "M": "orange",
    "G": "lightgreen",
    "L": "lightgrey",
    "J": "orange",  # dark orage/gold
    "N": "yellow",
    "Q": "yellow",
    "R": "yellow",
    "W": "yellow",
    "1": "red",
    "2": "red",
    "3": "red",
    "4": "green",
    "5": "green",
    "6": "green",
    "7": "purple",
  }

  geojson_path = 'Subway Lines.geojson'
  with open(geojson_path, 'r') as f:
    data = json.load(f)

  m = folium.Map(location=[40.7, -73.95], zoom_start=12, tiles="cartodb positron")

  for line in lines_to_colors:

    g_line_features = [feature for feature in data['features'] if line in feature['properties']['name']]

    g_line_features = sorted(g_line_features, key=lambda x: int(x['properties']['id']))

    coordinate_list = []
    for feature in g_line_features:
      coordinates = feature['geometry']['coordinates']
      new_coordinates = [[lat, lon] for lon, lat in coordinates]
      coordinate_list.extend(new_coordinates)
      folium.PolyLine(new_coordinates, color=lines_to_colors[line], weight=5, tooltip=line + " line", opacity=1).add_to(
        m)

  stop_data = open("gtfs_subway/stops.txt", "r")
  stop_data_content = stop_data.readlines()
  for i in range(1, len(stop_data_content)):
    l = stop_data_content[i].split(",")
    if (not "N" in l[0] and not "S" in l[0]):
      custom_icon = folium.CustomIcon(
        icon_image="noun-metro-station-79184.png",  # Path to the PNG file
        icon_size=(12, 12)
      )

      folium.Marker(location=[l[2], l[3]], tooltip=l[1], icon=custom_icon).add_to(m)

  link = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l"

  output_path = 'nyc_subway_map.html'
  m.save(output_path)
  return render_template('index.html', map_path=output_path)

@app.route('/setupTrainList', methods=['GET'])
@cross_origin()
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

  return "setup_done", 200


@app.route('/trainLocation', methods=['GET'])
@cross_origin()
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


