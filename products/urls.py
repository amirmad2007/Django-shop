from django.urls import path
from .views import *

urlpatterns = [
    path('product_detail/<slug:slug>/', detail, name='product_detail'),
]