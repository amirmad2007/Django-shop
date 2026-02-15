from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('contact/', ContactView.as_view(), name='contact'),
    
]