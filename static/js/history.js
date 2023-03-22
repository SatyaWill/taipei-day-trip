let history_model = {
    order: [],
    get_order(){
        return fetch('/api/order/history').then(res=>res.json()).then(data=>{
            this.order = data.data;
        })
    }
}

let history_view = {
    init(name, data){
        if(!data) 
        return el_qr(".headline").innerHTML = `您還沒有訂單資料，<a href="/">點我回首頁</a> 預定行程。`
        el_qr(".headline").innerHTML = `${name}您好，您的所有訂單如下：`
        data.forEach(i => {
            const section = add_el("section");
            const pic_box = add_el("div");
            const pic_inset = add_el("div");
            const info_box = add_el("div");
            const more = add_el("div");
            const contact_box = add_el("div");
            const time = i.time === "morning" ? "9:00-16:00" : "13:00-20:00";
            pic_box.innerHTML = `<img src = "${i.image}" class="history_img">`
            info_box.innerHTML = `
            <h3>${i.att_name}</h3>
            <h3>${i.date} ${time}</h3>
            <h4>訂單編號：<span>${i.order_number}</span></h4>
            <h4>地點：<span>${i.address}</span></h4>`
            more.innerHTML = "<b>聯絡資訊📲</b>"
            contact_box.innerHTML = `
            <h4>姓名：<span>${i.name}</span></h4>
            <h4>信箱：<span>${i.order_email}</span></h4>
            <h4>手機：<span>${i.phone}</span></h4>`
            section.className = "sec_1"
            pic_box.className = "history_pic";
            pic_inset.className ="pic_inset"
            info_box.className = "history_info";
            more.className="more";
            contact_box.setAttribute("hidden", true);
            more.onclick = ()=>{
                contact_box.toggleAttribute("hidden");
            };
            pic_box.appendChild(pic_inset);
            section.appendChild(pic_box);
            section.appendChild(info_box);
            info_box.appendChild(more);
            info_box.appendChild(contact_box);
            el("history_data").appendChild(section);
        });
    }
}

let history_controller = {
    init: async function(){
        await model.get_user_info();
        await history_model.get_order();
        if(!model.user_info) return location.href="/";
        history_view.init(model.user_info.name, history_model.order);
    },
}

history_controller.init();
