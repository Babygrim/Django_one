var modal_qty = document.getElementById("qtyModal");
var span_qty = document.getElementsByClassName("close qty")[0];
var updateBtns = document.getElementsByClassName('add-to-cart')
var decrement = document.getElementsByClassName('decrease-qty')
var increment = document.getElementsByClassName('increase-qty')
var input_field = document.getElementById('qty-value')
var submit_final = document.getElementById('submit-qty')
var caption = document.getElementById('quantity-caption');
var array_exclude = ['пакет', 'ФАСОВАНА', 'ПАКЕТ', 'фасована', 'уп', 'УП', 'упаковка', 'УПАКОВКА', 'Сітка', 'сітка', 'СІТКА']
var array_exclude2 = ['шт']
var grams = ['100г', '0.1кг','0,1кг']
var kilo = "кг"




for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        productId = this.dataset.product
        shop_name = this.dataset.shop
        user_id = this.dataset.user
        item_name = this.dataset.item
        item_price = this.dataset.price
        input_field.value = 1
        check3 = grams.some(v => item_price.includes(v));
        check4 = grams.some(v => item_name.includes(v));
        check5 = item_name.includes(kilo);
        check6 = item_price.includes(kilo);
        check7 = array_exclude.some(v => item_name.includes(v));
        check8 = array_exclude2.some(v => item_price.includes(v));
        caption.innerHTML = "Кількість (шт)";
        if(check3 == true || check4 == true){
          caption.innerHTML = "Вага (г)";
          input_field.value = 100;
        }
        else if((check5 == true || check6 == true) && check7 == false && check8 == false){
          caption.innerHTML = "Вага (кг)";
        }
        modal_qty.style.display = "block";
    })
}







// When the user clicks anywhere outside of the , close it
window.addEventListener('click', function(event) {
  if (event.target == modal_qty) {
    modal_qty.style.display = "none";
  }
},true);

// When the user clicks on <span_qty> (x), close the modal_qty
span_qty.onclick = function() {
  modal_qty.style.display = "none";
}


decrement[0].addEventListener('click', function(){
  if(caption.innerHTML == "Кількість (шт)" && parseInt(input_field.value) > 1){
    input_field.value = (parseInt(input_field.value) - 1)
  }
  else if (caption.innerHTML == "Вага (г)" && parseInt(input_field.value) > 0){
    input_field.value = (parseInt(input_field.value) - 50);
  }
  else if (caption.innerHTML == "Вага (кг)" && parseFloat(input_field.value) > 0.1){
    input_field.value = (parseFloat(input_field.value) - 0.1).toFixed(1)
  }
})

increment[0].addEventListener('click', function(){
  if(caption.innerHTML == "Кількість (шт)"){
      input_field.value = (parseInt(input_field.value) + 1)
  }
  else if (caption.innerHTML == "Вага (г)"){
    input_field.value = (parseInt(input_field.value) + 50)
  }
  else if (caption.innerHTML == "Вага (кг)"){
    input_field.value = (parseFloat(input_field.value) + 0.1).toFixed(1)
  }
})

submit_final.addEventListener('click', function(){
    modal_qty.style.display = "none";
    var quantity = parseFloat(input_field.value)
    updateWishList(productId, shop_name, user_id, quantity)
})



function updateWishList(productId, shop_name, user_id, quantity){

  var url = '/update_item/'
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
      FbotonOn(data)
  })
}