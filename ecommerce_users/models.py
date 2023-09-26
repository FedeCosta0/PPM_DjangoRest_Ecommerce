from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models

from utils.model_abstracts import Model


class MyUserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            first_name="",
            last_name=""
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser, Model):
    username = None
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class UserAddress(Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='user_address')
    address = models.CharField(max_length=50, null=False)
    city = models.CharField(max_length=50, null=False)
    postal_code = models.CharField(max_length=10, null=False)
    country = models.CharField(max_length=20, null=False)
    telephone = models.CharField(max_length=20)
