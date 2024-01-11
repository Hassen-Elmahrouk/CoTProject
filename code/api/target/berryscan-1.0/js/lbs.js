var TokenData = JSON.parse(localStorage.getItem('userToken'));

const map = L.map('map').setView([0, 0], 2);  // Set initial view

// Get the tile layer from OpenStreetMaps
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 20,
    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Fetch user's location
map.locate({ setView: true, maxZoom: 20 });

// Create a layer group for API locations
const apiLocationsLayer = L.layerGroup().addTo(map);

// When we have a location, draw a marker and accuracy circle
function onLocationFound(e) {
    var radius = e.accuracy / 2;

    L.marker(e.latlng).addTo(map)
        .bindPopup("You are within " + radius + " meters from this point").openPopup();

    L.circle(e.latlng, radius).addTo(map);
    console.log(e.latlng)
}

// Once we have a location, call this function
map.on('locationfound', onLocationFound);

// Fetch data from your API
fetch("https://berryscan.tech/api/getAnnotations", {
    method: 'GET',
    headers: {
        'Authorization': `Bearer ${TokenData.accessToken}`,  // Replace with your actual token
    },
})
    .then(response => response.json())
    .then(data => {

        // Iterate through the received annotations and add markers to the API layer
        data.annotations.forEach(annotation => {
            const lat = annotation.latitude;
            const lon = annotation.longitude;


            const category = annotation.category;
            const imageData = annotation.image_data;

            // Ensure imageData is a valid base64 string
            const base64Image = typeof imageData === 'object' ? '' : imageData;

            // Create a popup with the image data
            const popupContent = `<div style="max-width: 500px; max-height: 500px; position: relative;">
    <img src="data:image/png;base64,${imageData}" alt="${category}" style="width: 100%; height: auto;">
    <div style="text-align: center; margin-top: 5px;">${category}</div>
</div>`;
            // Create a popup with the image data

            // Create a marker with a popup for API locations
            const apiMarker = L.marker([lat, lon]).addTo(apiLocationsLayer)
                .bindPopup(popupContent);
            // Correct usage of template literals for popupContent

            // Add a click event to zoom in when the marker is clicked
            apiMarker.on('click', function () {
                map.setView([lat, lon], 15);
            });
        });
    })
    .catch(error => console.error('Error fetching data:', error));


// Handle location error
map.on('locationerror', function (e) {
    console.error('Location error:', e);
    alert("Location access denied.");
});

function error(err) {
    if (err.code === 1) {
        alert("Please allow geolocation access");
    } else {
        alert("Cannot get current location");
    }
}

