from django.urls import path
from .views import *

urlpatterns = [
       path('cart/',cart_detail, name ='cart'),
       path("add-to-cart/" , add_to_cart , name = "add_to_cart"),
       path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
]