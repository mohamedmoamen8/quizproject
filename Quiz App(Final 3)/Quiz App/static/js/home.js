document.addEventListener("DOMContentLoaded", function () {
  // Navbar toggle
  const navbarToggler = document.getElementById("navbar-toggler");
  const navLinks = document.getElementById("nav-links");
  if (navbarToggler && navLinks) {
    navbarToggler.addEventListener("click", function () {
      navLinks.classList.toggle("active");
    });
  }

  // ===== Contact Form Validation =====
  const userNameInput  = document.getElementById("userName");
  const userPhoneInput = document.getElementById("userPhone");
  const userEmailInput = document.getElementById("userEmail");
  const messageInput   = document.getElementById("message");

  const userNameReqError  = document.getElementById("userNameReq");
  const userEmailReqError = document.getElementById("userEmailReq");
  const userPhoneReqError = document.getElementById("userPhoneReq");
  const messageReqError   = document.getElementById("messageReq");

  const Btn  = document.getElementById("btnSubmit");
  const Form = document.getElementById("form");

  function validateField(input, regex, errorElement, correctPlaceholder, incorrectPlaceholder) {
    if (!input) return false;
    if (regex.test((input.value || "").trim())) {
      input.classList.add("is-valid");
      input.classList.remove("is-invalid");
      if (errorElement) errorElement.classList.add("d-none");
      input.placeholder = correctPlaceholder;
      return true;
    } else {
      input.classList.add("is-invalid");
      input.classList.remove("is-valid");
      if (errorElement) errorElement.classList.remove("d-none");
      input.placeholder = incorrectPlaceholder;
      return false;
    }
  }

  function validateUserName() {
    return validateField(
      userNameInput,
      /^([A-Za-z ]{3,15})$/,
      userNameReqError,
      "Your Name",
      "Name must be between 3 and 15 characters"
    );
  }

  function validateUserEmail() {
    return validateField(
      userEmailInput,
      /^([A-Za-z][.A-Za-z]{2,15}[0-9]{0,4}@(gmail|yahoo|outlook)\.com)$/,
      userEmailReqError,
      "Your Email",
      "Enter a valid email (e.g., example@gmail.com)"
    );
  }

  function validateUserPhone() {
    return validateField(
      userPhoneInput,
      /^(010|011|012)[0-9]{8}$/,
      userPhoneReqError,
      "Your Phone",
      "Enter a valid phone number (e.g., 01012345678)"
    );
  }

  function validateUserMessage() {
    return validateField(
      messageInput,
      /^([A-Za-z ]{2,200})$/,
      messageReqError,
      "Your Message",
      "Message must be between 2 and 200 characters"
    );
  }

  function validateAllFields() {
    const isNameValid    = validateUserName();
    const isEmailValid   = validateUserEmail();
    const isPhoneValid   = validateUserPhone();
    const isMessageValid = validateUserMessage();

    if (Btn) {
      Btn.disabled = !(isNameValid && isEmailValid && isPhoneValid && isMessageValid);
    }
  }

  if (userNameInput)  userNameInput.addEventListener("input", validateAllFields);
  if (userEmailInput) userEmailInput.addEventListener("input", validateAllFields);
  if (userPhoneInput) userPhoneInput.addEventListener("input", validateAllFields);
  if (messageInput)   messageInput.addEventListener("input", validateAllFields);

  if (Form) {
    Form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!Btn || !Btn.disabled) {
        Swal.fire({
          icon: "success",
          title: "Submitted!",
          text: "Form submitted successfully.",
        });
        Form.reset();
        validateAllFields();
      } else {
        Swal.fire({
          icon: "error",
          title: "Check the form",
          text: "Please fill out all fields correctly.",
        });
      }
    });
  }

  // ===== Quiz links (login gating + smart redirect) =====
  const isLoggedIn = !!window.APP_IS_LOGGED_IN;
  const loginUrl   = window.APP_LOGIN_URL || "/auth/login";

  document.querySelectorAll(".quiz-link").forEach(function (quizLink) {
    quizLink.addEventListener("click", function (event) {
      if (!isLoggedIn) {
        event.preventDefault();
        const category = quizLink.dataset.quiz;
        // حفظ الكاتيجوري علشان نرجع له بعد اللوجين
        try { localStorage.setItem("redirectCategory", category); } catch(e) {}

        Swal.fire({
          title: "Login Required",
          text: "You need to log in to access this quiz!",
          icon: "warning",
          confirmButtonText: "Go to Login",
          showCancelButton: true,
          cancelButtonText: "Cancel"
        }).then((result) => {
          if (result.isConfirmed) {
            window.location.href = loginUrl;
          }
        });
      }
    });
  });

  // بعد ما يعمل Login ويرجع للهوم، و لو فيه category محفوظة نودّيه عليها
  try {
    const pendingCategory = localStorage.getItem("redirectCategory");
    if (pendingCategory && isLoggedIn) {
      const targetLink = document.querySelector(`.quiz-link[data-quiz="${pendingCategory}"]`);
      localStorage.removeItem("redirectCategory");
      if (targetLink) {
        window.location.href = targetLink.getAttribute("href");
      }
    }
  } catch(e) {}

  // ===== Footer subscribe =====
  const emailInput = document.querySelector(".subscribe input");
  const subscribeButton = document.querySelector(".subscribe button");

  function validateEmail() {
    if (!emailInput || !subscribeButton) return;
    const emailValue = emailInput.value || "";
    const emailPattern = /^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$/;
    subscribeButton.disabled = !emailPattern.test(emailValue);
  }

  if (emailInput) {
    emailInput.addEventListener("input", validateEmail);
    // init
    validateEmail();
  }

  function clearInput() {
    if (!emailInput || !subscribeButton) return;
    emailInput.value = "";
    subscribeButton.disabled = true;
    Swal.fire({
      icon: "success",
      title: "Subscribed",
      text: "Thanks for subscribing!",
      timer: 1500,
      showConfirmButton: false
    });
  }

  if (subscribeButton) {
    subscribeButton.addEventListener("click", clearInput);
  }
});
