document.addEventListener('DOMContentLoaded', function() {
  // nav menu
  const menus = document.querySelectorAll('.side-menu');
  M.Sidenav.init(menus, {edge: 'right'});
  // add recipe form
  const forms = document.querySelectorAll('.side-form');
  M.Sidenav.init(forms, {edge: 'left'});
});
function updateDateTime() {
  const currentDate = new Date();
  const formattedDate = currentDate.toDateString();
  const currentTime = currentDate.toLocaleTimeString();

  const dateTimeString = `Current Date: ${formattedDate}, Time: ${currentTime}`;

  // Assuming you want to display it in the "recipe-ingredients" div
  const recipeIngredientsDiv = document.querySelector('.result-ingredients');
  recipeIngredientsDiv.textContent = dateTimeString;
}

const map = L.map('map') 
    
// Get the tile layer from OpenStreetMaps 
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { 

// Specify the maximum zoom of the map 
maxZoom: 20, 

// Set the attribution for OpenStreetMaps 
attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors' 
}).addTo(map); 

// Set the map view to the user's location 
map.locate({setView: true, maxZoom: 20}); 

// When we have a location draw a marker and accuracy circle
function onLocationFound(e) {
    var radius = e.accuracy / 2;

    L.marker(e.latlng).addTo(map)
        .bindPopup("You are within " + radius + " meters from this point").openPopup();

    L.circle(e.latlng, radius).addTo(map);
}

// Once we have a location, call this function
map.on('locationfound', onLocationFound);

// If the user issues a 'locationerror' event, log it to the console
map.on('locationerror', function(e) {
    console.log(e);
    alert("Location access denied.");
});



function error(err) {

  if (err.code === 1) {
      alert("Please allow geolocation access");
  } else {
      alert("Cannot get current location");
  }

}
function toggleMap() {
  var mapDiv = document.getElementById('map');
  if (mapDiv.style.display === 'none' || mapDiv.style.display === '') {
    mapDiv.style.display = 'block';
  } else {
    mapDiv.style.display = 'none';
  }
}