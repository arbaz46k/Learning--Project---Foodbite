from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db import IntegrityError
import requests
from .models import *
from django import forms
import json
import urllib.parse
# forms

class Dishes_form(forms.ModelForm):
    class Meta:
        model = Dishes
        fields = ("name", "description", "image", "price")
        

# Create your views here.

def index(request):
    order = request.session.get('order')
    print(order)
    return render(request, 'food_delivery/index.html',{
        "restaurant": User.objects.filter(is_restaurant=True)
    })

def partner_index(request):
    pending_orders = Order.objects.filter(restaurant=request.user,delivered=False).order_by('-timestamp')
    order_details = []
    com_order_details = []
    completed_orders = Order.objects.filter(restaurant=request.user, delivered=True).order_by('timestamp')
    for order in pending_orders:
        order_details = order_details + [Ordered_dishes.objects.get(order=order)]
    for order in completed_orders:
        com_order_details = com_order_details + [Ordered_dishes.objects.get(order=order)]
    return render(request, 'food_delivery/partner_index.html',{
        "order_details": order_details,
        "com_order_details": com_order_details
    })
   
def login_view(request):
    if request.method == 'POST':
        #signing user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        #Checking if the user is successfully authenticated 
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'food_delivery/login.html',{
                "message": "Invlaid email or password"
            })
    else:
        return render(request, 'food_delivery/login.html')
                
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'food_delivery/register.html',{
                "message": "Passwords must match"
            })

        # Attemp to create new user 
        try :
            user = User.objects.create_user(username, email, password) 
            user.save()
        except IntegrityError:
            return render(request, 'food_delivery/register.html',{
                "message" : "Email already taken"
            })

        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'food_delivery/register.html')

def partner_register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST["email"]
        image = request.FILES['image']
        password = request.POST["password"]
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'food_delivery/partner_register.html',{
                "message": "Passwords must match"
            })

        # Attemp to create new user 
        try :
            user = User.objects.create_user(username=username,email=email,password=password,hotel_image=image, is_restaurant=True) 
            user.save()
        except IntegrityError:
            return render(request, 'food_delivery/partner_register.html',{
                "message" : "Email already taken"
            })

        login(request, user)
        return HttpResponseRedirect(reverse('partner_index'))
    else:
        return render(request, 'food_delivery/partner_register.html')

def partner_login(request):
    if request.method == 'POST':
        #signing user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        #Checking if the user is successfully authenticated 
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('partner_index'))
        else:
            return render(request, 'food_delivery/partner_login.html',{
                "message": "Invlaid email or password"
            })
    else:
        return render(request, 'food_delivery/partner_login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def add_item(request):
    if request.method == "POST":
        form = Dishes_form(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.restaurant = request.user
            data.save()
        return HttpResponseRedirect(reverse('partner_index'))
    else:
        return render(request, 'food_delivery/add_item.html',{
            "form": Dishes_form()
        })

def dishes(request, restaurant):
    hotel = User.objects.filter(username=restaurant)
    if request.method == "POST":
        cart = request.session.get('cart')
        if "increment" in request.POST:
            id = request.POST['increment']
            if cart:
                quantity = cart.get(id) if cart.get(id) else 0
                cart[id] = quantity + 1
            else:
                cart = {}
                cart[id] = 1
        if "decrement" in request.POST:
            id = request.POST['decrement']
            if cart:
                quantity = cart.get(id) if cart.get(id) else 0
                cart[id] = quantity - 1
            else:
                cart = {}
                cart[id] = 1
        request.session['cart'] = cart       
    return render(request, 'food_delivery/dishes.html', {
        "restaurant" : restaurant,
        "dishes": Dishes.objects.filter(restaurant=hotel[0])
    })

def cart(request):
    cart = request.session.get('cart')
    print(cart)
    if cart:
        order = {}
        total = 0
        for key, value in cart.items():
            print(key, value, "in cart")
            order[value] = Dishes.objects.get(pk=key)
        # request.session['order'] = order
        print("------------------------------------------")
    else:
        return HttpResponse('Nothing in cart till now')
    return render(request, 'food_delivery/cart.html',{
        "order": order
    })

def book_order(request):
    if request.method == "POST":
        cart = request.session.get('cart')
        order = {}
        address = request.POST['address']
        mobile_no = request.POST['mobile-no']
        for key, value in cart.items():
            order[value] = Dishes.objects.get(pk=key)
        # print(address, mobile_no)
        for key, value in order.items():
            quantity = int(key)
            bill = quantity*value.price
            order_c = Order(restaurant=value.restaurant, customer=request.user, address=address, contact=mobile_no, total_bill=bill)
            order_c.save()
            order_details = Ordered_dishes(quantity=quantity, dish=value, order=order_c)
            order_details.save()
        del request.session['cart']
        return HttpResponseRedirect(reverse('index'))

def change_delivery_status(request):
    if request.method == "POST":
        order_id = request.POST["order"]
        order = Order.objects.get(pk=int(order_id))
        order.delivered = True
        order.save()
        return HttpResponseRedirect(reverse('partner_index'))
        
def recent_orders(request):
    recent_order = Order.objects.filter(customer=request.user).order_by('timestamp')
    order_details = []
    for i in recent_order:
        order_details = order_details + list(Ordered_dishes.objects.filter(order=i))
    print(order_details)
    return render(request, "food_delivery/recent_orders.html",{
        "order_details" : order_details
    })