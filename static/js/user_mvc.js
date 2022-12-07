const el = (name) => document.getElementById(name);
const el_tag = (name) => document.getElementsByTagName(name);
const el_class = (name) => document.getElementsByClassName(name);
const el_qr = (name) => document.querySelector(name);
let model = {
    user_info: null,
    signin_res: null,
    signup_res: null,
    signout_res: null,
    get_user_info(){
        return fetch("/api/user/auth").then(res=>res.json()).then(data=>{
            this.user_info = data.data;
        })
    },
    signin(){
        const data = {
            email: el("signin_email").value,
            password: el("signin_password").value
        }
        return fetch('/api/user/auth', {
            method: "PUT",
            body: JSON.stringify(data),
            headers: {
                "content-type": "application/json",
            }
        }).then(res=>res.json()).then(data=>{
            this.signin_res = data;
        })
    },
    signup(){
        const data = {
            name: el("signup_name").value,
            email: el("signup_email").value,
            password: el("signup_password").value
        }
        return fetch('/api/user', {
            method: "POST",
            credentials: "include",
            body: JSON.stringify(data),
            cache: "no-cache",
            headers: {
                "content-type": "application/json",
            }
        }).then(res=>res.json()).then(data=>{
            this.signup_res = data;
        })
    },
    signout(){
        return fetch('/api/user/auth', {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
            }
        }).then(res=>res.json()).then(data=>{
            this.signout_res = data;
        })
    },
};

let view = {
    // 已登入者：顯示登出按鈕
    show_signout_btn(){
        el("nav_signin_up").className = "hidden";
        el("nav_signout").className = "item"
    },
    // 未登入者：登入/註冊 dialog 開關控制
    dialog_control(){
        const signin_close = el_class("close")[0]
        const signup_close = el_class("close")[1]
        el("nav_signin_up").addEventListener("click", function(){
            el("signin_dialog").show();
        });
    
        el("to_signup").addEventListener("click", function(){
            el("signin_dialog").close();
            el("signup_dialog").show();
        });
        el("to_signin").addEventListener("click", function(){
            el("signup_dialog").close();
            el("signin_dialog").show();
        });
        signin_close.addEventListener("click", function(){
            el("signin_dialog").close();
        });
        signup_close.addEventListener("click", function(){
            el("signup_dialog").close();
        });
    },
    
    // 註冊dialog：成功/失敗訊息
    signup(data){
        const signup_info = el("signup_info");
        if(Object.keys(data)[0] === "ok"){
            signup_info.className = "ok";
            signup_info.textContent = "註冊成功，請重新登入";
        }
        else{
            signup_info.className = "error";
            signup_info.textContent = data["message"];
        }
    },
    // 登入dialog：成功/失敗訊息
    signin(data){
        if(Object.keys(data)[0] === "ok"){
            el("signin_dialog").close();
            el("signin_out_ok").innerHTML = "<h1>登入成功<br>歡迎回來~😊</h1>";
            el("signin_out_ok").show();
        }
        else{
            el("signin_info").className = "error";
            el("signin_info").textContent = data["message"];
        }
    },
    // 登出成功訊息
    signout(data){
        if(data.ok){
            el("signin_out_ok").innerHTML = "<h1>登出成功<br>歡迎再來喔~😊</h1>";
            el("signin_out_ok").show();
        }
    },
};
    
let contorller = {
    init: async function(){
        await model.get_user_info();
        if(model.user_info){
            view.show_signout_btn();
        }else{
            view.dialog_control();
        };
    },
    signup: async function(){
        await model.signup();
        view.signup(model.signup_res);
    },
    signin: async function(){
        await model.signin();
        await view.signin(model.signin_res);
        if(Object.keys(model.signin_res)[0] === "ok"){
            setTimeout(() => {
                location.reload()
            }, 500);
        }
    },
    signout:  async function(){
        await model.signout();
        await view.signout(model.signout_res);
        if(model.signout_res.ok){
            setTimeout(() => {
                location.reload()
            }, 500);
        }
    },
};
// 判斷使否登入，顯示"註冊/登入"或"登出系統"按鈕
contorller.init();
// 註冊
el("signup_form").addEventListener("submit", function(e){
    contorller.signup();
    e.preventDefault();
})
// 登入
el("signin_form").addEventListener("submit", function(e){
    contorller.signin();
    e.preventDefault();
})
// 登出
function signout(){
    contorller.signout();
}
