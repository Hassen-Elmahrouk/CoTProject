function performLogin() {
    // Replace this with your actual login logic
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
  
    // Perform authentication logic (e.g., check credentials against a server)
  
    // For demonstration purposes, simulate a successful login
    const isLoginSuccessful = true;
  
    if (isLoginSuccessful) {
      // Redirect to the index page after successful login
      window.location.href = "/pages/index.html";
    } else {
      // Handle unsuccessful login (e.g., show an error message)
      alert("Login failed. Please check your credentials.");
    }
  }
  