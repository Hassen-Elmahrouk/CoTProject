if('serviceWorker' in navigator){
  navigator.serviceWorker.register('/sw.js')
    .then(reg => console.log('service worker registered'))
    .catch(err => console.log('service worker not registered', err));
}


const map = L.map('map');
// Initializes map

let marker, circle, zoomed;

navigator.geolocation.watchPosition(success, error);

function success(pos) {

  const lat = pos.coords.latitude;
  const lng = pos.coords.longitude;
  const accuracy = pos.coords.accuracy;

  if (!map.setViewCalled) {
    map.setView([lat, lng], 5);
    map.setViewCalled = true;
  }

  if (marker) {
    map.removeLayer(marker);
    map.removeLayer(circle);
  }
  // Removes any existing marker and circle (new ones about to be set)

  marker = L.marker([lat, lng]).addTo(map);
  circle = L.circle([lat, lng], { radius: accuracy }).addTo(map);
  // Adds marker to the map and a circle for accuracy

  if (!zoomed) {
    zoomed = map.fitBounds(circle.getBounds());
  }
  // Set zoom to boundaries of accuracy circle

  map.setView([lat, lng]);
  // Set map focus to current user position

}

function error(err) {

  if (err.code === 1) {
    alert("Please allow geolocation access");
  } else {
    alert("Cannot get current location");
  }

}