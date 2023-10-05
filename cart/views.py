from django.shortcuts import render
from .models import Product
from django.views import generic
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .utils import get_or_set_order_session
from .forms import AddToCartForm

# Create your views here.

class ProductList(generic.ListView):
    queryset = Product.objects.all()
    template_name = 'cart/product_list.html'
    context_object_name = 'products'


class ProductDetail(generic.FormView):
    template_name = 'cart/product_detail.html'
    success_url = reverse_lazy('home') #TODO: cart
    form_class = AddToCartForm
 
    def get_object(self):
        return get_object_or_404(Product, slug=self.kwargs['slug'])
    
    def get_form_kwargs(self):
        kwargs = super(ProductDetail, self).get_form_kwargs()
        kwargs['product_id'] = self.get_object().id
        return kwargs
    
    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        product = self.get_object()
        item_filter = order.items.filter(
            product=product,
            colour = form.cleaned_data['colour'],
            size = form.cleaned_data['size'],
        )
        if item_filter.exists():
            item = item.filter.first()
            item.quantity = int(form.cleaned_data['quantity'])
            item.save()
        else:
            new_item = form.save(commit=False)
            new_item.product = product
            new_item.order = order
            new_item.save()
        return super(ProductDetail, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['product'] = self.get_object()
        return context

class CartView(generic.TemplateView):
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context['order'] = get_or_set_order_session(self.request)
        return context

    