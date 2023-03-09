from django.urls import path
from .views import *

urlpatterns = [
    path('', search_db, name='get_price'),
    path('about', about_page, name='about_page' )

]