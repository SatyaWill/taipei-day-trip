let booking_model = {
    booking: {},
    del_status: null,
    pay_status: null,
    order_number: null,
    async get_data(){
        return fetch('/api/booking').then(res=>res.json()).then(data=>{
            this.booking = data.data;
        })
    },
    async del_data(){
        return fetch('/api/booking', {
            method: "DELETE",
            headers: {"Content-Type": "application/json"}
        }).then(res=>{this.del_status = res.status;})
    },
    // 付款 (TapPay) 取得資料 
    prime() { // 從 callback 非同步，改成 Promise 非同步
        return new Promise((resolve, reject) => {
            TPDirect.card.getPrime((result) => {
                resolve(result);
            })
        })
    },
    pay: async function(info) {
        const result = await this.prime();
        const order_trip = Object.assign({}, info);
        delete order_trip.price;
        if (result.status === 0) 
        return fetch('/api/orders', {
            method: "POST",
            credentials: "include",
            body: JSON.stringify({
                prime: result.card.prime,
                order: {
                    price: info.price,
                    trip: order_trip,
                    contact: {
                        name: el("booking_name").value,
                        email: el("booking_email").value,
                        phone: el("booking_phone").value,
                    }
                }
            }),
            cache: "no-cache",
            headers: {"content-type": "application/json"}
        }).then(res=>{
            this.pay_status = res.status;
            return res.json();
        }).then(data=>{
            this.order_number = data.data.number;
        })
    },
}

let booking_view = {
    send_order: {},
    async init_user(data){
        el_tag("main")[0].className = "";
        el_qr(".headline").textContent = `您好，${data.name}，待預訂的行程如下：`
        el("booking_name").value = data.name;
        el("booking_email").value = data.email;
    },
    async init(data){
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
        el("booking_phone").value = data.phone;
        el("booking_total").textContent = `總價：新台幣 ${data.price} 元`;
// ==== 信用卡資訊 (TapPay) ====================================================
        TPDirect.setupSDK(app_id, app_key, 'sandbox');
        const fields = {
            number: {
                element: '#card-number',
                placeholder: 'xxxx xxxx xxxx xxxx'
            },
            expirationDate: {
                element: '#card-expiration-date',
                placeholder: 'MM / YY'
            },
            ccv: {
                element: '#card-ccv',
                placeholder: 'ccv'
            }
        };
        TPDirect.card.setup({
            fields: fields,
            styles: {
                'input': {},
                'input.ccv': {'font-size': '16px'},
                'input.expiration-date': {'font-size': '16px'},
                'input.card-number': {'font-size': '16px'},
                ':focus': {'color': 'black'},
                '.valid': {'color': 'green'},
                '.invalid': {'color': 'rgba(210, 20, 20, 0.8)'},
                '@media screen and (max-width: 400px)': {
                    'input': {'color': 'orange'}
                }
            },
            isMaskCreditCardNumber: true, // 卡號輸入正確後，顯示前六後四碼卡號
            maskCreditCardNumberRange: {
                beginIndex: 6,
                endIndex: 11
            }
        });

// ===== 聯絡 / 付款資訊 提示、付款 btn 可按控制  =============================================
        function input_check(item) {
            const fields = ["booking_name", "booking_email", "booking_phone", "booking_card"];
            const can_pay = () => el("to_pay").disabled = !fields.every(id => el(id).dataset.valid === "true");
          
            if (item === "card") 
            return TPDirect.card.onUpdate(u=>{ el(`booking_card`).dataset.valid = u.canGetPrime, can_pay()});
            input_event("booking", item, "error", "⚠️", can_pay, "change")
          }
          input_check("name");
          input_check("email");
          input_check("phone");
          input_check("card");
    },
}

let booking_controller = {
    init: async function(){
        await model.get_user_info(); // 未登入者導回首頁
        if(!model.user_info) return location.href="/";
        await booking_view.init_user(model.user_info);
        await booking_model.get_data();
        booking_view.init(booking_model.booking);
    },
    del_booking: async function(){
        await booking_model.del_data();
        if(booking_model.del_status===200) return location.reload();
    },
    pay: async function(){
        await booking_model.pay(booking_model.booking);
        if(booking_model.pay_status===200)
        return location.href=`/thankyou?number=${booking_model.order_number}`;
    }
}

booking_controller.init();
el("delete_booking").onclick = () => booking_controller.del_booking();

el("to_pay").onclick = () => {
    hint_dialog("<h1>付款資訊驗證中<br>請稍候...⏳</h1>")
    booking_controller.pay();
};