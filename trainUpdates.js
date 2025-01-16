// Wait for the iframe to load before attempting to access its contents
let map = null;
let trainMarkers = [];

function setupTrainList() {
    return fetch('http://127.0.0.1:5001/setupTrainList')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Setup failed: ${response.statusText}`);
            }
            return response.text();
        })
        .then(text => {
            if (text !== "setup_done") {
                throw new Error("Unexpected setup response");
            }
        });
}

function getTrainLocations() {
    return fetch('http://127.0.0.1:5001/trainLocation')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Failed to fetch train locations: ${response.statusText}`);
            }
            return response.json();
        });
}

function initializeMapInIframe() {
    return new Promise((resolve, reject) => {
        const mapFrame = document.getElementById('map-frame');
        const MAP_ID = 'map_4642b718e052e312603e2751e1bf5cb8';

        function checkMap() {
            try {
                const iframeWindow = mapFrame.contentWindow;
                const mapInstance = iframeWindow[MAP_ID];
                if (mapInstance && typeof mapInstance.addLayer === 'function') {
                    map = mapInstance; // Assign the actual Leaflet map object
                    console.log("Map successfully initialized!");
                    resolve(map);
                } else {
                    setTimeout(checkMap, 100); // Retry if not ready
                }
            } catch (error) {
                reject(error);
            }
        }

        if (mapFrame.contentDocument.readyState === 'complete') {
            checkMap();
        } else {
            mapFrame.onload = checkMap;
        }
    });
}

function updateMarkers(locations) {
    if (!map) {
        console.error("Map not initialized yet");
        return;
    }

    console.log("Map instance:", map);
    console.log("Locations:", locations);




    // Clear existing markers
    trainMarkers.forEach(marker => map.removeLayer(marker));
    trainMarkers = [];

    // Add new markers
    locations.forEach(([lat, lon]) => {
        const marker = L.marker([lat, lon]).addTo(map);
        trainMarkers.push(marker);
    });
}

async function initializeSystem() {
    try {
        // First, ensure the map is initialized
        console.log("Initializing map...");
        await initializeMapInIframe();
        
        // Then set up the train list
        console.log("Setting up train list...");
        await setupTrainList();
        console.log("Setup completed.");

        // Start periodic updates
        setInterval(async () => {
            console.log("Fetching train locations...");
            const trainLocations = await getTrainLocations();
            console.log("Updating train markers...");
            updateMarkers(trainLocations);
        }, 10000);
    } catch (error) {
        console.error("Error initializing system:", error);
    }
}

// Start the initialization process when the page loads
document.addEventListener('DOMContentLoaded', initializeSystem);