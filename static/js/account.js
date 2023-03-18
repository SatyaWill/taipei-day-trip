const account_model = {
    data: [],
    async get_data(){
        return fetch('/api/account').then(res=>res.json()).then(data=>{
            this.data = data.data;
        })
    },
    async edit_name(){
        return fetch('/api/name', {
            method: "PATCH",
            body: JSON.stringify({
                    name: el("new_name").value,
                }),
            headers: {"content-type": "application/json"}
        })
    },
    async edit_phone(){
        return fetch('/api/phone', {
            method: "PATCH",
            body: JSON.stringify({
                    phone: el("new_phone").value
                }),
            headers: {"content-type": "application/json"}
        })
    },
    async edit_password(){
        return fetch('/api/password', {
            method: "PATCH",
            body: JSON.stringify({
                old_password: el("old_password").value,
                new_password: el("new_password").value,
                }),
            headers: {"content-type": "application/json"}
        })
    },
}

const account_view = {
    input_status: false,
    init(data){
        el("account_data").className = "";
        el("account_email").value = data.email;
        el("account_name").value = data.name;
        el("account_phone").value = data.phone;

        see_pw(".account_eyes", "open_account_eyes") // 看密碼label 
        
        function dialog_control(item){ // dialog 開關
            el(`edit_${item}_icon`).onclick = ()=> el(`edit_${item}_dialog`).showModal();
            el(`edit_${item}_dialog`).onclose = ()=> el(`edit_${item}_form`).reset();
        }
        dialog_control("name")
        dialog_control("phone")

// 修改按鈕 disabled控制、click修改btn => 再驗證 ============================
        input_check("name", "姓名需2字以上")
        input_check("phone", "手機10碼")
        input_check("password", "需為英、數組合至少6字", "old")
        input_check("password", "需為英、數組合至少6字")
          
        function input_check(item, errhint, type="new") {
            const items = item === "password" ? ["new_password", "old_password"] : [`new_${item}`]
            const can_toggle = () => {
                input_status = items.every(i => el(i).dataset.valid === "true")
                el(`edit_${item}_btn`).disabled = !input_status;
            }
        
            const id =  el(`${type}_${item}`)    
            id.addEventListener("keyup", ()=>{
                const { value, dataset, classList } = id
                const isSame = item !== "password" ? value === data[item] : 
                               el("old_password").value === el("new_password").value
                const err = !RE[item].test(value.trim());

                dataset.valid = !err && !isSame;
                err_hint("edit", item, err || isSame , err ? errhint : "不可跟舊資料一樣"),
                classList.toggle("error_input", err || isSame),
                can_toggle()
            });
            el(`edit_${item}_btn`).onclick = e => (
                e.preventDefault(),
                !input_status || account_controller.edit_item(item)
            );
            item !== "phone" || id.addEventListener("input", ()=> id.value = id.value.replace(/\D/g, ''));
          }       
    },
}

const account_controller = {
    async init(){
        await model.get_user_info();
        await account_model.get_data();
        if(!model.user_info) return location.href="/";
        account_view.init(account_model.data);
    },
    async edit_item(item) {
        const res = await account_model[`edit_${item}`]();
        const data = await res.json()
        if (res.status === 400) return err_hint("edit", item, true, data.message)
        if (res.status === 200) {
            const i = item === "name" ? "名字" : item === "phone" ? "手機號碼" : "密碼"
            hint_dialog(`<h1>${i}修改成功~😊</h1>`);
            setTimeout(() => { location.reload() }, 500);
        }
    },
}

account_controller.init();
