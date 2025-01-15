import folium
import json
from Main import *
from flask import Flask, jsonify, request

app = Flask(__name__)



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

link = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l"

@app.route("/")
def index():
    map_html = m._repr_html_()
    html_content = f'''
        <!DOCTYPE html>
    <html>
    <head>
        <title>Subway Map with Real-Time Updates</title>
        <style>
            #map {{
                width: 100%;
                height: 600px;
            }}
        </style>
    </head>
    <body>
        <h1>Subway Map with Train Updates</h1>
        <div id="map">{map_html}</div>

        <!-- JavaScript for fetching and updating train positions -->
        <script>
            // Function to fetch initial train positions
            
            async function setupTrainList() {{
            try {{
                console.log("Attempting to call setupTrainList...");
                const response = await fetch('http://127.0.0.1:5001/setupTrainList', {{
                    method: 'POST',
                }});
                if (!response.ok) {{
                    console.error("Failed to call setupTrainList:", response.statusText);
                }} else {{
                    console.log("setupTrainList completed successfully");
                }}
            }} catch (error) {{
                console.error("Error during setupTrainList:", error);
            }}
        }}

        async function fetchTrainLocations() {{
            console.log("Fetching train locations...");
            try {{
                const response = await fetch('http://127.0.0.1:5001/trainLocation');
                const trainCoordinates = await response.json();
                console.log("Live train positions received:", trainCoordinates);
                updateTrainMarkers(trainCoordinates);
            }} catch (error) {{
                console.error("Error fetching train locations:", error);
            }}
        }}


            function updateTrainMarkers(coordinates) {{
                window.trainMarkers = window.trainMarkers || [];
                window.trainMarkers.forEach(marker => marker.remove());
                window.trainMarkers = [];
                window.map = map;

                coordinates.forEach(function(coord) {{
                    var marker = L.circleMarker([coord[0], coord[1]], {{
                        radius: 6,
                        fillColor: 'red',
                        color: 'red',
                        weight: 1,
                        opacity: 1,
                        fillOpacity: 0.6
                    }}).addTo(window.map);
                    window.trainMarkers.push(marker);
                }});
            }}

            document.addEventListener('DOMContentLoaded', async () => {{
                // Initialize setup first
                await setupTrainList();

                // Start fetching train locations every 5 seconds
                setInterval(fetchTrainLocations, 5000);
            }});
        </script>
    </body>
    </html>
    '''

    return html_content


if __name__ == '__main__':
    app.run(debug=True, port=5000)


output_path = 'nyc_subway_map.html'
m.save(output_path)
print(f"G-line map saved to {output_path}")
