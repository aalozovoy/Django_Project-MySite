from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    class Meta:
        ordering = ['price', 'name']
        '''ordering - сортировка, ['price', 'name'] - по цене,
        затем по имени (от min к max, наоборот: с "-")'''

        # db_tablr = 'tech_products' # указывает к какой таблице обращаться
        # verbose_name_plural = 'products' # указывает как объявлять данные во множественном числе



    name = models.CharField(max_length=100)
    '''name - имя продукта, CharField - поле, max_length - макс. длина'''
    description = models.TextField(null=False, blank=True)
    '''description - описание продукта, TextField - большое текстовое поле'''
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    '''price - цена, DecimalField - для работы с деньгами, default - по умолчанию,
        max_digits - макс. символов, decimal_places - символов после запятой'''
    discount = models.SmallIntegerField(default=0)
    '''discount - скидка'''
    crested_at = models.DateTimeField(auto_now_add=True)
    '''crested_at - сохранение информации о создании продукта,
    auto_now_add=True - автосохранение (при создании нового)'''
    archived = models.BooleanField(default=False)
    '''archived - архивировано ли'''

    # сокращение описания в description (см. admin.py)
    # @property
    # def description_short(self) -> str:
    #     if len(self.description) < 50:
    #         return self.description
    #     return self.description[:50] + '...'

    def __str__(self) -> str:
        return f'Product (pk={self.pk}, name={self.name!r})'
        ''' представление объекта в админ панели, !r - в " " '''


class Order(models.Model):
     delivery_address = models.TextField(null=True, blank=True)
     promocode = models.CharField(max_length=20, null=False, blank=True)
     crested_at = models.DateTimeField(auto_now_add=True)

     user = models.ForeignKey(User, on_delete=models.PROTECT)
     ''' связь с user, on_delete=models.PROTECT - защита от удаления заказов и user '''
     products = models.ManyToManyField(Product, related_name='orders')
     ''' связь с products через 'orders' '''

