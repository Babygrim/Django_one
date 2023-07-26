var updateBtns = document.getElementsByClassName('card-update-btn')
var modal_update = document.getElementById("updateModal");
var span_update = document.getElementsByClassName("close qty update")[0];
var decrease = document.getElementsByClassName('decrease-qty-update')
var increase = document.getElementsByClassName('increase-qty-update')
var input_field_update = document.getElementById('qty-value-update')
var submit_final_update = document.getElementById('submit-qty-update')
var caption_update = document.getElementById('quantity-caption-update');
var array_exclude = ['пакет', 'ФАСОВАНА', 'ПАКЕТ', 'фасована', 'уп', 'УП', 'упаковка', 'УПАКОВКА', 'Сітка', 'сітка', 'СІТКА']
var array_exclude2 = ['шт']
var grams = ['100г', '0.1кг','0,1кг']
var kilo = "кг"

for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        productId = this.dataset.item
        shop_name = this.dataset.shop
        user_id = this.dataset.user
        curr_qty = this.dataset.qty
        item_name = this.dataset.name_item
        item_price = this.dataset.price
        modal_update.style.display = "block";
        check3 = grams.some(v => item_price.includes(v));
        check4 = grams.some(v => item_name.includes(v));
        check5 = item_name.includes(kilo);
        check6 = item_price.includes(kilo);
        check7 = array_exclude.some(v => item_name.includes(v));
        check8 = array_exclude2.some(v => item_price.includes(v));
        caption_update.innerHTML = "Кількість (шт)";
        input_field_update.value = parseInt(curr_qty)
        if(check3 == true || check4 == true){
          caption_update.innerHTML = "Вага (г)";
          input_field_update.value = parseInt(curr_qty)
        }
        else if((check5 == true || check6 == true) && check7 == false && check8 == false){
          caption_update.innerHTML = "Вага (кг)";
          input_field_update.value = parseFloat(curr_qty)
        }
    })
}

// When the user clicks anywhere outside of the , close it
window.onclick = function(event) {
  if (event.target == modal_update) {
    modal_update.style.display = "none";
  }
}
// When the user clicks on <span_update> (x), close the modal_update
span_update.onclick = function() {
  modal_update.style.display = "none";
}


decrease[0].addEventListener('click', function(){
  if(caption_update.innerHTML == "Кількість (шт)" && parseInt(input_field_update.value) > 1){
    input_field_update.value = (parseInt(input_field_update.value) - 1)
  }
  else if (caption_update.innerHTML == "Вага (г)" && parseInt(input_field_update.value) > 50){
    input_field_update.value = (parseInt(input_field_update.value) - 50)
  }
  else if (caption_update.innerHTML == "Вага (кг)" && parseFloat(input_field_update.value) > 0.1){
    input_field_update.value = (parseFloat(input_field_update.value) - 0.1).toFixed(1)
  }
})

increase[0].addEventListener('click', function(){
  if(caption_update.innerHTML == "Кількість (шт)"){
      input_field_update.value = (parseInt(input_field_update.value) + 1)
  }
  else if (caption_update.innerHTML == "Вага (г)"){
    if (parseInt(input_field_update.value) < 50){
      input_field_update.value = 50
    }
    else{
      input_field_update.value = (parseInt(input_field_update.value) + 50)
    }
  }
  else if (caption_update.innerHTML == "Вага (кг)"){
    input_field_update.value = (parseFloat(input_field_update.value) + 0.1).toFixed(1)
  }
})

submit_final_update.addEventListener('click', function(){
    modal_update.style.display = "none";
    var quantity = parseFloat(input_field_update.value);
    edit(user_id, productId, shop_name, quantity)
})


var cards = document.getElementsByClassName('content-wishlist')

for (i = 0; i < cards.length; i++){
    card_name = cards[i].getElementsByClassName('price-to-change')
    card_quantity = cards[i].getElementsByClassName('quantity element')
    card_real_qty = cards[i].getElementsByClassName('hidden_qty')
    card_price = cards[i].getElementsByClassName('price element')
    check3 = grams.some(v => card_name[0].innerHTML.includes(v));
    check4 = grams.some(v => card_price[0].innerHTML.includes(v));
    check5 = card_name[0].innerHTML.includes(kilo);
    check6 = card_price[0].innerHTML.includes(kilo);
    card_quantity[0].innerHTML = card_quantity[0].innerHTML + "Кількість - " + parseInt(card_real_qty[0].value) + " шт";
    if(check3 == true || check4 == true){
      card_quantity[0].innerHTML = "Вага - " + parseInt(card_real_qty[0].value) + " г";
    }
    else if(check5 == true || check6 == true){
      card_quantity[0].innerHTML = "Вага - " + card_real_qty[0].value + " кг";
}
}



function edit(user_id, productId, shop_name, quantity){
  var url = '/edit_wish_list/'

  fetch(url, {
      method:'POST',
      headers:{
          'Content-Type':'application/json',
          'X-CSRFToken': csrftoken
      },
      body: JSON.stringify({'productId': productId , 'shop-name': shop_name, 'user': user_id, 'quantity': quantity})
  })
  .then((response) => {
      return response.json()
  })
  .then((data) => {
      window.location.reload()
  })  
}
