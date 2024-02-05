from django.contrib.auth.models import Group

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, reverse
from timeit import default_timer
from .models import Product, Order
from .forms import ProductForm, OrderForm

def shop_index(request: HttpRequest):
    products = [
        ('TV', 3000),
        ('Laptop', 5000),
        ('Smartphone', 2000),
        ]

    context = {
        'time_running': default_timer(),
        'products': products,
        # 'links': links,
    }
    return render(request, 'shopapp/shop-index.html', context=context) #для шаблона

def groups_list(request: HttpRequest):
    if request.method == 'POST':
        url = reverse('shopapp:index')
        return redirect(url)
    context = {
        'groups': Group.objects.prefetch_related('permissions').all(),
    }
    return render(request, 'shopapp/groups-list.html', context=context)  # для шаблона
    ''' prefetch_related('permissions') - оптимизация количества запросов '''

def products_list(request: HttpRequest):
    context = {
        'products': Product.objects.all(),
    }
    return render(request, 'shopapp/products-list.html', context=context)  # для шаблона
def orders_list(request: HttpRequest):
    context = {
        'orders': Order.objects.select_related('user').prefetch_related('products').all(),
    }
    '''prefetch_related('products') - оптимизация количества запросов
        select_related('user') - искл. лишние запросы '''
    return render(request, 'shopapp/orders-list.html', context=context)  # для шаблона

def create_product(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            # name = form.cleaned_data['name']
            # price = form.cleaned_data['price']
            # description = form.cleaned_data['description']
            # Product.objects.create(**form.cleaned_data) # form - словарь, поэтому **form.cleaned_data - его распаковка
            form.save() # если form валидна, сохранение
            url = reverse('shopapp:products_list')
            return redirect(url)
    else:
        form = ProductForm()
    context = {
        'form': form,
    }
    return render(request, 'shopapp/create_product.html', context=context)

def create_order(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Order.objects.create(**form.cleaned_data)
            form.save()
            url = reverse('shopapp:orders_list')
            return redirect(url)
    else:
        form = OrderForm()
    context = {
        'form': form,
    }
    return render(request, 'shopapp/create_order.html', context=context)



    # ]
    # links = [
    #     ("Groups list", 'shop/groups/'),
    #     ("Products list", 'shop/products/'),
    #     ("Orders list", 'shop/orders/'),
    #
    # ]


