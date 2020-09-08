document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');

    var  btn = document.getElementById("add_btn");
    if (btn) {
        btn.addEventListener('click', add_friend);
    }
});

function add_friend() {
    document.querySelector("#add_btn").setAttribute("disabled", true);
    var profile_username = JSON.parse(document.getElementById('profile_username').textContent);
    console.log(profile_username)

    fetch('/add_friend', {
        method: 'POST',
        body: JSON.stringify({
            body: profile_username
        })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result)
    });
};

function accept_friend(username) {
    console.log(username)
    fetch('/accept_friend', {
        method: 'POST',
        body: JSON.stringify({
            body: username
        })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result)
        window.location.href = 'http://127.0.0.1:8000/friend_request';
    });
};


