import json
import folium
# Load the GeoJSON file
with open('Subway Lines.geojson', 'r') as f:
    data = json.load(f)

l_line_routes = [feature for feature in data['features'] if feature['properties']['name'] == 'G']

merged_coordinates = []
for i in range(0,5):
    for point in l_line_routes[i]['geometry']['coordinates']:
        lat = point[0]
        lon = point[1]
        merged_coordinates.append([lon, lat])


print(merged_coordinates)

map_center = [40.7128, -74.0060]
map_nyc = folium.Map(location=map_center, zoom_start=12)

folium.PolyLine(merged_coordinates, color="green", weight=5, opacity=0.8).add_to(map_nyc)

# Save the map as an HTML file
map_nyc.save("nyc_subway_map.html")

# Display the map (if running in Jupyter Notebook or similar environments)
map_nyc
