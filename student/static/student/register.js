let cond1=false, cond2=false, cond3=false, cond4=false;
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".userid").forEach(userid => check_id(userid));
    document.querySelectorAll(".password").forEach(password => check_pass(password));
    document.querySelectorAll(".repassword").forEach(repassword => check_repass(repassword));
    document.querySelectorAll("input").forEach(input => check_conds(input));
    document.querySelectorAll(".registerButton").forEach(button => display_form(button));
    document.querySelectorAll(".email").forEach(email => check_email(email));
});

function check_id(userid) {
    userid.addEventListener("change", () =>{
            fetch(`student/check_id/${userid.value}`)
            .then(response => response.json())
            .then(data => {
            if(!data.is_valid) {
                document.querySelector("#message").innerHTML = "Invalid Student ID";
                cond1=false;
            }
            else {
                document.querySelector("#message").innerHTML = "";
                cond1=true;
            }
        });
    }); 
}

function check_pass(password) {
    password.addEventListener("change", () => {
        // checking if password's length is more than 8
        if (password.value.length < 8) {
            document.querySelector("#message").innerHTML = "Password must be atleast 8 characters long";
            cond2 = false
            return;
        }
        //checking if password contains a special character
        const special_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-',
         '_', '+', '=', '{', '}', '[', ']', '|', '\\', ';', ':', "'", '"', '<', '>', ',', '.', '?', '/', '~', '`'];
        let flag = true;
          for (i in password.value){
            for (j in special_chars) {
                if (password.value[i] == special_chars[j]) {
                    flag = false;
                    break;
                }
            }
        }
        if (flag) {
            document.querySelector("#message").innerHTML = "Password must contain at least one special character";
            cond2 = false
            return;
        }
        //checking if password contains a capital letter
        flag = true;
        for (i in password.value) {
            if (password.value.charCodeAt(i) >= 65 && password.value.charCodeAt(i) <= 90) {
                flag = false;
                break;
            }
        }
        if (flag) {
            document.querySelector("#message").innerHTML = "Password must contain at least one capital letter";
            cond2 = false
            return;
        }
        //checking if password contains a number
        flag = true;
        for (i in password.value) {
            if (password.value.charCodeAt(i) >= 48 && password.value.charCodeAt(i) <= 57) {
                flag = false;
                break;
            }
        }
        if (flag) {
            document.querySelector("#message").innerHTML = "Password must contain at least one numeric value";
            cond2 = false
            return;
        }
        document.querySelector("#message").innerHTML = "";
        cond2 = true;
    });
}

function check_repass(repassword) { 
    repassword.addEventListener("change", () => {
        document.querySelector("#message").innerHTML = "The confirmation password does not match";
        cond3=false;
        document.querySelectorAll(".password").forEach(password => {
            if (repassword.value == password.value) {
                document.querySelector("#message").innerHTML = "";
                cond3=true;
                return;
            }
        });
    });
}

//  Password@12

function check_conds(input) {
    input.addEventListener("change", ()=> {
        if (cond1 && cond2 && cond3 && cond4) {
            document.querySelectorAll(".submitButton").forEach(button=> {
                button.disabled = false;
            });
        }
        else {
            document.querySelectorAll(".submitButton").forEach(button=> {
                button.disabled = true;
            });
        }
        console.log(cond1, cond2, cond3, cond4);
    });
}

function display_form(button) {
    button.addEventListener("click", () => {
        if (button.value == "staff") {
            document.querySelector("#studentForm").style.display="none";
            if (document.querySelector("#staffForm").style.display == "block") {
                document.querySelector("#staffForm").style.display="none";
            }
            else {
                document.querySelector("#staffForm").style.display="block";
            }
        }
        if (button.value == "student") {
            document.querySelector("#staffForm").style.display="none";
            if (document.querySelector("#studentForm").style.display == "block") {
                document.querySelector("#studentForm").style.display="none";
            }
            else {
                document.querySelector("#studentForm").style.display="block";
            }
        }
    })
}

function check_email(email) {
    email.addEventListener("change", ()=> {
        document.querySelector("#message").innerHTML = "Validating your e-mail ID...";
        fetch(`https://mailcheck.p.rapidapi.com/?domain=${email.value}`, {
            method: 'GET',
	        headers: {
	        	'X-RapidAPI-Key': 'cb1dc8746fmshe31b265b3d3887dp19000fjsn63ccb9676755',
	        	'X-RapidAPI-Host': 'mailcheck.p.rapidapi.com'
	        }
        })
        .then(response=>response.json())
        .then(data=> {
            console.log(data);
            if (data.valid) {
                document.querySelector("#message").innerHTML = "";
                cond4 = true;
            }
            else {
                document.querySelector("#message").innerHTML = "Invalid email. Please provide a valid mail ID";
                cond4 = false;
            }
        })
    })
}