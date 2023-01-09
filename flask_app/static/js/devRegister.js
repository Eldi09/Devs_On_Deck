

let devRegForm = document.getElementById("devRegForm");
let is_valid = false;
function containsNumbers(str) {
    return /\d/.test(str);
}
function onlyLettersAndNumbers(str) {
    return Boolean(str.match(/^(?=.*[a-zA-Z])(?=.*[0-9])/));
}

devRegForm.onsubmit = function (e) {
    e.preventDefault();
    if (is_valid) {
        var form = new FormData(devRegForm)
        fetch("http://127.0.0.1:5000/create_dev", {
            method: "POST",
            body: form,
        })
        .then((response) => response.json())
        .then((data) => console.log(data));
        let first_name = document.forms["devRegForm"]["first_name"].value;
        let success = document.getElementById("success");
        success.classList.add('text-success');
        success.innerHTML = first_name + " you are registered successfully";
        setTimeout(location.reload.bind(location), 5000);
    }
};

function check_fname() {
    let fname = document.forms["devRegForm"]["first_name"].value;
    if (fname.length < 2 || containsNumbers(fname)) {
        document.getElementById("fnameError").innerHTML =
            "*Must be 2 or more characters letters only";
        is_valid = false;
        } else {
        document.getElementById("fnameError").innerHTML = "";
        is_valid = true;
        }
}

function check_lname() {
    let lname = document.forms["devRegForm"]["last_name"].value;
    if (lname.length < 2 || containsNumbers(lname)) {
        document.getElementById("lnameError").innerHTML =
            "*Must be 2 or more characters letters only";
        is_valid = false;
        } else {
        document.getElementById("lnameError").innerHTML = "";
        is_valid = true;
        }
}

function check_psw() {
    let psw = document.forms["devRegForm"]["password"].value;
    if (psw.length < 8 || onlyLettersAndNumbers(psw) == false) {
        document.getElementById("pswError").innerHTML =
            "*Password must be 8 character or longer letters and numbers";
        is_valid = false;
        } else {
        document.getElementById("pswError").innerHTML = "";
        is_valid = true;
        }
}

function check_cpsw() {
    let password = document.forms["devRegForm"]["password"].value;
    let confirmPassword = document.forms["devRegForm"]["confirmPassword"].value;
    if (password == "") {
        document.getElementById("cpswError").innerHTML =
        "*Please put password first";
        is_valid = false;
    } else if (password.length >= 8 && password != confirmPassword) {
        document.getElementById("cpswError").innerHTML =
        "*Confirm passord do not match";
        is_valid = false;
    } else {
        document.getElementById("cpswError").innerHTML = "";
        is_valid = true;
    }
}

function check_email() {
    let email = document.forms["devRegForm"]["email"].value;
    let regex = new RegExp("[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]");
    if (!regex.test(email)) {
        document.getElementById("emailError").innerHTML = "*Invalid email";
        is_valid = false;
    } else if (getUser(email)) {
        document.getElementById("emailError").innerHTML = "";
        is_valid = true
    }
}
async function getUser(email) {
    fetch("http://127.0.0.1:5000/getUser")
        .then((response) => response.json())
        .then((data) => {
        for (i = 0; i < data.length; i++) {
            if (email == data[i]["email"]) {
            document.getElementById("emailError").innerHTML = "*This email already exist";
            is_valid = false;
            } else {
            is_valid = true;
            }
        }
        });
    return is_valid;
}
