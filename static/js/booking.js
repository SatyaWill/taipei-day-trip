let booking_model = {
    data: [],
    del_status: null,
    get_data(){
        return fetch('/api/booking').then(res=>res.json()).then(data=>{
            this.data = data.data;
        })
    },
    del_data(){
        return fetch('/api/booking', {
            method: "DELETE",
            headers: {"Content-Type": "application/json"}
        }).then(res=>{this.del_status = res.status;})
    },
}

let booking_view = {
    init_user(data){
        el_tag("main")[0].className = "";
        el_qr(".headline").textContent = `您好，${data.name}，待預訂的行程如下：`
        el("booking_name").value = data.name;
        el("booking_email").value = data.email;
    },
    init(data){
        if(!data){
            el("booking_data").innerHTML = "目前沒有任何待預定的行程";
            el("booking_data").className = "";
            return;
        }
        el("booking_data").className = "";
        const att = data.attraction;
        el("booking_img").src = att.image;
        el("booking_title").textContent = `台北一日遊：${att.name}`;
        el("booking_date").textContent = data.date;
        el("booking_time").textContent = data.time === "morning" ? "早上 9 點到下午 4 點" : "下午 1 點到晚上 8 點";
        el("booking_price").textContent = `新台幣 ${data.price} 元`;
        el("booking_address").textContent = att.address;
        el("booking_total").textContent = `總價：新台幣 ${data.price} 元`;
        // input 控制
        el("booking_phone").onkeyup =function() {
            this.value = this.value.replace(/\D/g, '').replace(/^(\d{4})(\d{3})/g, '$1 $2 ');
        }; 
        el("cc_number").onkeyup =function() {
            this.value =this.value.replace(/\D/g, '').replace(/(\d{4})(?=\d)/g,"$1 "); 
        };  
        
        el("cc_exp").onkeyup =function() {
            this.value = this.value.replace(/\D/g, '').replace(/^(\d{2})/g, '$1 / ');
        }; 
        
        el("cc_cvv").onkeyup =function() {
            this.value = this.value.replace(/\D/g, '');
        }; 
    },
}

let booking_controller = {
    init: async function(){
        await model.get_user_info();
        if(!model.user_info) return location.href="/";
        await booking_view.init_user(model.user_info);
        await booking_model.get_data();
        booking_view.init(booking_model.data);
    },
    del_booking: async function(){
        await booking_model.del_data();
        if(booking_model.del_status===200) return location.reload();
    },
}

booking_controller.init();
el("delete_booking").onclick = ()=>{
    booking_controller.del_booking();
};

