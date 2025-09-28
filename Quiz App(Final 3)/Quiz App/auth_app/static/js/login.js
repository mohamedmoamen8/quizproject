
document.addEventListener("DOMContentLoaded", function () {
  const usernameField = document.getElementById("username");
  const passwordField = document.getElementById("password");
  const submitButton = document.getElementById("btnSubmit");

 
  function validateFields() {
    const username = usernameField.value;
    const password = passwordField.value;

    
    if (username && password) {
      submitButton.disabled = false;
    } else {
      submitButton.disabled = true;
    }
  }

  // Event listeners for the fields
  usernameField.addEventListener("input", validateFields);
  passwordField.addEventListener("input", validateFields);

  // Initial check in case the user has pre-filled fields
  validateFields();
});
