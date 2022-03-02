from django import template
import urllib

register = template.Library()

@register.filter(name="is_in_cart")
def is_in_cart(id, cart):
    if str(id) in cart:
        return cart[f'{id}']
    else:
        return False

@register.filter(name="total")
def total(price, quantity):
    quantity = int(quantity)
    return quantity*price

@register.filter(name="total_bill")
def total_bill(order):
    sum = 0 
    for key, value in order.items():
        sum = sum +(int(key)*value.price)
    return sum

