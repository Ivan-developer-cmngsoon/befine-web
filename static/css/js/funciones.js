document.addEventListener('DOMContentLoaded', function () {
    const passwordInput = document.getElementById('password');
    const toggleButton = document.getElementById('togglePassword');

    if (toggleButton && passwordInput) {
        toggleButton.addEventListener('click', function () {
            const tipo = passwordInput.type === 'password' ? 'text' : 'password';
            passwordInput.type = tipo;

            const icon = toggleButton.querySelector('i');
            icon.classList.toggle('bi-eye');
            icon.classList.toggle('bi-eye-slash');
        });
    }
});
