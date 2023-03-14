from django.shortcuts import render, HttpResponse
import django
django.setup()
from main import models
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
# def search_db(request):
#     if request.method == 'POST':
#         product_name = request.POST['product_name']
#         shops = request.POST.getlist('shop')
#         mylist_arsen = []
#         mylist_atb = []
#         mylist_silpo = []
#         if shops:
#             for shop in shops:
#                 response = []
#                 response_title = []
#                 response_price = []
#                 response_volume = []
#                 response_pictures = []
#                 if shop == 'Сільпо':
#                     for i in range(1, int(len(product_name)/2)):
#                         if search_engine_silpo.objects.filter(search_request__icontains = product_name[:len(product_name)-i]).exists():
#                             response = search_engine_silpo.objects.filter(search_request__icontains = product_name[:len(product_name)-i])
#                             break
#                         elif search_engine_silpo.objects.filter(search_request__icontains = product_name[i:]).exists():
#                             response = search_engine_silpo.objects.filter(search_request__icontains = product_name[i:])
#                             break
#                         else:
#                             continue
                        
#                     if response:
#                         for item in response:
#                             response_title.append(item.product_name)
#                             response_price.append(item.product_price)
#                             response_volume.append(item.product_volume)
#                             response_pictures.append(item.product_image)
                        
#                         mylist_silpo = zip(response_title, response_price, response_volume, response_pictures)
                            
#                     else:
#                         response = parse_silpo(product_name)
#                         for i, x, z, f in response:
#                             response_title.append(i)
#                             response_price.append(x)
#                             response_volume.append(z)
#                             response_pictures.append(f)    
#                         mylist_silpo = zip(response_title, response_price, response_volume, response_pictures)
                        
#                     return render(request, 'main/price.html', {'mylist_silpo':mylist_silpo})
                    
#                 elif shop == 'Арсен':
#                     for i in range(1, int(len(product_name)/2)):
#                         if search_engine_arsen.objects.filter(search_request__icontains = product_name[:len(product_name)-i]).exists():
#                             response = search_engine_arsen.objects.filter(search_request__icontains = product_name[:len(product_name)-i])
#                             break
#                         elif search_engine_arsen.objects.filter(search_request__icontains = product_name[i:]).exists():
#                             response = search_engine_arsen.objects.filter(search_request__icontains = product_name[i:])
#                             break
#                         else:
#                             continue
                        
#                     if response:
#                         for i, x, z, f in response:
#                             response_title.append(i)
#                             response_price.append(x)
#                             response_volume.append(z)
#                             response_pictures.append(f)
#                         mylist_arsen = zip(response_title, response_price, response_volume, response_pictures)
#                         continue
#                     else:
#                         # response = parse_arsen(product_name)
#                         # for i, x, z, f in response:
#                         #     response_title.append(i)
#                         #     response_price.append(x)
#                         #     response_volume.append(z)
#                         #     response_pictures.append(f)
#                         # mylist_arsen = zip(response_title, response_price, response_volume, response_pictures)    
#                         continue
                    
#                 elif shop == 'АТБ':
#                     if datetime.datetime.today().weekday() == 2:
#                         parse_silpo(product_name)
#                     for i in range(1, int(len(product_name)/2)):
#                         if search_engine_atb.objects.filter(search_request__icontains = product_name[:len(product_name)-i]).exists():
#                             response = search_engine_atb.objects.filter(search_request__icontains = product_name[:len(product_name)-i])
#                             break
#                         elif search_engine_atb.objects.filter(search_request__icontains = product_name[i:]).exists():
#                             response = search_engine_atb.objects.filter(search_request__icontains = product_name[i:])
#                             break
#                         else:
#                             continue
                        
#                     if response:
#                         for item in response:
#                             response_title.append(item.product_name)
#                             response_price.append(item.product_price)
#                             response_pictures.append(item.product_image)
#                         mylist_atb = zip(response_title, response_price, response_pictures)
#                         continue
                            

