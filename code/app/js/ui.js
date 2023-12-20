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

// Call the function when the page loads
document.addEventListener('DOMContentLoaded', () => {
  updateDateTime();

  // You can also set up an interval to update the time every second if needed
  setInterval(updateDateTime, 500);
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