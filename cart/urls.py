from django.urls import path
from .views import ProductList, ProductDetail

app_name = 'cart'

urlpatterns = [
    path('', ProductList.as_view(), name='product-list'),
    path('<slug>/', ProductDetail.as_view(), name='product-detail'),
]