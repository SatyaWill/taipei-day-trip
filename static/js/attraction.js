/*目錄
串接後端資料
載入資料fx
照片輪播控制
日期預設當天、上/下午不同導覽費用
預約行程
*/

// 串接後端資料
const id = new URL(location.href).pathname.split("/")[2];
fetch('/api/attraction/'+ id).then(res=>res.json()).then(data=>{
        detail = data.data;
        load(detail);
    })

// 載入資料fx
function load(detail){
    images = detail.images;
    images.forEach((item, index) => {
        const img = document.createElement('img');
        const dot = document.createElement("span");
        img.className = "slide_pic";
        img.src = item;
        img.style.display = "none";
        dot.className = "dot";
        dot.onclick = function(){
            let n = index+1;
            showSlides(slideIndex=n);
        };
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
};

// 照片輪播控制
const slide_pic = document.getElementsByClassName("slide_pic");
const dot = document.getElementsByClassName("dot");
let slideIndex = 1;
function slides(n){ // 前後控制
    showSlides(slideIndex += n);
};
function showSlides(n){ 
    let i;
    if(n > slide_pic.length){slideIndex = 1 }
    if(n < 1){ slideIndex = slide_pic.length }
    for(i = 0; i < slide_pic.length; i++){
        slide_pic[i].style.display = "none";
    }
    for(i = 0; i < dot.length; i++){
        dot[i].className = dot[i].className.replace(" active", "");
    }
    slide_pic[slideIndex - 1].style.display = "";
    dot[slideIndex - 1].className += " active";
}

// 日期預設當天、上/下午不同導覽費用
el("date").valueAsDate = new Date();
el("morning").addEventListener("click", event=>{
    el("price").value = 2000;
});
el("afternoon").addEventListener("click", event=>{
    el("price").value = 2500;
});
