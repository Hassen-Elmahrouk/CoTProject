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

