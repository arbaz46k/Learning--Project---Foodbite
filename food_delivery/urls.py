from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name='index'),
    path('register', views.register, name="register"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('partner_register', views.partner_register, name="partner_register"),
    path('partner_login', views.partner_login, name="partner_login"),
    path('partner_index', views.partner_index, name="partner_index"),
    path('dishes/<str:restaurant>', views.dishes, name="dishes"),
    path('add_item', views.add_item, name="add_item"),
    path('cart', views.cart, name="cart"),
    path('book_order', views.book_order, name="book_order"),
    path('delivered', views.change_delivery_status, name="change_delivery_status"),
    path('recent_orders', views.recent_orders, name="recent_orders")
]