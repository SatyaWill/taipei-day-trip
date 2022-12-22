let booking_model = {
    booking: {},
    del_status: null,
    pay_status: null,
    get_data(){
        return fetch('/api/booking').then(res=>res.json()).then(data=>{
            this.booking = data.data;
        })
    },
    del_data(){
        return fetch('/api/booking', {
            method: "DELETE",
            headers: {"Content-Type": "application/json"}
        }).then(res=>{this.del_status = res.status;})
    },
    // 付款 (TapPay) 取得資料 
    pay(info){TPDirect.card.getPrime((result) => {
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
            if(this.pay_status===200)
            return location.href=`/thankyou?number=${data.data.number}`;
            
        })
    })},
}

let booking_view = {
    send_order: {},
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
// ==== 信用卡資訊 (TapPay) ====================================================
        TPDirect.setupSDK(126850, 'app_tjaCOqhGDmAWl3IZvwnHKCkTAljYzk7JLFqXMCJHic4rg6fOpU01bfvXjaZj', 'sandbox');
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
        let booking_name_status = true;
        let booking_email_status = true;
        let booking_phone_status = false;
        let card_status = false;
        function can_pay_toggle(){
            if(booking_name_status*booking_phone_status*booking_email_status*card_status)
                return el("to_pay").removeAttribute('disabled');
            el("to_pay").setAttribute('disabled', true);
        }
        // 聯絡姓名確認
        el("booking_name").addEventListener("change", function(){
            if (el("booking_name").value == ""){
                el("booking_name_hint").innerHTML = "<b>請輸入聯絡姓名</b>";
                el("booking_name_hint").className = "error";
                booking_name_status = false;
                
            }else{
                el("booking_name_hint").className = "hidden";
                booking_name_status = true;
            }
            can_pay_toggle();
        });
        // email驗證
        el("booking_email").addEventListener("change", function(){
            if (el("booking_email").value !== ""){
                const email_rule = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,4}$/;
                if (!email_rule.test(el("booking_email").value)){
                    el("booking_email_hint").innerHTML = "<b>格式不符，請確認</b>";
                    el("booking_email_hint").className = "error";
                    el("booking_email").classList.add("error");
                    booking_email_status = false;
                }else{
                    el("booking_email_hint").className = "hidden";
                    el("booking_email").classList.remove("error");
                    booking_email_status = true;
                }
            }
            can_pay_toggle();
        });
        // 手機驗證
        el("booking_phone").addEventListener("change", function(){
            if (el("booking_phone").value !== ""){
                const phone_rule = /^09\d{8}$/;
                if (!phone_rule.test(el("booking_phone").value)){
                    el("booking_phone_hint").innerHTML = "<b>格式不符，請確認</b>";
                    el("booking_phone_hint").className = "error";
                    el("booking_phone").classList.add("error");
                    booking_phone_status = false;
                }else{
                    el("booking_phone_hint").className = "hidden";
                    el("booking_phone").classList.remove("error");
                    booking_phone_status = true;
                }
            }
            can_pay_toggle();
        });
        // 信用卡驗證 (TapPay)
        TPDirect.card.onUpdate(update=>{
            if(update.canGetPrime){
                card_status = true
            }else{
                card_status = false
            }
            can_pay_toggle();
        });
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
    pay(){
        booking_model.pay(booking_model.booking);
    }
}

booking_controller.init();
el("delete_booking").addEventListener("click",()=>{
    booking_controller.del_booking();
});

el("to_pay").addEventListener("click",()=>{
    booking_controller.pay();
});