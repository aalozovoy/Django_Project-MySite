from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

def shop_index(request: HttpRequest):
    # return render(request, "shopapp/shop-index.html")
    print(request.path)
    print(request.method)
    print(request.headers)
    return HttpResponse("<h1>Hello World<h1>")

