from django.contrib.auth.models import User, Permission
from django.test import TestCase
from shopapp.utils import add_two_numbers
from django.urls import reverse
from string import ascii_letters
from random import choices
from shopapp.models import Product, Order
from django.conf import settings

class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        '''вызывает функцию add_two_numbers с двумя аргументами и проверяет, что результат равен 5'''
        result = add_two_numbers(2, 3)
        self.assertEquals(result, 5) # сравнение результата с ожидаемым результатом (проверяет что из функции вернулось 5)

class ProductCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        permission = Permission.objects.get(codename='add_product')
        self.user.user_permissions.add(permission)
        self.user.save()
        self.client.login(username='testuser', password='12345')
        self.product_name = ''.join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()
    # @classmethod
    # def setUpClass(cls):
    #     cls.user = User.objects.create_user(username='Jeck', password='1')  # создание пользователя для теста
    #     permission = Permission.objects.get(codename='add_product')
    #     cls.user.add(permission)
    # @classmethod
    # def tearDownClass(cls):
    #     cls.user.delete()
    # def setUp(self) -> None:
    #     self.client.force_login(self.user)
    #     self.client.pe
    #     # self.product_name = ''.join(choices(ascii_letters, k=10))
    #     # Product.objects.filter(self.product_name).delete()

    def test_product_create(self):
        response = self.client.post(
            reverse('shopapp:create_product'),
            {
                # 'name': 'Virtual Glasses',
                'name': self.product_name,
                'price': '9999',
                'description': 'Virtual Reality',
                'discount': '7'
            }
        )
        self.assertRedirects(response, reverse('shopapp:products_list'))
        self.assertTrue(
            Product.objects.filter(self.product_name).exists()
        )

class ProductDetailViewTestCase(TestCase):
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
        self.assertQuerysetEqual(
            qs=Product.objects.filter(archived=False).all(), # ожидали получить
            values=(p.pk for p in response.context['products']), # получили
            transform=lambda p: p.pk, # преобразование данных из qs
        )
        self.assertTemplateUsed(response, 'shopapp/products-list.html') # проверка шаблона

class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='Jeck', password='12345')
        permission = Permission.objects.get(codename="view_order")
        cls.user.user_permissions.add(permission)
        cls.user.save()
    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.order = Order.objects.create(
            delivery_address="ul Pushkina, d 1",
            promocode="qwerty",
            user=self.user,
        )
    def tearDown(self) -> None:
        self.order.delete()
    def test_order_details(self):
        response = self.client.get(reverse("shopapp:order_details", kwargs={"pk": self.order.pk}))
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertEqual(response.context["object"].pk, self.order.pk)


class OrdersListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='Jeck', password='1') # создание пользователя для теста
    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
    def setUp(self) -> None:
        self.client.force_login(self.user) # вход пользователя
    def test_orders_view(self):
        response = self.client.get(reverse('shopapp:order_list'))
        self.assertContains(response, 'Orders')

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('shopapp:order_list'))
        self.assertEquals(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)





class ProductsExportViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
    ]
    def test_get_products_view(self):
        response = self.client.get(
            reverse('shopapp:products_export')
        )
        self.assertEquals(response.status_code, 200)
        products = Product.objects.order_by('pk').all()
        expected_data = [
            {
                'pk': products.pk,
                'name': products.name,
                'price': str(products.price),
                'archived': products.archived,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEquals(
            products_data['products'],
            expected_data
        )