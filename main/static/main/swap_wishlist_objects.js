var swapBtn = document.getElementsByClassName("card-edit-btn")
var modal_swap = document.getElementById('swapModal');
var span_swap = document.getElementsByClassName('close swap')[0];
const remove = (sel) => document.querySelectorAll(sel).forEach(el => el.remove());


for (i = 0; i < swapBtn.length; i++){
    swapBtn[i].addEventListener('click', function(){
        var shop = this.dataset.shop
        var search = this.dataset.search
        var elem = this.dataset.element
        var user = this.dataset.user
        modal_swap.style.display = "block";
        fetch_wish(search, shop, elem, user)
    })
}


function fetch_wish(search, shop, elem, user){
    var url = /fetch_wish_list/

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({'search': search, 'shop':shop})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        createCards(data, shop, elem, user)
    })  
}



document.addEventListener('click', function(event) {
    if (event.target == modal_swap) {
        modal_swap.style.display = "none";
        remove(".swap-body");
    }  
})
    

span_swap.onclick = function() {
    modal_swap.style.display = "none";
    remove(".swap-body");
}



function createCards(data, shop, id_to_swap, user){
    var window = document.getElementById('swap-cards-content');
    for(i = 0; i < data.length; i++){
        var body = document.createElement("div");
        body.className = "swap-body";
        var body_content = document.createElement("div");
        body_content.className = "content-swap";
        var image = document.createElement("div");
        image.className = "image";
        var img = document.createElement("img");
        img.src = data[i].product_image;
        image.appendChild(img);
        var h2 = document.createElement("h2");
        h2.className = "price-to-change";
        var swap_body = document.createElement("div")
        swap_body.className = "swap-body_wishlist";
        var text = document.createTextNode(data[i].product_name);
        var span = document.createElement("span");
        span.className = "price element";
        if(shop == 'silpo'){
            var span_txt = document.createTextNode(data[i].product_price + " грн")
        }
        else{
            var span_txt = document.createTextNode(data[i].product_price)
        }
        var btn = document.createElement("button");
        btn.className = "card-swap-btn";
        btn.textContent = "Замінити";
        btn.setAttribute('data-id', data[i].id);
        btn.setAttribute('data-shop', shop);
        btn.setAttribute('data-id_to_swap', id_to_swap);
        btn.setAttribute('data-user', user);
        btn.addEventListener('click', swapItems);
        span.appendChild(span_txt);
        h2.appendChild(text);
        body_content.appendChild(image);
        swap_body.appendChild(span);
        swap_body.appendChild(h2);
        swap_body.appendChild(btn);
        body_content.appendChild(swap_body);
        body.appendChild(body_content);
        window.appendChild(body);
    }
}


function swapItems(){
    element_to_swap = this.dataset.id_to_swap;
    element_id = this.dataset.id;
    shop_name = this.dataset.shop;
    user = this.dataset.user;

    var url = /swap_elements/

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({'id': element_to_swap, 'cur_id':element_id})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        window.location.reload()
    })  

}





