from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404, reverse
from timeit import default_timer

from django.urls import reverse_lazy
from django.views.generic import (TemplateView,
                                  ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)

from .models import Product, Order, ProductImage # из models.py
from .forms import ProductForm, OrderForm, GroupForm # из forms.py
from django.views import View # для создания классов View
from django.contrib.auth.mixins import (LoginRequiredMixin, # примесь на вход
                                        PermissionRequiredMixin, # примесь ограничение
                                        UserPassesTestMixin) # примесь ограничение для всех кроме superuser



from rest_framework.viewsets import ModelViewSet
from .serializers import ProductSerializers, OrderSerializers
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse

import logging

log = logging. getLogger(__name__)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ['delivery_address', 'user',]
    filterset_fields = [
        'delivery_address',
        'promocode',
        'crested_at',
        'user',
        'products',
    ]
    ordering_fields = [
        'delivery_address',
        'promocode',
        'crested_at',
        'user',
        'products',
    ]


@extend_schema(description='Product views CRUD')
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product.
    Полный CRUD для сущности товара.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ['name', 'description',]
    filterset_fields = [
        'name',
        'description',
        'price',
        'discount',
        'archived',
    ]
    ordering_fields = ['name', 'price', 'discount',]

    @extend_schema(
        summary='Get one product by ID',
        description='Retrieves product, returns 404 if not found',
        responses={
            200: ProductSerializers,
            400: OpenApiResponse(description='Empty response, product by id not found'),
        }
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

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
            'items': 1,
        }
        log.debug("Products for shop index: %s", products)
        log.info("Rendering shop index")
        return render(request, 'shopapp/shop-index.html', context=context)

class ProductListView(ListView):
    template_name = 'shopapp/products-list.html'
    model = Product
    context_object_name = 'products'
    queryset = Product.objects.filter(archived=False) # выводятся только не архивированные сущности

class ProductDetailsView(DetailView):
    # self.get_object()
    # self.request.user(self)
    template_name = 'shopapp/products_details.html'
    # model = Product
    queryset = Product.objects.prefetch_related('images')
    # queryset - для вывода изображений в деталях, prefetch_related - для связи одного ко многим
    context_object_name = 'product'

class ProductCreateView(PermissionRequiredMixin, CreateView): # CreateView использует суффикс form
    # def test_func(self):
    #     # return self.request.user.groups.filter(name='secret-group').exists()
    #     return self.request.user.is_superuser
    permission_required = 'shopapp.add_product'
    model = Product
    fields = 'name', 'price', 'description', 'discount', 'created_by', 'preview'
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        resource = super().form_valid(form)
        return resource

class ProductUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        # return self.request.user.groups.filter(name='secret-group').exists()
        return (self.request.user.is_superuser
                or self.request.user.has_perm('shopapp.change_product')
                and self.get_object().created_by == self.request.user)

    model = Product
    # fields = 'name', 'price', 'description', 'discount', 'created_by', 'preview'
    template_name_suffix = '_update_form'
    form_class = ProductForm
    # т.к. UpdateView также, как и CreateView использует суффикс form
    # template_name_suffix = '_update_form' новая форма
    def get_success_url(self):
        return reverse(
            'shopapp:product_details',
            kwargs={'pk': self.object.pk},
        )
    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist('images'):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response

class ProductDeleteView(UserPassesTestMixin, DeleteView): # шаблон product_confirm_delete
    def test_func(self):
        return self.request.user.is_superuser
    model = Product
    success_url = reverse_lazy('shopapp:products_list')
    def form_valid(self, form): # для добавления в архив вместо удаления
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects
        .select_related('user')
        .prefetch_related('products')
    )
    # переименовать шаблон на order_list (order - имя модели, list - суффикс)
    # object_list в шаблоне вместо orders
    # prefetch_related - связь ко многим

class OrdersDetailsView(PermissionRequiredMixin, DetailView):
    permission_required = 'shopapp.view_order'
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

class ProductsExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.order_by('pk').all()
        products_data = []
        for product in products:
            product_data = {
                'pk': product.pk,
                'name': product.name,
                'price': product.price,
                'archived': product.archived,
            }
            products_data.append(product_data)
        elem = products_data[0]
        name = elem["name"]
        print("name:", name)
        return JsonResponse({'products': products_data})