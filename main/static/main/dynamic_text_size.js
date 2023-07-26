var h2_elements = document.getElementsByClassName('price-to-change');


for (i = 0; i < h2_elements.length; i++){
    if(h2_elements[i].innerHTML.length >= 40) { // overflow
        h2_elements[i].style.fontSize = '1.1em';
    }
    if (h2_elements[i].innerHTML.length >= 60){
        h2_elements[i].style.fontSize = '1em';
    }
    if (h2_elements[i].innerHTML.length >= 85){
        h2_elements[i].style.fontSize = '0.9em';
    }
}
