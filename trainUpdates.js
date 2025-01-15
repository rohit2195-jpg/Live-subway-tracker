const mapFrame = document.getElementById('map-frame');

let trainMarkers = []; // To track and clear existing markers


async function setupTrainList() {
    try {
        const response = await fetch('http://127.0.0.1:5001/setupTrainList');
        if (!response.ok) {
            throw new Error(`Setup failed with status: ${response.status}`);
        }

        const result = await response.text();
        if (result === "setup_done") {
            console.log("Setup completed successfully.");
        } else {
            throw new Error("Unexpected setup response: " + result);
        }
    } catch (error) {
        console.error("Error during setupTrainList:", error);
    }
}

async function fetchTrainLocations() {
    try {
        const response = await fetch('http://127.0.0.1:5001/trainLocation');
        const trainCoordinates = await response.json();

        // Clear existing markers
        trainMarkers.forEach(marker => mapFrame.removeLayer(marker));
        trainMarkers = [];

        // Add new markers
        trainCoordinates.forEach(coord => {
            let marker = L.circleMarker([coord[0], coord[1]], {
                radius: 6,
                fillColor: 'red',
                color: 'red',
                weight: 1,
                opacity: 1,
                fillOpacity: 0.6
            }).addTo(mapFrame);
            trainMarkers.push(marker);
        });
    } catch (error) {
        console.error('Error fetching train locations:', error);
    }
}

(async () => {
    await setupTrainList(); // Wait until setup is done
    console.log("Starting live train updates...");

    // Fetch updates every 5 seconds
    setInterval(fetchTrainLocations, 10000);
})();
