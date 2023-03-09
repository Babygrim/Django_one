from django.shortcuts import render, HttpResponse
from .models import *

import requests
from bs4 import BeautifulSoup
from .forms import ProductForm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Create your views here.
def about_page(request):
    return render(request, 'main/about.html')

def parse_arsen(product_name):
    print('print arsen feedback',product_name)

def parse_atb(product_name):
    print('print atb feedback', product_name)
    
def parse_silpo(product_name):
    print('print сільпо feedback', product_name)
    response_title = []
    response_price = []
    response_volume = []
    response_pictures = []
    options = webdriver.ChromeOptions()
    options.add_argument("--disable")
    options.add_argument("--headless")
    driver = webdriver.Chrome('C:\\Users\\Pogkopi\\Downloads\\chromedriver', options=options)
    driver.implicitly_wait(10)
    driver.get(f'https://shop.silpo.ua/search/all?find={product_name}')    
    overall = driver.find_elements(By.CLASS_NAME, "new-product-list-item")
    
    for tit in overall:
        price = tit.find_element(By.CLASS_NAME, "current-integer")
        if price:
            volume = tit.find_element(By.CLASS_NAME, "product-weight")
            title = tit.find_element(By.CLASS_NAME, "product-title")
            image = tit.find_element(By.TAG_NAME, "img")
            image_source = image.get_attribute("src")
            response_price.append(price.text)
            response_title.append(title.text)
            response_volume.append(volume.text)
            response_pictures.append(image_source)
            print('here', image_source)
            db_object = search_engine(shop_name = 'Сільпо', product_name = title.text, product_price = price.text, product_volume = volume.text, product_image = image_source)
            db_object.save()
        else:
            continue
        
    driver.quit()
    mylist = zip(response_title, response_price, response_volume, response_pictures)
    return mylist

def choose_shop(shops, product_name):
    response_title = []
    response_price = []
    response_volume = []
    response_pictures = []
    silpo = []
    arsen = []
    atb = []
    
    if shops == 'Сільпо':
        silpo = parse_silpo(product_name)
    if shops == 'Арсен':
        arsen = parse_arsen(product_name)
    if shops == 'АТБ':
        parse_atb(product_name)
            
    if silpo:    
        for i, x, z, m in silpo:
            response_title.append(i)
            response_price.append(x)
            response_volume.append(z)
            response_pictures.append(m)
    if arsen:
        for x, y, z, m in arsen:
            response_title.append(x)
            response_price.append(y)
            response_volume.append(z)
            response_pictures.append(m) 
    if atb:
        for x, y, z, m in arsen:
            response_title.append(x)
            response_price.append(y)
            response_volume.append(z)
            response_pictures.append(m) 
         
    mylist = zip(response_title, response_price, response_volume, response_pictures)
    return mylist
        
def search_db(request):
    if request.method == 'POST':
        product_name = request.POST['product_name']
        shops = request.POST.getlist('shop')
        response_title = []
        response_price = []
        response_volume = []
        response_pictures = []
        if shops:
            for shop in shops:
                response = []
                for i in range(1, int(len(product_name)/2)):
                    if search_engine.objects.filter(shop_name = shop, product_name__icontains = product_name[i:len(product_name)-i]).exists():
                        response = search_engine.objects.filter(shop_name = shop, product_name__icontains = product_name[i:len(product_name)-i])
                        search_engine.objects.filter(shop_name = shop, product_name__icontains = product_name[i:len(product_name)-i]).update(search_date = datetime.datetime.now())
                        break
                    else:
                        continue
                    
                if response:
                    for item in response:
                        response_title.append(item.product_name)
                        response_price.append(item.product_price)
                        response_volume.append(item.product_volume)
                        response_pictures.append(item.product_image)
                    continue
                else:
                    response = choose_shop(shop, product_name)
                    for i, x, z, f in response:
                        response_title.append(i)
                        response_price.append(x)
                        response_volume.append(z)
                        response_pictures.append(f)
                    continue
                    
        else:
            shops.append("Сільпо")
            shops.append("Арсен")
            shops.append("АТБ")
            for shop in shops:
                response = []
                for i in range(1, int(len(product_name)/2)):
                    if search_engine.objects.filter(shop_name = shop, product_name__icontains = product_name[i:len(product_name)-i]).exists():
                        response = search_engine.objects.filter(shop_name = shop, product_name__icontains = product_name[i:len(product_name)-i])
                        search_engine.objects.filter(shop_name = shop, product_name__icontains = product_name[i:len(product_name)-i]).update(search_date = datetime.datetime.now())
                        break
                    else:
                        continue
                    
                if response:
                    for item in response:
                        response_title.append(item.product_name)
                        response_price.append(item.product_price)
                        response_volume.append(item.product_volume)
                        response_pictures.append(item.product_image)
                    continue
                else:
                    response = choose_shop(shop, product_name)
                    for i, x, z, f in response:
                        response_title.append(i)
                        response_price.append(x)
                        response_volume.append(z)
                        response_pictures.append(f)
                    continue
                                                          
        mylist = zip(response_title, response_price, response_volume, response_pictures)
        context = {
                    'mylist': mylist,
        }      
        return render(request, 'main/get_price.html', context)                                  
    else:
        return render(request, 'main/get_price.html')

