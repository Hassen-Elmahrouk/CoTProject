// register.js
async function registerUser(event) {
  event.preventDefault();
  try {
    var username = document.getElementById("username").value;
    var email = document.getElementById("myemail").value;

    var forname = document.getElementById("forname").value;
    var password = document.getElementById("password").value;

    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var raw = JSON.stringify({
      "email": email,
      "surname": username,
      "forname": forname,
      "password": password,
      "roles": ["ADMIN"]
    });

    console.log(raw);

    var requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: raw,
      redirect: 'follow'
    };

    const response = await fetch("http://localhost:8080/api/signup", requestOptions);

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const responseData = await response.text();
    window.location.href = "/index.html"
  } catch (error) {
    console.log('error', error);
  }
}
