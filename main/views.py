from django.shortcuts import render, HttpResponse
import django
django.setup()
from django.db.models import F, Value
from django.db.models.functions import Concat
from main import models
from .models import *
import time
import multiprocessing 
import numpy as np
from bs4 import BeautifulSoup
from .forms import ProductForm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException 


def about_page(request):
    return render(request, 'main/about.html')

def parse_glove(product_name, manage):
    response_title = []
    response_price = []
    response_pictures = []
    options = webdriver.ChromeOptions()
    options.add_argument("--disable")
    #options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument("window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.get(f'https://market.rukavychka.ua/search/?search={product_name}') 
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "content")))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "product-layout")))
    
    for tit in driver.find_elements(By.CLASS_NAME, "product-layout"):
        price = tit.find_element(By.CLASS_NAME, "fm-module-price-new")
        if price:
            image = tit.find_element(By.TAG_NAME, "img")
            product_tit = image.get_attribute("alt")
            if search_engine_glove.objects.filter(product_name = image.get_attribute("alt")).exists():
                search_engine_glove.objects.filter(product_name = image.get_attribute("alt")).update(search_date = datetime.date.today(), product_price = price.text, search_request = Concat(F('search_request'), Value(f'{product_name}')))
            else:
                db_object = search_engine_glove(search_request = product_name, product_name = product_tit.capitalize(), product_price = price.text,  product_image = image.get_attribute("src"))
                db_object.save()
            response_price.append(price.text)
            response_title.append(product_tit.capitalize())
            response_pictures.append(image.get_attribute("src"))
        else:
            continue
    
    driver.quit()
    mylist = zip(response_title, response_price, response_pictures)
    manage.put(mylist)
    
def parse_atb(product_name, manage):
    response_title = []
    response_price = []
    response_pictures = []
    options = webdriver.ChromeOptions()
    options.add_argument("--disable")
    #options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument("window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.get(f'https://atbmarket.com/sch?page=1&lang=uk&location=1154&query={product_name}') 
    
    for tit in driver.find_elements(By.TAG_NAME, "article"):
        try:
            price = tit.find_element(By.TAG_NAME, "data")
        except NoSuchElementException:
            continue
        if price:
            image = tit.find_element(By.TAG_NAME, "img")
            if search_engine_atb.objects.filter(product_name = image.get_attribute("alt")).exists():
                search_engine_atb.objects.filter(product_name = image.get_attribute("alt")).update(search_date = datetime.date.today())
                search_engine_atb.objects.filter(product_name = image.get_attribute("alt")).update(product_price = price.text)
                search_engine_silpo.objects.filter(product_name = image.get_attribute("alt")).update(search_request = Concat(F('search_request'), Value(f'{product_name}')))
            else:
                db_object = search_engine_atb(search_request = product_name, product_name = image.get_attribute("alt"), product_price = price.text,  product_image = image.get_attribute("src"))
                db_object.save()
            response_price.append(price.text)
            response_title.append(image.get_attribute("alt"))
            response_pictures.append(image.get_attribute("src"))
        else:
            continue
    
    driver.quit()
    mylist = zip(response_title, response_price, response_pictures)
    manage.put(mylist)
    
def parse_silpo(product_name, manage):
    response_title = []
    response_price = []
    response_pictures = []
    options = webdriver.ChromeOptions()
    options.add_argument("--disable")
    #options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument("window-size=1920,1080")
    driver = webdriver.Chrome('C:\\Users\\Pogkopi\\Downloads\\chromedriver', options=options)
    driver.get(f'https://shop.silpo.ua/search/all?find={product_name}')
    time.sleep(7)
    
    driver.execute_script("window.scrollTo(0, 1000);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(1000, 1400);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(1400, 1800);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(1800, 2200);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(2600, 3000);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(3000, document.body.scrollHeight);")
    time.sleep(1)
    
    elements = driver.find_elements(By.CLASS_NAME, "lazyload-wrapper")
    for tit in elements:
        try:
            price = tit.find_element(By.CLASS_NAME, "current-integer")
        except NoSuchElementException:
            continue
        if price:
            volume = tit.find_element(By.CLASS_NAME, "product-weight")
            title = tit.find_element(By.CLASS_NAME, "product-title")
            image = tit.find_element(By.TAG_NAME, "img")
            image_source = image.get_attribute("src")
            if search_engine_silpo.objects.filter(product_name = (title.text + ', ' + volume.text)).exists():
                search_engine_silpo.objects.filter(product_name =(title.text + ', ' + volume.text)).update(search_date = datetime.date.today(), 
                                                                                                           product_price = price.text, 
                                                                                                           search_request = Concat(F('search_request'), Value(f'{product_name}')))
            else:
                db_object = search_engine_silpo(search_request = product_name, product_name = (title.text + ', ' + volume.text), product_price = price.text, product_image = image_source)
                db_object.save()
                
            response_price.append(price.text)
            response_title.append(title.text + ', ' + volume.text)
            response_pictures.append(image_source)
        else:
            continue
        
    driver.quit()
    mylist = zip(response_title, response_price, response_pictures)
    manage.put(mylist)
    #r = urllib.request.Request("https://api.catalog.ecom.silpo.ua/api/2.0/exec/EcomCatalogGlobal", method='POST', headers="application/json;charset=UTF-8")
    #print(r)

