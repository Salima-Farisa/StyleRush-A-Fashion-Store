document.getElementById('forgotpasswordform').addEventListener('submit', function (event) {
    let valid = true;

    // Username validation
    const username = document.getElementById('username').value.trim();
    const userError = document.getElementById('usernameerror');
    userError.textContent = '';

    if (!username) {
        userError.textContent = 'Username is required';
        valid = false;
    }

    // New password validation
    const password = document.getElementById('password').value.trim();
    const pass1Error = document.getElementById('pass1error');
    pass1Error.textContent = '';

    if (!password) {
        pass1Error.textContent = 'New password is required';
        valid = false;
    }

    // Confirm password validation
    const password2 = document.getElementById('password2').value.trim();
    const pass2Error = document.getElementById('pass2error');
    pass2Error.textContent = '';

    if (!password2) {
        pass2Error.textContent = 'Please confirm your password';
        valid = false;
    } else if (password && password !== password2) {
        pass2Error.textContent = 'Passwords do not match';
        valid = false;
    }

    // Prevent form submit if invalid
    if (!valid) {
        event.preventDefault();
    }
});
