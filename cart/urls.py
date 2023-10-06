from django.urls import path
from .views import ProductList, ProductDetail, CartView, IncreaseQuantityView, DecreaseQuantityView, RemoveFromCartView, CheckOutView

app_name = 'cart'

urlpatterns = [
    path('', CartView.as_view(), name='summary'),
    path('shop/', ProductList.as_view(), name='product-list'),
    path('shop/<slug>/', ProductDetail.as_view(), name='product-detail'),
    path('increase-quantity/<pk>/', IncreaseQuantityView.as_view(), name='increase-quantity'),
    path('decrease-quantity/<pk>/', DecreaseQuantityView.as_view(), name='decrease-quantity'),
    path('remove-from-cart/<pk>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('checkout/', CheckOutView.as_view(), name='checkout'),
]