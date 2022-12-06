/*目錄：
取得登入狀態
登入/註冊 dialog 控制
註冊
登入
登出
登出 登入訊息 dialog */

const el = (name) => document.getElementById(name);
// 取得登入狀態 ================================================
function get_user_info(){
    fetch("/api/user/auth").then(res=>res.json()).then(data=>{
        if(data.data){
            el("nav_signin_up").className = "hidden";
            el("nav_signout").className = "item";
        }else{
            dialog_control();
        }
    })
};
get_user_info();

// 登入/註冊 dialog 控制 ================================================
function dialog_control(){
    const signin_close = document.getElementsByClassName("close")[0]
    const signup_close = document.getElementsByClassName("close")[1]
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
    el("signup_form").addEventListener("submit", function(e){
        signup();
        e.preventDefault();
    })
    el("signin_form").addEventListener("submit", function(e){
        signin();
        e.preventDefault();
    })
}

// 註冊 ================================================
function signup(){
    const data = {
        name: el("signup_name").value,
        email: el("signup_email").value,
        password: el("signup_password").value,
    }
    fetch('/api/user', {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(data),
        cache: "no-cache",
        headers: {
            "content-type": "application/json",
        }
    }).then(res=>res.json()).then(data=>{
        const signup_info = el("signup_info");
        if (Object.keys(data)[0] === "ok"){
            signup_info.className = "ok";
            signup_info.textContent = "註冊成功，請重新登入";
        }
        else{
            signup_info.className = "error";
            signup_info.textContent = data["message"];
        }
      })
};  

// 登入 ================================================
function signin(){
    const data = {
        email: el("signin_email").value,
        password: el("signin_password").value,
    }
    fetch('/api/user/auth', {
        method: "PUT",
        body: JSON.stringify(data),
        headers: {
            "content-type": "application/json",
        }
    }).then(res=>res.json()).then(data=>{
        if (Object.keys(data)[0] === "ok"){
            el("signin_dialog").close();
            const msg = "<h1>登入成功<br>歡迎回來~😊</h1>";
            signin_out_dialog(msg);
        }
        else{
            el("signin_info").className = "error";
            el("signin_info").textContent = data["message"];
        }
      })
}; 

// 登出 ================================================
function signout(){
    fetch('/api/user/auth', {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        }
      }).then(res=>res.json()).then(data=>{
        if(data.ok){
            const msg = "<h1>登出成功<br>歡迎再來喔~😊</h1>";
            signin_out_dialog(msg);
        }
      }) 
};

// 登出/入訊息 dialog ================================================
async function signin_out_dialog(msg){
    el("signin_out_ok").innerHTML= msg;
    await el("signin_out_ok").show();
    setTimeout(() => {
        location.reload()
    }, 500);
}

