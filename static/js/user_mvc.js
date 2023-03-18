const el = (name) => document.getElementById(name);
const el_tag = (name) => document.getElementsByTagName(name);
const el_class = (name) => document.getElementsByClassName(name);
const el_qr = (name) => document.querySelector(name);
const el_qrs = (name) => document.querySelectorAll(name);
const add_el = (name) => document.createElement(name);
const RE = {
    name: /^[^\s]{2,50}$/,
    email: /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$/,
    phone: /^09\d{8}$/,
    password: /^(?=.*[a-zA-Z])(?=.*[0-9]).{6,}$/
}

let model = {
    user_info: [],
    signin_status: null,
    signup_status: null,
    signup_res: [],
    signup_verify_res: [],
    signout_status: null,
    pic_url: "",
    to_s3_status: null,
    member_pic_status: null,
    async get_user_info(){
        return fetch("/api/user/auth").then(res=>res.json()).then(data=>{
            this.user_info = data.data;
        })
    },
    async signin(){
        return fetch('/api/user/auth', {
            method: "PUT",
            body: JSON.stringify({
                    email: el("signin_email").value,
                    password: el("signin_password").value
                }),
            headers: {"content-type": "application/json"}
        }).then(res=>{this.signin_status = res.status;})
    },
    async signup(){
        return fetch('/api/user', {
            method: "POST",
            credentials: "include",
            body: JSON.stringify({
                    name: el("signup_name").value,
                    email: el("signup_email").value,
                    phone: el("signup_phone").value,
                    password: el("signup_password").value
                }),
            cache: "no-cache",
            headers: {"content-type": "application/json"}
        }).then(res=>res.json()).then(data=>{
            this.signup_res = data;
        })
    },
    async signup_verify(token){
        return fetch("/verify/"+token).then(res=>res.json()).then(data=>{
            this.signup_verify_res = data;
        })
    },
    async signout(){
        return fetch('/api/user/auth', {
            method: "DELETE",
            headers: {"Content-Type": "application/json"}
        }).then(res=>{this.signout_status = res.status;})
    },
    async pic_name(){
        return fetch("/api/s3_url").then(res=>res.text()).then(data=>{
            this.pic_url = data;
        });
    }, 
    to_s3: async function(url, dataUrl) {
        const res =  await fetch(url, {
            method: "PUT",
            headers: {"Content-Type": "image/jpeg" },
            body: dataURItoBlob(dataUrl)
        }); 
        return this.to_s3_status = res.status;
    },
    member_pic: async function(url) {
        const res = await fetch("/api/member_pic", {
            method: "PATCH",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                member_pic: url
            }),
        })
        return this.member_pic_status = res.status
    }
};

