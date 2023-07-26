var wishbutton = document.getElementsByClassName('wish');

  for(var i = 0; i < wishbutton.length; i++){
      wishbutton[i].addEventListener('click', function(){
          var user_id = this.dataset.user
          wishlist(user_id)
      })
  }


function wishlist(user_id){
    var url = '/check_wish_list/'
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
        if (data == 'True') {
            location.href = '/wishlist/'
        } 
        else {
            FbotonOn(data)
        }
    })  
}