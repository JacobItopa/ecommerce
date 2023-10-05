from django.urls import path
from .views import ProductList, ProductDetail, CartView

app_name = 'cart'

urlpatterns = [
    path('', CartView.as_view(), name='summary'),
    path('shop/', ProductList.as_view(), name='product-list'),
    path('shop/<slug>/', ProductDetail.as_view(), name='product-detail'),
]