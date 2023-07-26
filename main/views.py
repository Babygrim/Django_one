from django.shortcuts import render
from django.db.models import F
import django
django.setup()
from .models import *
import requests
import multiprocessing 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException 
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
import json
import re


time_today = datetime.date.today()

def fetch_db(request):
    data = json.loads(request.body)
    search = data['search']
    shop = data['shop']
    choices = {'glove': search_db_glove(search),
               'silpo': search_db_silpo(search),
               'atb': search_db_atb(search)}
    response = choices.get(shop)
          
    return JsonResponse([item.serialize() for item in response], safe=False)


def swap_elements(request):
    data = json.loads(request.body)
    elem_to_delete = data['id']
    elem_to_insert = data['cur_id']
    wishlist.objects.filter(product_id = elem_to_delete, ).update(product_id = elem_to_insert, quantity='1.0')
    return JsonResponse('Success', safe=False)
    


def about_page(request):
    return render(request, 'main/price.html')

def add_to(request):
    data = json.loads(request.body)
    product_id = data['productId']
    shop = data['shop-name']
    user = data['user']
    qty = data["quantity"]
    if wishlist.objects.filter(user = user, product_id = product_id, shop = shop).exists():
        wishlist.objects.filter(user = user, product_id = product_id, shop = shop).update(quantity = F('quantity') + float(qty))
        return JsonResponse(f'Товар уже є у списку бажаних! Ще товарів додано', safe=False)
    else:
        db_object = wishlist(user = user, product_id = product_id, shop = shop, quantity = float(qty))
        db_object.save()
        return JsonResponse('Товар додано до списку бажаних', safe=False)

def check_wish_list(request):
    data = json.loads(request.body)
    user = data['user']
    if wishlist.objects.filter(user = user).exists():
        return JsonResponse('True', safe=False)
    else:
        return JsonResponse('Список бажаного порожній!', safe=False)
    
def delete(request):
    data = data = json.loads(request.body)
    user = data['user']
    shop_name = data['shop']
    product_id = data['item']
    
    wishlist.objects.get(user = user, shop = shop_name, product_id=product_id).delete()
    return JsonResponse("Success!", safe=False)

def delete_all(request):
    data = json.loads(request.body)
    user = data['user']
    wishlist.objects.filter(user = user).delete()
    return JsonResponse('Список бажаного порожній!', safe=False)
        
def wishlist_page(request):
    mylist_silpo = []
    mylist_glove = []
    mylist_atb = []
    total_silpo_price = 0
    total_glove_price = 0
    total_atb_price = 0
    query = wishlist.objects.filter(user = request.user.id)
    search_requests = []
    if query:
        for elem in query:
            if elem.shop == 'silpo':
                result = search_engine_silpo.objects.get(pk = elem.product_id)
                if float(elem.quantity) % 50 == 0 or float(elem.quantity) % 100 == 0:
                    quantity = float(elem.quantity) / 100
                else:
                    quantity = float(elem.quantity)
                total_silpo_price += (float(re.findall("\d+\.\d+",result.product_price)[0]) * quantity)
                mylist_silpo.append([result, float(elem.quantity)])
                if result.search_request not in search_requests:
                    search_requests.append(result.search_request)
                        
            elif elem.shop == 'glove':
                result = search_engine_glove.objects.get(pk = elem.product_id)
                if float(elem.quantity) % 50 == 0 or float(elem.quantity) % 100 == 0:
                    quantity = float(elem.quantity) / 100
                else:
                    quantity = float(elem.quantity)
                total_glove_price += (float(re.findall("\d+\.\d+",result.product_price)[0]) * quantity)
                mylist_glove.append([result, float(elem.quantity)])
                if result.search_request not in search_requests:
                    search_requests.append(result.search_request)
            elif elem.shop == 'atb':
                result = search_engine_atb.objects.get(pk = elem.product_id)
                if float(elem.quantity) % 50 == 0 or float(elem.quantity) % 100 == 0:
                    quantity = float(elem.quantity) / 100
                else:
                    quantity = float(elem.quantity)
                total_atb_price += (float(re.findall("\d+\.\d+",result.product_price)[0]) * quantity)
                mylist_atb.append([result, float(elem.quantity)])
                if result.search_request not in search_requests:
                    search_requests.append(result.search_request)
                
        context = {
            "mylist_atb":mylist_atb,
            "mylist_glove":mylist_glove,
            "mylist_silpo":mylist_silpo,
            "price_silpo":"{:.2f}".format(total_silpo_price),
            "price_atb":"{:.2f}".format(total_atb_price),
            "price_glove":"{:.2f}".format(total_glove_price),
            "query": search_requests
        }
        return render(request, 'main/wishlist.html', context)
    else:
        return redirect('home')
    
def edit_wishlist(request):
    data = json.loads(request.body)
    user = data['user']
    product = data['productId']
    shop = data['shop-name']
    qty = data['quantity']
    wishlist.objects.filter(user=user, product_id=product, shop=shop).update(quantity=qty)
    return JsonResponse("Кількість успішно оновлено!", safe=False)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, f'Your account has been created. You can log in now!')    
            return redirect('login')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'registration/register.html', context)

