function showElement() {
    element = document.getElementById('hidden-div');
    element.style.visibility = "visible";
    element.style.opacity = "1";
    element.style.transition = "all 2s";
}


function FbotonOn(data) {
    
    if (data == "This password is too short. It must contain at least 8 characters."){
        data = "Пароль повинен містити хоча б вісім символів!"
    }
    else if (data == "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters."){
        data = "Некоректний логін!"
    }
    else if (data == "The password is too similar to the username."){
        data = "Пароль занадто схожий на логін!"
    }
    else if (data == "The two password fields didn’t match."){
        data = "Паролі не збігаються!"
    }
    else if (data == "This password is entirely numeric."){
        data = "Пароль не може складатись лише з цифр!"
    }
    else if (data == "A user with that username already exists."){
        data = "Користувач з таким іменем уже існує!"
    }
    else if (data == "This password is too common."){
        data = "Пароль занадто простий!"
    }
    else if (data == "Please enter a correct username and password. Note that both fields may be case-sensitive."){
        data = "Введені дані некоректні!"
    }

    document.getElementById('texto').innerHTML = data;
    showElement()
    setTimeout(function empythetag() {
        element = document.getElementById('hidden-div');
        element.style.transition = "all 2s";
        element.style.visibility = "hidden";
        element.style.opacity = "0";
      }, 5000);
    
}
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