def search_db_silpo(product_name):
    print('searching in silpo db')
    response = []

    for i in range(1, int(len(product_name)/2)):
        if search_engine_silpo.objects.filter(search_request__icontains = product_name[:len(product_name)-i]).exists():
            response = search_engine_silpo.objects.filter(search_request__icontains = product_name[:len(product_name)-i])
            break
        elif search_engine_silpo.objects.filter(search_request__icontains = product_name[i:]).exists():
            response = search_engine_silpo.objects.filter(search_request__icontains = product_name[i:])
            break
        else:
            continue
           
    return response
             
def search_db_atb(product_name):
    print('searching in atb db')
    response = []
    for i in range(1, int(len(product_name)/2)):
        if search_engine_atb.objects.filter(search_request__icontains = product_name[:len(product_name)-i]).exists():
            response = search_engine_atb.objects.filter(search_request__icontains = product_name[:len(product_name)-i])
            break
        elif search_engine_atb.objects.filter(search_request__icontains = product_name[i:]).exists():
            response = search_engine_atb.objects.filter(search_request__icontains = product_name[i:])
            break
        else:
            continue
        
    return response
     
def search_db_glove(product_name):
    print('searching in glove db')
    response = []
    for i in range(1, int(len(product_name)/2)):
        if search_engine_glove.objects.filter(search_request__icontains = product_name[:len(product_name)-i]).exists():
            response = search_engine_glove.objects.filter(search_request__icontains = product_name[:len(product_name)-i])
            break
        elif search_engine_glove.objects.filter(search_request__icontains = product_name[i:]).exists():
            response = search_engine_glove.objects.filter(search_request__icontains = product_name[i:])
            break
        else:
            continue
        
    return response
        
