class UserToken {
  constructor(userId, accessToken, refreshToken) {
    this.userId = userId;
    this.accessToken = accessToken;
    this.refreshToken = refreshToken;
  }

  getUserId() {
    return this.userId;
  }

  setUserId(userId) {
    this.userId = userId;
  }

  getAccessToken() {
    return this.accessToken;
  }

  setAccessToken(accessToken) {
    this.accessToken = accessToken;
  }

  getRefreshToken() {
    return this.refreshToken;
  }

  setRefreshToken(refreshToken) {
    this.refreshToken = refreshToken;
  }
}

let userToken;

function performLogin() {
  // Replace this with your actual login logic
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/x-www-form-urlencoded");

  var urlencoded = new URLSearchParams();
  urlencoded.append("grand_type", "password");
  urlencoded.append("email", username);
  urlencoded.append("password", password);

  var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: urlencoded,
    redirect: 'follow'
  };
  fetch("https://api.berryscan.tech/api/oauth2/token", requestOptions)
    .then(response => response.json())
    .then(result => {
      const { userId, accessToken, refreshToken } = result;

      // Update the existing userToken object using setters
      if (userToken) {
        userToken.setUserId(userId);
        userToken.setAccessToken(accessToken);
        userToken.setRefreshToken(refreshToken);
      } else {
        // If userToken doesn't exist, create a new one
        userToken = new UserToken(userId, accessToken, refreshToken);
      }

      // Convert the userToken object to a string
      const userTokenString = JSON.stringify(userToken);

      // Store the string in local storage
      localStorage.setItem('userToken', userTokenString);

      window.location.href = "/pages/index.html"
    })
    .catch(error => console.log('error', error));
}
