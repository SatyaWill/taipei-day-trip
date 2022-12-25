const id = new URL(location.href).pathname.split("/")[2];
let slide_index = 1;

let att_model = {
    attraction: null,
    booking_status: null,
    get_attraction(){
        return fetch('/api/attraction/'+ id).then(res=>res.json()).then(data=>{
            this.attraction = data.data;
        })    
    },
    get_booking_res(){
        return fetch('/api/booking', {
            method: "POST",
            credentials: "include",
            body: JSON.stringify({
                attractionId: id,
                date: el("date").value,
                time: el_qr('input[name="time"]:checked').value,
                price: el("price").value
            }),
            cache: "no-cache",
            headers: {
                "content-type": "application/json",
            }
        }).then(res=>{this.booking_status = res.status;})    
    },
};
let att_view = {
    load(detail){
        images = detail.images;
        images.forEach((item, index) => {
            const img = document.createElement('img');
            const dot = document.createElement("span");
            img.className = "slide_pic";
            img.src = item;
            img.style.display = "none";
            dot.className = "dot";
            dot.onclick = ()=>{att_view.show_pic(slide_index=index+1)};
            el("slide").appendChild(img);
            el_class("dots")[0].appendChild(dot);
        });
        el_qr(".slide_pic").style.display = "block";
        el_tag("title")[0].textContent = detail.name;
        el_qr(".att_name").textContent = detail.name;
        let mrt
        if(detail.mrt){
            mrt = detail.mrt
          }else{mrt = "無"};
        el_qr(".cat_mrt").textContent = detail.category+" at "+mrt;
        el_qr(".desc").textContent = detail.description;
        el_qr(".address").textContent = detail.address;
        el_qr(".transport").textContent = detail.transport;
        el_tag("iframe")[0].src="https://maps.google.com.tw/maps?f=q&hl=zh-TW&geocode=&q="+detail.lat+","+detail.lng+"("+detail.name+")"+"&z=16&output=embed&t="
        
        // 日期預設/最小值為當天、選取區間 1 個月 
        let today = new Date();
        const tomorrow = new Date(today.setDate(today.getDate()+1));
        const max_day = new Date(today.setMonth(today.getMonth()+1)).toLocaleDateString('en-ca') ;
        el("date").valueAsDate = tomorrow;
        el("date").min = tomorrow.toLocaleDateString('en-ca');
        el("date").max = max_day;

        // 上/下午不同導覽費用 
        el("morning").onclick = ()=>{el("price").value = 2000};
        el("afternoon").onclick = ()=>{el("price").value = 2500};
        
        //
        el("prev").onclick = ()=>{att_view.show_pic(slide_index-=1)};
        el("next").onclick = ()=>{att_view.show_pic(slide_index+=1)};
    },
    // 照片輪播控制
    show_pic(n){
        const slide_pic = el_class("slide_pic");
        const dot = el_class("dot");
        if(n > slide_pic.length){slide_index = 1};
        if(n < 1){ slide_index = slide_pic.length};
        Array.from(slide_pic).forEach(pic=>{pic.style.display = "none";});
        Array.from(dot).forEach(dot=>{dot.classList.remove("active");});
        slide_pic[slide_index - 1].style.display = "";
        dot[slide_index - 1].className += " active";
    },
    // 預約行程
    booking(booking_status){
        if(booking_status===200) return location.href = "/booking";
        el("signin_dialog").showModal();
    }
};
let att_controller = {
    init: async function(){
        await att_model.get_attraction();
        att_view.load(att_model.attraction);
    },
    booking: async function(){
        await att_model.get_booking_res();
        att_view.booking(att_model.booking_status);
    }
}

att_controller.init();
el("reserve").onclick = ()=>{att_controller.booking()};