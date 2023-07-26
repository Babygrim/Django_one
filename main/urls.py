from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import *

urlpatterns = [
    path('', about_page, name='home'),
    path('price/', search_db, name='price'),
    path('update_item/', add_to, name='update_item'),
    path('update_silpo_db/', parse_silpo, name='update_silpo_db'),
    path('check_wish_list/', check_wish_list, name='checkwishlist'),
    path('fetch_wish_list/', fetch_db, name='fetch'),
    path('swap_elements/', swap_elements, name='swap'),
    path('delete_all/', delete_all, name='delete_all'),
    path('delete_item/', delete, name='delete' ),
    path('login/', include("django.contrib.auth.urls"), name='login'),
    path('register/', register, name='register'),
    path('wishlist/', wishlist_page, name='wishlist'),
    path('edit_wish_list/', edit_wishlist, name='edit')

]

urlpatterns += staticfiles_urlpatterns()