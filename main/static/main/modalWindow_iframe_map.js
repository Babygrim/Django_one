var modal_map = document.getElementById("mapModal");
var btn = document.getElementsByClassName("map-btn");
var span_map = document.getElementsByClassName("close map")[0];
var frame = document.getElementById("mapFrame");

for (i = 0; i < btn.length; i++){
    btn[i].onclick = function() {
    var shop = this.dataset.shop
    if (shop == "silpo"){
        frame.src = "https://www.google.com/maps/embed?pb=!1m12!1m8!1m3!1d82354.65230490985!2d23.9376343!3d49.8315044!3m2!1i1024!2i768!4f13.1!2m1!1z0YHRltC70YzQv9C-INC70YzQstGW0LI!5e0!3m2!1suk!2sua!4v1683574054378!5m2!1suk!2sua";
    }
    if (shop == "glove"){
        frame.src = "https://www.google.com/maps/embed?pb=!1m16!1m12!1m3!1d20586.678837231328!2d24.00839944661923!3d49.83616540437692!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!2m1!1z0YDRg9C60LDQstC40YfQutCwINC70YzQstGW0LI!5e0!3m2!1suk!2sua!4v1683574222292!5m2!1suk!2sua";
    }
    if (shop == "atb"){
        frame.src = "https://www.google.com/maps/embed?pb=!1m16!1m12!1m3!1d82354.37466272445!2d23.937634155921394!3d49.83166745171905!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!2m1!1z0LDRgtCxINC70YzQstGW0LI!5e0!3m2!1suk!2sua!4v1683574110730!5m2!1suk!2sua";
    }
    modal_map.style.display = "block";
    }
}

// When the user clicks anywhere outside of the , close it
document.addEventListener('click', function(event) {
  if (event.target == modal_map) {
    modal_map.style.display = "none";
  }
})

// When the user clicks on <span_qty> (x), close the modal_qty
span_map.onclick = function() {
  modal_map.style.display = "none";
}








