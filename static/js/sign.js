// 登入/註冊 dialog
let sign = document.getElementsByClassName("item")[1]
let signin_dialog = document.getElementById("signin_dialog")
let signup_dialog = document.getElementById("signup_dialog")
let to_signup = document.getElementById("to_signup")
let to_signin = document.getElementById("to_signin")
sign.addEventListener("click", event => {
    signin_dialog.show();
});
to_signup.addEventListener("click", event => {
    signin_dialog.close();
    signup_dialog.show();
});
to_signin.addEventListener("click", event => {
    signup_dialog.close();
    signin_dialog.show();
});