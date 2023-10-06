from django.contrib import admin
from .models import Product, Order, OrderItem, ColourVariation, SizeVariation, Address

# Register your models here.
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'address_line_1',
        'address_line_2',
        'city',
        'zip_code',
        'address_type',
    ]

admin.site.register(Address, AddressAdmin)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ColourVariation)
admin.site.register(SizeVariation)