from knox.models import AuthToken
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from ecommerce_users.models import CustomUser, UserAddress


class EcommerceUsersTestCase(APITestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create_user(email="TestMail1@mail.com", password="TestPassword1",
                                                    first_name="TestFirstName1", last_name="TestLastName1")
        self.user2 = CustomUser.objects.create_user(email="TestMail2@mail.com", password="TestPassword2",
                                                    first_name="TestFirstName2", last_name="TestLastName2")
        self.admin_user = CustomUser.objects.create_superuser(email="TestMail5@mail.com", password="TestPassword5")

        self.address1 = UserAddress.objects.create(user=self.user1, address='Test Address 1', city='TestCity1',
                                                   postal_code='TestPC1', country='TestCountry1',
                                                   telephone='3333333333')
        self.address2 = UserAddress.objects.create(user=self.user2, address='Test Address 2', city='TestCity2',
                                                   postal_code='TestPC2', country='TestCountry2',
                                                   telephone='3333333333')

        self.initial_users = CustomUser.objects.all().count()
        self.initial_addresses = UserAddress.objects.all().count()
        self.initial_addresses_user1 = len(UserAddress.objects.filter(user=self.user1))
        self.initial_addresses_user2 = len(UserAddress.objects.filter(user=self.user2))

        self.client = APIClient()

    def test_get_all_users_with_admin_user(self):
        instance, token = AuthToken.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_user_with_non_admin_user(self):
        instance, token = AuthToken.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_users_without_authentication(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_another_user_details_with_admin_user(self):
        instance, token = AuthToken.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(f'/users/{self.user1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_another_user_details_with_non_admin_user(self):
        instance, token = AuthToken.objects.create(user=self.user2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(f'/users/{self.user1.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_self_details_with_non_admin_user(self):
        instance, token = AuthToken.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(f'/users/{self.user1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_new_user(self):
        data = {
            "email": "testemail@test.com",
            "password": "testpassword",
            "password2": "testpassword",
            "first_name": "testfirstname",
            "last_name": "testlastname"
        }
        response = self.client.post('/users/', data=data, format='vnd.api+json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.all().count(), self.initial_users + 1)

    def test_create_new_address_with_admin_user(self):
        instance, token = AuthToken.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        user_id = self.user1.id
        data = {
            "user": user_id,
            "address": "Test Address",
            "city": "TestCity",
            "postal_code": "00000",
            "country": "TestCountry",
            "telephone": "0000000000"
        }
        response = self.client.post('/addresses/', data=data, format='vnd.api+json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED),
        self.assertEqual(UserAddress.objects.all().count(), self.initial_addresses + 1)

    def test_create_new_address_with_non_admin_user(self):
        instance, token = AuthToken.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        user_id = self.user1.id
        data = {
            "user": user_id,
            "address": "Test Address",
            "city": "TestCity",
            "postal_code": "00000",
            "country": "TestCountry",
            "telephone": "0000000000"
        }
        response = self.client.post('/addresses/', data=data, format='vnd.api+json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED),
        self.assertEqual(UserAddress.objects.all().count(), self.initial_addresses + 1)

    def test_get_all_addresses_with_admin_user(self):
        instance, token = AuthToken.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        response = self.client.get('/addresses/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.initial_addresses)

    def test_get_own_addresses_with_non_admin_user(self):
        instance, token = AuthToken.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/addresses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.initial_addresses_user1)
        for address in response.data:
            self.assertEqual(address['user_id'], self.address1.user.id)

        instance, token = AuthToken.objects.create(user=self.user2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/addresses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.initial_addresses_user2)
        for address in response.data:
            self.assertEqual(address['user_id'], self.address2.user.id)

    def test_get_another_user_address_with_admin_user(self):
        instance, token = AuthToken.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(f'/addresses/{self.address1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_another_user_address_with_non_admin_user(self):
        instance, token = AuthToken.objects.create(user=self.user2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(f'/addresses/{self.address1.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_own_address_with_non_admin_user(self):
        instance, token = AuthToken.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(f'/addresses/{self.address1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
