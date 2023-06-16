from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from ecommerce_users.models import CustomUser


class EcommerceUsersTestCase(APITestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create_user(email="TestMail1@mail.com", password="TestPassword1",
                                                    first_name="TestFirstName1", last_name="TestLastName1")
        self.user2 = CustomUser.objects.create_user(email="TestMail2@mail.com", password="TestPassword2",
                                                    first_name="TestFirstName2", last_name="TestLastName2")
        self.admin_user = CustomUser.objects.create_superuser(email="TestMail5@mail.com", password="TestPassword5")

        self.initial_users = CustomUser.objects.all().count()

        self.client = APIClient()

    def test_get_all_users_with_admin_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user=self.admin_user).key)
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_user_with_non_admin_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user=self.user1).key)
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_users_without_authentication(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_another_user_details_with_admin_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user=self.admin_user).key)
        response = self.client.get(f'/users/{self.user1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_another_user_details_with_non_admin_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user=self.user2).key)
        response = self.client.get(f'/users/{self.user1.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_self_details_with_non_admin_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user=self.user1).key)
        response = self.client.get(f'/users/{self.user1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_new_user(self):
        data = {
            "data": {
                "type": "CustomUser",
                "attributes": {
                    "email": "testemail@test.com",
                    "password": "testpassword",
                    "password2": "testpassword",
                    "first_name": "testfirstname",
                    "last_name": "testlastname"
                }
            }
        }
        response = self.client.post('/users/', data=data, format='vnd.api+json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.all().count(), self.initial_users + 1)
