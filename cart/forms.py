from django import forms
from .models import OrderItem, Product, ColourVariation, SizeVariation, Address
from django.contrib.auth import get_user_model

User = get_user_model()

class AddToCartForm(forms.ModelForm):
    colour = forms.ModelChoiceField(queryset=ColourVariation.objects.none())
    size = forms.ModelChoiceField(queryset=SizeVariation.objects.none())
    class Meta:
        model = OrderItem
        fields = ['quantity', 'colour', 'size']

    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id')
        product = Product.objects.get(id=product_id)
        super().__init__(*args, **kwargs)

        self.fields['colour'].queryset = product.available_colours.all()
        self.fields['size'].queryset = product.available_sizes.all()

class AddressForm(forms.Form):
    shipping_address_line_1 = forms.CharField(required=False)
    shipping_address_line_2 = forms.CharField(required=False)
    shipping_zip_code = forms.CharField(required=False)
    shipping_city = forms.CharField(required=False)

    billing_address_line_1 = forms.CharField(required=False)
    billing_address_line_2 = forms.CharField(required=False)
    billing_zip_code = forms.CharField(required=False)
    billing_city = forms.CharField(required=False)

    selected_shipping_address = forms.ModelChoiceField(Address.objects.none(), required=False)
    selected_billing_address = forms.ModelChoiceField(Address.objects.none(), required=False)

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        super().__init__(*args, **kwargs)

        user = User.objects.get(id=user_id)

        shipping_address_qs = Address.objects.filter(user=user, address_type='S')
        billing_address_qs = Address.objects.filter(user=user, address_type='B')

        self.fields['selected_shipping_address'].queryset = shipping_address_qs
        self.fields['selected_billing_address'].queryset = billing_address_qs

    def clean(self):
        data = self.cleaned_data

        selected_shipping_address = data.get('selected_shipping_address', None)
        if selected_shipping_address is None:
            if not data.get('shipping_address_line_1', None):
                self.add_error('shipping_address_line_1', 'please fill this field')
            if not data.get('shipping_address_line_2', None):
                self.add_error('shipping_address_line_2', 'please fill this field')
            if not data.get('shipping_zip_code', None):
                self.add_error('shipping_zip_code', 'please fill this field')
            if not data.get('shipping_city', None):
                self.add_error('shipping_city', 'please fill this field')

        selected_billing_address = data.get('selected_shipping_address', None)
        if selected_shipping_address is None:
            if not data.get('billing_address_line_1', None):
                self.add_error('billing_address_line_1', 'please fill this field')
            if not data.get('billing_address_line_2', None):
                self.add_error('billing_address_line_2', 'please fill this field')
            if not data.get('billing_zip_code', None):
                self.add_error('billing_zip_code', 'please fill this field')
            if not data.get('billing_city', None):
                self.add_error('billing_city', 'please fill this field')