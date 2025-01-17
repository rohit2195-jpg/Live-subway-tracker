This is a live NYC subway Tracker. Currently, only the L line has live subway tracking, and other lines are currently being developed. This project recieves stop data and expected arrival times from the Metropolitan Transportation Authority API. To gather the API data in Python, an additional github repo was used. In turn, the python backend collects the data and uses linear interpolation to calculate an estimated position of each train in the NYC subway. The backend then stores the train information in the Train Database directory. To complete this task, additional static datasets are used located in the gtfs_subway folder, which were especially helpful for finding locations of stations, the path of the trains, and more. Because of the lack of exact coordinates from the API, a linear interpolation technique was chosen to calculate positions of the trains. The backend then feeds the coordinates of the trains to the frontend HTML and Javascript. The JavaScript, located within the HTML file of index.html, initially plots a map of New York City using Leaflet. On top of that, it draws out the subway routes using Subway Lines.geojson, a resource from the NYC Open Data website. After setting up the initial map and setting up the backend, coordinates of different trains start coming in, and the frontend starts dynamically plotting them with a black marker. It updates around every 2-5 seconds. Hope you enjoy!

Useful links:
NYC subway map: https://new.mta.info/map/5341
NYC subway API: https://api.mta.info/#/subwayRealTimeFeeds
NYC API documentation: https://gtfs.org/documentation/realtime/reference/#enum-vehiclestopstatus
Github Repo: https://github.com/MobilityData/gtfs-realtime-bindings/tree/master or https://github.com/Andrew-Dickinson/nyct-gtfs
NYC Subway Route Data: https://data.cityofnewyork.us/Transportation/Subway-Lines/3qz8-muuu

More lines will be added soon!