#                     else:
#                         response = parse_atb(product_name)
#                         for i, x, f in response:
#                             response_title.append(i)
#                             response_price.append(x)
#                             response_pictures.append(f)
#                         mylist_atb = zip(response_title, response_price, response_pictures)
                    
                    
#         else:
#             shops.append("Сільпо")
#             shops.append("Арсен")
#             shops.append("АТБ")
#             for shop in shops:
#                 response = []
#                 response_title = []
#                 response_price = []
#                 response_volume = []
#                 response_pictures = []
#                 if shop == 'Сільпо':
#                     for i in range(1, int(len(product_name)/2)):
#                         if search_engine_silpo.objects.filter(search_request__icontains = product_name[:len(product_name)-i]).exists():
#                             response = search_engine_silpo.objects.filter(search_request__icontains = product_name[:len(product_name)-i])
#                             break
#                         elif search_engine_silpo.objects.filter(search_request__icontains = product_name[i:]).exists():
#                             response = search_engine_silpo.objects.filter(search_request__icontains = product_name[i:])
#                             break
#                         else:
#                             continue
                        
#                     if response:
#                         for item in response:
#                             response_title.append(item.product_name)
#                             response_price.append(item.product_price)
#                             response_volume.append(item.product_volume)
#                             response_pictures.append(item.product_image)
#                         mylist_silpo = zip(response_title, response_price, response_volume, response_pictures)

#                     else:
#                         response = parse_silpo(product_name)
#                         for i, x, z, f in response:
#                             response_title.append(i)
#                             response_price.append(x)
#                             response_volume.append(z)
#                             response_pictures.append(f)
#                         mylist_silpo = zip(response_title, response_price, response_volume, response_pictures)
     
                    
#                 elif shop == 'Арсен':
#                     for i in range(1, int(len(product_name)/2)):
#                         if search_engine_arsen.objects.filter(search_request__icontains = product_name[:len(product_name)-i]).exists():
#                             response = search_engine_arsen.objects.filter(search_request__icontains = product_name[:len(product_name)-i])
#                             break
#                         elif search_engine_arsen.objects.filter(search_request__icontains = product_name[i:]).exists():
#                             response = search_engine_arsen.objects.filter(search_request__icontains = product_name[i:])
#                             break
#                         else:
#                             continue
                        
#                     if response:
#                         for item in response:
#                             response_title.append(item.product_name)
#                             response_price.append(item.product_price)
#                             response_volume.append(item.product_volume)
#                             response_pictures.append(item.product_image)
#                         mylist_arsen = zip(response_title, response_price, response_volume, response_pictures)
#                         continue

#                     else:
#                         # response = parse_arsen(product_name)
#                         # for i, x, z, f in response:
#                         #     response_title.append(i)
#                         #     response_price.append(x)
#                         #     response_volume.append(z)
#                         #     response_pictures.append(f)
#                         #     break
#                         mylist_arsen = zip(response_title, response_price, response_volume, response_pictures)
#                         continue
                    
#                 elif shop == 'АТБ':
#                     if datetime.datetime.today().weekday() == 2:
#                         parse_silpo(product_name)
#                     for i in range(1, int(len(product_name)/2)):
#                         if search_engine_atb.objects.filter(search_request__icontains = product_name[:len(product_name)-i]).exists():
#                             response = search_engine_atb.objects.filter(search_request__icontains = product_name[:len(product_name)-i])
#                             break
#                         elif search_engine_atb.objects.filter(search_request__icontains = product_name[i:]).exists():
#                             response = search_engine_atb.objects.filter(search_request__icontains = product_name[i:])
#                             break
#                         else:
#                             continue
                        
#                     if response:
#                         for item in response:
#                             response_title.append(item.product_name)
#                             response_price.append(item.product_price)
#                             response_pictures.append(item.product_image)
#                         mylist_atb = zip(response_title, response_price, response_pictures)
#                         continue
                        
#                     else:
#                         response = parse_atb(product_name)
#                         for i, x, f in response:
#                             response_title.append(i)
#                             response_price.append(x)
#                             response_pictures.append(f)
#                         mylist_atb = zip(response_title, response_price, response_pictures)
                        
                    
                   
                    
#         context = {'mylist_atb': mylist_atb, 'mylist_arsen': mylist_arsen, 'mylist_silpo': mylist_silpo}      
                                           
#         return render(request, 'main/price.html', context)                                  
#     else:
#         return render(request, 'main/get_price.html')
def about_page(request):
    return render(request, 'main/about.html')

