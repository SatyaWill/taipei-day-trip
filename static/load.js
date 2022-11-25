let details; // 製作需載入的element
let main = document.getElementById('main');
function load(details){
    details.forEach(item =>{
        let picbox = document.createElement('div');
        let img = document.createElement('img');
        let name = document.createElement('div');
        let mrt;
        if(item.mrt){
          mrt = item.mrt
        }else{mrt = "無"};
        picbox.className = "picbox";
        name.className = "title";
        img.className = "pic";
        img.src = item.images[0];
        name.innerHTML= "<p>"+item.name+"</p>";
        picbox.innerHTML = "<p>"+mrt+"</p><p>"+item.category+"</p>";
        picbox.appendChild(img);
        picbox.appendChild(name);
        main.appendChild(picbox);
    })
};

function loadpage(keyword_str=""){  // 載入頁面的fx
    let page = 0;
    let options = {
        root: null,
        rootMargin: "0px",
        threshold: [0, 0.95]
    };
    const observer = new IntersectionObserver(callback, options);
    let target = document.querySelector('footer');
    observer.observe(target);
    function callback(entries, observer){
        entries.forEach((entry) => {
            if(entry.isIntersecting && entry.intersectionRatio >= 0.95) {
                fetch('/api/attractions?page='+ page +keyword_str).then((res) => {
                    return res.json();
                    }).then(function(data){
                        details = data.data;
                        if(details.length != 0){
                            load(details);
                            page = data.nextPage;
                        }else{
                            main.innerHTML = "查無資料"
                        };
                        observer.unobserve(target);
                    })
                    .then(() => {
                        if(page) {
                            observer.observe(target);
                            let search_icon = document.querySelector("#search_icon");
                            search_icon.addEventListener("click", function(){
                                if(search.value){
                                    observer.unobserve(target);
                                };
                            })
                        } else {
                            observer.unobserve(target);
                        }
                    })
            };
        }
    )};
};

// 載入頁面
loadpage();

// 查詢景點功能
let search = document.querySelector("#search");
let search_dialog = document.querySelector("#search_dialog");
let search_form = document.querySelector("#search_form");
let search_item = document.querySelectorAll(".search_item");
// 景點分類
fetch('/api/categories').then((res) => { 
    return res.json();
    }).then(function(data){
        data.data.forEach(item =>{
            let search_item = document.createElement('button');
            search_item.className = "search_item";
            search_item.textContent= item;
            search_form.appendChild(search_item);
            search_item.addEventListener('click', event => {
                search.value = event.target.textContent;
              });
    });
});
// 景點分類dialog
document.addEventListener("click", event => {
    if(search == event.target || search.contains(event.target)){
        search_dialog.show();
    }if(!search_dialog.contains(event.target) && !search.contains(event.target)){
        search_dialog.close();
    }
});

function search_att(){
    if(search.value){
        main.innerHTML="";
        page = 0;
        loadpage("&keyword="+search.value);
    }
};