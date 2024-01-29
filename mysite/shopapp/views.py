from django.contrib.auth.models import Group

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from timeit import default_timer

from .models import Product, Order

def shop_index(request: HttpRequest):
    products = [
        ('TV', 3000),
        ('Laptop', 5000),
        ('Smartphone', 2000),
    ]
    context = {
        'time_running': default_timer(),
        'products': products,
    }
    return render(request, 'shopapp/shop-index.html', context=context) #для шаблона


def groups_list(request: HttpRequest):
    context = {
        'groups': Group.objects.prefetch_related('permissions').all(),
    }
    return render(request, 'shopapp/groups-list.html', context=context)  # для шаблона

# prefetch_related('permissions') - оптимизация количества запросов

def products_list(request: HttpRequest):
    context = {
        'products': Product.objects.all(),
    }
    return render(request, 'shopapp/products-list.html', context=context)  # для шаблона

def orders_list(request: HttpRequest):
    context = {
        'orders': Order.objects.select_related('user').prefetch_related('products').all(), # select_related('user') - искл. лишние запросы
    }
    return render(request, 'shopapp/orders-list.html', context=context)  # для шаблона