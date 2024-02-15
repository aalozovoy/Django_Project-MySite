
from django.test import TestCase
from shopapp.utils import add_two_numbers
from django.urls import reverse
from string import ascii_letters
from random import choices
from shopapp.models import Product, User

class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        '''вызывает функцию add_two_numbers с двумя аргументами и проверяет, что результат равен 5'''
        result = add_two_numbers(2, 3)
        self.assertEquals(result, 5) # сравнение результата с ожидаемым результатом (проверяет что из функции вернулось 5)


class ProductCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        self.product_name = ''.join(choices(ascii_letters, k=10))
        Product.objects.filter(self.product_name).delete()
    def test_product_create(self):
        response = self.client.post(
            reverse('shopapp:create_product'),
            {
                'name': 'Virtual Glasses',
                'price': '9999',
                'description': 'Virtual Reality',
                'discount': '7',
                'created_by': 'John'
            }
        )
        self.assertRedirects(response, reverse('shopapp:products_list'))
        self.assertTrue(
            Product.objects.filter(self.product_name).exists()
        )

class ProductDeleteViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.product = Product.objects.create(name='Best Product')
    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse('shopapp:product_details', kwargs={'pk': self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse('shopapp:product_details', kwargs={'pk': self.product.pk})
        )
        self.assertContains(response, self.product.name)

class ProductsListViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
    ]
    def test_products(self):
        response = self.client.get(reverse('shopapp:products_list'))
