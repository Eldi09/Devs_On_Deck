let devLogin = document.getElementById("devLogin");
let is_valid = true;

// devRegForm.onsubmit = function (e) {
//     e.preventDefault();
//     if (is_valid) {
//         var form = new FormData(devRegForm);
//         fetch("http://127.0.0.1:5000/create_dev", {
//         method: "POST",
//         body: form,
//         })
//         .then((response) => response.json())
//         .then((data) => console.log(data));
//         let first_name = document.forms["devRegForm"]["first_name"].value;
//         let success = document.getElementById("success");
//         success.classList.add("text-success");
//         success.innerHTML = first_name + " you are registered successfully";
//         setTimeout(location.reload.bind(location), 5000);
//     }
// };
function check_email() {
    let email = document.forms["devLogin"]["login_email"].value;
    let regex = new RegExp("[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]");
    if (!regex.test(email)) {
        document.getElementById("emailError").innerHTML = "*Invalid email";
    } else if (getUser(email)) {
        document.getElementById("emailError").innerHTML = ""
    }else{
        document.getElementById("emailError").innerHTML = "*Email does not exist";
    }
}
async function getUser(email) {
    fetch("http://127.0.0.1:5000/getUser")
        .then((response) => response.json())
        .then((data) => {
        console.log(data);
        for (i = 0; i < data.length; i++) {
            if (email == data[i]["email"]) {
                is_valid = true;
                return is_valid;
            }
            else{
                is_valid = false;
            }
        }
        });
    console.log(is_valid);
    return is_valid;
}