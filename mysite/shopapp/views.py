from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404, reverse
from timeit import default_timer

from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Product, Order # из models.py
from .forms import ProductForm, OrderForm, GroupForm # из forms.py
from django.views import View # для создания классов View


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('TV', 3000),
            ('Laptop', 5000),
            ('Smartphone', 2000),
        ]
        context = {
            'time_running': default_timer(),
            'products': products,
        }
        return render(request, 'shopapp/shop-index.html', context=context)

class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'POST':
            url = reverse('shopapp:index')
            return redirect(url)
        context = {
            'form': GroupForm(),
            'groups': Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)
    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)

class ProductDetailsView(DetailView):
    template_name = 'shopapp/products_details.html'
    model = Product
    context_object_name = 'product'

class ProductListView(ListView):
    template_name = 'shopapp/products-list.html'
    # model = Product
    context_object_name = 'products'
    queryset = Product.objects.filter(archived=False) # выводятся только не архивированные сущности

class OrdersListView(ListView):
    queryset = (
        Order.objects
        .select_related('user')
        .prefetch_related('products')
    )
    # переименовать шаблон на order_list (order - имя модели, list - суффикс)
    # object_list в шаблоне вместо orders


class ProductCreateView(CreateView): # CreateView использует суффикс form
    model = Product
    fields = 'name', 'price', 'description', 'discount'
    success_url = reverse_lazy('shopapp:products_list')

class ProductUpdateView(UpdateView):
    model = Product
    fields = 'name', 'price', 'description', 'discount'
    template_name_suffix = '_update_form'
    # т.к. UpdateView также, как и CreateView использует суффикс form
    # template_name_suffix = '_update_form' новая форма
    def get_success_url(self):
        return reverse(
            'shopapp:product_details',
            kwargs={'pk': self.object.pk},
        )

class ProductDeleteView(DeleteView): # шаблон product_confirm_delete
    model = Product
    success_url = reverse_lazy('shopapp:products_list')
    def form_valid(self, form): # для добавления в архив вместо удаления
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)

class OrdersDetailsView(DetailView):
    queryset = (
        Order.objects
        .select_related('user')
        .prefetch_related('products')
    )

class OrderCreateView(CreateView): # CreateView использует суффикс form
    model = Order
    fields = "delivery_address", "promocode", "user", "products"
    success_url = reverse_lazy('shopapp:order_list')

class OrderUpdateView(UpdateView):
    model = Order
    fields = "delivery_address", "promocode", "user", "products"
    template_name_suffix = '_update_form'
    # т.к. UpdateView также, как и CreateView использует суффикс form
    # template_name_suffix = '_update_form' новая форма
    def get_success_url(self):
        return reverse(
            'shopapp:order_details',
            kwargs={'pk': self.object.pk},
        )

class OrderDeleteView(DeleteView): # шаблон order_confirm_delete
    model = Order
    success_url = reverse_lazy('shopapp:order_list')