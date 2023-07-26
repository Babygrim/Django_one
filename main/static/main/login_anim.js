var username = document.getElementById('reg-username')
var password1 = document.getElementById('reg-password')
var password2 = document.getElementById('reg-password-two')

username.addEventListener("input", function(){
    if (username.value.length < 1 && username.value != ""){
        username.style.borderColor = "#ff4a4a";
        username.style.boxShadow = "0 0 1em #ff4a4a";
    }
    else{
        username.style.borderColor = "#00af17";
        username.style.boxShadow = "0 0 1em #00af17";
    }
    if (username.value == ""){
        username.style.borderColor = "#9ecaed";
        username.style.boxShadow = "0 0 1em #9ecaed";
    }
});


password1.addEventListener("input", function(){
    if (password1.value.length < 8 || (username.value).includes(password1.value)) {
        password1.style.borderColor = "#ff4a4a";
        password1.style.boxShadow = "0 0 1em #ff4a4a";

    }
    else{
        password1.style.borderColor = "#00af17";
        password1.style.boxShadow = "0 0 1em #00af17";
    }
    if (password1.value == ""){
        password1.style.borderColor = "#9ecaed";
        password1.style.boxShadow = "0 0 1em #9ecaed";
    }
});

password2.addEventListener("input", function(){
    if (password1.value != password2.value) {
        password2.style.borderColor = "#ff4a4a";
        password2.style.boxShadow = "0 0 1em #ff4a4a";
    }
    else{
        password2.style.borderColor = "#00af17";
        password2.style.boxShadow = "0 0 1em #00af17";
    }
    if (password2.value == ""){
        password2.style.borderColor = "#9ecaed";
        password2.style.boxShadow = "0 0 1em #9ecaed";
    }
});

username.addEventListener("blur", function(){
    if (username.value == ""){
        username.style.borderColor = "";
        username.style.boxShadow = "";
    }
});


password1.addEventListener("blur", function(){
    if (password1.value == "") {
        password1.style.borderColor = "";
        password1.style.boxShadow = "";
    }
});

password2.addEventListener("blur", function(){
    if (password2.value == "") {
        password2.style.borderColor = "";
        password2.style.boxShadow = "";
    }
});

