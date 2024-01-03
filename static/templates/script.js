// script.js
document.getElementById("signupForm").addEventListener("submit", function (event) {
    event.preventDefault();
    signup();
});

async function signup() {
    const id = document.getElementById("signupUserId").value;
    const username = document.getElementById("signupUsername").value;
    const password = document.getElementById("signupPassword").value;
    const email = document.getElementById("signupEmail").value;
    console.log(id);
    console.log(username);
    console.log(email);
    console.log(password);

    const response = await fetch("/user/home", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            id: id,
            username: username,
            password: password,
            email: email
        })
    });

    const data = await response.json();
    if (response.ok) {
        window.location.href = "/welcome";
    } else {
        alert(data.message);
    }
}
