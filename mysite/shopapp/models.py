from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    class Meta:
        ordering = ['price', 'name'] # сортировка по цене, затем по имени (от min r max, наоборот: с "-")
        # db_tablr = 'tech_products' # указывает к какой таблице обращаться
        # verbose_name_plural = 'products' # указывает как объявлять данные во множественном числе

    # name - имя продукта, CharField - поле, max_length - макс. длина
    name = models.CharField(max_length=100)
    # description - описание продукта, TextField - большое текстовое поле
    description = models.TextField(null=False, blank=True)
    # price - цена, DecimalField - для работы с деньгами,
    # default - по умолчанию, max_digits - макс. символов, decimal_places - символов после запятой
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    # discount - скидка
    discount = models.SmallIntegerField(default=0)
    # crested_at - сохранение информации о создании продукта, auto_now_add=True - автосохранение (при создании нового)
    crested_at = models.DateTimeField(auto_now_add=True)
    # archived - архивировано ли
    archived = models.BooleanField(default=False)

class Order(models.Model):
     delivery_address = models.TextField(null=True, blank=True)
     promocode = models.CharField(max_length=20, null=False, blank=True)
     crested_at = models.DateTimeField(auto_now_add=True)

     # on_delete=models.PROTECT - защита от удаления заказов и user
     user = models.ForeignKey(User, on_delete=models.PROTECT)

     products = models.ManyToManyField(Product, related_name='orders')

