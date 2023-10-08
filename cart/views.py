from django.shortcuts import redirect
from .models import Product, OrderItem, Address
from django.views import generic
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from .utils import get_or_set_order_session
from .forms import AddToCartForm, AddressForm
from django.contrib import messages
from django.conf import settings
import json
from django.http import JsonResponse
import datetime

# Create your views here.

class ProductList(generic.ListView):
    queryset = Product.objects.all()
    template_name = 'cart/product_list.html'
    context_object_name = 'products'


class ProductDetail(generic.FormView):
    template_name = 'cart/product_detail.html'
    success_url = reverse_lazy('cart:summary') #TODO: cart
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

class IncreaseQuantityView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        order_item.quantity += 1
        order_item.save()
        return redirect('cart:summary')

class DecreaseQuantityView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])

        if order_item.quantity <= 1:
            order_item.delete()
        else:
            order_item.quantity -= 1
            order_item.save()
        return redirect('cart:summary')
    
class RemoveFromCartView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        order_item.delete()
        return redirect('cart:summary')

class CheckOutView(generic.FormView):
    template_name = 'cart/checkout.html'
    form_class = AddressForm
    success_url = reverse_lazy('cart:payment')

    def get_context_data(self, **kwargs):
        context = super(CheckOutView, self).get_context_data(**kwargs)
        context['order'] = get_or_set_order_session(self.request)
        return context
    
    def get_form_kwargs(self):
        kwargs = super(CheckOutView, self).get_form_kwargs()
        kwargs['user_id'] = self.request.user.id
        return kwargs

    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        selected_shipping_address = form.cleaned_data.get('selected_shipping_address')
        selected_billing_address = form.cleaned_data.get('selected_billing_address')

        if selected_shipping_address:
            order.shipping_address = selected_shipping_address
        else:
            address = Address.objects.create(
                user = self.request.user,
                address_type = 'S',
                address_line_1 = form.cleaned_data['shipping_address_line_1'],
                address_line_2 = form.cleaned_data['shipping_address_line_2'],
                zip_code = form.cleaned_data['shipping_zip_code'],
                city = form.cleaned_data['shipping_city']
            )
            order.shipping_address = address
        order.save()

        if selected_billing_address:
            order.billing_address = selected_billing_address
        else:
            address = Address.objects.create(
                user = self.request.user,
                address_type = 'B',
                address_line_1 = form.cleaned_data['billing_address_line_1'],
                address_line_2 = form.cleaned_data['billing_address_line_2'],
                zip_code = form.cleaned_data['billing_zip_code'],
                city = form.cleaned_data['billing_city']
            )
            order.billing_address = address
        order.save()

        messages.info(
            self.request, 'You have successfully added your address',
        )
        return super(CheckOutView, self).form_valid(form)

class PaymentView(generic.TemplateView):
    template_name = "cart/payment.html"

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        context["PAYPAL_CLIENT_ID"] = settings.PAYPAL_CLIENT_ID
        context["order"] = get_or_set_order_session(self.request)
        context["CALLBACK_URL"] = reverse("cart:thank-you")
        return context
    
class ThankYouView(generic.TemplateView):
    template_name = "cart/thanks.html"

class ConfirmOrderView(generic.View):
    def post(self, request, *args, **kwargs):
        order = get_or_set_order_session(request)
        body = json.load(request.body)
        print(body)
        payment = payment.objects.create(
            order=order,
            successful=True,
            raw_response=json.dumps(body),
            amount=float(body['purchase_units'][0]['amount']['value']),
            payment_method='paypal',
        )
        order.ordered=True
        order.ordered_date = datetime.date.today()
        order.save()
        return JsonResponse({'data':'success'})