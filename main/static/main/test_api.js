var search_form =  document.getElementById("search_form")
var chekbpox1 = document.getElementById('shop1')


search_form.addEventListener('submit', function(e){
	if (chekbpox1.checked == true){
		e.preventDefault();
		search_request = document.getElementById('product_name')
		// silpo
		fetch("https://api.catalog.ecom.silpo.ua/api/2.0/exec/EcomCatalogGlobal", {
		"method": "POST",
		"headers": {
			"content-type": "application/json;charset=UTF-8",
		},
		"body": JSON.stringify({
			"method": "GetSimpleCatalogItems",
			"data": {
				"customFilter": search_request.value,
				"filialId": "2405",
				"skuPerPage": 100,
				"pageNumber": 1
			}
		}),
		}).then((response) => {
			return response.json()
		})
		.then((data) => {
			for(var i = 0; i < data.items.length; i++)
			{
				fetch("/update_silpo_db/", {
				method:'POST',
				headers:{
					'Content-Type':'application/json',
					'X-CSRFToken': csrftoken
				},
				body: JSON.stringify({'product_name': data.items[i].name, 'search_request':search_request.value, 'product_price':data.items[i].price, 'product_image':data.items[i].mainImage, 'weight':data.items[i].unit})
				})
				.then((response) => {
					return response.json()
				})
				.then((data) => {
					
				}) 
			}
			search_form.submit();

			
		})  
	}
	else{
		search_form.submit();
	}
})