def parse_metro(product_name, manage):
    print('print arsen feedback',product_name)

def parse_atb(product_name, manage):
    print('print atb feedback', product_name)
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
        price = tit.find_element(By.TAG_NAME, "data")
        if price:
            image = tit.find_element(By.TAG_NAME, "img")
            # if search_engine_atb.objects.filter(product_name = image.get_attribute("alt")).exists():
            #     search_engine_atb.objects.filter(product_name = image.get_attribute("alt")).update(search_date = datetime.datetime.now())
            #     search_engine_atb.objects.filter(product_name = image.get_attribute("alt")).update(product_price = price.text)
            # # else:
            # #     db_object = search_engine_atb(search_request = product_name, product_name = image.get_attribute("alt"), product_price = price.text,  product_image = image.get_attribute("src"))
            # #     db_object.save()
            response_price.append(price.text)
            response_title.append(image.get_attribute("alt"))
            response_pictures.append(image.get_attribute("src"))
        else:
            continue
    
    driver.quit()
    mylist = zip(response_title, response_price, response_pictures)
    manage.put(mylist)
    
def parse_silpo(product_name, manage):
    print('print silpo feedback', product_name)
    response_title = []
    response_price = []
    response_volume = []
    response_pictures = []
    options = webdriver.ChromeOptions()
    options.add_argument("--disable")
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument("window-size=1920,1080")
    driver = webdriver.Chrome('C:\\Users\\Pogkopi\\Downloads\\chromedriver', options=options)
    driver.get(f'https://shop.silpo.ua/search/all?find={product_name}')
    time.sleep(7)
    
    driver.execute_script("window.scrollTo(0, 800);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(800, 1200);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(1200, 1600);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(1600, 2000);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(2000, 2400);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(2400, document.body.scrollHeight);")
    time.sleep(1)
    
    elements = driver.find_elements(By.CLASS_NAME, "lazyload-wrapper")
    for tit in elements:
        price = tit.find_element(By.CLASS_NAME, "current-integer")
        if price:
            volume = tit.find_element(By.CLASS_NAME, "product-weight")
            title = tit.find_element(By.CLASS_NAME, "product-title")
            image = tit.find_element(By.TAG_NAME, "img")
            image_source = image.get_attribute("src")
            # if search_engine_silpo.objects.filter(product_name = title.text).exists():
            #     search_engine_silpo.objects.filter(product_name = title.text).update(search_date = datetime.datetime.now())
            #     search_engine_silpo.objects.filter(product_name = title.text).update(product_price = price.text)
            # # else:
            # #     db_object = search_engine_silpo(search_request = product_name, product_name = title.text, product_price = price.text, product_volume = volume.text, product_image = image_source)
            # #     db_object.save()
            response_price.append(price.text)
            response_title.append(title.text)
            response_volume.append(volume.text)
            response_pictures.append(image_source)
            
        else:
            continue
        
    driver.quit()
    mylist = zip(response_title, response_price, response_volume, response_pictures)
    manage.put(mylist)
    #r = urllib.request.Request("https://api.catalog.ecom.silpo.ua/api/2.0/exec/EcomCatalogGlobal", method='POST', headers="application/json;charset=UTF-8")
    #print(r)
    
def start_threads(request):
    if request.method == 'POST':
        product_name = request.POST['product_name']
        shops = request.POST.getlist('shop')
        __name__ = '__main__'
        if __name__ == '__main__':
            manage_silpo = multiprocessing.Queue()
            manage_atb = multiprocessing.Queue()
           # manage_metro = multiprocessing.Queue()
            p1 = multiprocessing.Process(target=parse_silpo, args=(product_name, manage_silpo))
            p2 = multiprocessing.Process(target=parse_atb, args=(product_name, manage_atb))
           # p3 = multiprocessing.Process(target=parse_metro, args=(product_name, manage_metro))
            p1.start()
            p2.start()
          #  p3.start()
            value_silpo = manage_silpo.get()
            value_atb = manage_atb.get()
           # value_metro = manage_metro.get()
            p1.join()     
            p2.join()
            #p3.join()
        
        
        return render(request, 'main/price.html', ) 
    else:
        return render(request, 'main/get_price.html')
    