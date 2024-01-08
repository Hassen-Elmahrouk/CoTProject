// Retrieve the userToken data from local storage
const userTokenData = JSON.parse(localStorage.getItem('userToken'));

// Check if userTokenData exists
if (userTokenData) {
  // Construct the Authorization header using the access token
  const myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");
  myHeaders.append("Authorization", `Bearer ${userTokenData.accessToken}`);

  const requestOptions = {
    method: 'GET',
    headers: myHeaders,
    redirect: 'follow',
  };

  // Fetch user data from the server
  fetch(`http://localhost:8080/modernparker-0.0/api/user/${userTokenData.userId}`, requestOptions)
    .then(response => response.json()) // Assuming the server returns JSON data
    .then(userData => {
      // Update the user name and email in the HTML form
      document.getElementById('user_name').value = userData.name;
      document.getElementById('user_email').value = userData.email;
    })
    .catch(error => console.log('error', error));
}
