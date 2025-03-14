from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path

from .common import save_csv_products
from .models import Product, Order, ProductImage
from .admin_mixins import ExpotrasCVSMixin
from .forms import CSVImportForm


class OrderInline(admin.TabularInline):
    ''' ProductInline подключает встроенные записи '''
    model = Product.orders.through
    ''' through указывает, что свойства необходимо взять из заказа '''

class ProductInline(admin.StackedInline):
    model = ProductImage

@admin.action(description='Archive products')
def merk_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    ''' merk_archived функция для архивирования '''
    queryset.update(archived=True)

@admin.action(description='Unarchive products')
def merk_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    ''' merk_unarchived функция для разархивирования '''
    queryset.update(archived=False)


@admin.register(Product) # 2 вариант
class ProductAdmin(admin.ModelAdmin, ExpotrasCVSMixin):
    actions = [
        merk_archived,
        merk_unarchived,
        'export_csv',
    ]
    inlines = [
        OrderInline,
        ProductInline,
    ]
    list_display = 'pk', 'name', 'description_short', 'price', 'discount', 'archived'
    ''' list_display - графы таблицы '''
    list_display_links = 'pk', 'name'
    '''активация (возможность кликнуть) 'name' в таблице админ панели '''
    ordering = 'pk', 'name'
    ''' ordering - сортировка (от min к max, наоборот: с "-")
    сортировка по порядковому номеру, далее по имени (одинаковые товары) '''
    search_fields = 'name', 'description', 'price', 'discount'
    ''' search_fields - поиск по 'name' или 'description' '''
    fieldsets = [
        (None, {'fields': ('name', 'description'),}),
        ('Price options', {
            'fields': ('price', 'discount'),
            'classes': ('wide', 'collapse')
        }),
        ('Images', {
            'fields': ('preview',),
        }),
        ('Extra options', {
            'fields': ('archived',),
            'classes': ('collapse',),
        'description': 'Extra options. Field archived is for soft delete'
        })
    ]
    ''' fieldsets определяет поля которые будут отображаться в админ панели (для products)
        'collapse' - скрытие лишнего (нужно будет разворачивать в админ панели Price options (Show)) 
        'wide' - добавляет расстояние по ширине 
        'archived' - заархивированный (description - описание (Дополнительные опции. Поле "Архивировано" предназначено для мягкого удаления)) '''

    change_list_template = "shopapp/products_changelist.html"
    def description_short(self, obj: Product) -> str:
        ''' сокращение описания в description прописывается здесь,
        если нужен только для админ панели, иначе в models.py '''
        if len(obj.description) < 50:
            return obj.description
        return obj.description[:50] + '...'
# admin.site.register(Product, ProductAdmin) # 1 вариант

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportForm()
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context)
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context, status=400)

        save_csv_products(
            file=form.files["csv_file"].file,
            encoding=request.encoding,
        )
        self.message_user(request, "Data from CSV was imported")
        return redirect("..")

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "import-products-csv/",
                self.import_csv,
                name="import_products_csv",
            ),
        ]
        return new_urls + urls



# class ProductInline(admin.TabularInline):
class ProductInline(admin.StackedInline):
    ''' ProductInline подключает встроенные записи '''
    model = Order.products.through
    ''' through указывает, что свойства необходимо взять из заказа '''

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]
    list_display = 'delivery_address', 'promocode', 'crested_at', 'user_verbose'
    ''' list_display - графы таблицы заказа '''

    def get_queryset(self, request):
        ''' get_queryset искл. лишние запросы с помощью select_related('user') '''
        return Order.objects.select_related('user').prefetch_related('products')
        ''' prefetch_related('products') - оптимизация количества запросов '''

    def user_verbose(self, odj: Order) -> str:
        ''' user_verbose возвращает first_name (при наличии) или username
        first_name можно добавить через админ панель '''
        return odj.user.first_name or odj.user.username

    change_list_template = "shopapp/orders_changelist.html"
    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportForm()
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context)
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context, status=400)

        save_csv_products(
            file=form.files["csv_file"].file,
            encoding=request.encoding,
        )
        self.message_user(request, "Data from CSV was imported")
        return redirect("..")

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "import-orders-csv/",
                self.import_csv,
                name="import_orders_csv",
            ),
        ]
        return new_urls + urls