let view = {
    // 已登入者：顯示會員中心及購物車
    canvas_url: "",
    default_url: "/static/pic/user.png",
    show_btn(data){
        el("nav_signin_up").className = "hidden";
        el("nav_member").className = "item";
        el("nav_booking").className = "item";
        el_qr(".member_name").textContent = data.name;
        el_qrs("#member_pic, #dl_member_pic, #nav_member_pic").forEach(i => {
            i.onerror = ()=> {i.onerror = null, i.src = this.default_url} // 避免錯誤時不斷觸發
            i.src = data.member_pic || this.default_url;
        });

        document.addEventListener("click", event => {
            const dl = el("member_dialog");
            if (dl.contains(event.target)) return dl.show();
            if (!el("nav_member").contains(event.target)) return dl.close();
          });
          
        const pic_dl = el("pic_dialog")
        el("chg_pic_btn").onclick = () => pic_dl.showModal();
        pic_dl.getElementsByClassName("close")[0].onclick = () => pic_dl.close();
    },
    chg_member_pic: async function(){
        el('member_pic_input').addEventListener("change", function(){
            const file = el('member_pic_input').files[0]
            if(!file) return 
            if (!/^image/.test(file.type)) return alert("請選擇圖檔")
            el("save_btn").disabled = !/^image/.test(file.type)
            
            const img = new Image();
            img.onload = () => {
                const picbox = el("dl_member_picbox");
                let canvas = document.createElement('canvas');
                canvas.width = picbox.offsetWidth;
                canvas.height = picbox.offsetHeight;
                canvas.getContext('2d').drawImage(img, 0, 0, canvas.width, canvas.height);
                el('dl_member_pic').src = canvas.toDataURL();
                view.canvas_url = canvas.toDataURL();
                el_qr(".cr-slider").addEventListener('input', function() {
                    const s = -canvas.width*(this.value-1)/2
                    canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
                    canvas.getContext('2d').drawImage(img, s, s, canvas.width * this.value, canvas.height * this.value);
                    el('dl_member_pic').src = canvas.toDataURL();
                    view.canvas_url = canvas.toDataURL();
                });
            }
            img.src = URL.createObjectURL(file);
        })
    },
    // 未登入者：登入/註冊 dialog 開關控制
    dialog_control(){
        el("nav_signin_up").onclick = () =>{el("signin_dialog").showModal();};
        el("to_signup").onclick = () => (el("signin_dialog").close(), el("signup_dialog").showModal());
        el("to_signin").onclick = () => (el("signup_dialog").close(), el("signin_dialog").showModal());
        see_pw(".see_password", "open_eyes") // 看密碼控制
     
        function form_reset(type){
            el(`${type}_dialog`).onclose = ()=>{
                el(`${type}_form`).reset();
                el_qrs(".hint_el").forEach(el=>el.classList.remove("error"));
                el_qrs(".sign").forEach(el=>el.classList.remove("error_input"));
                el(`${type}_eyes`).textContent = "🕶";
                el(`${type}_eyes`).className = "see_password";
            }
        }
        form_reset("signin")
        form_reset("signup")    

        // 註冊 / 登入 驗證提示 ==============================================
        function input_check(type, item, errhint="格式不符", action="change") {
            const items = type === "signin" ? ["email", "password"] : ["name", "email", "password", "phone"]
            const can_toggle = () => el(`${type}_btn`).disabled = !items.every(i => el(`${type}_${i}`).dataset.valid === "true");
            input_event(type, item, "error_input", errhint, can_toggle, action)
          }
          input_check("signup", "name", "姓名長度應2字以上");
          input_check("signup", "email");
          input_check("signup", "phone");
          input_check("signup", "password", "需為英、數組合6字以上", "keyup");
          input_check("signin", "email");
          input_check("signin", "password", "需為英、數組合6字以上", "keyup");
    },
    signup(data) { // 註冊dialog：成功/失敗訊息
        el("hint_dialog").close();
        if (Object.keys(data)[0]==="ok") {
            el("signup_dialog").close();
            hint_close_dialog(`請於半小時內至您的email，點擊驗證連結，完成註冊手續`)
        } else {
            el("signup_info").classList.add("error");
            el("signup_info").innerHTML = data["message"];
        }
      },
    signup_verify(data) {
        const msg = Object.keys(data)[0] === "ok" ? "註冊成功<br/>請重新登入" : data["message"]
        el("hint_close_dialog_content").innerHTML = msg
        el("hint_close_dialog").onclose =()=>{return location.href="/"}
    },
    signin(data){ // 登入dialog：成功/失敗訊息
        if(data === 200){
            el("signin_dialog").close();
            hint_dialog("<h1>登入成功<br>歡迎回來~😊</h1>");
        }
        else{
            el("signin_info").classList.add("error");
            el("signin_info").textContent = "帳號或密碼錯誤";
        }
    },
    signout(data){ // 登出成功訊息
        if(data === 200) return hint_dialog("<h1>登出成功<br>歡迎再來喔~😊</h1>");
    },
};
    
