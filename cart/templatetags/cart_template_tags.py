from cart.utils import get_or_set_order_session
from django import template

register = template.Library()

@register.filter
def cart_item_count(request):
    order = get_or_set_order_session(request)
    count = order.items.count()
    return count