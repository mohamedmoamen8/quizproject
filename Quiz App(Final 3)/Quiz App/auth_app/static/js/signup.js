// signup.js

document.addEventListener("DOMContentLoaded", function () {
  const passwordField = document.getElementById("password");
  const confirmPasswordField = document.getElementById("confirm_password");
  const submitButton = document.getElementById("btnSubmit");

  // Function to validate if passwords match
  function validatePasswords() {
    const password = passwordField.value;
    const confirmPassword = confirmPasswordField.value;

    // Check if passwords match and enable/disable the submit button
    if (password && confirmPassword && password === confirmPassword) {
      submitButton.disabled = false;
    } else {
      submitButton.disabled = true;
    }
  }

  // Event listeners for password fields
  passwordField.addEventListener("input", validatePasswords);
  confirmPasswordField.addEventListener("input", validatePasswords);

  // Initial check in case the user has pre-filled fields
  validatePasswords();
});