let contorller = {
    init: async function(){
        const token = window.location.search.split('token=')[1];
        if (token) {
            hint_close_dialog("...⏳")
            await model.signup_verify(token)
            view.signup_verify(model.signup_verify_res)
        }
        await model.get_user_info();
        if(model.user_info){
            view.show_btn(model.user_info);
            el("nav_booking").onclick = ()=>location.href = "/booking";
            el("nav_member").onclick = () => el("member_dialog").toggleAttribute("open");
            el("nav_account").onclick = ()=> location.href = "/account";
            el("nav_history").onclick = ()=> location.href = "/history";

            el('rm_btn').disabled = el("dl_member_pic").src.endsWith("user.png");
            el('rm_btn').onclick = (e)=>{
                e.preventDefault()
                e.stopPropagation()
                el('dl_member_pic').src = view.default_url
                el("save_btn").disabled = false
                view.canvas_url = ''
            }
            el("chg_btn").onclick = ()=>{ 
                el('member_pic_input').click();
                view.chg_member_pic();
            }
            el('save_btn').addEventListener("click", async e=>{
                e.preventDefault();
                if (view.canvas_url === '') {
                  await model.member_pic("");
                } else {
                  await model.pic_name();
                  await model.to_s3(model.pic_url, view.canvas_url);
                  await model.member_pic(new URL(model.pic_url.split('?')[0]).pathname.split("/")[2]);
                }
                const message = model.member_pic_status === 200 ? "照片更新成功" : "照片未更新";
                hint_dialog(`<h1>${message}</h1>`);
                setTimeout(() => location.reload(), 500);
              });              
        }else{
            view.dialog_control();
            el("nav_booking").onclick = ()=> el("signin_dialog").showModal();
        };
    },
    signup: async function(){
        await model.signup();
        view.signup(model.signup_res);
    },
    signin: async function(){
        await model.signin();
        view.signin(model.signin_status);
        if(model.signin_status === 200) 
        return setTimeout(() => location.reload(), 500);
    },
    signout:  async function(){
        await model.signout();
        view.signout(model.signout_status);
        if(model.signout_status === 200)
        return setTimeout(() => location.reload(), 500);
    },
};
// 判斷使否登入，顯示"註冊/登入"或"登出系統"按鈕
contorller.init();

el("signup_form").onsubmit = (e)=>{ // 註冊
    hint_dialog("<h1>資料處理中<br>請稍候...⏳</h1>")
    contorller.signup();
    e.preventDefault();
};
el("signin_form").onsubmit = e => { contorller.signin(), e.preventDefault() };
el('nav_signout').onclick = () => contorller.signout();

window.addEventListener("scroll", () => { // 回到上方
    el("go_top").classList.toggle("hidden", window.scrollY < 100)
});
el("go_top").onclick = () => window.scrollTo({ top:0, behavior:"smooth" });

// 關閉 dialog
el_qrs(".close").forEach(i=> i.addEventListener("click", ()=>{
    el_qrs(".sign_dialog").forEach(e=>e.close())
}))   

function dataURItoBlob(dataURI) {
    const binary = atob(dataURI.split(',')[1]);
    let array = [];
    for(let i = 0; i < binary.length; i++) { array.push(binary.charCodeAt(i)) }
    return new Blob([new Uint8Array(array)], {type: 'image/jpeg'});
}

function see_pw(els_name, open_class){
    el_qrs(els_name).forEach(e => {
        e.onclick = () => {
          const el = e.previousElementSibling;
          el.type = el.type === "password" ? "text" : "password";
          e.textContent = el.type === "password" ? "🕶" : "👀";
          e.classList.toggle(open_class, el.type === "text");
        };
    });
}

function input_event(type, item, err_class, errhint, can_toggle, action="change") {
    const id = el(`${type}_${item}`);
    id.addEventListener(action, () => {
      const { value, classList, dataset } = id;
      const err = !RE[item].test(value.trim());
      classList.toggle(err_class, err);
      dataset.valid = !err;
      err_hint(type, item, err, errhint);
      can_toggle();
      !["signup", "signin"].includes(type) || el(`${type}_info`).classList.remove("error");
    });
    item !== "phone" || id.addEventListener("input", ()=> id.value = id.value.replace(/\D/g, ''));
  }
  
function err_hint(type, item, err, err_hint){
    el(`${type}_${item}_hint`).classList.toggle("error", err);
    el(`${type}_${item}_hint`).innerHTML = err_hint;
}

function hint_dialog(msg){
    el("hint_dialog").innerHTML = msg;
    el("hint_dialog").showModal();
}

function hint_close_dialog(msg){
    el("hint_close_dialog_content").innerHTML = msg;
    el("hint_close_dialog").showModal();
}



