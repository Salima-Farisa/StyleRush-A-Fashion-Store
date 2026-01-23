document.getElementById('loginform').addEventListener('submit', function(event){
    let valid = true;
    const username = document.getElementById('username').value.trim();
    if (!username) {
        document.getElementById("usererror").textContent = 'Username is required';
        valid = false;
    }
    const pass = document.getElementById('password').value.trim();
    if (!pass) {
    document.getElementById("passerror").textContent = 'Password is required';
        valid = false;
    }
    if(!valid){
        event.preventDefault()
   }
});