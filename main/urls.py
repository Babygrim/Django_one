from django.urls import path
from .views import *

urlpatterns = [
    path('', start_threads, name='get_price'),
    path('about', about_page, name='about_page' )

]