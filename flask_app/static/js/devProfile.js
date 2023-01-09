
// function addSkill(e){
//     let skill = e.innerText;
//     let newSkill = document.createElement('small');
//     console.log(document.getElementsByClassName('numOfSkills').length);
//     progress = document.getElementById('skillProgress');
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
//         console.log(skill);
//         newSkill.innerHTML = skill;
//         document.getElementById('devSkills').appendChild(newSkill);
//         progress.classList.add("w_" + percentage_of_progres);
//         progress.innerHTML = percentage_of_progres +'%';
//     }
//     else{
//         alert("You can`t add more than 5 skills")
//     }
// }


function updateInfo() {
    let e = document.getElementById("updateInfo");
    e.classList.toggle("d-none");
    if (!document.getElementById("skillSection").classList.contains("d-none")) {
        document.getElementById("skillSection").classList.add("d-none");
    }
    if (!document.getElementById("appliedPos").classList.contains("d-none")) {
        document.getElementById("appliedPos").classList.toggle("d-none");
    }else{
        document.getElementById("appliedPos").classList.toggle("d-none");
    }
}

function skillSection() {
    let e = document.getElementById('skillSection');
    e.classList.toggle('d-none');
    if (!document.getElementById("updateInfo").classList.contains("d-none")) {
        document.getElementById("updateInfo").classList.add("d-none");
    }
    if (!document.getElementById("appliedPos").classList.contains("d-none")) {
        document.getElementById("appliedPos").classList.toggle("d-none");
    } else {
        document.getElementById("appliedPos").classList.toggle("d-none");
    }
}