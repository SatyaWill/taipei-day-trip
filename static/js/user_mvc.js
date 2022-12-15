const el = (name) => document.getElementById(name);
const el_tag = (name) => document.getElementsByTagName(name);
const el_class = (name) => document.getElementsByClassName(name);
const el_qr = (name) => document.querySelector(name);
const el_qrs = (name) => document.querySelectorAll(name);
let model = {
    user_info: null,
    signin_status: null,
    signup_res: null,
    signout_status: null,
    get_user_info(){
        return fetch("/api/user/auth").then(res=>res.json()).then(data=>{
            this.user_info = data.data;
        })
    },
    signin(){
        return fetch('/api/user/auth', {
            method: "PUT",
            body: JSON.stringify({
                    email: el("signin_email").value,
                    password: el("signin_password").value
                }),
            headers: {"content-type": "application/json"}
        }).then(res=>{this.signin_status = res.status;})
    },
    signup(){
        return fetch('/api/user', {
            method: "POST",
            credentials: "include",
            body: JSON.stringify({
                    name: el("signup_name").value,
                    email: el("signup_email").value,
                    password: el("signup_password").value
                }),
            cache: "no-cache",
            headers: {"content-type": "application/json"}
        }).then(res=>res.json()).then(data=>{
            this.signup_res = data;
        })
    },
    signout(){
        return fetch('/api/user/auth', {
            method: "DELETE",
            headers: {"Content-Type": "application/json"}
        }).then(res=>{this.signout_status = res.status;})
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
        el("nav_signin_up").onclick = ()=>{el("signin_dialog").showModal();};

        signin_close.onclick = ()=>{el("signin_dialog").close();};
        signup_close.onclick = ()=>{el("signup_dialog").close();};

        el("signup_dialog").onclose = ()=>{
            el("signup_form").reset();
            const els = el_qrs("#check_email, #check_password, #signup_info, #signup_email_hint, #signup_password_hint");
            els.forEach(el=>{el.className = "hidden"});
            el("signup_email").className = "sign"
            el("signup_password").className = "sign"
        };
        el("signin_dialog").onclose = ()=>{
            el("signin_form").reset();
            const els = el_qrs("#signin_info, #signin_email_hint, #signin_password_hint");
            els.forEach(el=>{el.className = "hidden"});
            el("signin_email").className = "sign"
            el("signin_password").className = "sign"
        };

        el("to_signup").onclick = ()=>{
            el("signin_dialog").close();
            el("signup_dialog").showModal();
        };
        el("to_signin").onclick = ()=>{
            el("signup_dialog").close();
            el("signin_dialog").showModal();
        };

        // 註冊驗證提示 ==============================================
        el("signup_email").onchange = ()=>{
            if (el("signup_email").value !== ""){
                const email_rule = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,4}$/;
                if (!email_rule.test(el("signup_email").value)){
                    el("signup_email").className = "error_input"
                    el("check_email").className = "error";
                    el("check_email").innerHTML= "✖";
                    el("signup_email_hint").innerHTML="格式不符";
                    el("signup_email_hint").className = "error";
                }else{
                    el("signup_email").className = "sign"
                    el("check_email").className = "hidden";
                    el("signup_email_hint").className = "hidden";
                }
            }
        };

        el("signup_password").onchange = ()=>{
            if (el("signup_password").value !== ""){
                const password_rule = /^(?=.*[a-zA-Z])(?=.*[0-9]).{6,}$/;
                if (!password_rule.test(el("signup_password").value)){
                    el("signup_password").className = "error_input"
                    el("check_password").className = "error";
                    el("check_password").innerHTML= "✖";
                    el("signup_password_hint").innerHTML="需為英、數組合，且至少6字以上";
                    el("signup_password_hint").className = "error";
                }else{
                    el("signup_password").className = "sign";
                    el("check_password").className = "hidden";
                    el("signup_password_hint").className = "hidden";
                }
            }
        };
        // 登入驗證提示 ==============================================
        el("signin_email").onchange = ()=>{
            if (el("signin_email").value !== ""){
                const email_rule = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,4}$/;
                if (!email_rule.test(el("signin_email").value)){
                    el("signin_email").className = "error_input"
                    el("signin_email_hint").innerHTML="格式不符";
                    el("signin_email_hint").className = "error";
                }else{
                    el("signin_email").className = "sign"
                    el("signin_email_hint").className = "hidden";
                }
            }
        };

        el("signin_password").onchange = ()=>{
            if (el("signin_password").value !== ""){
                const password_rule = /^(?=.*[a-zA-Z])(?=.*[0-9]).{6,}$/;
                if (!password_rule.test(el("signin_password").value)){
                    el("signin_password").className = "error_input"
                    el("signin_password_hint").innerHTML="需為英、數組合，且至少6字以上";
                    el("signin_password_hint").className = "error";
                }else{
                    el("signin_password").className = "sign";
                    el("signin_password_hint").className = "hidden";
                }
            }
        };
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
        if(data === 200){
            el("signin_dialog").close();
            el("signin_out_ok").innerHTML = "<h1>登入成功<br>歡迎回來~😊</h1>";
            el("signin_out_ok").showModal();
        }
        else{
            el("signin_info").className = "error";
            el("signin_info").textContent = "帳號或密碼錯誤";
        }
    },
    // 登出成功訊息
    signout(data){
        if(data === 200){
            el("signin_out_ok").innerHTML = "<h1>登出成功<br>歡迎再來喔~😊</h1>";
            el("signin_out_ok").showModal();
        }
    },
};
    
let contorller = {
    init: async function(){
        await model.get_user_info();
        if(model.user_info){
            view.show_signout_btn();
            el("nav_booking").onclick = ()=>{
                location.href = "/booking";
            }
        }else{
            view.dialog_control();
            el("nav_booking").onclick = ()=>{
                el("signin_dialog").showModal();
            }
        };
    },
    signup: async function(){
        await model.signup();
        view.signup(model.signup_res);
    },
    signin: async function(){
        await model.signin();
        await view.signin(model.signin_status);
        if(model.signin_status === 200) 
        return setTimeout(() => {location.reload()}, 500);
    },
    signout:  async function(){
        await model.signout();
        await view.signout(model.signout_status);
        if(model.signout_status === 200)
        return setTimeout(() => {location.reload()}, 500);
    },
};
// 判斷使否登入，顯示"註冊/登入"或"登出系統"按鈕
contorller.init();
// 註冊
el("signup_form").onsubmit = (e)=>{
    contorller.signup();
    e.preventDefault();
};
// 登入
el("signin_form").onsubmit = (e)=>{
    contorller.signin();
    e.preventDefault();
};
// 登出
el('nav_signout').onclick = ()=>{
    contorller.signout();
};

