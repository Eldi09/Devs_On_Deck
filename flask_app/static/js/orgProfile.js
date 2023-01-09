
// function addSkill(e){
//     let skill = e.innerText;
//     // let list_of_skills = document.createElement('ul');
//     // list_of_skills.setAttribute('id', 'skill_id')
//     let newSkill = document.createElement('li');
//     console.log(document.getElementsByClassName('numOfSkills').length);
//     progress = document.getElementById("skillProgress");
//     percentage_of_progres = progress.innerHTML;
//     if (percentage_of_progres=='0%') {
//         percentage_of_progres = 20;
//     }
//     else if (percentage_of_progres == '20%') {
//         percentage_of_progres = 40;
//     }
//     else if (percentage_of_progres == '40%') {
//         percentage_of_progres = 60;
//     }
//     else if (percentage_of_progres == '60%') {
//         percentage_of_progres = 80;
//     }
//     else if (percentage_of_progres = '80%') {
//         percentage_of_progres = 100
//     }
//     if(document.getElementsByClassName('numOfSkills').length<5){
//         newSkill.classList.add('numOfSkills');
//         newSkill.classList.add("m-2");
//         newSkill.setAttribute('value', skill)
//         newSkill.setAttribute("name","skill_" + document.getElementsByClassName("numOfSkills").length);
//         console.log(skill);
//         newSkill.innerHTML = skill;
//         document.getElementById("skill_id").appendChild(newSkill);
//         progress.classList.add("w_" + percentage_of_progres);
//         progress.innerHTML = percentage_of_progres +'%';
//     }
//     else{
//         alert("You can`t add more than 5 skills")
//     }
// }
let createPos = document.getElementById("addPosition");
let is_valid = false;
let all_selections = [];
let all_frameworks = []
function containsNumbers(str) {
    return /\d/.test(str);
}

function check_name() {
    let name = document.forms["addPosition"]["position_name"].value;
    if (name.length < 5 || containsNumbers(name)) {
        document.getElementById("namePosError").innerHTML =
            "*Must be 5 or more characters letters only";
        is_valid = false;
        } else {
        document.getElementById("namePosError").innerHTML = "";
        is_valid = true;
        }
}

function check_description() {
    let name = document.forms["addPosition"]["description"].value;
    if (name.length < 10) {
        document.getElementById("descriptionError").innerHTML =
        "*Must be 10 or more characters letters only";
        is_valid = false;
    } else {
        document.getElementById("descriptionError").innerHTML = "";
        is_valid = true;
    }
}

function check(e) {
    console.log(document.getElementsByClassName("multiselect").length);
    let count = 0;
    for(i = 0; i < document.getElementsByClassName("multiselect").length; i++){
        let j = document.getElementsByClassName("multiselect")[i];
        if(j.checked == true){
            count++;
        }
    }
    if (count > 5) {
        document.getElementById("multiSelectError").innerHTML = "*You can`t select more than 5 skills";
        e.checked = false;
    }else{
        document.getElementById("multiSelectError").innerHTML ="";
        all_selections.push(e.value);
        console.log(all_selections);
    }
}
function check_frame(e) {
    console.log(document.getElementsByClassName("multiselect_f").length);
    let count = 0;
    for (i = 0; i < document.getElementsByClassName("multiselect_f").length; i++) {
        let j = document.getElementsByClassName("multiselect_f")[i];
        if (j.checked == true) {
        count++;
        }
    }
    if (count > 5) {
        document.getElementById("multiSelectFrameError").innerHTML =
        "*You can`t select more than 5 frameworks";
        e.checked = false;
    } else {
        document.getElementById("multiSelectFrameError").innerHTML = "";
        all_frameworks.push(e.value);
        console.log(all_frameworks);
    }
}
function show_update() {
    let e = document.getElementById("infoDiv");
    if (e.style.display == "none") {
        e.style.display = "inline";
        document.getElementById("scroll").style.display = "none";
        document.getElementById('createPos').style.display = "none";
    }else{
        e.style.display = "none";
        document.getElementById("scroll").style.display = "inline";
    }
    
}

function show_pos() {
    let e = document.getElementById("createPos");
    if (e.style.display == "none") {
        e.style.display = "inline";
        document.getElementById("infoDiv").style.display = "none";
        document.getElementById("scroll").style.display = "none";
    } else {
        e.style.display = "none";
        document.getElementById("scroll").style.display = "inline";
    }
}

async function check_skill() {
    fetch("http://127.0.0.1:5000/check_skill")
        .then((response) => response.json())
        .then((data) => {
            // console.log(data);
            // console.log(all_selections);
            count = 0;
            for (i = 0; i < all_selections.length; i++) {
                for (j = 0; j < data.length; j++) {
                    if (all_selections[i] == data[j]['skill']) {
                        count++;
                        data.splice(j, 1);
                        break;
                    }
                }
                if (count <= 5 && count > 0) {
                    console.log('sucess');
                    is_valid = true;
                }
            }
            if (count == 0) {
                console.log("fail");
                document.getElementById("multiSelectError").innerHTML = "*You should select at least one skill";
                is_valid = false;
            }
        });
}

async function check_framework() {
    fetch("http://127.0.0.1:5000/check_framework")
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            console.log(all_frameworks);
            count = 0;
            for (i = 0; i < all_frameworks.length; i++) {
                for (j = 0; j < data.length; j++) {
                    if (all_frameworks[i] == data[j]["framework"]) {
                        count++;
                        data.splice(j, 1);
                        break;
                    }
                }
                if (count <= 5 && count > 0) {
                    console.log("sucess");
                    is_valid = true;
                }
            }
            if (count == 0) {
            console.log("fail");
            document.getElementById("multiSelectFrameError").innerHTML =
                "*You should select at least one framework";
            is_valid = false;
            }
        });
}

createPos.onsubmit = function (e) {
    e.preventDefault();
    if (is_valid) {
        var form = new FormData(createPos);
        let all = all_selections;
        let all_f = all_frameworks;
        if(all[0] != ""){
            form.append("skill_1", all[0]);
        }
        if (all[1] != "") {
            form.append("skill_2", all[1]);
        }
        if (all[2] != "") {
            form.append("skill_3", all[2]);
        }
        if (all[3] != "") {
            form.append("skill_4", all[3]);
        }
        if(all[4] != ""){
            form.append("skill_5", all[4]);
        }

        if (all_f[0] != "") {
            form.append("frame_1", all_f[0]);
        }
        if (all_f[1] != "") {
            form.append("frame_2", all_f[1]);
        }
        if (all_f[2] != "") {
            form.append("frame_3", all_f[2]);
        }
        if (all_f[3] != "") {
            form.append("frame_4", all_f[3]);
        }
        if (all_f[4] != "") {
            form.append("frame_5", all_f[4]);
        }
        console.log(form);
        // console.log(all);
        fetch("http://127.0.0.1:5000/create_position", {
            method: "POST",
            body: form,
        })
        .then((response) => response.json())
        .then((data) => console.log(data));
        document.getElementById('created').innerHTML = "This position is created succesfully";
        setTimeout(location.reload.bind(location), 5000);
    }
};