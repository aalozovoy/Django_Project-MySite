from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from timeit import default_timer

def shop_index(request: HttpRequest):
    # print(request.path)
    # print(request.method)
    # print(request.headers)
    # return HttpResponse('<h1>Hello World!</h1>')
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
