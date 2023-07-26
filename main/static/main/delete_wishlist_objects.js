document.getElementById("wishlist-delete").addEventListener('click', function(){
    var user_id = this.dataset.user;
    delete_wishlist(user_id);
});

function delete_wishlist(user_id){
    
    url = "/delete_all/"
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({'user': user_id})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        if (data == 'Список бажаного порожній!') {
            
            history.back();
        }
    })
};  

var card_delete_btns = document.getElementsByClassName("card-delete-btn")

for (i = 0; i< card_delete_btns.length; i++){
    card_delete_btns[i].addEventListener('click', function(){
        var user = this.dataset.user
        var item = this.dataset.item
        var shop = this.dataset.shop
        delete_wishlist_item(user,shop,item)
    })
}
    
function delete_wishlist_item(user, shop, item){
    url = "/delete_item/"

    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({'user':user, 'shop':shop, 'item':item})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        let url1 = '/check_wish_list/'
        fetch(url1, {
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({'user': user})
        })
        .then((response) => {
            return response.json()
        })
        .then((data2) => {
            if (data2 == 'True') {
                window.location.reload();
            } 
            else {
                history.back()
            }
        })  
    })
    
}