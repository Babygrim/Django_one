var prices = document.getElementsByClassName('total_price_tag')
var shops = document.getElementsByClassName('shop_name')
var array = new Array()
var regex = /[+-]?\d+(\.\d+)?/g;
var min = 10000;

for (i = 0; i < prices.length; i++){
    var floats = (prices[i].innerHTML).match(regex);
    array.push(parseFloat(floats[0]));
}

for (j = 0; j < array.length; j++){
    if (array[j] < min && array[j] != 0){
        min = array[j];
    }
}

prices[(array.indexOf(min))].style.textShadow = "#00af17 1px 0 10px"
prices[(array.indexOf(min))].style.color = "#39FF7B"
shops[(array.indexOf(min))].style.textShadow = "#00af17 1px 0 10px"
shops[(array.indexOf(min))].style.color = "#39FF7B"


var item = document.getElementsByClassName('content-wishlist')
var elem_from_input = document.getElementById('hidden_query_array')
var query = elem_from_input.value.replace(/'/g, '')
query = query.replace(/\[/g, '')
query = query.replace(/]/g, '')
query = query.split(', ')

array_of_elements = new Array()
temp = new Array()

for (f = 0; f < query.length; f++){
    for (k = 0; k < item.length; k++){
        val = item[k].getElementsByClassName('hidden_search')
        if (query[f] == val[0].value){
            temp.push(item[k])
        }
    }
    array_of_elements.push(temp);
    temp = [];
}

var min_price = 9999999;

for (elem of array_of_elements){
    for (i = 0; i < elem.length; i++){
        price = elem[i].getElementsByClassName('price element')
        price = (price[0].innerHTML).match(regex)
        quantity = elem[i].getElementsByClassName('quantity element')
        quantity = (quantity[0].innerHTML).match(regex);
        if (price[0] * quantity[0] < min_price){
            min_price = price[0] * quantity[0]
            elem_to_color = elem[i];
        }
    }
    elem_to_color.style.borderColor = "#00af17";
    elem_to_color.style.boxShadow = "0 0 1em #00af17";
    min_price = 9999999
}

elem_to_color.style.borderColor = "#00af17";
elem_to_color.style.boxShadow = "0 0 1em #00af17";
