# NYC Subway Tracker 🚇

This is a live NYC subway Tracker. Currently, only the L line has live subway tracking, and other lines are currently being developed. 


## Overview  
This project receives stop data and expected arrival times from the **Metropolitan Transportation Authority (MTA) API**. The Python backend collects this data and uses **linear interpolation** to estimate the position of each train in the NYC subway system.  

## Testing instructions
1. To run this map on your device, first clone or download this repository.
2. Start the backend by running python Main.py
3. Start the frontend by clicking index.html

## Features  
1. Initializes a NYC map and overlays subway routes using `Subway Lines.geojson`, a resource from NYC Open Data.  
2. Dynamically updates train positions on the map with black markers every 2-5 seconds.  
3. Uses **linear interpolation** to calculate train positions due to the lack of exact coordinates from the API.  

## Long explanation on how it works
This project recieves stop data and expected arrival times from the Metropolitan Transportation Authority API. To gather the API data in Python, an additional github repo was used. In turn, the python backend collects the data and uses linear interpolation to calculate an estimated position of each train in the NYC subway. The backend then stores the train information in the Train Database directory. To complete this task, additional static datasets are used located in the gtfs_subway folder, which were especially helpful for finding locations of stations, the path of the trains, and more. Because of the lack of exact coordinates from the API, a linear interpolation technique was chosen to calculate positions of the trains. The backend then feeds the coordinates of the trains to the frontend HTML and Javascript. The JavaScript, located within the HTML file of index.html, initially plots a map of New York City using Leaflet. On top of that, it draws out the subway routes using Subway Lines.geojson, a resource from the NYC Open Data website. After setting up the initial map and setting up the backend, coordinates of different trains start coming in, and the frontend starts dynamically plotting them with a black marker. It updates around every 2-5 seconds. Hope you enjoy!

## Understanding the files
- Main.py - This is the backend of the application. It handles recieving data from the API and communicating with the frontend
- Train.py - This file is a class of a Train. Essentially it stores all the API data for each train as a Train Object. It updates the data when needed and performs calculations on the data to find estimated coordinates of the object's position
- index.html - This is the frontend, responsible for recieving data from the backend, creating the map, and updating the map.
- Other - Many of the other files are just static datasets about the subway found on NYC's website

## Useful links:
- [NYC subway map] (https://new.mta.info/map/5341)
- [NYC subway API] (https://api.mta.info/#/subwayRealTimeFeeds)
- [NYC API documentation] (https://gtfs.org/documentation/realtime/reference/#enum-vehiclestopstatus)
- [Github Repo for acessing data in Python] (https://github.com/MobilityData/gtfs-realtime-bindings/tree/master)
- [Github Repo for acessing data in Python2] (https://github.com/Andrew-Dickinson/nyct-gtfs)
- [NYC Subway Route Data] (https://data.cityofnewyork.us/Transportation/Subway-Lines/3qz8-muuu)

More lines will be added soon!


