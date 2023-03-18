let order_model = {
    order: [],
    async get_order(number){
        return fetch('/api/order/'+number).then(res=>res.json()).then(data=>{
            this.order = data.data;
        })
    }
}

let order_view = {
    init(data){
        if(!data) return location.href="/";
        if(data.status){
            el_qr(".headline").innerHTML = `訂單未付款成功，<a href="/">點我回首頁</a> 重新預定行程。`
            el("booking_data").innerHTML = "";
            el("booking_data").className = "";
            return
        } 
        const att = data.trip.attraction;
        const time = data.trip.time === "morning" ? "9:00-16:00" : "13:00-20:00";
        el_qr(".headline").textContent = `${att.name} (編號${data.number}) 已付款成功，祝順心愉快 😀`
        el("booking_data").className = "";
        el("booking_img").src = att.image;
        el("order_time").textContent = data.trip.date+"　"+time;
        el("order_address").textContent = att.address;
        el("order_name").textContent = data.contact.name;
        el("order_email").textContent = data.contact.email;
        el("order_phone").textContent = data.contact.phone;
    }
}

let order_controller = {
    init: async function(){
        const number = new URL(location.href).searchParams.get('number');
        await model.get_user_info();
        await order_model.get_order(number);
        if(!model.user_info) return location.href="/";
        order_view.init(order_model.order);
    },
}

order_controller.init();
