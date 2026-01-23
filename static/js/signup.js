document.getElementById('signupForm').addEventListener('submit', function(event) {
   
    let valid = true;
    console.log(valid)

    const error = document.getElementsByClassName('error')

    for (let i = 0; i < error.length; i++) {
            error[i].textContent = '';
        }

    
    // Validate each field individually
    const fname = document.getElementById('fname').value.trim();
    if (!fname) {
        error[0].textContent = 'This field is required';
        valid = false;
    }

    const lname = document.getElementById('lname').value.trim();
    if (!lname) {
        error[1].textContent = 'This field is required';
        valid = false;
    }

    const email = document.getElementById('email').value.trim();
    if (!email) {
        error[2].textContent = 'This field is required';
        valid = false;
    }

    const username = document.getElementById('username').value.trim();
    if (!username) {
        error[3].textContent = 'This field is required';
        valid = false;
    }

    const pass1 = document.getElementById('password1').value.trim();
    
    const pass2 = document.getElementById('password2').value.trim();

    if (!pass1) {
        error[4].textContent = 'This field is required';
        valid = false;
    }

    if (!pass2) {
        error[5].textContent = 'This field is required';
        valid = false;
    }

    if (pass1 && pass2 && pass1 !== pass2) {
        document.getElementById('pass2Error').textContent = 'Passwords do not match';
        valid = false;
    }
    
console.log(valid)
   if(!valid){
    event.preventDefault()
   }
});
