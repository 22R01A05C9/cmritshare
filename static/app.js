async function validateUser(e) {
    e.preventDefault()
    const email = document.getElementById('emailAddress').value;
    const password = document.getElementById('password').value;
    if (email === '' || password === '') {
        console.log('email or password is empty')
        return;
    }
    fetch('/login_api', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: email, password: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect) {
            window.location.href = data.redirect;
        } else if (data.error) {
            alert(data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}