def parse_glove(product_name, manage):

    options = webdriver.ChromeOptions()
    options.add_argument("--disable")
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument("window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.get(f'https://market.rukavychka.ua/search/?search={product_name}') 
    
   # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "content")))
    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "product-layout")))
    
    for tit in driver.find_elements(By.CLASS_NAME, "product-layout"):
        try:
            price = tit.find_element(By.CLASS_NAME, "fm-module-price-new")
        except NoSuchElementException:
            continue
        if price:
            image = tit.find_element(By.TAG_NAME, "img")
            product_tit = image.get_attribute("alt")
            quantity = tit.find_element(By.CLASS_NAME, "form-control")
            quantity_number = quantity.get_attribute("value")
            data = (price.text).split(" ")
            coefficient = 1 / float(quantity_number)
            final_pr = float(data[0]) * coefficient
            pr_string = "{:.2f}".format(final_pr)+" "+data[1]
            if search_engine_glove.objects.filter(product_name = product_tit.capitalize()).exists():
                search_engine_glove.objects.filter(product_name = product_tit.capitalize()).update(search_date = time_today)

            else:
                db_object = search_engine_glove(search_request = product_name, product_name = product_tit.capitalize(), product_price = pr_string,  product_image = image.get_attribute("src"), search_date = time_today)
                db_object.save()
        else:
            continue
    
    
    driver.quit()
    
    mylist = search_engine_glove.objects.filter(search_request = product_name)
    manage.put(mylist)
    
def parse_atb(product_name, manage):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable")
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
                search_engine_atb.objects.filter(product_name = image.get_attribute("alt")).update(search_date = time_today)
            else:
                db_object = search_engine_atb(search_request = product_name, product_name = image.get_attribute("alt"), product_price = price.text,  product_image = image.get_attribute("src"), search_date = time_today)
                db_object.save()
        else:
            continue
    
    
    driver.quit()
    
    mylist = search_engine_atb.objects.filter(search_request = product_name)
    
    manage.put(mylist)
    
    
def parse_silpo(request):
    data = json.loads(request.body)
    product = data['product_name']
    search = data['search_request']
    price = data['product_price']
    image = data['product_image']
    weight = data['weight']
    
    if search_engine_silpo.objects.filter(product_name = product + " " + weight).exists():
        search_engine_silpo.objects.filter(product_name = product + " " + weight).update(product_price = "{:.2f}".format(price), search_date = time_today)
    else:
        db_object = search_engine_silpo(search_request = search, product_name = product + " " + weight, product_price = "{:.2f}".format(price), product_image = image, search_date = time_today)
        db_object.save()
                  
    return JsonResponse("Success!", safe=False)


def search_db_silpo(product_name):
    response = []
    for i in range(1, int(len(product_name)/2)):
        if search_engine_silpo.objects.filter(search_request__icontains = product_name[:len(product_name)-i]).exists():
            result = search_engine_silpo.objects.filter(search_request__icontains = product_name[:len(product_name)-i])
            for elem in result:
                if elem in response:
                    continue
                else:
                    response.append(elem)
        elif search_engine_silpo.objects.filter(search_request__icontains = product_name[i:]).exists():
            result = search_engine_silpo.objects.filter(search_request__icontains = product_name[i:])
            for elem in result:
                if elem in response:
                    continue
                else:
                    response.append(elem)
        elif search_engine_silpo.objects.filter(product_name__icontains = product_name).exists():
            result = search_engine_silpo.objects.filter(product_name__icontains = product_name)
            for elem in result:
                if elem in response:
                    continue
                else:
                    response.append(elem)
        elif search_engine_silpo.objects.filter(product_name__icontains = product_name).exists():
            result = search_engine_silpo.objects.filter(product_name__icontains = product_name)
            for elem in result:
                if elem in response:
                    continue
                else:
                    response.append(elem)
        else:
            continue
    return response
             
def search_db_atb(product_name):
    response = []
    for i in range(1, int(len(product_name)/2)):
        if search_engine_atb.objects.filter(search_request__icontains = product_name[:len(product_name)-i]).exists():
            result = search_engine_atb.objects.filter(search_request__icontains = product_name[:len(product_name)-i])
            for elem in result:
                if elem in response:
                    continue
                else:
                    response.append(elem)
        elif search_engine_atb.objects.filter(search_request__icontains = product_name[i:]).exists():
            result = search_engine_atb.objects.filter(search_request__icontains = product_name[i:])
            for elem in result:
                if elem in response:
                    continue
                else:
                    response.append(elem)
        elif search_engine_atb.objects.filter(product_name__icontains = product_name).exists():
            result = search_engine_atb.objects.filter(product_name__icontains = product_name)
            for elem in result:
                if elem in response:
                    continue
                else:
                    response.append(elem)
        elif search_engine_atb.objects.filter(product_name__icontains = product_name).exists():
            result = search_engine_atb.objects.filter(product_name__icontains = product_name)
            for elem in result:
                if elem in response:
                    continue
                else:
                    response.append(elem)
        else:
            continue
    return response
     
