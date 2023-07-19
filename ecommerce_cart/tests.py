from knox.models import AuthToken
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from ecommerce_cart.models import ShoppingSession
from ecommerce_products.models import Product, ProductCategory, ProductInventory, Discount
from ecommerce_users.models import CustomUser


class EcommerceCartTestCase(APITestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create_user(email="TestMail1@mail.com", password="TestPassword1",
                                                    first_name="TestFirstName1", last_name="TestLastName1")
        self.user2 = CustomUser.objects.create_user(email="TestMail2@mail.com", password="TestPassword2",
                                                    first_name="TestFirstName2", last_name="TestLastName2")
        self.admin_user = CustomUser.objects.create_superuser(email="TestMail5@mail.com", password="TestPassword5")

        self.category1 = ProductCategory.objects.create(name="TestProductCategoryName1",
                                                        description="Test Product Category Description 1")
        self.category2 = ProductCategory.objects.create(name="TestProductCategoryName2",
                                                        description="Test Product Category Description 2")

        self.product_inventory1 = ProductInventory.objects.create(stock=10)
        self.product_inventory2 = ProductInventory.objects.create(stock=15)

        self.discount1 = Discount.objects.create(name="TestDiscountName1", description="Test Discount Description 1",
                                                 discount_percent=10.00, active=True)
        self.discount2 = Discount.objects.create(name="TestDiscountName2", description="Test Discount Description 2",
                                                 discount_percent=20.00, active=True)

        self.product1 = Product.objects.create(name="TestProductName1", description="Test Product Description 1",
                                               price=49.99, category=self.category1,
                                               inventory=self.product_inventory1, discount=self.discount1)
        self.product2 = Product.objects.create(name="TestProductName2", description="Test Product Description 2",
                                               price=99.00, category=self.category2,
                                               inventory=self.product_inventory2, discount=self.discount2)

        self.client = APIClient()

    def test_get_own_cart_with_authenticated_user(self):
        instance, token = AuthToken.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['cart_products']), 0)

    def test_get_own_cart_with_unauthenticated_user(self):
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_product_to_cart_with_authenticated_user(self):
        quantity = 3
        data = {
            "product": self.product1.id,
            "quantity": quantity
        }

        instance, token = AuthToken.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        response = self.client.post('/cart-product/', data=data, format='vnd.api+json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get('/cart/')

        self.assertEqual(float(response.data['total']), float(self.product1.price) * float(quantity))
        self.assertEqual(len(response.data['cart_products']), 1)
        self.assertEqual(response.data['cart_products'][0]['quantity'], quantity)

    def test_add_product_to_cart_with_unauthenticated_user(self):
        quantity = 3
        data = {
            "product": self.product1.id,
            "quantity": quantity
        }

        response = self.client.post('/cart-product/', data=data, format='vnd.api+json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_submit_empty_order(self):
        instance, token = AuthToken.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        ShoppingSession.objects.create(user=self.user1)
        response = self.client.post('/cart/', format='vnd.api+json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_submit_order_with_unauthenticated_user(self):
        response = self.client.post('/cart/', format='vnd.api+json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_submit_order_with_authenticated_user(self):
        instance, token = AuthToken.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        quantity = 3
        data = {
            "product": self.product1.id,
            "quantity": quantity
        }
        self.client.post('/cart-product/', data=data, format='vnd.api+json')

        response = self.client.post('/cart/', format='vnd.api+json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get('/cart/')
        self.assertEqual(float(response.data['total']), 0.00)
        self.assertEqual(len(response.data['cart_products']), 0)

    def test_delete_product_from_cart_with_authenticated_user(self):
        quantity = 3
        data = {
            "product": self.product1.id,
            "quantity": quantity
        }

        instance, token = AuthToken.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        response = self.client.post('/cart-product/', data=data, format='vnd.api+json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        cart_product_id = response.data['id']
        response = self.client.delete(f'/cart-product/{cart_product_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get('/cart/')
        self.assertEqual(float(response.data['total']), 0.00)
        self.assertEqual(len(response.data['cart_products']), 0)
