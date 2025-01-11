import folium
import json


lines_to_colors = {
    "A":"blue",
    "C":"blue",
    "E":"blue",
    "S":"grey",
    "B":"orange",
    "D":"orange",
    "F":"orange",
    "M":"orange",
    "G":"lightgreen",
    "L":"lightgrey",
    "J":"orange",#dark orage/gold
    "N": "yellow",
    "Q":"yellow",
    "R":"yellow",
    "W":"yellow",
    "1":"red",
    "2":"red",
    "3":"red",
    "4":"green",
    "5":"green",
    "6":"green",
    "7":"purple",
}

geojson_path = 'Subway Lines.geojson'
with open(geojson_path, 'r') as f:
    data = json.load(f)

g_line_features = [feature for feature in data['features'] if feature['properties']['name'] == 'L']

g_line_features = sorted(g_line_features, key=lambda x: int(x['properties']['id']))

m = folium.Map(location=[40.7, -73.95], zoom_start=12, tiles="cartodb positron")

coordinate_list = []
for feature in g_line_features:
    coordinates = feature['geometry']['coordinates']
    new_coordinates = [[lat, lon] for lon, lat in coordinates]
    coordinate_list.extend(new_coordinates)
    folium.PolyLine(new_coordinates, color="green", weight=3).add_to(m)

output_path = 'nyc_subway_map.html'
m.save(output_path)
print(f"G-line map saved to {output_path}")
