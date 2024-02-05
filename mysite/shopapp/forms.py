from django import forms
from .models import Product, Order
from django.core import validators # дополнительные валидаторы


class ProductForm(forms.ModelForm):
    '''ModelForm - генерирует форму на основе существующей модели'''
    class Meta:
        model = Product
        fields = "name", "description", "price", "discount" # название полей как в model Product

# Чтобы отобразить форму на странице передаем экземпляр в views.py -> функция -> context

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "delivery_address", "promocode", "user", "products"




    # delivery_address = forms.CharField(max_length=200)
    # promocode = forms.CharField(max_length=20)
    # order = forms.CharField(label='Order by', max_length=100)
    # product_in_order = forms.CharField(label='Products in order', widget=forms.Textarea)





# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     price = forms.DecimalField(min_value=1, max_value=1000000, decimal_places=2)
#     description = forms.CharField(label='Product description',
#                                   widget=forms.Textarea(attrs={'rows': 5, 'cols': 30}),
#                                   validators=[validators.RegexValidator(
#                                       regex=r'Memory',
#                                       message='The amount of memory is not specified',)]
#                                   )
#     '''
#     CharField() - поле для ввода символов
#     DecimalField() - поле для работы с деньгами, дробными числами
#     label - отображается перед полем
#     widget - виджет для отображения
#     max_length - max длина
#     min_value - max значение
#     max_value - min значение
#     decimal_places - символы после запятой (для DecimalField())
#     TextField - большое текстовое поле
#     attrs={'rows': 5, 'cols': 30} - строки/колонки
#     '''
#     # Чтобы отобразить форму на странице передаем экземпляр в views.py -> функция -> context



