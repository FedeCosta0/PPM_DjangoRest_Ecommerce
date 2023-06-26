from knox.models import AuthToken

from ecommerce_users.models import CustomUser
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from ecommerce_products.models import Product, ProductCategory, ProductInventory, Discount


class EcommerceProductsTestCase(APITestCase):

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

        self.initial_products = Product.objects.all().count()
        self.initial_products_category1 = Product.objects.filter(category=self.category1).count()
        self.initial_products_category2 = Product.objects.filter(category=self.category2).count()
        self.initial_categories = ProductCategory.objects.all().count()
        self.initial_stock1 = self.product_inventory1.stock
        self.initial_stock2 = self.product_inventory2.stock

        self.client = APIClient()

    def test_get_all_products_with_admin_user(self):
        instance, token = AuthToken.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_products_with_non_admin_user(self):
        instance, token = AuthToken.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_products_with_unauthenticated_user(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_product_with_admin_user(self):
        instance, token = AuthToken.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(f'/products/{self.product1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_product_with_non_admin_user(self):
        instance, token = AuthToken.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(f'/products/{self.product1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_product_with_unauthenticated_user(self):
        response = self.client.get(f'/products/{self.product1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product_with_admin_user(self):
        category_id = self.category1.id
        data = {
            "name": "TestProduct",
            "description": "Test Product",
            "price": 100,
            "category": category_id
        }

        instance, token = AuthToken.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/products/', data=data, format='vnd.api+json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.all().count(), self.initial_products + 1)
        self.assertEqual(Product.objects.filter(category=self.category1).count(), self.initial_products_category1 + 1)
        self.assertEqual(Product.objects.filter(category=self.category2).count(), self.initial_products_category2)

    def test_create_product_with_non_admin_user(self):
        category_id = self.category1.id
        data = {
            "name": "TestProduct",
            "description": "Test Product",
            "price": 100,
            "category": category_id
        }

        instance, token = AuthToken.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/products/', data=data, format='vnd.api+json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_product_with_unauthenticated_user(self):
        category_id = self.category1.id
        data = {
            "name": "TestProduct",
            "description": "Test Product",
            "price": 100,
            "category": category_id
        }

        response = self.client.post('/products/', data=data, format='vnd.api+json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_categories_with_admin_user(self):
        instance, token = AuthToken.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/products-category/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_categories_with_non_admin_user(self):
        instance, token = AuthToken.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/products-category/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_categories_with_unauthenticated_user(self):
        response = self.client.get('/products-category/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_category_with_admin_user(self):
        instance, token = AuthToken.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(f'/products-category/{self.category1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_category_with_non_admin_user(self):
        instance, token = AuthToken.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(f'/products-category/{self.category1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_category_with_unauthenticated_user(self):
        response = self.client.get(f'/products-category/{self.category1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category_with_admin_user(self):
        data = {
            "name": "TestCategoryName",
            "description": "Test Category Description"
        }

        instance, token = AuthToken.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post(f'/products-category/', data=data, format='vnd.api+json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProductCategory.objects.all().count(), self.initial_categories + 1)

    def test_create_category_with_non_admin_user(self):
        data = {
            "name": "TestCategoryName",
            "description": "Test Category Description"
        }

        instance, token = AuthToken.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post(f'/products-category/', data=data, format='vnd.api+json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_category_with_unauthenticated_user(self):
        data = {
            "name": "TestCategoryName",
            "description": "Test Category Description"
        }

        response = self.client.post(f'/products-category/', data=data, format='vnd.api+json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