def search_db_glove(product_name):
    response = []
    for i in range(1, int(len(product_name)/2)):
        if search_engine_glove.objects.filter(search_request__icontains = product_name[:len(product_name)-i]).exists():
            result = search_engine_glove.objects.filter(search_request__icontains = product_name[:len(product_name)-i])
            for elem in result:
                if elem in response:
                    continue
                else:
                    response.append(elem)
        elif search_engine_glove.objects.filter(search_request__icontains = product_name[i:]).exists():
            result = search_engine_glove.objects.filter(search_request__icontains = product_name[i:])
            for elem in result:
                if elem in response:
                    continue
                else:
                    response.append(elem)
        elif search_engine_glove.objects.filter(product_name__icontains = product_name).exists():
            result = search_engine_glove.objects.filter(product_name__icontains = product_name)
            for elem in result:
                if elem in response:
                    continue
                else:
                    response.append(elem)
        elif search_engine_glove.objects.filter(product_name__icontains = product_name).exists():
            result = search_engine_glove.objects.filter(product_name__icontains = product_name)
            for elem in result:
                if elem in response:
                    continue
                else:
                    response.append(elem)
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
        mylist_glove = []
        mylist_atb = []
        mylist_silpo = []
        manage_glove = []
        manage_atb = []
        mprocesses = []
        if shops:
            for shop in shops:
                if shop == 'Рукавичка':
                    response = search_db_glove(product_name)
                    if response:
                        date = str(response[0].search_date).split(" ")
                        if (datetime.date.today()- (datetime.datetime.strptime(str(date[0]), "%Y-%m-%d")).date()).days > 4:
                            manage_glove = multiprocessing.Queue()
                            p2 = multiprocessing.Process(target = parse_glove, args = (product_name, manage_glove))
                            p2.start()
                            mprocesses.append(p2)
                            glove = True
                            break
                        else:
                            mylist_glove = response
                            continue
                    else:
                        manage_glove = multiprocessing.Queue()
                        p2 = multiprocessing.Process(target = parse_glove, args = (product_name, manage_glove))
                        p2.start()
                        mprocesses.append(p2)
                        glove = True
                        continue
                    
                elif shop == 'АТБ':
                    response = search_db_atb(product_name)
                    if response:
                        date = str(response[0].search_date).split(" ")
                        if (datetime.date.today()- (datetime.datetime.strptime(str(date[0]), "%Y-%m-%d")).date()).days > 4:
                            manage_atb = multiprocessing.Queue()
                            p3 = multiprocessing.Process(target = parse_atb, args = (product_name, manage_atb))
                            p3.start()
                            mprocesses.append(p3)
                            atb = True
                            break
                        else:
                            mylist_atb = response
                            continue
                            
                    else:
                        manage_atb = multiprocessing.Queue()
                        p3 = multiprocessing.Process(target = parse_atb, args = (product_name, manage_atb))
                        p3.start()
                        mprocesses.append(p3)
                        atb = True
                        continue   
                
                    
                    
        else:
            for shop in shops:
                if shop == 'Рукавичка':
                    response = search_db_glove(product_name)
                    if response:
                        date = str(response[0].search_date).split(" ")
                        if (datetime.date.today()- (datetime.datetime.strptime(str(date[0]), "%Y-%m-%d")).date()).days > 4:
                            manage_glove = multiprocessing.Queue()
                            p2 = multiprocessing.Process(target = parse_glove, args = (product_name, manage_glove))
                            p2.start()
                            mprocesses.append(p2)
                            glove = True
                            break
                        else:
                            mylist_glove = response
                            continue
                    else:
                        manage_glove = multiprocessing.Queue()
                        p2 = multiprocessing.Process(target = parse_glove, args = (product_name, manage_glove))
                        p2.start()
                        mprocesses.append(p2)
                        glove = True
                        continue
                    
                elif shop == 'АТБ':
                    response = search_db_atb(product_name)
                    if response:
                        date = str(response[0].search_date).split(" ")
                        if (datetime.date.today()- (datetime.datetime.strptime(str(date[0]), "%Y-%m-%d")).date()).days > 4:
                            manage_atb = multiprocessing.Queue()
                            p3 = multiprocessing.Process(target = parse_atb, args = (product_name, manage_atb))
                            p3.start()
                            mprocesses.append(p3)
                            atb = True
                            break
                        else:
                            mylist_atb = response
                            continue
                            
                    else:
                        manage_atb = multiprocessing.Queue()
                        p3 = multiprocessing.Process(target = parse_atb, args = (product_name, manage_atb))
                        p3.start()
                        mprocesses.append(p3)
                        atb = True
                        continue
                
                          
        if atb:
            mylist_atb = manage_atb.get()
        if glove:
            mylist_glove = manage_glove.get()
            
        for p in mprocesses:
            p.join() 
            
        if 'Сільпо' in shops:
            mylist_silpo = search_db_silpo(product_name) 
              
        context = {'mylist_atb': mylist_atb, 'mylist_glove': mylist_glove, 'mylist_silpo': mylist_silpo}      
                                           
        return render(request, 'main/price.html', context)                                  
    else:
        return render(request, 'main/layout.html')
