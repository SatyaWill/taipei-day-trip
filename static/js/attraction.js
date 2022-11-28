let id = new URL(location.href).pathname.split("/")[2];
fetch('/api/attraction/'+ id).then((res) => {
    return res.json();
    }).then(function(data){
        detail = data.data;
        images = detail.images;
        images.forEach((item, index) =>{
            let slide = document.getElementById("slide");
            let dotbox = document.getElementsByClassName("dots")[0];
            let img = document.createElement('img');
            img.className = "slide_pic";
            img.src = item;
            img.style.display = "none";
            let dot = document.createElement("span");
            dot.className = "dot";
            dot.onclick = "dots(index+1)";
            slide.appendChild(img);
            dotbox.appendChild(dot);
        });
        let slide_pic = document.getElementsByClassName("slide_pic");
        slide_pic[0].style.display = "block";
        let att_name = document.getElementsByClassName("att_name")[0];
        let cat_mrt = document.getElementsByClassName("cat_mrt")[0];
        let desc = document.getElementsByClassName("desc")[0];
        let address = document.getElementsByClassName("address")[0];
        let transport = document.getElementsByClassName("transport")[0];
        att_name.textContent = detail.name;
        let mrt
        if(detail.mrt){
            mrt = detail.mrt
          }else{mrt = "無"};
        cat_mrt.textContent = detail.category+" at "+mrt;
        desc.textContent = detail.description;
        address.textContent = detail.address;
        transport.textContent = detail.transport;
    });

let slide_pic = document.getElementsByClassName("slide_pic");
let dot = document.getElementsByClassName("dot");
let slideIndex = 1;
function slides(n){ // 前後PIC控制
    showSlides(slideIndex += n);
};
function dots(n){ // 原點PIC控制
    showSlides(slideIndex = n);
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

let morning = document.getElementById("morning");
let afternoon = document.getElementById("afternoon");
let content =  document.getElementsByClassName("content")[1];
morning.addEventListener("click", event=>{
 content.textContent = "新台幣 2000 元";
});
afternoon.addEventListener("click", event=>{
    content.textContent = "新台幣 2500 元";
});