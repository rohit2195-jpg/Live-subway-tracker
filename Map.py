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


m = folium.Map(location=[40.7, -73.95], zoom_start=12, tiles="cartodb positron")






for line in lines_to_colors:

    g_line_features = [feature for feature in data['features'] if line in feature['properties']['name']]

    g_line_features = sorted(g_line_features, key=lambda x: int(x['properties']['id']))

    coordinate_list = []
    for feature in g_line_features:
        coordinates = feature['geometry']['coordinates']
        new_coordinates = [[lat, lon] for lon, lat in coordinates]
        coordinate_list.extend(new_coordinates)
        folium.PolyLine(new_coordinates, color=lines_to_colors[line], weight=5, tooltip=line+" line", opacity=1).add_to(m)




stop_data = open("gtfs_subway/stops.txt", "r")
stop_data_content = stop_data.readlines()
for i in range(1, len(stop_data_content)):
    l = stop_data_content[i].split(",")
    if(not "N" in l[0] and not "S" in l[0]):
        custom_icon = folium.CustomIcon(
            icon_image="noun-metro-station-79184.png",  # Path to the PNG file
            icon_size=(12, 12)
        )

        folium.Marker(location=[l[2], l[3]], tooltip=l[1], icon=custom_icon).add_to(m)


output_path = 'nyc_subway_map.html'
m.save(output_path)
print(f"G-line map saved to {output_path}")
