// Retrieve the userToken data from local storage
const userTokenData = JSON.parse(localStorage.getItem('userToken'));


console.log(userTokenData)

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
  fetch(`http://localhost:8080/api/user/${userTokenData.userId}`, requestOptions)
    .then(response => response.json()) // Assuming the server returns JSON data
    .then(userData => {
      // Update the user name and email in the HTML form
      console.log(userData)
      document.getElementById('surname').value = userData.surname;
        document.getElementById('forname').value = userData.forname;

        document.getElementById('user_email').value = userData.email;
    })
    .catch(error => console.log('error', error));


}

function saveChanges() {
  // Retrieve the updated user information from the HTML form
  const updatedUser = {
    forname: document.getElementById('forname').value,
    surname: document.getElementById('surname').value,
    email: document.getElementById('user_email').value,
    password :document.getElementById('password').value
    // Add any other fields you want to update
  };

  // Retrieve the userToken data from local storage
  const userTokenData = JSON.parse(localStorage.getItem('userToken'));

  // Check if userTokenData exists
  if (userTokenData) {
    // Construct the Authorization header using the access token
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("Authorization", `Bearer ${userTokenData.accessToken}`);

    const requestOptions = {
      method: 'PUT',
      headers: myHeaders,
      body: JSON.stringify(updatedUser),
      redirect: 'follow',
    };

    // Fetch user data from the server
    fetch(`http://localhost:8080/api/user/update`, requestOptions)
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
        })
        .then(updatedUserData => {
          // Assuming the server returns the updated user data
          console.log(updatedUserData);
          // Optionally, you can update the user information in the HTML form or take any other actions
        })
        .catch(error => console.error('Error:', error));
  }
}

function logout() {
    var myHeaders = new Headers();
    // Assuming you have the access token stored in a variable or retrieved it from somewhere
    var accessToken = userTokenData.accessToken;  // Replace with your actual access token

    myHeaders.append("Authorization", "Bearer " + accessToken);

    var requestOptions = {
        method: 'DELETE',
        headers: myHeaders,
        redirect: 'follow'
    };

    fetch("http://localhost:8080/api/logout/"+userTokenData.userId, requestOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.text();
        })
        .then(result => {
            // Handle the successful logout, for example, redirect to the login page
            localStorage.removeItem('userToken');

            // Redirect to the index.html page
            window.location.href = "/index.html";

            // Log the result (optional)
            console.log(result);
            // Add logic here to redirect to the login page or perform any other actions
        })
        .catch(error => console.log('error', error));
}