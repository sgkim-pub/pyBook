let signup = document.querySelector("#signup_link");
let signin = document.querySelector("#signin_link");
let signout = document.querySelector("#signout_link");
let myinfo = document.querySelector("#myinfo_link");

function showAndHideNavbarMenu() {
    let authtoken = window.sessionStorage.getItem("authtoken");

    if(authtoken){
        signup.style.display = "none";
        signin.style.display = "none";
    }
    else{
        signout.style.display = "none";
        myinfo.style.display = "none";
    }
}

window.addEventListener("load", showAndHideNavbarMenu);

function signOutHandler() {
    window.sessionStorage.removeItem("authtoken");
    window.sessionStorage.removeItem("username");

    let url = '/home';
    window.location.replace(url);
}

signout.addEventListener("click", signOutHandler);
