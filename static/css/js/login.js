document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("togglePassword");
    const passwordInput = document.getElementById("id_password");
    const icon = toggleBtn.querySelector("i");

    toggleBtn.addEventListener("click", () => {
        const isVisible = passwordInput.type === "text";
        passwordInput.type = isVisible ? "password" : "text";
        icon.classList.toggle("bi-eye");
        icon.classList.toggle("bi-eye-slash");
    });

    // Animación de entrada
    const card = document.querySelector(".login-card");
    card.classList.add("animate__animated", "animate__fadeInUp");
});