def search_db(request):
    __name__ = '__main__'
    if request.method == 'POST' and __name__ == '__main__':
        product_name = request.POST['product_name']
        shops = request.POST.getlist('shop')
        glove = False
        atb = False
        silpo = False
        mylist_glove = []
        mylist_atb = []
        mylist_silpo = []
        manage_silpo = []
        manage_glove = []
        manage_atb = []
        mprocesses = []
        if shops:
            for shop in shops:
                if shop == 'Сільпо':
                    response_title = []
                    response_price = []
                    response_pictures = []
                    response = search_db_silpo(product_name)
                    if response:
                        for item in response:
                            date = str(item.search_date).split(" ")
                            if (datetime.date.today() - (datetime.datetime.strptime(str(date[0]), "%Y-%m-%d")).date()).days > 4:
                                manage_silpo = multiprocessing.Queue()
                                p1 = multiprocessing.Process(target = parse_silpo, args = (product_name, manage_silpo))
                                p1.start()
                                mprocesses.append(p1)
                                silpo = True
                                break
                            else:
                                response_title.append(item.product_name)
                                response_price.append(item.product_price)
                                response_pictures.append(item.product_image)
                                mylist_silpo = zip(response_title, response_price, response_pictures)
                                continue
                    
                    else:
                        manage_silpo = multiprocessing.Queue()
                        p1 = multiprocessing.Process(target = parse_silpo, args = (product_name, manage_silpo))
                        p1.start()
                        mprocesses.append(p1)
                        silpo = True
                        continue
                            
                 
                elif shop == 'Рукавичка':
                    response_title = []
                    response_price = []
                    response_pictures = []
                    response = search_db_glove(product_name)
                    if response:
                        for item in response:
                            date = str(item.search_date).split(" ")
                            if (datetime.date.today()- (datetime.datetime.strptime(str(date[0]), "%Y-%m-%d")).date()).days > 4:
                                manage_glove = multiprocessing.Queue()
                                p2 = multiprocessing.Process(target = parse_glove, args = (product_name, manage_glove))
                                p2.start()
                                mprocesses.append(p2)
                                glove = True
                                break
                            else:
                                response_title.append(item.product_name)
                                response_price.append(item.product_price)
                                response_pictures.append(item.product_image)
                                mylist_glove = zip(response_title, response_price, response_pictures)
                                continue
                    else:
                        manage_glove = multiprocessing.Queue()
                        p2 = multiprocessing.Process(target = parse_glove, args = (product_name, manage_glove))
                        p2.start()
                        mprocesses.append(p2)
                        glove = True
                        continue
                    
                elif shop == 'АТБ':
                    response_title = []
                    response_price = []
                    response_pictures = []
                    response = search_db_atb(product_name)
                    if response:
                        for item in response:
                            date = str(item.search_date).split(" ")
                            if (datetime.date.today()- (datetime.datetime.strptime(str(date[0]), "%Y-%m-%d")).date()).days > 4:
                                manage_atb = multiprocessing.Queue()
                                p3 = multiprocessing.Process(target = parse_atb, args = (product_name, manage_atb))
                                p3.start()
                                mprocesses.append(p3)
                                atb = True
                                break
                            else:
                                response_title.append(item.product_name)
                                response_price.append(item.product_price)
                                response_pictures.append(item.product_image)
                                mylist_atb = zip(response_title, response_price, response_pictures)
                                continue
                            
                    else:
                        manage_atb = multiprocessing.Queue()
                        p3 = multiprocessing.Process(target = parse_atb, args = (product_name, manage_atb))
                        p3.start()
                        mprocesses.append(p3)
                        atb = True
                        continue
                        
                
                    
                    
        else:
            shops.append('Сільпо')
            shops.append('Рукавичка')
            shops.append('АТБ')
            for shop in shops:
                if shop == 'Сільпо':
                    response_title = []
                    response_price = []
                    response_pictures = []
                    response = search_db_silpo(product_name)
                    if response:
                        for item in response:
                            date = str(item.search_date).split(" ")
                            if (datetime.date.today() - (datetime.datetime.strptime(str(date[0]), "%Y-%m-%d")).date()).days > 4:
                                manage_silpo = multiprocessing.Queue()
                                p1 = multiprocessing.Process(target = parse_silpo, args = (product_name, manage_silpo))
                                p1.start()
                                mprocesses.append(p1)
                                silpo = True
                                break
                            else:
                                response_title.append(item.product_name)
                                response_price.append(item.product_price)
                                response_pictures.append(item.product_image)
                                mylist_silpo = zip(response_title, response_price, response_pictures)
                                continue
                    
                    else:
                        manage_silpo = multiprocessing.Queue()
                        p1 = multiprocessing.Process(target = parse_silpo, args = (product_name, manage_silpo))
                        p1.start()
                        mprocesses.append(p1)
                        silpo = True
                        continue
                            
                    
                elif shop == 'Рукавичка':
                    response_title = []
                    response_price = []
                    response_pictures = []
                    response = search_db_glove(product_name)
                    if response:
                        for item in response:
                            date = str(item.search_date).split(" ")
                            if (datetime.date.today()- (datetime.datetime.strptime(str(date[0]), "%Y-%m-%d")).date()).days > 4:
                                manage_glove = multiprocessing.Queue()
                                p2 = multiprocessing.Process(target = parse_glove, args = (product_name, manage_glove))
                                p2.start()
                                mprocesses.append(p2)
                                glove = True
                                break
                            else:
                                response_title.append(item.product_name)
                                response_price.append(item.product_price)
                                response_pictures.append(item.product_image)
                                mylist_glove = zip(response_title, response_price, response_pictures)
                                continue
                    else:
                        manage_glove = multiprocessing.Queue()
                        p2 = multiprocessing.Process(target = parse_glove, args = (product_name, manage_glove))
                        p2.start()
                        mprocesses.append(p2)
                        glove = True
                        continue
                    
                elif shop == 'АТБ':
                    response_title = []
                    response_price = []
                    response_pictures = []
                    response = search_db_atb(product_name)
                    if response:
                        for item in response:
                            date = str(item.search_date).split(" ")
                            if (datetime.date.today()- (datetime.datetime.strptime(str(date[0]), "%Y-%m-%d")).date()).days > 4:
                                manage_atb = multiprocessing.Queue()
                                p3 = multiprocessing.Process(target = parse_atb, args = (product_name, manage_atb))
                                p3.start()
                                mprocesses.append(p3)
                                atb = True
                                break
                            else:
                                response_title.append(item.product_name)
                                response_price.append(item.product_price)
                                response_pictures.append(item.product_image)
                                mylist_atb = zip(response_title, response_price, response_pictures)
                                continue
                            
                    else:
                        manage_atb = multiprocessing.Queue()
                        p3 = multiprocessing.Process(target = parse_atb, args = (product_name, manage_atb))
                        p3.start()
                        mprocesses.append(p3)
                        atb = True
                        continue
                   
        for p in mprocesses:
            p.join()     
               
        if atb:
            mylist_atb = manage_atb.get()
        if glove:
            mylist_glove = manage_glove.get()
        if silpo:
            mylist_silpo = manage_silpo.get()
            
        context = {'mylist_atb': mylist_atb, 'mylist_glove': mylist_glove, 'mylist_silpo': mylist_silpo}      
                                           
        return render(request, 'main/price.html', context)                                  
    else:
        return render(request, 'main/get_price.html')
