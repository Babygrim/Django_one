from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import *

urlpatterns = [
    path('', search_db, name='get_price'),
    path('about', about_page, name='about_page' )

]

urlpatterns += staticfiles_urlpatterns()