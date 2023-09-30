from django.shortcuts import render
from .models import Product
from django.views import generic

# Create your views here.

class ProductList(generic.ListView):
    queryset = Product.objects.all()
    template_name = 'cart/product_list.html'
    context_object_name = 'products'